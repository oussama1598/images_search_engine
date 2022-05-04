from functools import lru_cache

from cassandra.auth import PlainTextAuthProvider
from cassandra.cluster import Cluster, Session

from backend.src.settings import settings


@lru_cache()
def get_session() -> Session:
    auth_provider = PlainTextAuthProvider(username=settings.DB_USERNAME, password=settings.DB_PASSWORD)
    cluster = Cluster([settings.DB_HOST], port=settings.DB_PORT, auth_provider=auth_provider)

    return cluster.connect()
