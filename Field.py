from copy import deepcopy
from random import choice, randint


class Field:  # Класс поля
    blocks_falling = [2, 3]
    blocks_static = [1]
    shapes = list({
                      'I': [((0, -1), (0, 1), (0, 2)), ((-1, 0), (1, 0), (2, 0))],
                      'J': [((0, -1), (1, -1), (0, 1)), ((-1, 0), (1, 0), (1, 1)),
                            ((0, -1), (-1, 1), (0, 1)), ((-1, -1), (-1, 0), (1, 0))],
                      'L': [((-1, -1), (0, -1), (0, 1)), ((1, 1), (-1, 0), (1, 0)),
                            ((0, -1), (0, 1), (1, 1)), ((-1, 0), (1, 0), (-1, 1))],
                      'O': [((1, 0), (0, 1), (1, 1))],
                      'S': [((0, -1), (1, 0), (1, 1)), ((1, 0), (-1, 1), (0, 1))],
                      'T': [((0, -1), (-1, 0), (1, 0)), ((0, -1), (1, 0), (0, 1)),
                            ((-1, 0), (1, 0), (0, 1)), ((0, -1), (-1, 0), (0, 1))],
                      'Z': [((1, -1), (1, 0), (0, 1))]
                  }.items())  # Координаты относительно центра: (x, y)

    # Названия всех вариантов фигур со всеми вариантами расположения,
    # первым считать вертикальное положение "головой" вверх

    def __init__(self, size=(10, 15)):
        self.size = self.width, self.height = size # размеры
        if self.width < 4 or self.height < 5: # проверка на слишком маленькое поле
            self.size = self.width, self.height = (10, 15)
        self.board = self.clear_board()
        self.new_board = self.clear_board()
        self.shift_side = 0  # Сдвиг фигуры на x клеток("-" - влево, "+" - вправо)
        self.figure_center = (0, 0) # Переменная для сохранения центра фигуры

        self.new_figure()  # Появление первой фигуры
        self.board = deepcopy(self.new_board)

    def update(self):  # Следующий кадр
        self.new_board = self.clear_board()
        try:
            for y in range(self.height):
                for x in range(self.width):
                    cell_value = self.board[y][x]
                    if cell_value in self.blocks_falling:
                        if self.board[y + 1][x + self.shift_side] in self.blocks_static:
                            raise OverlayError  # Обнаружение мешающего блока снизу TODO учёт сдвига в сторону
                        elif 0 <= x + self.shift_side < self.width:
                            self.new_board[y + 1][x + self.shift_side] = self.board[y][x]
                        else:
                            self.new_board[y + 1][x] = self.board[y][x]  # Сдвиг блока вниз
                    elif self.board[y][x] in self.blocks_static:  # Перенос статичного блока на новую доску
                        self.new_board[y][x] = cell_value
        except OverlayError:
            self.new_figure()
        except IndexError:  # TODO Переделать (убрать стандартную ошибку из except), может вызывать последующие затруднения
            self.new_figure()
        self.board = deepcopy(self.new_board)

    def new_figure(self):  # "Затвердевание старой и появление новой фигуры"
        self.new_board = deepcopy(self.board)  # Откат изменений падения
        for y in range(self.height):  # Фиксирование всех клеток
            for x in range(self.width):
                if self.board[y][x] in self.blocks_falling:
                    self.new_board[y][x] = 1

        figure_type, possible_turns = choice(self.shapes)  # Выбор новой фигуры
        cur_turn = randint(0, len(possible_turns) - 1)
        center_x, center_y = self.figure_center = (self.width // 2 - 1, 1)
        self.new_board[self.figure_center[1]][self.figure_center[0]] = 3  # Установка нового центра фигуры
        for yd, xd in possible_turns[cur_turn]:  # расстановка остальных блоков фигуры
            self.new_board[center_y + yd][center_x + xd] = 2

    def clear_board(self): # Возвращает пустую таблицу
        return [[0] * self.width for _ in range(self.height)]


class OverlayError(Exception):
    pass
