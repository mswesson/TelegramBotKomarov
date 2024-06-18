from telebot.types import Message
from loader import bot


@bot.message_handler(commands=["help"])
def bot_help(message: Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Когда-то я пропишу помощь :)')