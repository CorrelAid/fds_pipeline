from dagster import op, job, Config, Out, RetryRequested, graph, OpExecutionContext, In, Output, Nothing
from dagster_pandas import DataFrame
from urllib.error import HTTPError
from sqlalchemy import exc
from psycopg2.errors import ForeignKeyViolation
from fds_pipeline.ressources import FDSAPI, PostgresQuery
from fds_pipeline.processing import (
    process_foi_request,
    process_jurisdictions,
    process_public_body,
    process_campaigns,
    process_messages,
    gen_sql_insert_new,
    del_col,
)

from fds_pipeline.df_types import FOIRequestDf, JurisdictionDf, PublicBodyDf, CampaignDf, MessageDf


class APIConfig(Config):
    id_: int


# Foi Requests sometimes dont have a public body
@op(out={"Success": Out(dict, is_required=False), "Failure": Out(is_required=False)})
def get_foi_request(context: OpExecutionContext, config: APIConfig, fds_api: FDSAPI):
    context.log.info(f"Getting foi request with id {config.id_}")
    try:
        foi_req = fds_api.get_foi_request(config.id_)
        yield Output(foi_req, "Success")
    except HTTPError as err:
        if err.status == 404:
            context.log.info(f"ID:{config.id_} does not exist!")
            yield Output(None, "Failure")
        else:
            raise Exception(err)


###### Extract Objects
@op(out=Out(FOIRequestDf))
def extract_foi_request(get_foi_request) -> DataFrame:
    df = process_foi_request(get_foi_request)
    return df


# Foi Requests sometimes dont have a public body
@op(out={"Success": Out(PublicBodyDf, is_required=False), "Failure": Out(is_required=False)})
def extract_public_body(context: OpExecutionContext, get_foi_request):
    try:
        df = process_public_body(get_foi_request)
        yield Output(df, "Success")
    except KeyError:
        context.log.info("Foi request was not assigned a public body!")
        yield Output(None, "Failure")


@op(out=Out(MessageDf))
def extract_messages(get_foi_request) -> DataFrame:
    df = process_messages(get_foi_request)
    return df


###### Execute SQL
@op
def insert_public_body(extract_public_body, postgres_query: PostgresQuery):
    try:
        sql = gen_sql_insert_new(extract_public_body, "public_bodies")
        postgres_query.execute(sql)
    # if foreign key not present, retry (jurisdiction table is updated once every hour)
    except exc.IntegrityError as err:
        if isinstance(err.orig, ForeignKeyViolation):
            raise RetryRequested(max_retries=1, seconds_to_wait=3600) from err
        else:
            raise Exception(err)


@op(ins={"start": In(Nothing)})
def insert_foi_request(context: OpExecutionContext, extract_foi_request, postgres_query: PostgresQuery):
    try:
        sql = gen_sql_insert_new(extract_foi_request, "foi_requests")
        postgres_query.execute(sql)
    # if foreign key for campaign not present, retry (campaign  is updated once every hour)
    # if not present again, change campaign_id to be NULL
    except exc.IntegrityError as err:
        if isinstance(err.orig, ForeignKeyViolation):
            if "campaigns" in str(err) and "fk_campaign" in str(err):
                if context.retry_number > 0:
                    sql = gen_sql_insert_new(extract_foi_request, "foi_requests")
                    sql = del_col(sql)
                    postgres_query.execute(sql)
                else:
                    raise RetryRequested(max_retries=1, seconds_to_wait=3600) from err
            else:
                raise Exception(err)
        else:
            raise Exception(err)


@op(ins={"start": In(Nothing)})
def insert_messages(extract_messages, postgres_query: PostgresQuery):
    sql = gen_sql_insert_new(extract_messages, "messages")
    postgres_query.execute(sql)


@graph
def proc_insert() -> None:
    # Everything depends on data, so if data is not present, all other ops wont execute
    data, fail_foi = get_foi_request()

    public_body, fail = extract_public_body(data)
    foi_request = extract_foi_request(get_foi_request=data)
    messages = extract_messages(data)

    insert_messages(messages, start=insert_foi_request(foi_request, start=insert_public_body(public_body)))

    insert_messages(messages, start=insert_foi_request(foi_request, start=fail))


proc_insert_job = proc_insert.to_job()


# Campaigns
# We have to do this separetely because foi_request object retreived from api doesnt contain all the data
@op
def get_campaigns(context, fds_api: FDSAPI) -> list:
    return fds_api.get_list("campaign")


@op(out=Out(CampaignDf))
def extract_campaigns(get_campaigns) -> DataFrame:
    return process_campaigns(get_campaigns)


@op
def insert_campaigns(extract_campaigns, postgres_query: PostgresQuery):
    sql = gen_sql_insert_new(extract_campaigns, "campaigns")
    postgres_query.execute(sql)


@job
def proc_insert_campaigns():
    insert_campaigns(extract_campaigns(get_campaigns()))


# Jurisdictions
# We have to do this separetely because foi_request object retreived from api doesnt contain all jurisdiction data when
# public body is null
@op
def get_jurisdictions(context, fds_api: FDSAPI) -> list:
    return fds_api.get_list("jurisdiction")


@op(out=Out(JurisdictionDf))
def extract_jurisdictions(get_jurisdictions) -> DataFrame:
    return process_jurisdictions(get_jurisdictions)


@op
def insert_jurisdictions(extract_jurisdictions, postgres_query: PostgresQuery):
    sql = gen_sql_insert_new(extract_jurisdictions, "jurisdictions")
    postgres_query.execute(sql)


@job
def proc_insert_jurisdictions():
    insert_jurisdictions(extract_jurisdictions(get_jurisdictions()))
