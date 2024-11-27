import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, html, types, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.types import ContentType
from aiogram.fsm.context import FSMContext

from aiogram.fsm.state import State, StatesGroup
import speech_recognition as sr

from pydub import AudioSegment



import io

from icecream import ic

class File(StatesGroup):
    file_id = State()

# Bot token can be obtained via https://t.me/BotFather
TOKEN = "7165039458:AAHGxwzN3uaCiDSTYKSC0xXTlzIWkhgLmZs"

# All handlers should be attached to the Router (or Dispatcher)

dp = Dispatcher()


@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.reply("Привет! Отправь мне аудиосообщение (голосовое или музыкальное), и я попытаюсь его распознать.")



@dp.message()
async def echo_handler(message: types.Message, state: FSMContext) -> None:
    """
    Handler will forward receive a message back to the sender

    By default, message handler will handle all message types (like a text, photo, sticker etc.)
    """
    
    recognizer = sr.Recognizer()
    # Send a copy of the received message

    file_id = message.voice.file_id
    # Получение файла с серверов Telegram
    file = await bot.get_file(file_id)
    file_bytes = await bot.download_file(file.file_path)
    
    try:
    # Загружаем аудиофайл в память
        audio_segment = AudioSegment.from_file(io.BytesIO(file_bytes.read()), format="ogg")
        wav_io = io.BytesIO()
        audio_segment.export(wav_io, format="wav")
        wav_io.seek(0)

        # Читаем и распознаем
        with sr.AudioFile(wav_io) as source:
            audio = recognizer.record(source)
            text = recognizer.recognize_google(audio)

            await message.reply(f"{text}")

    except sr.UnknownValueError:
        await message.reply("Sphinx не смог распознать речь.")
    except sr.RequestError as e:
        await message.reply(f"Ошибка Sphinx: {e}")




# @dp.message()
# async def handle_file(file: types.File, state: FSMContext):
#     ic(message.file_id)


async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    global bot
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())