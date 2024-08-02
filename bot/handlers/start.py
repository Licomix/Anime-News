from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

# from database.database_manager import SQLiteDatabaseManager

start_router = Router(name=__name__)

@start_router.message(CommandStart())
async def start_command(message: Message, state: FSMContext) -> None:
    await message.answer("Hi! I'm Anime/2/UA bot, made for @animeua2 channel! You can add me to your channel and I will send actual anime news in ukrainian language!")

# async def db_add_chat(chat_id: int, locale: str, anonime_statistic: int) -> None:
#     """Add chat info into database

#     Args:
#         chat_id (int): Chat ID
#         locale (str): Localisation, such as: en, ru, etc.
#         anonime_statistic (int): Anonime statistic bool
#     """
#     async with SQLiteDatabaseManager() as cursor:
#         await cursor.execute(
#             """
#             INSERT INTO chat_settings (chat_id, lang, anonime_statistic)
#             SELECT ?, ?, ?
#             WHERE NOT EXISTS (
#                 SELECT 1 FROM chat_settings WHERE chat_id = ?
#             )
#             """,
#             (chat_id, locale, anonime_statistic, chat_id),
#         )
