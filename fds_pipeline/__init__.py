from dagster import Definitions, EnvVar, ScheduleDefinition, DefaultScheduleStatus

from dagster_aws.s3 import s3_pickle_io_manager, s3_resource
from fds_pipeline.jobs import proc_insert, proc_insert_campaigns, proc_insert_jurisdictions
from fds_pipeline.ressources import FDSAPI, PostgresQuery
from fds_pipeline.sensors import new_foi_requests


campaigns_every_hour = ScheduleDefinition(
    job=proc_insert_campaigns, cron_schedule="0 * * * *", default_status=DefaultScheduleStatus.RUNNING
)
jurisdictions_every_hour = ScheduleDefinition(
    job=proc_insert_jurisdictions, cron_schedule="0 * * * *", default_status=DefaultScheduleStatus.RUNNING
)

defs = Definitions(
    jobs=[proc_insert, proc_insert_campaigns, proc_insert_jurisdictions],
    sensors=[new_foi_requests],
    schedules=[campaigns_every_hour, jurisdictions_every_hour],
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
