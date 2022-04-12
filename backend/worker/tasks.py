"""Adam Cohen Hillel 2022, All Rights Reserved
"""
from celery import shared_task

from backend.api.matchmaker.models import MatchRequest


@shared_task(bind=True, name='analayze.keyword_extract')
def analayzer(self, match_request_id: MatchRequest) -> None:
    """
    """
    print("Heyoooo")

def matcher():
    pass