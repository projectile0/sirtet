from random import randint
from pygame.locals import *

fig_w, fig_h = 5, 5 #Шаблон размера фигуры

class Field:  # Класс поля
    shapes = {
        'I': [0, 1],
        'J': [0, 1, 2, 3],
        'L': [0, 1, 2, 3],
        'O': [0],
        'S': [0, 1],
        'T': [0, 1, 2, 3],
        'Z': [0, 1]
    }  # Названия всех вариантов фигур со всеми вариантами расположения,

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
                    case 2, 3:
                        if self.board[y + 1][x] == 1:
                            self.new_figure()

    def new_figure(self):  # "Затвердевание старой и появление новой фигуры"
        pass
