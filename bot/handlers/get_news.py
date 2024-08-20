import asyncio
import json
import os

import aiofiles
from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from database.database_manager import SQLiteDatabaseManager
from main import bot
from utils.get_latest_new import get_latest_news
from utils.make_telegraph import create_post

news_router = Router(name=__name__)

@news_router.message(Command("get_news"))
async def get_news_command(message: Message, state: FSMContext) -> None:
    await message.answer(create_post(get_latest_news()))

@news_router.message(Command("subscribe"))
async def subscribe_command(message: Message, state: FSMContext) -> None:
    async with SQLiteDatabaseManager() as cursor:
        await cursor.execute(
            """
            INSERT INTO subscriber_list (user_id, lang)
            SELECT ?, ?
            WHERE NOT EXISTS (
                SELECT 1 FROM subscriber_list WHERE user_id = ?
            )
            """,
            (message.chat.id, "uk", message.chat.id),
        )

    await message.answer("You subscribed to Anime/2/UA news!")

@news_router.message(Command("unsubscribe"))
async def unsubscribe_command(message: Message, state: FSMContext) -> None:
    async with SQLiteDatabaseManager() as cursor:
        await cursor.execute(
            """
            DELETE FROM subscriber_list
            WHERE user_id = ?;
            """,
            (message.chat.id, ),
        )


@news_router.startup()
async def on_ready() -> None:
    print("News module started")
    asyncio.create_task(send_news())

async def send_news() -> None:
    while True:
        await asyncio.sleep(1800)

        if await check_is_newest_news():
            news_link = create_post(get_latest_news())
            await notify_subscribers(news_link)

async def check_is_newest_news() -> bool:
    newest_news_link = get_latest_news()
    temp_file_path = "temp.json"

    if os.path.exists(temp_file_path):
        print("Checking if temp.json exists")
        async with aiofiles.open(temp_file_path, "r") as file:
            data = json.loads(await file.read())
            old_news_link = data.get("news_link", "")
    else:
        async with aiofiles.open(temp_file_path, "w") as file:
            await file.write(json.dumps({"news_link": newest_news_link}))
        return True

    if old_news_link == newest_news_link:
        return False

    async with aiofiles.open(temp_file_path, "w") as file:
        await file.write(json.dumps({"news_link": newest_news_link}))

    return True

async def notify_subscribers(news_link: str) -> None:
    async with SQLiteDatabaseManager() as cursor:
        await cursor.execute("SELECT DISTINCT user_id FROM subscriber_list")
        rows = await cursor.fetchall()

    for row in rows:
        user_id = row[0]
        try:
            await asyncio.sleep(10)
            await bot.send_message(user_id, news_link)
        except Exception as e:
            print(f"Failed to send message to {user_id}: {e}")
