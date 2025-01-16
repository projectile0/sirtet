from random import randint
class Field:  # Класс поля
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
        pass

a = Field()
