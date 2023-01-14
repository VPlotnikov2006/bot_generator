import json  # Сохранение словарей
import os  # Переход в директорию бота
import graphviz  # Отрисовка графа

def print_adj_list(lst):
    """Функция вывода списка смежности"""
    print('Сейчас список смежости бота выглядит так (индексация с нуля):')
    for i, l in enumerate(lst):
        print(f'Из вершины {i} можно попасть в вершины: ', *l)


# Переход в папку бота
sep = '\\' if os.name == 'nt' else '/'
s = input('Введите адрес папки для бота:\n') + f'{sep}TelegramBotData{sep}static'
os.chdir(s)

# Считывание списка смежности
adj_list = json.load(open('adjacency_list.json', 'r'))

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
    u, v = list(map(int, input('Введите номера вершин, между которыми есть ребро (из первой во вторую) (индексация '
                               'идет с нуля): \n').split()))
    adj_list[u].append(v)

# Сохранение изменений
open('adjacency_list.json', 'w').write(json.dumps(adj_list, indent=4, ensure_ascii=False))

os.environ["PATH"] += os.pathsep + 'C:\\Program Files\\Graphviz\\bin'
print(os.system("dot -V"))

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