from telebot import types
from src.config.settings import bot

@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.InlineKeyboardMarkup()
    register_button = types.InlineKeyboardButton("Зарегистрироваться", callback_data="register")
    login_button = types.InlineKeyboardButton("Залогиниться", callback_data="login")
    markup.add(register_button, login_button)

    welcome_message = f"Добро пожаловать, {message.from_user.first_name}! Я - бот Task Manager."

    bot.send_message(message.chat.id, welcome_message, parse_mode='html', reply_markup=markup)

# Запуск бота
if __name__ == '__main__':
    bot.infinity_polling()
