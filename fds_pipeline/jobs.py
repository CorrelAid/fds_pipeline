from dagster import op, job, Config
from fds_pipeline.ressources import FDSAPI


class APIConfig(Config):
    id_: int


# job that calls an op that retrieves a foi request given an id
# handle not found error
@op
def get_foi_request(context, config: APIConfig, fds_api: FDSAPI):
    foi_req = fds_api.get_foi_request(config.id_)

    return foi_req


@job
def single_foi_request():
    get_foi_request()
