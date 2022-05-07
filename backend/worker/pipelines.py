"""
"""

from celery import chain, signature


def analyze_deep_request(deep_request: str, node_id: int, celery_app):
    """
    """
    return chain(
        signature('analyze.text_extraction', args=(deep_request, node_id), app=celery_app),
        signature('analyze.add_describers_nodes', app=celery_app, kwargs={'node_id': node_id})
    )