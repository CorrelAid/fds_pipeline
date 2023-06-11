from dagster import op, job, Config, Out
from dagster_pandas import DataFrame
from fds_pipeline.ressources import FDSAPI
from fds_pipeline.processing import (
    process_foi_request,
    process_jurisdiction,
    process_public_body,
    process_campaigns,
    process_messages,
)
from fds_pipeline.df_types import FOIRequestDf, JurisdictionDf, PublicBodyDf, CampaignDf, MessageDf


class APIConfig(Config):
    id_: int


# job that calls an op that retrieves a foi request given an id
# handle not found error
@op
def get_foi_request(context, config: APIConfig, fds_api: FDSAPI) -> dict:
    foi_req = fds_api.get_foi_request(config.id_)
    return foi_req


@op(out=Out(FOIRequestDf))
def extract_foi_request(get_foi_request) -> DataFrame:
    df = process_foi_request(get_foi_request)
    return df


@op(out=Out(JurisdictionDf))
def extract_jurisdiction(get_foi_request) -> DataFrame:
    df = process_jurisdiction(get_foi_request)
    return df


@op(out=Out(PublicBodyDf))
def extract_public_body(get_foi_request) -> DataFrame:
    df = process_public_body(get_foi_request)
    return df


@op(out=Out(MessageDf))
def extract_messages(get_foi_request) -> DataFrame:
    df = process_messages(get_foi_request)
    return df


@job
def proc_insert_foi_request():
    data = get_foi_request()
    foi_request = extract_foi_request(data)
    public_body = extract_public_body(data)
    jurisdiction = extract_jurisdiction(data)
    messages = extract_messages(data)
    return foi_request, public_body, jurisdiction, messages


# We have to do this separetely because foi_request object retreived from api doesnt contain all the data
@op(out=Out(CampaignDf))
def retreive_campaigns(context, fds_api: FDSAPI) -> DataFrame:
    data = fds_api.get_campaigns()
    campaigns = process_campaigns(data)
    return campaigns


@job
def proc_insert_campaigns():
    return retreive_campaigns()
