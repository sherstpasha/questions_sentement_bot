from telegram import ReplyKeyboardMarkup
import requests as r

from config import BACKEND


# Список курсов
def get_courses():
    courses = r.get(BACKEND + '/courses')
    if courses.status_code == 200:
        courses = courses.json()
    return courses

# Словарь вопросов по курсам
def get_questions():
    questions = r.get(BACKEND + '/questions')
    if questions.status_code == 200:
        questions = questions.json()
    return questions

# Функция для создания клавиатуры с курсами
def course_keyboard():
    #return ReplyKeyboardMarkup([[course] for course in COURSES], resize_keyboard=True, one_time_keyboard=True)

    courses = get_courses()
    return ReplyKeyboardMarkup([[course['name']] for course in courses], resize_keyboard=True, one_time_keyboard=True)
    