# from dagster import (
#     build_init_resource_context,
#     DagsterInstance,
# )
# from fds_pipeline.ressources import FDSAPI


# def test_fds_api():

#     with DagsterInstance.ephemeral() as instance:
#         context = build_init_resource_context(instance=instance)
#         FDSAPI().with_resource_context(context).get_foi_request(config.id_)
