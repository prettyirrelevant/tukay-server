import base64
from enum import IntEnum, unique
from typing import Any

import requests
import shortuuid


class TriviaError(Exception):
    ...


@unique
class TriviaCategory(IntEnum):
    ART = 25
    MUSIC = 12
    SPORTS = 21
    COMICS = 29
    HISTORY = 23
    ANIMALS = 27
    POLITICS = 24
    MYTHOLOGY = 20
    GEOGRAPHY = 22
    MATHEMATICS = 19
    BOARD_GAMES = 16
    CELEBRITIES = 26
    VIDEO_GAMES = 15
    GENERAL_KNOWLEDGE = 9
    SCIENCE_AND_NATURE = 17
    JAPANESE_COMICS_AND_MANGA = 31


class Trivia:
    base_url = 'https://opentdb.com'

    @classmethod
    def fetch_questions(cls, category: TriviaCategory) -> dict[str, Any]:
        response = requests.get(
            timeout=10,
            url=f'{cls.base_url}/api.php',
            params={
                'amount': 4,
                'encode': 'base64',
                'type': 'multiple',
                'difficulty': 'easy',
                'category': category.value,
            },
        )
        if response.status_code != 200:
            raise TriviaError(response.text)

        data = response.json()
        if data.get('response_code', None) != 0:
            raise TriviaError(response.text)

        answers = {}
        questions = {}
        for entry in data['results']:
            question_id = f'ques_{shortuuid.uuid()}'
            answer = base64.b64decode(entry['correct_answer']).decode()
            questions[question_id] = {
                'question': base64.b64decode(entry['question']).decode(),
                'options': [base64.b64decode(i).decode() for i in entry['incorrect_answers']] + [answer],
            }
            answers[question_id] = answer

        return {'questions': questions, 'answers': answers}
