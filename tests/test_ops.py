from fds_pipeline.jobs import get_foi_request, APIConfig
from dagster import build_op_context
from fds_pipeline.ressources import FDSAPI


def test_get_foi_request():
    context = build_op_context(resources={"fds_api": FDSAPI()})
    get_foi_request(context, APIConfig(id_=82))
