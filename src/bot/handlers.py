from telebot import types
from src.config.settings import bot
from src.database.db import get_db
from src.database.models import User, Task
from sqlalchemy.orm import Session


# Обработка нажатия на Inline-кнопку
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    if call.data == "register":
        register_user(call)
    elif call.data == "login":
        login_user(call)

    # Удаляем сообщение с кнопками после обработки
    bot.delete_message(call.message.chat.id, call.message.message_id)


# Обработчик для регистрации пользователя
def register_user(call):
    with next(get_db()) as db:
        user_in_db = db.query(User).filter(User.telegram_id == call.from_user.id).first()

        if user_in_db:
            bot.send_message(call.message.chat.id, "Вы уже зарегистрированы!")
        else:
            new_user = User(
                first_name=call.from_user.first_name,
                username=call.from_user.username,
                telegram_id=call.from_user.id
            )
            db.add(new_user)
            db.commit()
            bot.send_message(call.message.chat.id, "Регистрация успешна!")


# Обработчик для логина пользователя
def login_user(call):
    with next(get_db()) as db:
        user_in_db = db.query(User).filter(User.telegram_id == call.from_user.id).first()

        if user_in_db:
            bot.send_message(call.message.chat.id, "Вы успешно залогинились и можете работать с задачами.")
            markup = types.InlineKeyboardMarkup()
            my_tasks_button = types.InlineKeyboardButton("Мои задачи", callback_data="my_tasks")
            add_task_button = types.InlineKeyboardButton("Добавить задачу", callback_data="add_task")
            markup.add(my_tasks_button, add_task_button)
            bot.send_message(call.message.chat.id, "Выберите действие:", reply_markup=markup)
        else:
            bot.send_message(call.message.chat.id, "Пожалуйста, зарегистрируйтесь сначала.")

    bot.delete_message(call.message.chat.id, call.message.message_id)
