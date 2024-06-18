from telebot.types import Message
from loader import bot


@bot.message_handler()
def bot_start(message: Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Не понимаю тебя. Возможно стоит обратиться к /start')