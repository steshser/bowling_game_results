# -*- coding: utf-8 -*-
# Вас взяли на работу в молодой стартап. Идея стартапа - предоставлять сервис расчета результатов игр.
# Начать решили с боулинга, упрощенной версии.
#
# Правила такие.
#
# Всего 10 кеглей. Игра состоит из 10 фреймов. В одном фрейме до 2х бросков, цель - сбить все кегли.
# Результаты фрейма записываются символами:
#   «Х» – «strike», все 10 кеглей сбиты первым броском
#   «<число>/», например «4/» - «spare», в первый бросок сбиты 4 кегли, во второй – остальные
#   «<число><число>», например, «34» – в первый бросок сбито 3, во второй – 4 кегли.
#   вместо <число> может стоять прочерк «-», например «-4» - ни одной кегли не было сбито за первый бросок
# Результат игры – строка с записью результатов фреймов. Символов-разделителей между фреймами нет.
# Например, для игры из 4 фреймов запись результатов может выглядеть так:
#   «Х4/34-4»
# Предлагается упрощенный способ подсчета количества очков:
#   «Х» – strike всегда 20 очков
#   «4/» - spare всегда 15 очков
#   «34» – сумма 3+4=7
#   «-4» - сумма 0+4=4
# То есть для игры «Х4/34-4» сумма очков равна 20+15+7+4=46
#
# Надо написать python-модуль (назвать bowling), предоставляющий API расчета количества очков:
# функцию get_score, принимающую параметр game_result. Функция должна выбрасывать исключения,
# когда game_result содержит некорректные данные. Использовать стандартные исключения по максимуму,
# если не хватает - создать свои.
#
# Обязательно написать тесты на этот модуль. Расположить в папке tests.


import warnings

# from abc import ABC, abstractmethod

BOWLING_ELEMENTS = '123456789X-/'


class IncorrectDataError(Exception):
    pass


class FrameQuantityError(Exception):
    pass


class GameOverError(Exception):
    pass


class SkittleQuantityError(Exception):
    pass


class SpareError(Exception):
    pass


# Выдает ошибку ImportError: cannot import name ABC
# class GameResult(ABC):
#
#     @abstractmethod
#     def get_score(self):
#         pass


class InternalGameResult:

    def __init__(self, game_result):
        self.game_result = game_result
        self.total_score = 0
        self.game_data = []
        self.STRIKE_POINTS = 20
        self.SPARE_POINTS = 15

    def get_score(self):
        self.game_result = list(self.game_result)
        for i in range(len(self.game_result)):
            if self.game_result[i] not in BOWLING_ELEMENTS:
                raise IncorrectDataError('Некорректные данные')
        if (len(self.game_result) == self.game_result.count('Х') and len(self.game_result) > 10) or len(
                self.game_result) > 20:
            raise FrameQuantityError('Сделано больше 10 фреймов')
        self.total_score += self.game_result.count('X') * self.STRIKE_POINTS
        strikes_quantity = self.game_result.count('X')
        while self.game_result.count('X') != 0:
            self.game_result.remove('X')
        for i in range(0, len(self.game_result), 2):
            self.game_data.append(self.game_result[i:i + 2])
        if (len(self.game_data) + strikes_quantity) < 10:
            raise GameOverError('Игра не закончена')
        for i in range(len(self.game_data)):
            if self.game_data[i][0] == '/':
                raise SpareError('Некорректные данные spare')
            if self.game_data[i][1] == '/':
                self.total_score += self.SPARE_POINTS
                continue
            elif self.game_data[i][0] == '-' and self.game_data[i][1] == '-':
                continue
            elif self.game_data[i][0] == '-':
                self.total_score += int(self.game_data[i][1])
                continue
            elif self.game_data[i][1] == '-':
                self.total_score += int(self.game_data[i][0])
                continue
            elif (int(self.game_data[i][0]) + int(self.game_data[i][1])) > 10:
                raise SkittleQuantityError('Сбито больше 10 кеглей')
            elif (int(self.game_data[i][0]) + int(self.game_data[i][1])) == 10:
                warnings.warn('Не был учтен spare, но мы все исправили')
                self.total_score += self.SPARE_POINTS
            else:
                self.total_score += int(self.game_data[i][0]) + int(self.game_data[i][1])
        return self.total_score


