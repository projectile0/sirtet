from random import choice
from pygame.locals import *

fig_w, fig_h = 5, 5  # Шаблон размера фигуры


class Field:  # Класс поля
    shapes = list({
                      'I': [0, 1],
                      'J': [0, 1, 2, 3],
                      'L': [0, 1, 2, 3],
                      'O': [0],
                      'S': [0, 1],
                      'T': [0, 1, 2, 3],
                      'Z': [0, 1]
                  }.items())  # Названия всех вариантов фигур со всеми вариантами расположения,

    # считать нулевым вертикальное положение "головой" вверх

    def __init__(self, size=(10, 15)):
        self.size = self.width, self.height = size
        if self.width < 4 or self.height < 5:
            self.size = self.width, self.height = (10, 15)
        self.board = [[0] * self.width] * self.height
        self.new_figure()

    def update(self):  # Следующий кадр
        for y in range(self.height):
            for x in range(self.width):
                match self.board[y][x]:
                    case 2:
                        if self.board[y + 1][x] == 1:
                            self.new_figure()

    def new_figure(self):  # "Затвердевание старой и появление новой фигуры"
        for y in range(self.height):  # Фиксирование всех клеток
            for x in range(self.width):
                if self.board[y][x] in [2, 3]:
                    self.board[y][x] = 1

        figure_next = choice(self.shapes)  # Выбор новой фигуры
        cur_turn = choice(figure_next[1])
