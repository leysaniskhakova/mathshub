from random import randint
from functools import reduce


class LifeGame:
    DEATH = '0'   # значение ячейки, если она мертва
    LIFE = '1'    # значение ячейки, если она жива
    RELATIVE_NEIGHBORS = [[-1, -1], [-1, 0], [-1, +1],  # список координат удаления соседей от ячейки
                          [0, -1],           [0, +1],
                          [+1, -1], [+1, 0], [+1, +1]]

    def __init__(self, side: int):
        self.board_size = side  # сторона квадратного поля
        self.board_start = 0    # начало координат поля для поиска соседей
        self.board_end = side - 1   # конец координат поля для поиска соседей
        self.cell_number = side * side  # сколько всего ячеек в поле
        self.past_generations = []  # список для сбора предыдущих поколений
        self.game_over = None   # условие окончания игры

    @property
    def generation_number(self):    # считаем
        return len(self.past_generations)   # и возвращаем количество предыдущих поколений

    def first_generation(self):     # генерируем первое поколение
        first_gen = [[str(randint(0, 1)) for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.past_generations.append(first_gen)     # и добавляем его в конец списка для сбора предыдущих поколений

    def get_next_generation(self) -> list:    # получаем следующее поколение на основе предыдущего
        generation = []                 # создаем пустой список для сбора нового поколения
        for x in range(self.board_size):     # проходим по х координатам поля

            cell_row = []                # создаем пустой список сбора одного из рядов нового поколения
            for y in range(self.board_size):     # проходим по y координатам поля
                # берем значение ячейки на соответствующей координате прошлого поколения
                cell = self.past_generations[-1][x][y]
                alive = self.alive_neighbors(x, y)         # запрашиваем количество живых соседей ячейки

                if cell == self.LIFE and alive in (2, 3):    # если ячейка живая и у нее два или три живых соседа
                    cell = self.LIFE                         # то она остается живой
                elif cell == self.DEATH and alive == 3:      # если она мертвая и у нее три живых соседа
                    cell = self.LIFE                         # то она оживает
                else:
                    cell = self.DEATH                        # в других случаях ячейка мертвая

                cell_row.append(cell)   # добавляем ячейку в список одного из рядов нового поколения
            generation.append(cell_row)  # добавляем собранный ряд поколения в список для сбора поколения

        return generation       # возвращаем новое поколение в виде списка списков

    def alive_neighbors(self, x: int, y: int) -> int:    # ищем количество живых соседей
        neighbor_positions = self.neighbor_positions(x, y)   # запрашиваем список координат соседей ячейки
        # в функции map при помощи функции lambda создаем список значений соседей ячейки по списку координат
        neighbor_state = list(map(lambda pos: self.past_generations[-1][pos[0]][pos[1]], neighbor_positions))
        alive_count = neighbor_state.count(self.LIFE)   # считаем количество живых соседей в списке значений соседей

        return alive_count  # возвращаем количество живых соседей ячейки

    def neighbor_positions(self, pos_x: int, pos_y: int):     # ищем координаты соседей ячейки
        def trans(pos):     # создаем внутреннюю функцию trans, которая
            return pos_x + pos[0], pos_y + pos[1]   # возвращает координату одного соседа ячейки
        # в функции map при помощи функции trans создаем итерируемый объект с координатами все "возможных"
        # соседей ячейки исходя из списка координат удаления соседей от ячейки
        # потом в функции filer при помощи функции hit удаляем координаты, которые не являются соседями ячейки
        # hit принимает как аргумент элемент итерируемого объекта в функции map
        # возвращаем итерируемый объект с координатами соседей ячейки
        return filter(self.hit, map(trans, self.RELATIVE_NEIGHBORS))

    def hit(self, point) -> bool:   # проверяем не входит ли координата за границы поля
        # распакуем элемент итерируемого объекта в функции map (координата x и y - список)
        x, y = point    # в переменные x и y для легкого чтения
        # создадим диапазон значений координат от начала и до конца поля координат для поиска соседей
        bounds = range(self.board_start, self.board_end + 1)
        return (x in bounds) and (y in bounds)   # возвращаем True, если и x, и y входят в этот диапазон

    def play(self):     # запускаем игру

        self.first_generation()     # создаем первое поколение

        while True:                 # запускаем цикл жизни последующих поколений

            generation = self.get_next_generation()     # создаем новое поколение на основе предыдущего
            # считаем количество мертвых ячеек в новом поколении
            # функция reduce берет итерируемый объект (generation) и складывает все его значения в одно
            # функция lambda берет очередное значение ряда из поколения, считает в нем значение мертвых
            # ячеек и прибавляет это значение к переменной s, которая хранит количество уже найденных
            # мертвых ячеек в поколении, которых изначально 0, что записано в конце функции reduce
            dead = reduce(lambda s, row: s + row.count(self.DEATH), generation, 0)

            if dead == self.cell_number:    # если количество мертвых клеток равно количеству ячеек поля, то это значит
                # что живых ячеек не осталось, игра заканчивается и условие окончания игры обновляется
                self.game_over = f'После {self.generation_number} поколения колония вымерла.'
                return  # игра закончилась, выходим из метода

            if generation in self.past_generations:     # если новое поколение повторяет какое-либо предыдущее
                # поколение из списка предыдущих поколений, то складывается периодическая или стабильная конфигурация
                # условие окончания игры обновляется
                self.game_over = f'{self.generation_number + 1} поколение повторило ошибки {self.past_generations.index(generation) + 1} поколения.'
                return  # игра закончилась, выходим из метода
            # если в новое поколение состоит не только их мертвых ячеек и не повторяет какое-либо предыдущее
            # поколение из списка предыдущих поколений, то добавляем его в конец списка предыдущих поколений
            self.past_generations.append(generation)

    def __str__(self):      # возвращает строковое представление объекта класса
        # ' '.join(row) for row in generation - объединяем элементы ряда в строку через пробел
        # '\n'.join(^) for generation in self.past_generations - объединяем элементы поколения в строку
        #             v                                          с перенесением каждого ряда на другую строку
        # '\n\n'.join(^) - объединяем поколения в сроку с перенесением каждого поколения на другую строку два раза
        life = '\n\n'.join('\n'.join(' '.join(row) for row in generation) for generation in self.past_generations)
        # возвращаем строковое представление жизненного цикла игры, причину и результат ее окончания
        return life + '\n\n' + self.game_over


# вводим одну сторону для квадратного поля
field = int(input('Введите размер стороны квадратной области обитания будущей колонии: '))
print()     # пустой вывод для красоты вывода игры

game = LifeGame(field)      # создаем игру согласно введенному размеру стороны квадратного поля (объект класса)
game.play()                 # запускаем игру через метод класса play

print(game)                 # выводим игру на экран

