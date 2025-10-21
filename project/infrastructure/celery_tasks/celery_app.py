from celery import Celery

from project.application.interfaces.job_dispatcher_interface import IJobDispatcher
from project.core.config import settings

celery = Celery(
    main=settings.celery.name,
    broker=settings.celery.broker_url,
    backend=settings.celery.result_backend,
)

celery.autodiscover_tasks(["project.infrastructure.celery_tasks"])


class CeleryJobDispatcher(IJobDispatcher):

    def dispatch(self, job_name: str, payload: dict):
        celery.send_task(job_name, args=[payload])
