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
    elif call.data == "my_tasks":
        show_tasks(call)
    elif call.data == "add_task":
        prompt_add_task(call)
    elif call.data.startswith("delete_task_"):
        delete_task(call)

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

# Обработчик для просмотра задач
def show_tasks(call):
    with next(get_db()) as db:
        # Retrieve the user by telegram_id
        user_in_db = db.query(User).filter(User.telegram_id == call.from_user.id).first()

        if not user_in_db:
            bot.send_message(call.message.chat.id, "Пожалуйста, зарегистрируйтесь сначала.")
            return

        tasks = db.query(Task).filter(Task.user_id == user_in_db.id).all()

        print(f"Tasks for user {user_in_db.id}: {tasks}")  

        if tasks:
            for task in tasks:
                markup = types.InlineKeyboardMarkup()
                delete_button = types.InlineKeyboardButton(f"Удалить задачу {task.id}",
                                                           callback_data=f"delete_task_{task.id}")
                markup.add(delete_button)
                bot.send_message(call.message.chat.id, f"Задача: {task.description}", reply_markup=markup)
        else:
            bot.send_message(call.message.chat.id, "У вас нет задач.")


# Обработчик для добавления задачи
def prompt_add_task(call):
    msg = bot.send_message(call.message.chat.id, "Введите описание задачи:")
    bot.register_next_step_handler(msg, add_task)

def add_task(message):
    with next(get_db()) as db:
        user_in_db = db.query(User).filter(User.telegram_id == message.from_user.id).first()

        if user_in_db:
            new_task = Task(
                description=message.text,
                user_id=user_in_db.id
            )
            db.add(new_task)
            db.commit()
            print(f"Task added: {new_task.description}, User: {new_task.user_id}")
            bot.send_message(message.chat.id, "Задача успешно добавлена!")
        else:
            bot.send_message(message.chat.id, "Сначала залогиньтесь!")

# Обработчик для удаления задачи
def delete_task(call):
    task_id = int(call.data.split("_")[-1])
    with next(get_db()) as db:
        task = db.query(Task).filter(Task.id == task_id).first()

        if task:
            db.delete(task)
            db.commit()
            bot.send_message(call.message.chat.id, f"Задача {task_id} успешно удалена!")
        else:
            bot.send_message(call.message.chat.id, "Задача не найдена.")
