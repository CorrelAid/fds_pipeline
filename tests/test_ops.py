from fds_pipeline.jobs import (
    get_foi_request,
    APIConfig,
    extract_foi_request,
    get_jurisdictions,
    extract_jurisdictions,
    extract_campaigns,
    extract_public_body,
    get_campaigns,
    extract_messages,
)
from fds_pipeline.processing import gen_sql_insert_new
import importlib
from dagster import build_op_context
import pandas as pd
from fds_pipeline.ressources import FDSAPI


### Data from single FOI request ######
def test_get_foi_request():
    context = build_op_context(resources={"fds_api": FDSAPI()})
    temp = get_foi_request(context, APIConfig(id_=82))
    temp = list(temp)[0]._value
    assert isinstance(temp, dict)
    assert "id" in temp
    context = build_op_context(resources={"fds_api": FDSAPI()})
    temp = get_foi_request(context, APIConfig(id_=1))
    temp = list(temp)[0]._value
    assert temp is None


def test_extract_foi_request_regular():
    test_dct = importlib.import_module("tests.data.test_foi_req").test_foi_req
    temp = extract_foi_request(test_dct)
    assert isinstance(temp, pd.DataFrame)


def test_extract_foi_request_no_pb():
    # no public body id
    test_dct = importlib.import_module("tests.data.test_foi_req_46").test_foi_req
    temp = extract_foi_request(test_dct)
    temp = list(temp)[0]
    assert temp == "id"


def test_extract_public_body():
    context = build_op_context()
    test_dct = importlib.import_module("tests.data.test_foi_req").test_foi_req
    temp = extract_public_body(context, test_dct)
    temp = list(temp)[0]._value
    assert isinstance(temp, pd.DataFrame)


def test_extract_public_body_no_pb():
    context = build_op_context()
    # no public body id
    test_dct = importlib.import_module("tests.data.test_foi_req_46").test_foi_req
    temp = extract_public_body(context, test_dct)
    temp = list(temp)[0]._value
    assert temp is None


def test_extract_messages():
    test_dct = importlib.import_module("tests.data.test_foi_req").test_foi_req
    temp = extract_messages(test_dct)
    assert isinstance(temp, pd.DataFrame)


def test_sql_public_body():
    test_df = importlib.import_module("tests.data.test_public_body_df").df
    test_sql = importlib.import_module("tests.data.test_public_body_sql").sql
    temp = gen_sql_insert_new(test_df, "public_bodies")
    assert temp == test_sql


def test_sql_foi_request():
    test_df = importlib.import_module("tests.data.test_foi_req_df").df
    test_sql = importlib.import_module("tests.data.test_foi_req_sql").sql
    temp = gen_sql_insert_new(test_df, "foi_requests")
    assert temp == test_sql


#### Data from List of Campaigns ######
def test_get_campaigns():
    context = build_op_context(resources={"fds_api": FDSAPI()})
    temp = get_campaigns(context)
    assert isinstance(temp, list)


def test_extract_campaigns():
    test_dct = importlib.import_module("tests.data.test_campaigns").test_dct
    temp = extract_campaigns(test_dct)
    assert isinstance(temp, pd.DataFrame)


def test_sql_campaigns():
    test_df = importlib.import_module("tests.data.test_campaigns_df").df
    temp = gen_sql_insert_new(test_df, "campaigns")
    test_sql = importlib.import_module("tests.data.test_campaigns_sql").string
    assert temp == test_sql


#### Data from List of Jurisdictions ######


def test_get_jurisdictions():
    context = build_op_context(resources={"fds_api": FDSAPI()})
    temp = get_jurisdictions(context)
    assert isinstance(temp, list)


def test_extract_jurisdictions():
    test_dct = importlib.import_module("tests.data.test_jurisdictions").dct
    temp = extract_jurisdictions(test_dct)
    assert isinstance(temp, pd.DataFrame)
