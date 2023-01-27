import json  # Сохранение словарей
import os  # Переход в директорию бота
import sys  # Завершение работы программы
try:
    import graphviz  # Отрисовка графа
except ModuleNotFoundError:
    print('Модуль graphviz не установлен')
    print('Команда для установки: ')
    print('pip install graphviz')
    input()
    sys.exit(1)


def print_adj_list(lst):
    """Функция вывода списка смежности"""
    print('Сейчас список смежости бота выглядит так (индексация с нуля):')
    for i, l in enumerate(lst):
        print(f'Из вершины {i} можно попасть в вершины: ', *l)


# Переход в папку бота
sep = '\\' if os.name == 'nt' else '/'
file = input('Введите адрес папки для бота:\n')
s = file + f'{sep}TelegramBotData{sep}static'
try:
    os.chdir(s)
except FileNotFoundError:
    print('Указанной папки не существует')
    input()
    sys.exit(1)

# Считывание списка смежности
try:
    adj_list = json.load(open('adjacency_list.json', 'r'))
except FileNotFoundError:
    print('В файлах бота отсутствует TelegramBotData/static/adjacency_list.json')
    print('Вы можете создать его сами')
    print('В этот файл нужно записать такую строку: ')
    print('[[], [], [], ... столько раз, сколько вершин в графе]')
    input()
    sys.exit(1)

# Вывод списка смежности
print_adj_list(adj_list)

# Удаление ребер
for _ in range(int(input('Введите количество удалений, которое хотите сделать: '))):
    v = int(input('Введите индекс вершины, у которой хотите удалить связь: '))
    u = int(input('Введите индекс вершины, связь с которой хотите удалить: '))
    while u in adj_list[v]:
        adj_list[v].remove(u)

# Вывод списка смежности
print_adj_list(adj_list)

# Добавление новых ребер
for _ in range(int(input('Введите количество ребер в графе, которое вы хотите сейчас добавить: '))):
    try:
        u, v = list(map(int, input('Введите номера вершин, между которыми есть ребро (из первой во вторую) (индексация '
                                   'идет с нуля): \n').split()))
    except ValueError:
        print('При вводе чисел произошла ошибка')
        print('Убедитесь что вы ввели 2 числа в одну строку через пробел')
    else:
        try:
            adj_list[u].append(v)
        except IndexError:
            print('Введен некорректный индекс')
            print('Будьте внимательны. Индексация с нуля')

# Сохранение изменений
open('adjacency_list.json', 'w').write(json.dumps(adj_list, indent=4, ensure_ascii=False))

# Указание пути для отрисовки графов
if os.name == 'nt':
    os.environ["PATH"] += os.pathsep + 'C:\\Program Files\\Graphviz\\bin'

try:
    button_list = json.load(open('button.json', 'r'))
except FileNotFoundError:
    print('В файлах бота отсутствует TelegramBotData/static/button.json')
    print('Вы можете создать его сами')
    print('В этот файл нужно записать такую строку: ')
    print('[["", "", ... столько раз, сколько вершин в графе], ["", "", ... столько раз, сколько вершин в графе], '
          '... столько раз, сколько вершин в графе]')
    input()
    sys.exit(1)

try:
    text_list = json.load(open('text.json', 'r'))
except FileNotFoundError:
    print('В файлах бота отсутствует TelegramBotData/static/text.json')
    print('Вы можете создать его сами')
    print('В этот файл нужно записать такую строку: ')
    print('["", "", ... столько раз, сколько вершин в графе]')
    input()
    sys.exit(1)
# Указание, куда сохранять картинку
s = file + f'{sep}TelegramBotData{sep}graph'
try:
    os.chdir(s)
except FileNotFoundError:
    print('Указанной папки не существует')
    input()
    sys.exit(1)

# Создание графа
try:
    g = graphviz.Digraph('Graph for bot', comment='Your graph', format='png')

    # Создание нормальных окон(не однострочных)
    for i in range(len(adj_list)):
        text_split = text_list[i].split()
        text = ''
        l = 0
        for j in range(len(text_split)):
            if l <= 20:
                text += text_split[j] + " "
                l += len(text_split[j]) + 1
            else:
                text += '\n'
                text += text_split[j] + " "
                l = 0
                l += len(text_split[j])

        if not text:
            text = f'No text for vertex №{i}'
        else:
            pass
        g.node(f'{i}', text)

    for i, h in enumerate(adj_list):
        for j in h:
            g.edge(f'{i}', f'{j}',
                   label=button_list[i][j] if button_list[i][j] else f'No text wor edge from {i} to {j}')

    print('Вы хотите увидеть получившийся граф?(Y/N)')
    if input().upper() == 'Y':
        g.view()
    else:
        g.render()

    print(f'Граф сохранён по адресу {s}')
except Exception as e:
    print('При создании графа бота возникли проблемы')
    print('Убедитесь что вы скачали graphviz (не только библиотеку, но и само приложение)')
    print(e)
    input()
