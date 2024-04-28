from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import keyboard as kb
from config import BOT_TOKEN 
import requests as r
from config import BACKEND


# Делаем функции асинхронными и используем await для асинхронных вызовов
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(
        "Привет! Выберите курс, по которому хотите пройти вопросы:",
        reply_markup=kb.course_keyboard()
    )

async def handle_course_selection(update: Update, context: CallbackContext) -> None:
    course = update.message.text
    courses = kb.get_courses()
    if course in map(lambda x: x['name'], courses):
        for i in courses: 
            if i['name'] == course: 
                index = i['id']
                break
        context.user_data['current_course'] = index
        context.user_data['question_index'] = 0
        await ask_question(update, context)
    else:
        await update.message.reply_text("Пожалуйста, выберите курс из предложенных.")

async def ask_question(update: Update, context: CallbackContext) -> None:
    course = context.user_data['current_course']
    index = context.user_data['question_index']
    if 'questions' in context.user_data:
        questions = context.user_data['questions']
    else:
        questions = kb.get_questions()
        context.user_data['questions'] = questions
        context.user_data['answers_id'] = []
    if index < len(questions):
        await update.message.reply_text(questions[index]['text'])
    else:

        data = {
            'course': context.user_data['current_course'], # тут надо вставить айди курса который выбрал пользователь
            'answers': context.user_data['answers_id']
        }    
        data = r.post(BACKEND + '/data/', json=data)
        if data.status_code == 201:
             print(data.json())

        await update.message.reply_text("Вы ответили на все вопросы курса!")
        del context.user_data['current_course']
        del context.user_data['question_index']
        del context.user_data['questions']
        del context.user_data['answers_id']

async def handle_response(update: Update, context: CallbackContext) -> None:
    if 'current_course' in context.user_data:

        answer = answer = {'question': context.user_data['questions'][context.user_data['question_index']]['id'],
              'text': update.message.text,
              }
        
        answer = r.post(BACKEND + '/answers/', json=answer) # /answers/ слеш в конце обязательно
        if answer.status_code == 201:
            answer = answer.json()
        context.user_data['answers_id'].append(answer['id'])

        context.user_data['question_index'] += 1
        await ask_question(update, context)

def main() -> None:
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    # Разделяем обработку сообщений на две разные функции
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND & filters.Regex('^(' + '|'.join(map(lambda x: x['name'], kb.get_courses())) + ')$'), handle_course_selection))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND & ~filters.Regex('^(' + '|'.join(map(lambda x: x['name'], kb.get_courses())) + ')$'), handle_response))

    application.run_polling()

if __name__ == '__main__':
    main()
