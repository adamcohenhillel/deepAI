"""Deeper 2022, All Rights Reserved

TODO: Need to not be depended on OpenAI API, Too expensive
"""
from random import randint
import logging
from typing import Dict

import openai

openai.api_key = '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'
TO_EXTRACT = ['Categories', 'Keywords', 'Gender', 'Age Range']
_TO_EXTRACT_JOINED = ', '.join(TO_EXTRACT)
_OPENAI_PROMPT = f"Classify the following tweet into: {_TO_EXTRACT_JOINED}\n\n\nTweet: "  # TODO: Optimize this prompt

_s = 'abcdefghijklmnopkrstuvwxyz123456789ABCDEFGHIJKLMNOPQRSTUVWX!@£$%^&*'

async def openai_text_extraction(deep_request: str) -> Dict:
    """Calling OpenAI API with a prompt and extract
    the relevant information out of it into a dict

    :param str deep_request: A raw text to send to openai

    :return:
    """
    return {'Categories': _s[randint(0, len(_s))], 'Keywords': _s[randint(0, len(_s))], 'Gender': 'Male', 'Age Range': '18-25'}
    prompt = f"{_OPENAI_PROMPT}\"{deep_request}\""
    logging.info(f'About to query OpenAI with the folloiwng prompt: "{prompt}"')
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
