from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from utils.get_latest_new import get_latest_news

news_router = Router(name=__name__)

@news_router.message(Command("get_news"))
async def help_command(message: Message, state: FSMContext) -> None:
    await message.answer(get_latest_news())
