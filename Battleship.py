from random import randint

#Создаем и описываем класс точки
class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f'({self.x}, {self.y})'

#Создаем и описываем класс корабля
class Ship:
    def __init__(self, bow, l, o):
        self.bow = bow
        self.l = l
        self.o = o
        self.lives = l

    @property
    def dots(self):
        ship_dots = []
        for i in range(self.l):
            cur_x = self.bow.x
            cur_y = self.bow.y
            if self.o == 0:
                cur_x += i
            elif self.o == 1:
                cur_y += i
            ship_dots.append(Dot(cur_x, cur_y))
        return ship_dots

    def shooten(self, shot):
        return shot in self.dots

#Создаем классы исключений
#"Общий" класс, для содержания в нем всех остальных исключений
class BoardException(Exception):
    pass

#Исключение - стреляем за пределы доски
class BoardOutException(BoardException):
    def __str__(self):
        return 'Вы пытаетесь выстрелить за доску!'

#Исключение - стреляли уже в эту точку
class BoardUsedException(BoardException):
    def __str__(self):
        return 'Вы уже стреляли в эту клетку'

#Исключение для правильного размещения кораблей
class BoardWrongShipException(BoardException):
    pass

#Создаем и описываем игровое поле
class Board:
    def __init__(self, hid=False, size=6):
        self.size = size
        self.hid = hid
        self.count = 0
        self.field = [['O'] * size for _ in range(size)]
        self.busy = []
        self.ships = []

    #Отрисовываем доску
    def __str__(self):
        res = ''
        res += '  | 1 | 2 | 3 | 4 | 5 | 6 |'
        for i, row in enumerate(self.field):
            res += f'\n{i + 1} | ' + ' | '.join(row) + ' |'
        if self.hid:
            res = res.replace('■', 'O')
        return res

    #Проверяем где находится точка
    def out(self, d):
        return not ((0 <= d.x < self.size) and (0 <= d.y < self.size))

    #Метод для определения контура корабля
    def contour(self, ship, verb=False):
        near = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for d in ship.dots:
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
                if not (self.out(cur)) and cur not in self.busy:
                    if verb:
                        self.field[cur.x][cur.y] = '.'
                    self.busy.append(cur)

    #Проверяем что весь корабль не выходит за границы и точки не заняты
    def add_ship(self, ship):
        for d in ship.dots:
            if self.out(d) or d in self.busy:
                raise BoardWrongShipException()
        for d in ship.dots:
            self.field[d.x][d.y] = '■'
            self.busy.append(d)
        self.ships.append(ship)
        self.contour(ship)

    #Метод для выстрела
    def shot(self, d):
        if self.out(d):
            raise BoardOutException()
        if d in self.busy:
            raise BoardUsedException()
        self.busy.append(d)
        for ship in self.ships:
            if ship.shooten(d):
                ship.lives -= 1
                self.field[d.x][d.y] = 'X'
                if ship.lives == 0:
                    self.count += 1
                    self.contour(ship, verb=True)
                    print()
                    print('Корабль уничтожен!')
                    return False
                else:
                    print()
                    print('Корабль ранен!')
                    return True
        self.field[d.x][d.y] = '.'
        print()
        print('Мимо!')
        return False

    def begin(self):
        self.busy = []

    def defeat(self):
        return self.count == len(self.ships)

#Создаем и описываем класс игрока
class Player:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except BoardException as e:
                print(e)

#Класс "Игрок-компьютер"
class AI(Player):
    def ask(self):
        d = Dot(randint(0, 5), randint(0, 5))
        print(f'Ход компьютера: {d.x + 1} {d.y + 1}')
        return d

#Класс "Игрок-пользователь"
class User(Player):
    def ask(self):
        while True:
            cords = input('Ваш ход: ').split()
            if len(cords) != 2:
                print(' Введите 2 координаты! ')
                continue
            x, y = cords
            if not (x.isdigit()) or not (y.isdigit()):
                print(' Введите числа! ')
                continue
            x, y = int(x), int(y)
            return Dot(x - 1, y - 1)

#Создаем класс игры
class Game:
    def __init__(self, size=6):
        self.lens = [3, 2, 2, 1, 1, 1, 1]
        self.size = size
        pl = self.random_board()
        co = self.random_board()
        co.hid = True
        self.ai = AI(co, pl)
        self.us = User(pl, co)

    #Создаем доску с кораблями
    def random_place(self):
        board = Board(size=self.size)
        attempts = 0
        for l in self.lens:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), l, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.begin()
        return board

    #В случае, если метод выше не смог сгенерировать доску, то мы благодаря этому методу гарантированно создаем доску
    def random_board(self):
        board = None
        while board is None:
            board = self.random_place()
        return board

    #Метод для приветствия
    def greet(self):
        print('---------------------------')
        print('  Добро пожаловать в игру  ')
        print('        Морской бой        ')
        print('---------------------------')
        print()
        print(' формат ввода: x y ')
        print(' x - номер строки  ')
        print(' y - номер столбца ')
        print()

    def print_boards(self):
        print('-' * 20)
        print('Доска пользователя:')
        print()
        print(self.us.board)
        print()
        print('-' * 20)
        print('Доска компьютера:')
        print()
        print(self.ai.board)
        print()

    #Сам игровой цикл
    def loop(self):
        num = 0
        while True:
            self.print_boards()
            if num % 2 == 0:
                print('-' * 20)
                print('Ходит пользователь!')
                repeat = self.us.move()
                print()
            else:
                print('-' * 20)
                print('Ходит компьютер!')
                repeat = self.ai.move()
                print()
            if repeat:
                num -= 1
            if self.ai.board.defeat():
                self.print_boards()
                print('-' * 20)
                print('Пользователь выиграл!')
                break
            if self.us.board.defeat():
                self.print_boards()
                print('-' * 20)
                print('Компьютер выиграл!')
                break
            num += 1

    #Метод который совмещае в себе процесс игры
    def start(self):
        self.greet()
        self.loop()


g = Game()
g.start()