#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Модуль документации"""

from random import sample, randint, shuffle

__author__ = "Sergey Igoshin"
__version__ = "1.0.1"
__email__ = "sergey@csb-mirena.ru"


def print_color(arg):
    format_color = {
        'NOT_NUM': '\033[51;3;33;43m',
        'WHITESPACE': '\033[38;5;236m',
        'LINE_EVEN': '\033[51;3;43;97;7;9m',
        'LINE_ODD': '\033[52;3;43;97;7;9m',
        'NUM_EVEN': '\033[51;3;43;97;7m',
        'NUM_ODD': '\033[52;3;43;97;7m',
        'KEG': '\033[51;3;43;97m',
        'END': '\033[0m',
    }
    return format_color[arg]


NOT_NUM = print_color('NOT_NUM')
WHITESPACE = print_color('WHITESPACE')
LINE_EVEN = print_color('LINE_EVEN')
LINE_ODD = print_color('LINE_ODD')
NUM_EVEN = print_color('NUM_EVEN')
NUM_ODD = print_color('NUM_ODD')
KEG = print_color('KEG')
END = print_color('END')


def null_cell(text):
    return NOT_NUM + f'{text:^4}' + END


def whitespace_cell(text):
    return WHITESPACE + f'{text:^4}' + END


def header(text):
    return NUM_EVEN + f'{" " + text:<36}' + END


def num_cell(text, item, data):
    if item % 2 == 0:
        if text in data:
            return NUM_EVEN + f' {text:^3}' + END
        else:
            return LINE_EVEN + f' {text:^3}' + END
    else:
        if text in data:
            return NUM_ODD + f' {text:^3}' + END
        else:
            return LINE_ODD + f' {text:^3}' + END


def kegs(keg):
    return KEG + f' {keg:^3}' + END


class LottoCard:
    def __init__(self, type_player):
        self.__player = type_player
        self.__card = [[], [], []]
        self.__ticket = f'билет № {str(randint(1, 99999)).zfill(7)}'
        self.__data = list(range(1, 91))

    def __str__(self):
        return str('\n'.join([''.join(
            [str(self.color_cell(el, item, self.__data)) for item, el in enumerate(i)]) for i in self.__card]))

    def __add__(self, other):
        for row in range(len(self.__card)):
            self.__card[row] = self.__card[row] + ['*'] + other.__card[row]
        return self

    @classmethod
    def get_player(cls, user):
        if user == '' or len(user) > 25:
            return 'Ваша карточка'
        else:
            return user

    @classmethod
    def color_cell(cls, text, item, data):
        if text == '':
            return null_cell(text)
        elif text == "*":
            return whitespace_cell(text)
        elif len(str(text)) > 2:
            return header(text)
        else:
            return num_cell(text, item, data)

    @property
    def create_card(self):
        for i in range(9):
            if i < 9:
                min_range = max_range = i * 10
            else:
                min_range = i * 10 - 1
                max_range = i * 10 + 1

            for key, val in enumerate(sample(range(1 + min_range, 10 + max_range), 3)):
                self.__card[key].append(val)

        for row in range(2):
            for column in sample(range(0, 9), 4):
                self.__card[row][column] = ''

        for column, _ in enumerate(self.__card[2]):
            if [self.__card[0][column], self.__card[1][column]].count('') == 0:
                self.__card[2][column] = ''

        row = True
        while row:
            if self.__card[2].count('') != 4:
                column = randint(0, len(self.__card[2]) - 1)
                if [self.__card[0][column], self.__card[1][column]].count('') == 2:
                    continue
                else:
                    self.__card[2][column] = ''
            else:
                row = False

        header_card = ' ' + self.get_player(self.__player) + ' '
        header_spacing = header_card.center(34, '*')
        self.__card.insert(0, [header_spacing])
        self.__card.append([self.__ticket])

        return self

    def del_num_data(self, num):
        return self.__data.remove(num)

    @property
    def card(self):
        card = [el for i in self.__card[1:-1] for el in i if el]
        return card


class LottoGame:
    def __init__(self):
        self.__user = LottoCard(input('Для начала игры введите ваше имя: ').capitalize())
        self.__comp = LottoCard('Карточка компьютера')
        self.__kegs = list(range(1, 91))
        self.__user_card = self.__user.create_card
        self.__comp_card = self.__comp.create_card
        self.__user_num_card = self.__user.card
        self.__comp_num_card = self.__comp.card
        self.__card = self.__user + self.__comp

    @property
    def play(self) -> int:
        shuffle(self.__kegs)
        keg = self.__kegs.pop()
        print('Игра началась!', self.__card, sep='\n')
        print(f'В мешке осталось {len(self.__kegs)} боченков\n'
              f'Боченок номер: {kegs(keg)}')

        answer = input('Зачеркнуть цифру? (y/enter): ').lower()
        if answer != 'y' and keg in self.__user_num_card or answer == 'y' and not keg in self.__user_num_card:
            return 2

        if keg in self.__user_num_card:
            self.__user_num_card.remove(keg)
            if len(self.__user_num_card) == 0:
                return 1

        if keg in self.__comp_num_card:
            self.__comp_num_card.remove(keg)
            if len(self.__comp_num_card) == 0:
                return 2

        self.__user.del_num_data(keg)

        return 0


if __name__ == '__main__':
    game = LottoGame()
    while True:
        count = game.play
        if count == 1:
            print('Вы победили')
            break
        elif count == 2:
            print('К сожалению вы проиграли')
            break
