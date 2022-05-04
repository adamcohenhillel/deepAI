"""Deeper 2022, All Rights Reserved
"""
import logging
from typing import Dict
import openai
from celery import shared_task

from worker.task_base import TaskBase


openai.api_key = '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'
TO_EXTRACT = ['Categories', 'Keywords', 'Gender', 'Age Range']
_TO_EXTRACT_JOINED = ', '.join(TO_EXTRACT)
# TODO: Optimize this prompt
_OPENAI_PROMPT = f"Classify the following tweet into: {_TO_EXTRACT_JOINED}\n\n\nTweet: "


@shared_task(bind=True, name='text_analyzer')
def text_analyzer(self: TaskBase, deep_request: str, node_id: int) -> Dict:
    """
    """
    prompt = f"{_OPENAI_PROMPT}\"{deep_request}\""
    logging.info(
        f'About to query OpenAI with the folloiwng prompt: "{prompt}"')
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        temperature=0,
        max_tokens=140,
        top_p=1,
        frequency_penalty=2,
        presence_penalty=0
    )
    logging.info(f'OpenAI response is: {response}')

    # Extract:
    found = {}
    raw_text_response = response['choices'][0]['text']
    for line in raw_text_response.splitlines():
        if line:
            for item in TO_EXTRACT:
                line_start = f'{item.lower()}: '
                if line.lower().startswith(line_start):
                    found[item] = line.lower().replace(
                        line_start, '').split(', ')
                    break
    logging.info(f'Extraction found:\n{found}')
    return found


@shared_task(bind=True, name='add_to_database')
def add_to_database(self, data: Dict) -> None:
    """
    """
    pass
