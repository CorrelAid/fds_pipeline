from dagster import op, job, Config, Out, Failure
from dagster_pandas import DataFrame
from urllib.error import HTTPError
from fds_pipeline.ressources import FDSAPI, PostgresQuery
from fds_pipeline.processing import (
    process_foi_request,
    process_jurisdictions,
    process_public_body,
    process_campaigns,
    process_messages,
    gen_sql_insert_new,
)
from fds_pipeline.df_types import FOIRequestDf, JurisdictionDf, PublicBodyDf, CampaignDf, MessageDf


class APIConfig(Config):
    id_: int


@op
def get_foi_request(context, config: APIConfig, fds_api: FDSAPI) -> dict:
    context.log.info(f"Getting foi request with id {config.id_}")
    try:
        foi_req = fds_api.get_foi_request(config.id_)
        return foi_req
    except HTTPError as err:
        if err.status == 404:
            raise Failure(
                description=err.msg,
                metadata={"http_status": err.status, "error_message": err.msg},
            )


###### Extract Objects
@op(out=Out(FOIRequestDf))
def extract_foi_request(get_foi_request) -> DataFrame:
    df = process_foi_request(get_foi_request)
    return df


@op(out=Out(PublicBodyDf))
def extract_public_body(get_foi_request) -> DataFrame:
    try:
        df = process_public_body(get_foi_request)
        return df
    except KeyError as err:
        raise Failure(description=str(err))


@op(out=Out(MessageDf))
def extract_messages(get_foi_request) -> DataFrame:
    df = process_messages(get_foi_request)
    return df


###### Generate SQL


@op
def sql_public_body(extract_public_body) -> str:
    return gen_sql_insert_new(extract_public_body, "public_bodies")


@op
def sql_foi_request(extract_foi_request) -> str:
    return gen_sql_insert_new(extract_foi_request, "foi_requests")


@op
def sql_messages(extract_messages) -> str:
    return gen_sql_insert_new(extract_messages, "messages")


###### Execute SQL
@op
def insert_public_body(sql_public_body, postgres_query: PostgresQuery):
    print(sql_public_body)
    print(type(sql_public_body))
    postgres_query.execute(sql_public_body)


@op
def insert_foi_request(sql_foi_request, postgres_query: PostgresQuery):
    postgres_query.execute(sql_foi_request)


@op
def insert_messages(sql_messages, postgres_query: PostgresQuery):
    postgres_query.execute(sql_messages)


@job
def proc_insert() -> None:
    data = get_foi_request()
    try:
        public_body = extract_public_body(data)
    except Failure:
        pass
    else:
        insert_public_body(sql_public_body(public_body))
    insert_foi_request(sql_foi_request(extract_foi_request(data)))
    insert_messages(sql_messages(extract_messages(data)))


# Campaigns
# We have to do this separetely because foi_request object retreived from api doesnt contain all the data
@op
def get_campaigns(context, fds_api: FDSAPI) -> list:
    return fds_api.get_list("campaign")


@op(out=Out(CampaignDf))
def extract_campaigns(get_campaigns) -> DataFrame:
    return process_campaigns(get_campaigns)


@op
def sql_campaigns(extract_campaigns) -> str:
    return gen_sql_insert_new(extract_campaigns, "campaigns")


@op
def insert_campaigns(sql_campaigns, postgres_query: PostgresQuery):
    postgres_query.execute(sql_campaigns)


@job
def proc_insert_campaigns():
    insert_campaigns(sql_campaigns(extract_campaigns(get_campaigns())))
    # return retreive_campaigns()


# Jurisdictions
# We have to do this separetely because foi_request object retreived from api doesnt contain jurisdiction data when its
# null
@op
def get_jurisdictions(context, fds_api: FDSAPI) -> list:
    return fds_api.get_list("jurisdiction")


@op(out=Out(JurisdictionDf))
def extract_jurisdictions(get_jurisdictions) -> DataFrame:
    return process_jurisdictions(get_jurisdictions)


@op
def sql_jurisdictions(extract_jurisdictions) -> str:
    return gen_sql_insert_new(extract_jurisdictions, "jurisdictions")


@op
def insert_jurisdictions(sql_jurisdictions, postgres_query: PostgresQuery):
    postgres_query.execute(sql_jurisdictions)


@job
def proc_insert_jurisdictions():
    insert_jurisdictions(sql_jurisdictions(extract_jurisdictions(get_jurisdictions())))
    # return retreive_campaigns()
