import asyncio
import logging
import sys
import os

from aiogram import Bot, Dispatcher, html, types, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.types import ContentType
from aiogram.fsm.context import FSMContext
from aiogram.utils import chat_action

from aiogram.fsm.state import State, StatesGroup
import speech_recognition as sr

from pydub import AudioSegment

import keyboard as kb

import io
from icecream import ic
from gpt import genarateResponse
from prompts import *


recognizer = sr.Recognizer()

TOKEN = os.getenv("TELEGRAM_TOKEN")

dp = Dispatcher()

#State manager
class Main(StatesGroup):
    text = State()
    action = State()


@dp.message(CommandStart())
async def cmd_start(message: types.Message, state: FSMContext):
    await bot.send_message(chat_id=message.chat.id, text="Hello! Please send me audio or text")
    await state.set_state(Main.text)
    

    

@dp.message(Main.text)
async def chosingFormat(message: Message, state: FSMContext):
    if message.voice:
        text = await recognize_text(voice_id=message.voice.file_id)
        await message.reply(f"""Your text: {text} 
                            When creating a response, format text using Telegram HTML syntax:
                            Bold text should be enclosed with <b> and </b>.
                            Italic text should be enclosed with <i> and </i>.
                            """)
    else:
        text = message.text
        
    await state.update_data(text=text)
    data = await state.get_data()
    text = data.get("text")
    await state.set_state(Main.action)
    await bot.send_message(chat_id=message.chat.id, text="Choose the action!!!!!", reply_markup=kb.actions)



@dp.message(Main.action)
async def chooseAction(message: types.Message, state: FSMContext):

    match message.text:
        case 'Detailed Text Analysis':
            prompt = textAnalysis
        case 'Create Grammar Exercises':
            prompt = grammarExercises
        case 'Check Grammar':
            prompt = grammarCheck
        
    data = await state.get_data()
    text = data.get('text')
    
    await bot.send_chat_action(chat_id=message.chat.id, action='typing')
    result = genarateResponse(text=text, prompt=prompt)
    await bot.send_message(chat_id=message.chat.id, text=result)
    await state.set_state(Main.text)


async def recognize_text(voice_id) -> str:
    """
    Handler will forward receive a message back to the sender

    By default, message handler will handle all message types (like a text, photo, sticker etc.)
    """
    # Send a copy of the received message

    # Получение файла с серверов Telegram
    file = await bot.get_file(voice_id)
    file_bytes = await bot.download_file(file.file_path)
    
    # Загружаем аудиофайл в память
    audio_segment = AudioSegment.from_file(io.BytesIO(file_bytes.read()), format="ogg")
    wav_io = io.BytesIO()
    audio_segment.export(wav_io, format="wav")
    wav_io.seek(0)

    # Читаем и распознаем
    with sr.AudioFile(wav_io) as source:
        audio = recognizer.record(source)
        text = recognizer.recognize_google(audio)
        return text

async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    global bot
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    # And the run events dispatching
    await dp.start_polling(bot)



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())