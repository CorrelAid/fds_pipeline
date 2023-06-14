from fds_pipeline.jobs import (
    get_foi_request,
    APIConfig,
    extract_foi_request,
    get_jurisdictions,
    extract_jurisdictions,
    sql_campaigns,
    sql_foi_request,
    extract_campaigns,
    extract_public_body,
    get_campaigns,
    extract_messages,
    sql_public_body,
)
import importlib
from dagster import build_op_context
from dagster._core.definitions.events import Failure
import pandas as pd
from fds_pipeline.ressources import FDSAPI


### Data from single FOI request ######
def test_get_foi_request():
    context = build_op_context(resources={"fds_api": FDSAPI()})
    temp = get_foi_request(context, APIConfig(id_=82))
    assert isinstance(temp, dict)
    assert "id" in temp
    context = build_op_context(resources={"fds_api": FDSAPI()})
    try:
        temp = get_foi_request(context, APIConfig(id_=1))
    except Failure as err:
        assert err.description == "FOI request not found"


def test_extract_foi_request_regular():
    test_dct = importlib.import_module("tests.data.test_foi_req").test_foi_req
    temp = extract_foi_request(test_dct)
    assert isinstance(temp, pd.DataFrame)


def test_extract_foi_request_no_pb():
    # no public body id
    test_dct = importlib.import_module("tests.data.test_foi_req_46").test_foi_req
    temp = extract_foi_request(test_dct)
    assert isinstance(temp, pd.DataFrame)


def test_extract_public_body():
    test_dct = importlib.import_module("tests.data.test_foi_req").test_foi_req
    temp = extract_public_body(test_dct)
    assert isinstance(temp, pd.DataFrame)


def test_extract_public_body_no_pb():
    # no public body id
    test_dct = importlib.import_module("tests.data.test_foi_req_46").test_foi_req
    try:
        extract_public_body(test_dct)
    except Failure as err:
        assert str(err) == repr("FOI request was not assigned a public body")


def test_extract_messages():
    test_dct = importlib.import_module("tests.data.test_foi_req").test_foi_req
    temp = extract_messages(test_dct)
    assert isinstance(temp, pd.DataFrame)


def test_sql_public_body():
    test_df = importlib.import_module("tests.data.test_public_body_df").df
    test_sql = importlib.import_module("tests.data.test_public_body_sql").sql
    temp = sql_public_body(test_df)
    print(temp)
    assert temp == test_sql


def test_sql_foi_request():
    test_df = importlib.import_module("tests.data.test_foi_req_df").df
    test_sql = importlib.import_module("tests.data.test_foi_req_sql").sql
    temp = sql_foi_request(test_df)
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
    temp = sql_campaigns(test_df)
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
