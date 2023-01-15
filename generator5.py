import json  # Сохранение списков
import os  # Переход в другую директорию
import graphviz  # Отрисовка графа

def print_buttons(buttons):
    """Функция вывода текстов для кнопок"""
    print('Сейчас кнопки для вершин выглядят вот так:')
    for i, l in enumerate(buttons):
        for j, txt in enumerate(l):
            if txt:
                print(f'Переход из вершины {i} в вершину {j} (индексация с нуля) сопровождается текстом:\n"{txt}"')


# Переход в папку бота
sep = '\\' if os.name == 'nt' else '/'
file = input('Введите адрес папки для бота:\n')
s = file + f'{sep}TelegramBotData{sep}static'
os.chdir(s)

# Считывание текстов кнопок
button = json.load(open('button.json', 'r'))

# Вывод текстов
print_buttons(button)

# Удаление текста кнопки
for _ in range(int(input('Введите количество удалений, которое хотите сделать: '))):
    u, v = [int(i) for i in input('Введите индексы вершин, кнопку между которыми вы хотите удалить: ').split()]
    button[u][v] = ''

# Вывод текстов
print_buttons(button)

# Обновление текстов кнопок
for _ in range(int(input('Введите количество текстов для кнопок, которое вы хотите добавить: '))):
    u, v = [int(i) for i in input('Введите индексы двух вершин:\n').split()]
    t = input('Введите текст для кнопочки. Важно чтобы у одной вершины не было кнопочек с одинаковым названием\n')
    button[u][v] = t

# Сохранение текстов
open('button.json', 'w').write(json.dumps(button, indent=4, ensure_ascii=False))

# Указание путя для отрисовки графов
os.environ["PATH"] += os.pathsep + 'C:\\Program Files\\Graphviz\\bin' #

adj_list = json.load(open('adjacency_list.json', 'r'))
button_list = json.load(open('button.json', 'r'))
text_list = json.load(open('text.json', 'r'))

# Указание, куда сохранять картинку
s = file + f'{sep}TelegramBotData{sep}graph'
os.chdir(s)

# Создание графа
g = graphviz.Digraph('Graph for bot', comment='Your graph', format='png')

for i in range(len(adj_list)):
    g.node(f'{i}', text_list[i] if text_list[i] else f'No text for vertex №{i}')

for i, h in enumerate(adj_list):
    for j in h:
        g.edge(f'{i}', f'{j}',
               label=button_list[i][j] if button_list[i][j] else f'No text wor edge from {i} to {j}')

print('Вы хотите увидеть получившийся граф?(Y/N)')
if input() == 'Y':
    g.view()
else:
    g.render()

print(f'Граф сохранён по адресу {file}{sep}TelegramBotData{sep}graph')
