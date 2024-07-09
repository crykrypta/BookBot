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
                                    create_edit_keyboard)
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
@router.message(Command(commands=['continue']))
async def process_continue_command(message: Message):
    text = book[users_db[message.from_user.id]['page']]
    await message.answer(
        text=text,
        reply_markup=create_pagination_kb(
            'backward',
            f'{users_db[message.from_user.id]["page"]}/{len(book)}',
            'forward'
        )
    )


# /bookmarks
# - Проверяет наличие закладок в ДБ пользователя
# - Присылает список закладок при их наличии
# - ответа из лексикона в противном случае
@router.message(Command(commands=['bookmarks']))
async def process_bookmarks_command(message: Message):
    if users_db[message.from_user.id]['bookmarks']:
        await message.answer(
            text=LEXICON[message.text],
            reply_markup=create_bookmarks_keyboard(
                *users_db[message.from_user.id]['bookmarks']
            )
        )
    else:
        await message.answer(LEXICON['no_bookmarks'])


# forward page
@router.callback_query(F.data == 'forward')
async def process_forward_command(callback: CallbackQuery):
    if users_db[callback.from_user.id]['page'] < len(book):
        users_db[callback.from_user.id]['page'] += 1
        text = book[users_db[callback.from_user.id]['page']]

        await callback.message.edit_text(
            text=text,
            reply_markup=create_pagination_kb(
                'backward',
                f'{users_db[callback.from_user.id]["page"]}/{len(book)}',
                'forward'
            )
        )
    await callback.answer()


# backward page
@router.callback_query(F.data == 'backward')
async def process_backward_command(callback: CallbackQuery):
    if users_db[callback.from_user.id]['page'] > 1:
        users_db[callback.from_user.id]['page'] -= 1
        text = book[users_db[callback.from_user.id]['page']]
        await callback.message.edit_text(
            text=text,
            reply_markup=create_pagination_kb(
                'backward',
                f'{users_db[callback.from_user.id]["page"]}/{len(book)}',
                'forward'
            )
        )
    callback.answer()


# Добавление новой закладки
@router.callback_query(lambda x: '/' in x.data and x.data.replace('/', '').isdigit())
async def process_page_press(callback: CallbackQuery):
    users_db[callback.from_user.id]['bookmarks'].add(
        users_db[callback.from_user.id]['page']
    )
    await callback.answer('Страница добавлена в закладки')


# Нажатие на инлайн-кнопку с закладкой из списка закладок
@router.callback_query(IsDigitCallbackData())
async def process_bookmark_press(callback: CallbackQuery):
    text = book[int(callback.data)]
    users_db[callback.from_user.id]['page'] = int(callback.data)
    await callback.message.edit_text(
        text=text,
        reply_markup=create_pagination_kb(
            'backward',
            f'{users_db[callback.from_user.id]["page"]}/{len(book)}',
            'forward'
        )
    )


# Нажатие на инлайн-кнопку "Редактировать" под списком закладок
@router.callback_query(F.data == 'edit_bookmarks')
async def process_edit_press(callback: CallbackQuery):
    callback.message.edit_text(
        text=LEXICON[callback.data],
        reply_markup=create_edit_keyboards(
            *users_db[callback.from_user.id]['bookmarks']
        )
    )


# Нажатие на кнопку "Отменить"
@router.callback_query(F.data == 'cancel')
async def process_cancel_press(callback: CallbackQuery):
    callback.message.edit_text(text=LEXICON['cancel_text'])


# Нажатие на инлайн кнопку с закладкой для ее удаления
@router.callback_query(IsDelBookmarkCallbackData())
async def process_del_bookmarks_press(callback: CallbackQuery):
    if users_db[callback.from_user.id]['bookmarks']:
        users_db[callback.from_user.id]['bookmarks'].remove(
            int(callback.data[:-3])  # [:-3] - Отбрасываем 'del'
        )
        await callback.message.edit_text(
            text=LEXICON['/bookmarks'],
            reply_markup=create_edit_keyboard(
                *users_db[callback.from_user.id]['bookmarks']
            )
        )
    else:
        await callback.message.edit_text(LEXICON['no_bookmarks'])
