from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

from text import courses
from text import questions
from config import number_of_courses


def generate_course_selection_menu():
    menu = []
    for i, course in enumerate(courses):
        menu.append([InlineKeyboardButton(text=course, callback_data=f"course_{i}")])
    return InlineKeyboardMarkup(inline_keyboard=menu)


def generate_question_kb():
    # Вопросы, которые будут отображаться на кнопках
    questions = [
        'О каком вебинаре Вы хотите рассказать?',
        'Что вам больше всего понравилось в теме вебинара и почему?',
        'Были ли моменты в вебинаре, которые вызвали затруднения в понимании материала? Можете описать их?',
        'Какие аспекты вебинара, по вашему мнению, нуждаются в улучшении и какие конкретные изменения вы бы предложили?',
        'Есть ли темы или вопросы, которые вы бы хотели изучить более подробно в следующих занятиях?'
    ]

    # Создание списка кнопок, где каждая кнопка — это InlineKeyboardButton
    buttons = [[InlineKeyboardButton(text=question, callback_data=f"question_{i}")] for i, question in enumerate(questions)]

    # Создание InlineKeyboardMarkup с кнопками
    questions_kb = InlineKeyboardMarkup(inline_keyboard=buttons)

    return questions_kb


exit_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="◀️ Выйти в меню")]], resize_keyboard=True)
iexit_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="◀️ Выйти в меню", callback_data="menu")]])

