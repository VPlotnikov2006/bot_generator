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


def print_ireq(ireq):
    """Функция вывода требований по инвентарю"""
    print('Сейчас требования по инвентарю выглядят так:')
    for v, txt in ireq:
        print(f'Что-бы попасть в вершину {v} (индексация с нуля), нужно иметь элемент инвентаря №{txt}')


def print_vreq(vreq):
    """Функция вывода требований по посещенным вершинам"""
    print('Сейчас требования по посещённым вершинам выглядят так:')
    for v, txt in vreq:
        print(f'Что-бы попасть в вершину {v} (индексация с нуля), нужно посетить вершину №{txt}')


def print_ilist(ilst):
    """Функция вывода обновлений инвенторя"""
    print('Сейчас в этих точках обновляется инвентарь так:')
    for v, txt in enumerate(ilst):
        print(f'В точке {v} (индексация с нуля), изменяются элементы инвентаря ', *txt)


# Переход в папку бота
cls = 'cls' if os.name == 'nt' else 'clear'
sep = '\\' if os.name == 'nt' else '/'
file = input('Введите адрес папки для бота:\n')
s = file + f'{sep}TelegramBotData{sep}static'
try:
    os.chdir(s)
except FileNotFoundError:
    print('Указанной папки не существует')
    input()
    sys.exit(1)

# Требования по предметам в инвентаре
# Считывание требований
try:
    inv_req = json.load(open('inventory_req_list.json', 'r'))
except FileNotFoundError:
    print('В файлах бота отсутствует TelegramBotData/static/inventory_req_list.json')
    print('Вы можете создать его сами')
    print('В этот файл нужно записать такую строку: ')
    print('[]')
    input()
    sys.exit(1)

# Вывод требований
print_ireq(inv_req)

# Удаление требований
for _ in range(int(input('Введите количество удалений, которое хотите сделать: '))):
    t = [int(i) for i in input('Введите индекс вершины и поле инвенторя:\n').split()]
    while t in inv_req:
        inv_req.remove(t)

# Вывод требований
print_ireq(inv_req)

# Добавление новых требований
for _ in range(int(input('Введите количество требований по инвентарю, которые вы хотите сейчас добавить: '))):
    try:
        u = int(input('Введите индекс вершины (индексация с нуля): '))
        t = int(input('Введите номер поля инвентаря (индексация с нуля): '))
    except ValueError:
        print('Ошибка ввода')
        print('Убедитесь что вы ввели одно число')
    else:
        inv_req.append([u, t])

# Сохранение
open('inventory_req_list.json', 'w').write(json.dumps(inv_req, indent=4, ensure_ascii=False))
os.system(cls)

# Требования по посещенным вершинам
# Считывание требований
try:
    visit_req = json.load(open('visited_req_list.json', 'r'))
except FileNotFoundError:
    print('В файлах бота отсутствует TelegramBotData/static/visited_req_list.json')
    print('Вы можете создать его сами')
    print('В этот файл нужно записать такую строку: ')
    print('[]')
    input()
    sys.exit(1)

# Вывод требований
print_vreq(visit_req)

# Удаление требований
for _ in range(int(input('Введите количество удалений, которое хотите сделать: '))):
    t = [int(i) for i in input('Введите индексы двух вершин:\n').split()]
    while t in visit_req:
        visit_req.remove(t)

# Вывод требований
print_vreq(visit_req)

# Добавление новых требований
for _ in range(int(input('Введите количество требований по инвентарю, которые вы хотите сейчас добавить: '))):
    try:
        u = int(input('Введите индекс вершины (индексация с нуля): '))
        t = int(input('Введите индекс вершины, которую нужно посетить (индексация с нуля): '))
    except ValueError:
        print('Ошибка ввода')
        print('Убедитесь что вы ввели одно число')
    else:
        visit_req.append([u, t])

# Сохранение
open('visited_req_list.json', 'w').write(json.dumps(visit_req, indent=4, ensure_ascii=False))
os.system(cls)

# Обновления полей инвентаря
# Считывание
try:
    inv_list = json.load(open('inventory_list.json', 'r'))
except FileNotFoundError:
    print('В файлах бота отсутствует TelegramBotData/static/inventory_list.json')
    print('Вы можете создать его сами')
    print('В этот файл нужно записать такую строку: ')
    print('[[], [], [], ... столько раз, сколько вершин в графе]')
    input()
    sys.exit(1)


# Вывод
print_ilist(inv_list)

# Удаление ненужных обновлений
for _ in range(int(input('Введите количество удалений, которое хотите сделать: '))):
    try:
        u = int(input('Введите индекс вершины для которой производится удаление: '))
        t = int(input('Введите номер поля инвентаря (индексайия с нуля): '))
    except ValueError:
        print('Ошибка ввода')
        print('Убедитесь что вы ввели одно число')
    else:
        while t in inv_list[u]:
            inv_list[u].remove(t)
    
# Вывод
print_ilist(inv_list)

# Обновление
for _ in range(int(input('Введите количество изменений инвентаря: '))):
    try:
        u = int(input('Введите индекс вершины, в которой меняется инвентарь (индексация с нуля): '))
        t = int(input('Введите индекс вершины инвентаря (индексация с нуля): '))
    except ValueError:
        print('Ошибка ввода')
        print('Убедитесь что вы ввели одно число')
    else:
        inv_list[u].append(t)


# Сохранение
open('inventory_list.json', 'w').write(json.dumps(inv_list, indent=4, ensure_ascii=False))
os.system(cls)

# Указание пути для отрисовки графов
if os.name == 'nt':
    os.environ["PATH"] += os.pathsep + 'C:\\Program Files\\Graphviz\\bin'

try:
    adj_list = json.load(open('adjacency_list.json', 'r'))
except FileNotFoundError:
    print('В файлах бота отсутствует TelegramBotData/static/adjacency_list.json')
    print('Вы можете создать его сами')
    print('В этот файл нужно записать такую строку: ')
    print('[[], [], [], ... столько раз, сколько вершин в графе]')
    input()
    sys.exit(1)

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
os.chdir(s)

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
                text += text_split[j]
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
