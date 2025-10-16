from celery import Celery

from project.application.interfaces.job_dispatcher_interface import \
    IJobDispatcher
from project.core.config import (CELERY_BROKER_URL, CELERY_NAME,
                                 CELERY_RESULT_BACKEND)

celery = Celery(
    main=CELERY_NAME,
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND,
)

celery.autodiscover_tasks(["project.infrastructure.celery_tasks"])


class CeleryJobDispatcher(IJobDispatcher):

    def dispatch(self, job_name: str, payload: dict):
        celery.send_task(job_name, args=[payload])
