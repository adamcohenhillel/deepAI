"""Adam Cohen Hillel 2022, All Rights Reserved
"""
from celery import Celery


def create_app():
    """
    """
    celery_app = Celery()


if __name__ == '__main__':
    app = create_app()
    