"""Deeper 2022, All Rights Reserved
"""
import logging
from worker import create_celery_instance


if __name__ == '__main__':
    logging.info('Starting worker...')

    argv = ['worker', '--loglevel=info']
    worker2 = create_celery_instance()
    worker2.worker_main(argv=argv)
