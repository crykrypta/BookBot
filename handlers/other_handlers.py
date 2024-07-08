from aiogram import Router
from aiogram.types import Message


router = Router()


# Это просто хэндлер Эхо
@router.message()
async def send_echo(message: Message):
    await message.answer(f'Это эхо! {message.text}')
