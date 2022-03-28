# -*- coding: utf-8 -*-

# Прибежал менеджер и сказал что нужно срочно просчитать протокол турнира по боулингу в файле tournament.txt
#
# Пример записи из лога турнира
#   ### Tour 1
#   Алексей	35612/----2/8-6/3/4/
#   Татьяна	62334/6/4/44X361/X
#   Давид	--8/--8/4/8/-224----
#   Павел	----15623113-95/7/26
#   Роман	7/428/--4-533/34811/
#   winner is .........
#
# Нужно сформировать выходной файл tournament_result.txt c записями вида
#   ### Tour 1
#   Алексей	35612/----2/8-6/3/4/    98
#   Татьяна	62334/6/4/44X361/X      131
#   Давид	--8/--8/4/8/-224----    68
#   Павел	----15623113-95/7/26    69
#   Роман	7/428/--4-533/34811/    94
#   winner is Татьяна

# Код обаботки файла расположить отдельном модуле, модуль bowling использовать для получения количества очков
# одного участника. Если захочется изменить содержимое модуля bowling - тесты должны помочь.
import bowling


class MethodError(Exception):
    pass


def tournament_result(tournament_protocol_file, tournament_result_file, method):
    name_result_dict = {}
    with open(tournament_protocol_file, 'r', encoding='UTF8') as file, \
            open(tournament_result_file, mode='w+', encoding='UTF8') as result_file:
        for line in file:
            try:
                line = line[:-1]
                line = line.split('\t')
                if line[0].count('###') != 0 or line[0] == '':
                    result_file.write('{}\n'.format(line[0]))
                    continue
                if line[0].count('winner is .........') != 0:
                    winner_name = max(name_result_dict, key=name_result_dict.get)
                    result_file.write('winner is {}\n'.format(winner_name))
                    name_result_dict = {}
                    continue
                else:
                    name = line[0]
                    game_result = line[1]
                    if method == 'Internal':
                        result = bowling.InternalGameResult(game_result)
                    elif method == 'International':
                        result = bowling.InternationalGameResult(game_result)
                        pass
                    else:
                        raise MethodError('Нет такого метода подсчета очков. Выберите Internal или International')
                    score = result.get_score()
                    name_result_dict[name] = score
                    result_file.write('{} {} {}\n'.format(name, game_result, name_result_dict[name]))
            except (bowling.IncorrectDataError, bowling.FrameQuantityError,
                    bowling.GameOverError, bowling.SkittleQuantityError,
                    bowling.SpareError, MethodError, Exception) as exc:
                result_file.write('Ошибка {} линия {}\n'.format(exc, line))
    file.close()
    result_file.close()