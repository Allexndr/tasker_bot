from telebot import types
from src.config.settings import bot


@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.InlineKeyboardMarkup()

    register_button = types.InlineKeyboardButton("Зарегистрироваться", callback_data="register")
    login_button = types.InlineKeyboardButton("Залогиниться", callback_data="login")

    markup.add(register_button, login_button)

    welcome_message = """Добро пожаловать, {0.first_name}!
    Я - <b>{1.first_name}</b>, бот Task Manager
""".format(message.from_user, bot.get_me())

    bot.send_message(message.chat.id, welcome_message, parse_mode='html', reply_markup=markup)


# Обрабатываем нажатие на Inline-кнопки
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    if call.data == "register":
        bot.send_message(call.message.chat.id, "Вы выбрали Зарегистрироваться")
    elif call.data == "login":
        bot.send_message(call.message.chat.id, "Вы выбрали Залогиниться")

    bot.delete_message(call.message.chat.id, call.message.message_id)


if __name__ == '__main__':
    bot.infinity_polling()
