import os
import sys

import pygame as pg

COLOR_BACKGROUND = '#2F3741'
COLOR_FIELD_BACKGROUND = '#323B47'
COLOR_FIGURE = '#AFB8C5'
COLOR_FIGURE_BORDERS = '#2F3741'
COLOR_FIELD_BORDERS = '#A0AFC5'
COLOR_TEXT = '#A9B2C7'


def load_image(name, colorkey=None):  # Загрузить изображение из папки data
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


def get_frames(dir_name):
    frame_names = os.listdir(os.path.join('data', dir_name))
    frame_names.sort(key=lambda x: int(x.replace('.png', '').replace('_', '')))
    frames = []
    for frame_name in frame_names:
        frame_path = os.path.join(dir_name, frame_name)
        image = load_image(frame_path)
        image = pg.transform.rotate(image, -90)
        frames.append(image)
    return frames


def terminate():  # Закрыть программу
    pg.quit()
    sys.exit()
