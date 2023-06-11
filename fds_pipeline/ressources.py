from dagster import ConfigurableResource, List
import requests
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.engine import Connectable
from pydantic import PrivateAttr


class FDSAPI(ConfigurableResource):
    url: str = "https://fragdenstaat.de/api/v1/"

    def get_total(self) -> int:
        query = {"limit": 1, "offset": 0}
        url = self.url + "request/"
        res = requests.get(url, params=query, headers={"content-type": "application/json"})
        res = res.json()
        return res["meta"]["total_count"]

    def get_foi_request(self, id_) -> dict:
        res = requests.get(self.url + f"request/{id_}", headers={"content-type": "application/json"})
        res = res.json()
        return res


class PostgresQuery(ConfigurableResource):
    db: str
    user: str
    pw: str
    port: str
    host: str
    _db_connection: Connectable = PrivateAttr()

    @contextmanager
    def yield_for_execution(self, context):
        engine = create_engine(f"postgresql://{self.user}:{self.pw}@{self.host}:{self.port}/{self.db}")
        with engine.connect() as conn:
            # set up the connection attribute so it can be used in the execution
            self._db_connection = conn

            # yield, allowing execution to occur
            yield self

    def single(self, query: str) -> List[str]:
        rows = self._db_connection.execute(query)
        data = [row[0] for row in rows]
        return data[0]
