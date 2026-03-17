from celery import Celery
from celery.signals import task_postrun, task_prerun
from celery.utils.log import get_task_logger
from kombu import Exchange, Queue


logger = get_task_logger(__name__)


def _task_name(sender) -> str:
    """Resolve a human-friendly task name for signal callbacks."""
    if hasattr(sender, "name") and sender.name:
        return sender.name
    if isinstance(sender, str):
        return sender
    return "unknown"


@task_prerun.connect(weak=False)
def announce_task_start(sender=None, task_id=None, **_: object) -> None:
    logger.info("Task %s (%s) starting", _task_name(sender), task_id)


@task_postrun.connect(weak=False)
def announce_task_finish(sender=None, task_id=None, state=None, **_: object) -> None:
    logger.info("Task %s (%s) finished with state %s", _task_name(sender), task_id, state)


def create_celery_app() -> Celery:
    modules = ["interview.tasks"]

    app = Celery(
        "interview",
        include=modules,
    )

    default_exchange = Exchange("default", type="direct", durable=True)

    default_queue = Queue(
        "default",
        exchange=default_exchange,
        routing_key="default",
        durable=True,
    )

    app.conf.update(
        task_default_queue="default",
        task_default_exchange="default",
        task_default_routing_key="default",
        task_queues=[default_queue],
        task_track_started=True,
        task_acks_late=True,
        task_reject_on_worker_lost=True,
        worker_prefetch_multiplier=1,
        result_expires=3600,
        worker_hijack_root_logger=False,
        worker_redirect_stdouts=False,
        worker_log_color=False,
    )

    return app


celery_app: Celery = create_celery_app()
