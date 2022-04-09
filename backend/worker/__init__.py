"""Adam Cohen Hillel 2022, All Rights Reserved
"""
from unittest import result
from celery import Celery


def create_celery_instance():
    """
    """
    celery_app = Celery(
        broker='redis://localhost',
        backend='redis://localhost',
        include=['worker.tasks'],
        fixups=[],
        task_cls='worker.task_base:TaskBase'
    )
    celery_app.conf.update(result_extended=True)
    celery_app.conf.update(task_track_started=True)
    # celery_app.conf.update(result_expires=0) # TODO: do we want this? IDK

    return celery_app
