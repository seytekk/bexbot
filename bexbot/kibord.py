from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from bexbot.quest import questions


async def get_buttons(num):
    testki=ReplyKeyboardBuilder()
    options=questions[num]["options"]
    for j in options.keys():
        testki.add(KeyboardButton(text=j))
    return testki.as_markup(resize_keyboard=True)



main=ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="test")]],resize_keyboard=True,one_time_keyboard=True)