from telebot.types import Message
from loader import bot
from states.states import StateTranslate
import re
import requests
import json
from config_data.config import YANDEX_API
from keyboards.keyboard_start_menu import gen_markup


def get_translate(api_key: str, format: str, text: str):
    url = ('https://dictionary.yandex.net/api/v1/dicservice.json/lookup?key='
           '{api}&lang={format}&text={text}').format(
        api=api_key,
        format=format,
        text=text)
    response = requests.get(url)
    if response.ok:
        data = json.loads(response.text)
        res = search_key(data, 'text')
        return res[1:3]
    else:
        raise ConnectionError


def search_key(collection: dict | list, key: str) -> list:
    final_res = list()
    if collection.get(key):
        final_res.append(collection.get(key))

    for val in collection.values():
        if isinstance(val, dict):
            final_res += search_key(val, key)
        elif isinstance(val, list):
            for elem in val:
                final_res += search_key(elem, key)
    return final_res


translate_memory = 'ru-en'


@bot.message_handler(commands=["translate"])
def bot_translate_start(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    bot.set_state(user_id, StateTranslate.format, chat_id)
    bot.send_message(chat_id, 'Функция "Давай переведем"')
    bot.send_message(chat_id, "На какой язык будем переводить?\n"
                              "1. Русский\n"
                              "2. English")


@bot.message_handler(state=StateTranslate.format)
def bot_translate_format(message: Message):
    global translate_memory
    chat_id = message.chat.id
    user_id = message.from_user.id
    pattern_ru = '|'.join(["русский", "рус", "российский", "1", "один", "one", "rus", "russian", "рашн", "рашен"])
    pattern_en = '|'.join(["английский", "2", "два", "two", "енглиш", "english", "eng"])
    if re.search(pattern_ru, str(message.text).lower()):
        bot.set_state(user_id, StateTranslate.end, chat_id)
        bot.send_message(chat_id, 'Понял тебя. Переводим на русский язык')
        bot.send_message(chat_id, 'Введи слово на английском')
        translate_memory = 'en-ru'
    elif re.search(pattern_en, str(message.text).lower()):
        bot.set_state(user_id, StateTranslate.end, chat_id)
        bot.send_message(chat_id, 'Понял тебя. Переводим на английский язык')
        bot.send_message(chat_id, 'Введи слово на русском')
        translate_memory = 'ru-en'
    else:
        bot.send_message(chat_id, 'Я не понимаю тебя, попробуй выразиться по другому')


@bot.message_handler(state=StateTranslate.end)
def bot_translate_end(message: Message):
    global translate_memory
    chat_id = message.chat.id
    user_id = message.from_user.id
    if str(message.text).isalpha():
        if not re.fullmatch(r'[а-я]+', str(message.text).lower()) and translate_memory == 'ru-en':
            bot.send_message(chat_id, 'Нужно вводить на русском языке')
            return
        elif not re.fullmatch(r'[a-z]+', str(message.text).lower()) and translate_memory == 'en-ru':
            bot.send_message(chat_id, 'Нужно вводить на английском языке')
            return
        else:
            result = get_translate(YANDEX_API, translate_memory, str(message.text).lower())
            bot.send_message(chat_id, 'Что-то вроде "{}" или "{}"'.format(result[0], result[1]))
            bot.send_message(chat_id, 'Завершаю функцию "Давай переведем"', reply_markup=gen_markup())
            bot.send_message(chat_id, 'Чем займемся?')
            bot.delete_state(user_id, chat_id)
    else:
        bot.send_message(chat_id, 'Цифры, пробелы и другие спец. символы слишком сложны для меня')
        bot.send_message(chat_id, 'Попробуй еще раз')
