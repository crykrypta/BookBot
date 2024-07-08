from aiogram import Bot
from aiogram.types import BotCommand

from lexicon.lexicon import LEXICON_COMMANDS


# Функция для настроки кнопки Menu у бота
async def set_main_menu(bot: Bot):
    # Вложенный генератор списков, с перебором пар ключ=значение
    # В словаре LEXICON_COMMAND "Распаковываем" в модуль
    main_menu_commands = [
        BotCommand(command=command, description=description)
        for command, description in LEXICON_COMMANDS.items()
        ]
    await bot.set_my_commands(main_menu_commands)
