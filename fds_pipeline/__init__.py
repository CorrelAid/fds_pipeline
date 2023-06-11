from dagster import Definitions, EnvVar

from dagster_aws.s3 import s3_pickle_io_manager, s3_resource
from fds_pipeline.jobs import proc_insert_foi_request
from fds_pipeline.ressources import FDSAPI, PostgresQuery
from fds_pipeline.sensors import new_foi_requests


defs = Definitions(
    jobs=[proc_insert_foi_request],
    sensors=[new_foi_requests],
    resources={
        "io_manager": s3_pickle_io_manager.configured({"s3_bucket": {"env": "MINIO_BUCKET"}}),
        "s3": s3_resource.configured({"endpoint_url": {"env": "MINIO_ENDPOINT_URL"}}),
        "postgres_query": PostgresQuery(
            db=EnvVar("POSTGRES_DB"),
            user=EnvVar("POSTGRES_USER"),
            pw=EnvVar("POSTGRES_PASSWORD"),
            host=EnvVar("POSTGRES_HOST"),
            port=EnvVar("POSTGRES_PORT"),
        ),
        "fds_api": FDSAPI(),
    },
)
