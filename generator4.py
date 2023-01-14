import json  # Сохранение списков
import os  # Переход в другую директорию
import graphviz  # Отрисовка графа

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
s = input('Введите адрес папки для бота:\n') + f'{sep}TelegramBotData{sep}static'
os.chdir(s)

# Требования по предметам в инвентаре
# Считывание требований
inv_req = json.load(open('inventory_req_list.json', 'r'))

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
    u = int(input('Введите индекс вершины (индексация с нуля): '))
    t = int(input('Введите индекс вершины инвентаря (индексация с нуля): '))
    inv_req.append([u, t])

# Сохранение
open('inventory_req_list.json', 'w').write(json.dumps(inv_req, indent=4, ensure_ascii=False))
os.system(cls)

# Требования по посещенным вершинам
# Считывание требований
visit_req = json.load(open('visited_req_list.json', 'r'))

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
for _ in range(int(input('Введите количество требований по посещённым вершинам, которые вы хотите сейчас добавить: '))):
    u = int(input('Введите индекс вершины (индексация с нуля): '))
    t = int(input('Введите индекс вершины, которую нужно посетить (индексация с нуля): '))
    visit_req.append([u, t])

# Сохранение
open('visited_req_list.json', 'w').write(json.dumps(visit_req, indent=4, ensure_ascii=False))
os.system(cls)

# Обновления полей инвентаря
# Считывание
inv_list = json.load(open('inventory_list.json', 'r'))

# Вывод
print_ilist(inv_list)

# Удаление ненужных обновлений
for _ in range(int(input('Введите количество удалений, которое хотите сделать: '))):
    u = int(input('Введите индекс вершины для которой производится удаление: '))
    t = int(input('Введите номер поля инвенторя (индексайия с нуля): '))
    while t in inv_list[u]:
        inv_list[u].remove(t)

# Вывод
print_ilist(inv_list)

# Обновление
for _ in range(int(input('Введите количество изменений инвентаря: '))):
    u = int(input('Введите индекс вершины, в которой меняется инвентарь (индексация с нуля): '))
    t = int(input('Введите индекс вершины инвентаря (индексация с нуля): '))
    inv_list[u].append(t)

# Сохранение
open('inventory_list.json', 'w').write(json.dumps(inv_list, indent=4, ensure_ascii=False))
os.system(cls)

os.environ["PATH"] += os.pathsep + 'C:\\Program Files\\Graphviz\\bin'
print(os.system("dot -V"))

adj_list = json.load(open('adjacency_list.json', 'r'))
button_list = json.load(open('button.json', 'r'))
text_list = json.load(open('text.json', 'r'))

g = graphviz.Digraph('round-table', comment='The Round Table', format='png')

for i, h in enumerate(adj_list):
    for j in h:
        if text_list[i] == '' or text_list[j] == '':
            g.edge(f'No text for vertex №{i}', f'No text for vertex №{j}', label=button_list[i][j])
        else:
            g.edge(text_list[i], text_list[j], label=button_list[i][j])

g.view()