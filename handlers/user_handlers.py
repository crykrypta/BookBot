# Framework AIOGRAM
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart

# Microservices
from lexicon.lexicon import LEXICON
from services.file_handling import book
from filters.filters import IsDelBookmarkCallbackData, IsDigitCallbackData

# Keyboards
from keyboards.bookmarks_kb import (create_bookmarks_keyboard,
                                    create_edit_keyboards)
from keyboards.pagination_kb import create_pagination_kb

#NEW
from database.database import user_dict_template, users_db
from copy import deepcopy

router = Router()


# # Handler /start
# - Отправляем сообщение LEXICON[/start]
# - Проверяем наличие пользователя в БД
# - Если нет, то добавляем его в БД
@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(LEXICON[message.text])
    if message.from_user.id not in users_db:
        users_db[message.from_user.id] = deepcopy(user_dict_template)


# /help
@router.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(LEXICON[message.text])


# /beggining
# - Устанавливает атрибута пользователя (страница = 1)
# - Создает переменную <text> - с текстом текущей страницы
# - Отправляет сообщение с текстом текущей страницы
# - Прилагает к сообщению Пагинацию
@router.message(Command(commands=['beggining']))
async def process_beginning_command(message: Message):
    users_db[message.from_user.id]['page'] = 1
    text = book[users_db[message.from_user.id]['page']]
    await message.answer(
        text=text,
        reply_markup=create_pagination_kb(
            'backward',
            f'{users_db[message.from_user.id]["page"]}/{len(book)}',
            'forward'
        )
    )


# /continue
