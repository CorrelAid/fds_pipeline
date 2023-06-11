# from dagster import validate_run_config, build_sensor_context
# from fds_pipeline.jobs import proc_insert_foi_request
# from fds_pipeline.ressources import PostgresQuery,FDSAPI
# from fds_pipeline.sensors import new_foi_requests
# from dagster._core.test_utils import instance_for_test

# from fds_pipeline import defs
# from dotenv import load_dotenv
# import os
# load_dotenv()

# def test_new_foi_requests():
#     context = build_sensor_context(definitions=defs)
#     print(context.__dict__)
#     new_foi_requests(context)
