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


def print_texts(texts):
    """Функция вывода текстов вершин"""
    print('Сейчас тексты для вершин графа выглядят так:')
    for v, txt in enumerate(texts):
        if txt:
            print(f'Текст для вершины {v} (индексация с нуля): \n"{txt}"')


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

# Считывание текстов вершин
try:
    text = json.load(open('text.json', 'r'))
except FileNotFoundError:
    print('В файлах бота отсутствует TelegramBotData/static/text.json')
    print('Вы можете создать его сами')
    print('В этот файл нужно записать такую строку: ')
    print('["", "", ... столько раз, сколько вершин в графе]')
    input()
    sys.exit(1)

# Вывод текстов
print_texts(text)

# Удаление текстов вершин
for _ in range(int(input('Введите количество удалений, которое хотите сделать: '))):
    try:
        u = int(input('Введите индекс вершины, текст которой хотите удалить: '))
    except ValueError:
        print('Ошибка ввода')
        print('Убедитесь что вы ввели одно число')
    else:
        try:
            text[u] = ''
        except IndexError:
            print('Введен некорректный индекс')
            print('Будьте внимательны. Индексация с нуля')

# Вывод текстов
print_texts(text)

# Обновление текстов вершин
for _ in range(int(input('Введите количество вершин в графе, тексты для которых вы хотите сейчас добавить: '))):
    try:
        u = int(input('Введите индекс вершины (индексация с нуля): '))
    except ValueError:
        print('Ошибка ввода')
        print('Убедитесь что вы ввели одно число')
    else:
        try:
            t = input('Введите текст для этой вершины:\n')
            text[u] = t
        except IndexError:
            print('Введен некорректный индекс')
            print('Будьте внимательны. Индексация с нуля')

# Сохранение текстов
open('text.json', 'w').write(json.dumps(text, indent=4, ensure_ascii=False))

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
