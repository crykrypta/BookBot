import os
import sys


def _get_part_text(text: str, start: int, page_size: int) -> tuple[str, int]:
    # Получаем максимально возможный отрезок
    end = start + page_size

    # Находим ближайший символ из marks
    marks = ['.', ',', '!', ':', ';', '?']
    while text[end:][:1] in marks:
        end -= 1

    # Обрезаем все после найденного символа
    text = text[start: end]

    # Подстраховка
    text = text[: max(map(text.rfind, marks)) + 1]

    return text, len(text)


book: dict[int, str] = {}
PAGE_SIZE = 1050


def prepare_book(path: str) -> None:
    path = os.path.normpath(os.path.join(sys.path[0], path))
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()

    i = 1
    start = 0
    while True:

        page, size = _get_part_text(text,
                                    start=start,
                                    page_size=PAGE_SIZE)
        if size == 0:
            break
        book.update({i: page.lstrip()})
        start += size
        i += 1


prepare_book('BookBot/book/book.txt')
print(book[1])
