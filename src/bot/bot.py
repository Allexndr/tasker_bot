from telebot import types
from src.config.settings import bot  # Импортируем настройки бота
from src.bot.handlers import handle_callback  # Импортируем обработчики

@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.InlineKeyboardMarkup()

    register_button = types.InlineKeyboardButton("Зарегистрироваться", callback_data="register")
    login_button = types.InlineKeyboardButton("Залогиниться", callback_data="login")

    markup.add(register_button, login_button)

    welcome_message = """Добро пожаловать, {0.first_name}!
    Я - <b>{1.first_name}</b>, бот Task Manager""".format(message.from_user, bot.get_me())

    bot.send_message(message.chat.id, welcome_message, parse_mode='html', reply_markup=markup)


if __name__ == '__main__':
    bot.infinity_polling()
