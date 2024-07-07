# Функционал
import asyncio
import logging

# AIOGRAM
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

# Структура проекта
from config_data.config import Config, load_config
from handlers import user_handlers, other_handlers
from keyboards.main_menu import set_main_menu


# Init logger
logger = logging.getLogger(__name__)


# main function
async def main():
    # Log config
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
        '[%(asctime)s - %(name)s] - %(message)s'
    )

    # Inform that Bot Started
    logger.info('Starting bot')

    # load config
    config: Config = load_config()

    # Init bot
    bot = Bot(
        token=config.tg_bot.token,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML
        )
    )
    # Init dispatcher
    dp = Dispatcher()

    # Configuration the main menu of Bot
    await set_main_menu(bot)

    # Registry routers in DP
    dp.include_router(user_handlers.router)
    dp.include_router(other_handlers.router)

    # Pass updates and start polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


asyncio.run(main())
