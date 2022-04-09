"""Adam Cohen Hillel 2022, All Rights Reserved
"""
from celery import shared_task


@shared_task(bind=True, name='analayzer')
def analayzer(self):
    """
    """
    print("Heyoooo")

def matcher():
    pass