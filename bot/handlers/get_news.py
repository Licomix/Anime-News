from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from utils.get_latest_new import get_latest_news
from utils.make_telegraph import create_post

news_router = Router(name=__name__)

@news_router.message(Command("get_news"))
async def help_command(message: Message, state: FSMContext) -> None:

    await message.answer(create_post(get_latest_news()))
