from telebot.handler_backends import State, StatesGroup


class StateTranslate(StatesGroup):
    format = State()
    end = State()
