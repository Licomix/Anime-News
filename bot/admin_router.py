from aiogram import Router
from bot.handlers.start import start_router
from bot.handlers.get_news import news_router
# from bot.user.handlers.url import url_router

router = Router(name=__name__)

router.include_routers(start_router, news_router)
