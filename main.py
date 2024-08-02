import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from bot import admin_router
from config.config_manager import ConfigManager
from database.database_manager import create_table_channels

config_manager = ConfigManager()

# Initialize MemoryStorage
storage = MemoryStorage()
# Initialize dispatcher with MemoryStorage
dp = Dispatcher(storage=storage)

# Event when bot is ready
@dp.startup()
async def on_ready():
    print('Bot is ready')

# Main startup function
async def main():
    await create_table_channels()

    # Initialize bot
    bot = Bot(token=config_manager.get_config_value("BOT_TOKEN", str))

    # Register Routes
    dp.include_routers(admin_router.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
