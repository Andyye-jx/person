import logging
import inject
from celery import Task, Celery
from celery.result import AsyncResult
from kombu import Exchange, Queue
from config import Config, PersonSession

logger = logging.getLogger(__name__)


class APITask(Task):

    def run(self, *args, **kwargs):
        return super().run(*args, **kwargs)

    abstract = True

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        inject.instance(PersonSession).remove()

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        logger.error('exc: %s, task_id: %s, args: %s, einfo: %s', exc, task_id, args, einfo, exc_info=True)


class MyAsyncResult(AsyncResult):
    def get(self, *args, **kwargs):
        if not args:
            if "timeout" not in kwargs:
                kwargs["timeout"] = 60
        return super().get(*args, **kwargs)


class MyCelery(Celery):
    AsyncResult = MyAsyncResult


@inject.params(config=Config)
def init_celery(config: Config):
    broker = config.celery_broker_url
    result_backend = config.celery_result_backend

    celery = Celery('person', set_as_current=False)
    celery.conf.update(
        CELERY_QUEUES=(
            Queue('celery', Exchange('celery'), routing_key='default'),
        ),
        CELERY_DEFAULT_QUEUE='celery',
        CELERY_DEFAULT_ROUTING_KEY='default',
        CELERY_DEFAULT_EXCHANGE_TYPE='direct',
        BROKER_URL=broker,
        CELERY_RESULT_BACKEND=result_backend,
        CELERY_RESULT_PERSISTENT=False,
        CELERY_TASK_RESULT_EXPIRES=300,
        CELERY_TASK_SERIALIZER='json',
        CELERY_ACCEPT_CONTENT=['json'],  # Ignore other content
        CELERY_RESULT_SERIALIZER='json',
        CELERY_TIMEZONE='Asia/Shanghai',
        CELERY_ENABLE_UTC=True,
        TOTORO_AMQP_CONNECTION_POOL={
            'max_idle_connections': 1,
            'max_open_connections': 500,
            'max_recycle_sec': 3600
        }, )
    return celery
