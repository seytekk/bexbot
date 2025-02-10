from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from bexbot.quest import questions
from bexbot.kibord import get_buttons, main

router=Router()

class TestUser(StatesGroup):
    name = State()
    question = State()
    


@router.message(CommandStart())
async def cmd_strt(message:Message):
    await message.answer(f'Привет! Этот тест проверит твою меркантильность по 10 бальной шкале',reply_markup=main)
    
@router.message(Command('help'))
async def cmnd_help(message:Message):
    await message.answer(f'Для перезапуска теста введи /test')

@router.message(F.text == 'test')
async def test(message: Message, state: FSMContext):
    await state.set_state(TestUser.name)
    await message.answer("Введи свое имя:")
@router.message(TestUser.name)
async def handle_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text, quents=0, count=0)
    await state.set_state(TestUser.question)
    await ask_question(message, state)

async def ask_question(message: Message, state: FSMContext):
    user_data = await state.get_data()
    quents = user_data.get("quents", 0)

    if quents < len(questions):
        question_data = questions[quents]
        question_text = question_data["question"]
        buttons = await get_buttons(quents)
        await message.answer(text=question_text, reply_markup=buttons)
    else:
        await show_result(message, state)


async def show_result(message: Message, state: FSMContext):
    user_data = await state.get_data()
    count = user_data.get("count", 0)
    name = user_data.get("name", "Пользователь")

    if count <= 3:
        result = f"Поздравляю {name}, ты wife material."
    elif 4 <= count <= 7:
        result = f"{name}, тебе стоит пересмотреть в себе некоторые моменты."
    else:
        result = f"Поздравляю {name}, ты чайка."

    await message.answer(result, reply_markup=main)
    await state.clear()


@router.message(TestUser.question)
async def handle_answer(message: Message, state: FSMContext):
    user_data = await state.get_data()
    quents = user_data.get("quents", 0)
    count = user_data.get("count", 0)

    # Получаем баллы за ответ
    answer = message.text
    options = questions[quents]["options"]
    score = options.get(answer, 0)

    # Обновляем данные состояния
    await state.update_data(quents=quents + 1, count=count + score)
    await ask_question(message, state)