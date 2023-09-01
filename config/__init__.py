import inject
import logging

from celery import Celery
from sqlalchemy.orm import scoped_session, Session, sessionmaker
from sqlalchemy import create_engine
from redis import StrictRedis


logging.basicConfig(
    level=logging.INFO,
    format="[%(name)s]:%(asctime)s:%(filename)s:%(lineno)d %(levelname)s/%(processName)s %(message)s",
)
logging.getLogger("sqlalchemy.engine.base.Engine").disabled = True
logging.getLogger("werkzeug").disabled = True

logger = logging.getLogger(__name__)


class Config:
    admin_port = 5001
    app_port = 5556
    cache_redis_url = "redis://:123456@127.0.0.1:6379/0"
    database_url = "mysql+pymysql://root:KLAEKHiwi3/S@127.0.0.1:3306/person"
    celery_broker_url = "redis://:123456@127.0.0.1:6379/1"
    celery_result_backend = "redis://:123456@127.0.0.1:6379/2"
    # app token密钥
    app_token_secret_key = ""
    # admin token密钥
    admin_token_secret_key = ""


class ConfigFromFile(Config):
    pass


class CacheRedis(StrictRedis):
    pass


class PersonSession(scoped_session, Session):
    pass


def create_session(database_url: str) -> scoped_session:
    engine = create_engine(database_url, pool_size=10)
    return scoped_session(sessionmaker(engine))


def configure_fromfile(binder: inject.Binder):
    binder.bind(Config, ConfigFromFile)
    binder.bind_to_constructor(
        PersonSession, lambda: create_session(ConfigFromFile.database_url)
    )
    binder.bind_to_constructor(
        CacheRedis, lambda: StrictRedis.from_url(ConfigFromFile.cache_redis_url)
    )
    from service.tasks import init_celery

    binder.bind_to_constructor(Celery, init_celery)
