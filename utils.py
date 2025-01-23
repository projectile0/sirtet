import os
import pygame as pg
import sys


def load_image(name, colorkey=None): # Загрузить изображение из папки data
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        raise FileNotFoundError
    image = pg.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def terminate(): # Закрыть программу
    pg.quit()
    sys.exit()
