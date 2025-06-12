import logging
import random
import wikipedia
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
import asyncio
user_game_state = {}


wikipedia.set_lang("uz")

from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("7907710172:AAE4-3uLtI6YEc7l1k-42qU-l-OPaaLBl9s")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: Message):
    await message.answer("Assalomu alaykum! Men sizga yordam beradigan Telegram botman 😊")

@dp.message(Command("help"))
async def help(message: Message):
    await message.answer(
        "/start - Botni ishga tushirish\n"
        "/about - Bot haqida\n"
        "/help - Yordam\n"
        "/game - Tasodifiy raqam o'yini\n"
        "/wikipedia [so'z] - Wikipedia maqola qidiruv"
    )

@dp.message(Command("about"))
async def about(message: Message):
    await message.answer("Bu oddiy Telegram bot bo‘lib, sizga turli xizmatlarni taqdim etadi.")

@dp.message(Command("game"))
async def game(message: Message):
    user_id = message.from_user.id
    number = random.randint(1, 10)
    user_game_state[user_id] = number
    await message.answer("🎲 Men 1 dan 10 gacha bir son o‘yladim. Uni topishga harakat qiling!")


@dp.message()
async def guess(message: Message):
    user_id = message.from_user.id
    if user_id in user_game_state:
        try:
            guess = int(message.text.strip())
            number = user_game_state[user_id]
            if guess == number:
                await message.answer("✅ To‘g‘ri! Yutdingiz! 🎉")
            else:
                await message.answer(f"❌ Noto‘g‘ri. Men {number} sonini o‘ylagan edim.")
            del user_game_state[user_id]  # O‘yin tugadi
        except ValueError:
            await message.answer("❗ Iltimos, 1 dan 10 gacha butun son kiriting.")
    else:
        await message.answer("🤖 Men siz bilan o‘yin o‘ynamayapman. Boshlash uchun /game deb yozing.")
    


@dp.message(Command("wikipedia"))
async def wiki(message: Message):
    query = message.text.split(maxsplit=1)
    if len(query) == 2:
        try:
            result = wikipedia.summary(query[1], sentences=2)
            await message.answer(result)
        except wikipedia.exceptions.PageError:
            await message.answer("Kechirasiz, bunday maqola topilmadi.")
        except Exception as e:
            await message.answer(f"Xatolik: {e}")
    else:
        await message.answer("Iltimos, maqola nomini kiriting: /wikipedia [so'z]")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

