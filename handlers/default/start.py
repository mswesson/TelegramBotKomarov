from telebot.types import Message
from loader import bot
from keyboards.keyboard_start_menu import gen_markup, ReplyKeyboardRemove
from handlers.special import translate
from handlers.default import help


@bot.message_handler(commands=["start"])
def bot_start(message: Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Привет, {name}!".format(
        name=message.from_user.full_name), reply_markup=gen_markup())


@bot.message_handler(func=lambda message: message.text == 'Режим "Давай переведем"')
def bot_translate(message: Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Окей, включаю".format(
        name=message.from_user.full_name), reply_markup=ReplyKeyboardRemove())
    translate.bot_translate_start(message)


@bot.message_handler(func=lambda message: message.text == 'Все сначала')
def bot_start_2(message: Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Все сначала, так все сначала".format(
        name=message.from_user.full_name))
    bot_start(message)


@bot.message_handler(func=lambda message: message.text == 'Помощь')
def bot_start_2(message: Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Открываю раздел \"Помощь\"".format(
        name=message.from_user.full_name))
    help.bot_help(message)