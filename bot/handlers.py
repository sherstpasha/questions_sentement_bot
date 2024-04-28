from aiogram import types, Router
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from kb import generate_course_selection_menu, generate_question_kb
import text

#from aiogram import flags
#from aiogram.fsm.context import FSMContext
#from aiogram.types.callback_query import CallbackQuery

import utils
from states import Gen


class CourseStates(StatesGroup):
    Selected_course = State()  # Состояние выбранного курса
    waiting_for_answer = State()


router = Router()

@router.message(Command('start', 'restart'))
async def start_command(message: types.Message):
    """Отправляет приветственное сообщение и клавиатуру выбора курса."""
    await message.answer(text.greet.format(name=message.from_user.full_name), reply_markup=generate_course_selection_menu())


@router.callback_query(lambda c: c.data.startswith('course_'))
async def course_selected(callback_query: CallbackQuery, state: FSMContext):
    course_id = callback_query.data.split('_')[1]  # Это значение может быть использовано для других целей
    await callback_query.answer()
    try:
        questions_kb = generate_question_kb()  # Теперь вызываем без аргументов
        await callback_query.message.edit_text("Выберите вопрос:", reply_markup=questions_kb)
        await state.set_state(CourseStates.selected_course)
        await state.update_data(course_id=course_id)
    except Exception as e:
        print(f"Ошибка при генерации клавиатуры: {str(e)}")


@router.callback_query(lambda c: c.data.startswith('question_'))
async def question_selected(callback_query: CallbackQuery, state: FSMContext):
    """Обрабатывает выбор вопроса и запрашивает ответ."""
    await callback_query.answer()
    question_number = callback_query.data.split('_')[2]
    await callback_query.message.edit_text(f"Введите ответ на {question_number}:")
    await state.set_state(CourseStates.waiting_for_answer)
    await state.update_data(question_number=question_number)


@router.message(CourseStates.waiting_for_answer)
async def answer_received(message: types.Message, state: FSMContext):
    """Принимает ответ и сохраняет его в состоянии."""
    user_data = await state.get_data()
    question_number = user_data['question_number']
    await state.update_data({f"answer_{question_number}": message.text})
    course_id = user_data['course_id']  # Получение ID курса из состояния
    await message.answer("Ответ принят. Выберите следующий вопрос или закончите опрос.", reply_markup=generate_question_kb())

    # Проверка, получены ли все ответы
    answers = {k: v for k, v in (await state.get_data()).items() if k.startswith('answer_')}
    if len(answers) == 5:
        await message.answer("Все ответы получены.")
        await state.reset_state()
        print(answers)  # Вывод ответов в консоль

