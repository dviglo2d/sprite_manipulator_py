# Copyright (c) the Dviglo project
# License: MIT

from PIL import Image


# Расширяет изображение на border_size в каждую сторону, копируя крайние пиксели исходного изображения
def expand_image(src_image: Image, border_size: int) -> Image:
    if border_size < 0:
        raise ValueError("border_size < 0")

    src_width, src_height = src_image.size
    
    # Создаём новое изображение с увеличенным размером
    new_width = src_width + border_size * 2
    new_height = src_height + border_size * 2
    ret = Image.new("RGB", (new_width, new_height))
    
    # Копируем исходное изображение в центр нового изображения
    ret.paste(src_image, (border_size, border_size))

    # Копируем верхние пиксели
    line = ret.crop((0, border_size, new_width, border_size + 1))
    for y in range(border_size):
        ret.paste(line, (0, y))

    # Копируем нижние пиксели
    line = ret.crop((0, src_height + border_size - 1, new_width, src_height + border_size))
    for y in range(src_height + border_size, new_height):
        ret.paste(line, (0, y))

    # Копируем левые пиксели
    column = ret.crop((border_size, 0, border_size + 1, new_height))
    for x in range(border_size):
        ret.paste(column, (x, 0))

    # Копируем правые пиксели
    column = ret.crop((src_width + border_size - 1, 0, src_width + border_size, new_height))
    for x in range(src_width + border_size, new_width):
        ret.paste(column, (x, 0))

    return ret


# Пример использования
input_image = Image.open("input_image.png")
expand_image = expand_image(input_image, 3)
expand_image.save("expanded_image.png")
