from telebot import types
from src.config.settings import bot
from src.database.db import get_db
from src.database.models import User
from sqlalchemy.orm import Session


# Обрабатываем нажатие на Inline-кнопки
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    if call.data == "register":
        register_user(call)
    elif call.data == "login":
        bot.send_message(call.message.chat.id, "Вы выбрали Залогиниться")

    # Удаляем сообщение с кнопками после обработки
    bot.delete_message(call.message.chat.id, call.message.message_id)


# Обработчик для регистрации пользователя
def register_user(call):
    db: Session = next(get_db())  # Получаем сессию базы данных

    # Проверяем, зарегистрирован ли уже пользователь
    user_in_db = db.query(User).filter(User.telegram_id == call.from_user.id).first()

    if user_in_db:
        bot.send_message(call.message.chat.id, "Вы уже зарегистрированы!")
    else:
        # Добавляем нового пользователя в базу данных
        new_user = User(
            first_name=call.from_user.first_name,
            username=call.from_user.username,
            telegram_id=call.from_user.id
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        bot.send_message(call.message.chat.id, "Регистрация успешна!")
