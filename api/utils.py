from random import randint
from src.predict import predict_single_input


def nn(answers):
    text = ''
    for answer_question in answers:
        question = answer_question[0]
        answer = answer_question[1]
        if question[-1] != '?': question += '?'
        if answer[-1] != '.': answer += '.'
        text += question + " - " + answer + ' '
    print(text)
    out = predict_single_input(text)
    return out