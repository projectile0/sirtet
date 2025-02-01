from random import choice, randint


class Field:  # Класс поля
    shapes = list({
                      'I': [((0, -1), (0, 0), (0, 1), (0, 2)), ((-1, 0), (0, 0), (1, 0), (2, 0))],
                      'J': [((0, -1), (1, -1), (0, 0), (0, 1)), ((-1, 0), (0, 0), (1, 0), (1, 1)),
                            ((0, -1), (0, 0), (-1, 1), (0, 1)), ((-1, -1), (0, 0), (-1, 0), (1, 0))],
                      'L': [((-1, -1), (0, -1), (0, 0), (0, 1)), ((1, 1), (0, 0), (-1, 0), (1, 0)),
                            ((0, -1), (0, 0), (0, 1), (1, 1)), ((-1, 0), (0, 0), (1, 0), (-1, 1))],
                      'O': [((0, 0), (1, 0), (0, 1), (1, 1))],
                      'S': [((0, -1), (0, 0), (1, 0), (1, 1)), ((0, 0), (1, 0), (-1, 1), (0, 1))],
                      'T': [((0, -1), (-1, 0), (0, 0), (1, 0)), ((0, -1), (0, 0), (1, 0), (0, 1)),
                            ((-1, 0), (0, 0), (1, 0), (0, 1)), ((0, -1), (-1, 0), (0, 0), (0, 1))],
                      'Z': [((1, -1), (0, 0), (1, 0), (0, 1)), ((-1, -1), (0, -1), (0, 0), (1, 0))]
                  }.items())  # Координаты относительно центра: (x, y)

    # Названия всех вариантов фигур со всеми вариантами расположения,
    # первым считать вертикальное положение "головой" вверх

    def __init__(self, size=(10, 15)):
        self.size = self.width, self.height = size  # размеры
        if self.width < 4 or self.height < 5:  # проверка на слишком маленькие параметры поля
            self.size = self.width, self.height = (10, 15)
        self.board_fixed = self.board_clear()  # Таблица фиксированных блоков
        self.board_show = []  # Таблица для отображения
        self.shift_side = 0  # Сдвиг фигуры на x клеток("-" - влево, "+" - вправо)
        self.figure_center = (0, 0)  # Переменная для сохранения центра фигуры
        self.cur_figure_turn = 0  # Номер варианта поворота фигуры
        self.all_turns = ()  # Запись всех вариантов положения фигуры в виде координат блоков относительно центра

        self.new_figure()  # Появление первой фигуры

    def update(self):  # Следующий кадр
        self.figure_fall()

    def figure_fall(self):
        cells_checked = set(map(self.empty_block, self.all_turns[self.cur_figure_turn]))
        x, y = self.figure_center
        if len(cells_checked) == 1 and cells_checked.pop() == 2:  # Перемещение центра на основе границ
            self.figure_center = x + self.shift_side, y + 1
        elif 0 not in cells_checked:
            self.figure_center = x, y + 1
        else:
            self.fix_board()
            self.new_figure()

    def empty_block(self, coords):  # Проверка на нахождение в таблице и пустоту клетки
        x = coords[0] + self.figure_center[0]
        y = coords[1] + self.figure_center[1]
        if 0 <= y + 1 < self.height:
            if 0 <= x + self.shift_side < self.width:
                if self.board_fixed[y + 1][x + self.shift_side] == 0:
                    return 2
            if 0 <= x < self.width:
                if self.board_fixed[y + 1][x] == 0:
                    return 1
        return 0

    # empty_block:
    # (0: Клетка не пустая/вне таблицы по координате Y; 1: В таблице, пустая без сдвига; 2: В таблице, пустая клетка)
    # Вход координат относительно центра фигуры

    def new_figure(self):  # Появление новой фигуры
        self.all_turns = choice(self.shapes)[1]  # Выбор новой фигуры, запись положений всех блоков относительно центра
        self.cur_figure_turn = randint(0, len(self.all_turns) - 1)
        self.figure_center = (self.width // 2 - 1, 1)

    def fix_board(self):  # Фиксация текущей фигуры
        c_x, c_y = self.figure_center  # центр фигуры
        for x, y in self.all_turns[self.cur_figure_turn]:
            self.board_fixed[y + c_y][x + c_x] = 1

    def board_clear(self):  # Возвращает пустую таблицу
        return [[0] * self.width for _ in range(self.height)]


class OverlayError(Exception):
    pass
