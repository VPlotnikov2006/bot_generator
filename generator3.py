import json  # Сохранение списков
import os  # Переход в другую директорию
import graphviz  # Отрисовка графа

def print_texts(texts):
    """Функция вывода текстов вершин"""
    print('Сейчас тексты для вершин графа выглядят так:')
    for v, txt in enumerate(texts):
        if txt:
            print(f'Текст для вершины {v} (индексация с нуля): \n"{txt}"')


# Переход в папку бота
sep = '\\' if os.name == 'nt' else '/'
s = input('Введите адрес папки для бота:\n') + f'{sep}TelegramBotData{sep}static'
os.chdir(s)

# Считывание текстов вершин
text = json.load(open('text.json', 'r'))

# Вывод текстов
print_texts(text)

# Удаление текстов вершин
for _ in range(int(input('Введите количество удалений, которое хотите сделать: '))):
    u = int(input('Введите индекс вершины, текст которой хотите удалить: '))
    text[u] = ''

# Вывод текстов
print_texts(text)

# Обновление текстов вершин
for _ in range(int(input('Введите количество вершин в графе, тексты для которых вы хотите сейчас добавить: '))):
    u = int(input('Введите индекс вершины (индексация с нуля): '))
    t = input('Введите текст для этой вершины:\n')
    text[u] = t

# Сохранение текстов
open('text.json', 'w').write(json.dumps(text, indent=4, ensure_ascii=False))

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