from dagster import sensor, RunRequest, SkipReason, RunConfig, SensorEvaluationContext

from fds_pipeline.jobs import proc_insert_foi_request, APIConfig


# Sensor that counts number of foi requests in db and if number is lower than items in
# api, then calculates difference. a variable is declared resulting from difference
# subtracted by 50.
#  if below 0, set to exact difference.
# checks highest id in db, create a list of length of this var with ascending ids, then
# starts job with this list of ids.
@sensor(job=proc_insert_foi_request, minimum_interval_seconds=10, required_resource_keys={"fds_api", "postgres_query"})
def new_foi_requests(context: SensorEvaluationContext):
    last_max_id = int(context.cursor) if context.cursor else None
    total_api = context.resources.fds_api.get_total()

    total_db = context.resources.postgres_query.single("""SELECT COUNT(*) FROM 
        foi_requests
        """)

    if total_db < total_api:
        # determine number of runs
        diff = total_api - total_db
        length = 2
        test = diff - length
        # if standard number of runs is below number of not loaded foi requests
        if test < 0:
            length = diff

        max_id = context.resources.postgres_query.single("""
        SELECT MAX(id)
        FROM foi_requests
        """)
        # if db is empty
        if max_id is None:
            max_id = 0
        # generate list of ids (each entry will be one run)
        # if the last max id is not equal to current max id in db, let list start from last max id id as this or ids
        # before it were not succesfull. Otherwise max_id from db would be equal.
        if last_max_id != max_id and last_max_id is not None:
            id_lst = range(last_max_id + 1, last_max_id + 1 + length)
        else:
            id_lst = range(max_id + 1, max_id + 1 + length)
        context.update_cursor(str(max(id_lst)))
        context.log.info(last_max_id)
        for id_ in id_lst:
            yield RunRequest(
                run_key=str(f"new_{id_}"),
                run_config=RunConfig(ops={"get_foi_request": APIConfig(id_=id_)}),
            )

    else:
        yield SkipReason("Number of entries in database equal to entries in API")


# Sensor that retreives 50 newest items from api and checks if these items are same than
# in db. if old items in list, start job with new items. if all new, make new request to
#  retreive 50 more items etc.
