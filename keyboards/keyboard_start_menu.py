from loader import bot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


def gen_markup():
    button_1 = KeyboardButton(text='Режим "Давай переведем"')
    button_2 = KeyboardButton(text='Все сначала')
    button_3 = KeyboardButton(text='Помощь')

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(button_1)
    keyboard.add(button_2, button_3)
    return keyboard
