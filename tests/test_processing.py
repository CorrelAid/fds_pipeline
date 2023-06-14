from fds_pipeline.processing import del_col
import importlib


def test_del_col():
    test_sql = importlib.import_module("tests.data.test_foi_req_sql_del").sql
    temp = del_col(test_sql)
    assert test_sql == temp