class InternationalGameResult:

    def __init__(self, game_result):
        self.game_result = game_result
        self.total_score = 0
        self.game_data = []

    def get_score(self):
        self.game_result = list(self.game_result)
        if (len(self.game_result) == self.game_result.count('X') and len(self.game_result) > 10) \
                or len(self.game_result) > 20:
            raise FrameQuantityError('Сделано больше 10 фреймов')
        strikes_quantity = self.game_result.count('X')
        if ((len(self.game_result) - strikes_quantity) // 2) + strikes_quantity < 10:
            raise GameOverError('Игра не закончена')
        for x in range(len(self.game_result)):
            if self.game_result[x] not in BOWLING_ELEMENTS:
                raise IncorrectDataError('Некорректные данные')
            if self.game_result[x] == '-':
                self.game_result[x] = 0
        for i in range(len(self.game_result)):
            # условия для подсчета strike
            if i != (len(self.game_result)-1) and i != (len(self.game_result) - 2) and \
                    self.game_result[i] == 'X' and self.game_result[i + 1] == 'X' and self.game_result[i + 2] == 'X':
                self.total_score += 30
            elif i != (len(self.game_result)-1) and i != (len(self.game_result) - 2) and \
                    self.game_result[i] == 'X' and self.game_result[i + 2] == '/':
                self.total_score += 20
            elif i == (len(self.game_result) - 2) and self.game_result[i] == 'X' and self.game_result[i + 1] == 'X':
                self.total_score += 20
            elif i == (len(self.game_result) - 1) and self.game_result[i] == 'X':
                self.total_score += 10
            elif i != (len(self.game_result) - 1) and i != (len(self.game_result) - 2) and \
                    self.game_result[i] == 'X' and self.game_result[i + 1] != 'X' and \
                    (self.game_result[i + 2] != 'X' or self.game_result[i + 2] != '/'):
                self.total_score += (10 + int(self.game_result[i + 1]) + int(self.game_result[i + 2]))
            elif i != (len(self.game_result) - 1) and i != (len(self.game_result) - 2) and \
                    self.game_result[i] == 'X' and self.game_result[i + 1] == 'X' \
                    and (self.game_result[i + 2] != 'X'):
                self.total_score += (20 + int(self.game_result[i + 2]))
                # условия для подсчета spare
            elif i == (len(self.game_result) - 1) and self.game_result[i] == '/':
                self.total_score += 10 - int(self.game_result[i - 1])
            elif i != (len(self.game_result) - 1) and self.game_result[i] == '/' and self.game_result[i + 1] == 'X':
                self.total_score += 20 - int(self.game_result[i - 1])
            elif i != (len(self.game_result) - 1) and self.game_result[i] == '/':
                self.total_score += 10 - int(self.game_result[i - 1]) + int(self.game_result[i + 1])
                # условия для подсчета незакрытого фрейма
            elif self.game_result[i] == '-':
                continue
            else:
                self.total_score += int(self.game_result[i])
            # добавляем проверку суммы сбитых кеглей и spare
        while self.game_result.count('X') != 0:
            self.game_result.remove('X')
        for n in range(0, len(self.game_result), 2):
            self.game_data.append(self.game_result[n:n + 2])
        for k in range(len(self.game_data)):
            if self.game_data[k][0] == '/':
                raise SpareError('Некорректные данные spare')
            elif (self.game_data[k][1] == '/') or (self.game_data[k][0] == '-') or (self.game_data[k][1] == '-'):
                continue
            elif (int(self.game_data[k][0]) + int(self.game_data[k][1])) > 10:
                raise SkittleQuantityError('Сбито больше 10 кеглей')
            elif (int(self.game_data[k][0]) + int(self.game_data[k][1])) == 10:
                raise SpareError('Некорректные данные spare')
        return self.total_score

