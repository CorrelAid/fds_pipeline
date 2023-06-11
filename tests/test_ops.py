from fds_pipeline.jobs import (
    get_foi_request,
    APIConfig,
    extract_foi_request,
    extract_jurisdiction,
    extract_public_body,
    retreive_campaigns,
    extract_messages,
)
import importlib
from dagster import build_op_context
import pandas as pd
from fds_pipeline.ressources import FDSAPI


def test_get_foi_request():
    context = build_op_context(resources={"fds_api": FDSAPI()})
    temp = get_foi_request(context, APIConfig(id_=82))
    assert isinstance(temp, dict)
    assert "id" in temp


def test_extract_foi_request():
    test_dct = importlib.import_module("tests.data.test_foi_req").test_foi_req
    temp = extract_foi_request(test_dct)
    assert isinstance(temp, pd.DataFrame)


def test_extract_jurisdiction():
    test_dct = importlib.import_module("tests.data.test_foi_req").test_foi_req
    temp = extract_jurisdiction(test_dct)
    assert isinstance(temp, pd.DataFrame)


def test_extract_public_body():
    test_dct = importlib.import_module("tests.data.test_foi_req").test_foi_req
    temp = extract_public_body(test_dct)
    assert isinstance(temp, pd.DataFrame)


def test_extract_messages():
    test_dct = importlib.import_module("tests.data.test_foi_req").test_foi_req
    temp = extract_messages(test_dct)
    assert isinstance(temp, pd.DataFrame)


def test_retreive_campaigns():
    context = build_op_context(resources={"fds_api": FDSAPI()})
    temp = retreive_campaigns(context)
    assert isinstance(temp, pd.DataFrame)
