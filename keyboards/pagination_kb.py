from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from lexicon.lexicon import LEXICON


def create_pagination_kb(*buttons: str) -> InlineKeyboardMarkup:
    """
    Create pagination keyboard << page >>
    """
    kb_builder = InlineKeyboardBuilder()

    kb_builder.row(*[InlineKeyboardButton(
        text=LEXICON[button] if button in LEXICON else button,
        callback_data=button) for button in buttons]
    )

    return kb_builder.as_markup()
