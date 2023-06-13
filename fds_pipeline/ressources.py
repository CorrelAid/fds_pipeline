from dagster import ConfigurableResource, List
import requests
from urllib.error import HTTPError
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
        try:
            url = self.url + f"request/{id_}"
            res = requests.get(url, headers={"content-type": "application/json"})
            res.raise_for_status()  # Raises an exception for any 4xx or 5xx status code
            return res.json()
        except requests.exceptions.HTTPError as err:
            if res.status_code == 404:
                raise HTTPError(url, 404, "FOI request not found", hdrs={}, fp=None)
            else:
                raise HTTPError(url, res.status_code, err, hdrs={}, fp=None)

    def get_campaigns(self) -> list:
        query = {"limit": 50, "offset": 0}
        url = self.url + "campaign/"
        res = requests.get(url, params=query, headers={"content-type": "application/json"})
        res = res.json()["objects"]
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
