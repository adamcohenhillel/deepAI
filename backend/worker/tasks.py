"""Adam Cohen Hillel 2022, All Rights Reserved
"""
import logging
import openai
from celery import shared_task

from api.matchmaker.models import MatchRequest
from backend.worker.task_base import TaskBase


openai.api_key = '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'
TO_EXTRACT = ['Categories', 'Keywords', 'Gender', 'Age Range']
_TO_EXTRACT_JOINED = ', '.join(TO_EXTRACT)


@shared_task(bind=True, name='analayze.keyword_extract')
def analayzer(self: TaskBase, match_request_id: int) -> None:
    """
    """
    match_request = self.session.query(MatchRequest).get(match_request_id)
    prompt = f"Classify the following tweet into: {_TO_EXTRACT_JOINED}\n\n\nTweet: \"{match_request.raw_request}\""
    logging.info('About to query OpenAI with the folloiwng prompt:')
    logging.info(prompt)
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        temperature=0,
        max_tokens=140,
        top_p=1,
        frequency_penalty=2,
        presence_penalty=0
    )
    logging.info('OpenAI response is:')
    logging.info(response)
    text_result = response['choices'][0]['text']

    # Extract: 
    found = {}
    for line in text_result.splitlines():
        if line:
            for item in TO_EXTRACT:
                line_start = f'{item.lower()}: '
                if line.lower().startswith(line_start):
                    found[item] = line.lower().replace(line_start, '').split(', ')
                    break
    logging.info(f'Extraction found:\n{found}')
