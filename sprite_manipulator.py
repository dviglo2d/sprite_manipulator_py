# Copyright (c) the Dviglo project
# License: MIT

from PIL import Image
import numpy


# Делит изображение на тайлы
def split_image(image: Image, tile_width: int, tile_height: int) -> numpy.ndarray:
    if tile_width <= 0:
        raise ValueError("tile_width <= 0")
    
    if tile_height <= 0:
        raise ValueError("tile_height <= 0")

    num_tiles_x = image.size[0] // tile_width
    num_tiles_y = image.size[1] // tile_height

    # Создаём двумерный массив для хранения тайлов
    ret = numpy.empty((num_tiles_y, num_tiles_x), dtype=object)

    for index_y in range(num_tiles_y):
        for index_x in range(num_tiles_x):
            box = (index_x * tile_width, index_y * tile_height, (index_x + 1) * tile_width, (index_y + 1) * tile_height)
            ret[index_y, index_x] = image.crop(box)

    return ret


# Расширяет изображение на border_size в каждую сторону, копируя крайние пиксели исходного изображения
def expand_image(src_image: Image, border_size: int) -> Image:
    if border_size < 0:
        raise ValueError("border_size < 0")

    src_width, src_height = src_image.size
    
    # Создаём новое изображение с увеличенным размером
    new_width = src_width + border_size * 2
    new_height = src_height + border_size * 2
    ret = Image.new("RGBA", (new_width, new_height))
    
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


# Округляет вверх до ближайшей степени двойки
def ceil_power_of_2(n: int) -> int:
    if n < 1:
        raise ValueError("n < 1")
    
    ret = 1
    while ret <= n:
        ret *= 2 # 1, 2, 4, 8, 16, 32, ...

    return ret


# Объединяет двумерный массив тайлов в атлас
def join_tiles(tiles: numpy.ndarray) -> Image:
    if tiles.ndim != 2 or tiles.size == 0 : # Убеждаемся, что массив двумерный и не пустой
        raise ValueError()
    
    tile_width, tile_height = tiles[0, 0].size
    atlas_width = ceil_power_of_2(tiles.shape[1] * tile_width)
    atlas_height = ceil_power_of_2(tiles.shape[0] * tile_height)
    ret = Image.new("RGBA", (atlas_width, atlas_height), (0, 0, 0, 0))

    for index_y in range(tiles.shape[0]):
        for index_x in range(tiles.shape[1]):
            ret.paste(tiles[index_y, index_x], (index_x * tile_width, index_y * tile_height))

    return ret


# Пример использования
src_atlas_path = "input_atlas.png"
src_tile_width = 16 # Ширина тайла в исходном аталасе
src_tile_height = 32
border_size = 4 # На сколько будет расширен каждый тайл
result_atlas_path = "expanded_atlas.png"

# Загружаем текстурный атлас
input_image = Image.open(src_atlas_path)

# Делим атлас на тайлы
tiles = split_image(input_image, src_tile_width, src_tile_height)

# Расширяем каждый тайл
for index_y in range(tiles.shape[0]):
    for index_x in range(tiles.shape[1]):
        tiles[index_y, index_x] = expand_image(tiles[index_y, index_x], 2)

# Объединяем тайлы в новый атлас
expanded_atlas = join_tiles(tiles)

# Сохраняем результат
expanded_atlas.save(result_atlas_path)
