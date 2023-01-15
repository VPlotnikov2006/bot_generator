import os  # Переход в другую директорию + создание папки для файлов бота
import sys  # Завершение работы программы
import shutil  # Копирование неизменяемых файлов пользователю
import json  # Сохранение списков и словарей для корректной работы других генераторов
import telebot  # Для подтверждения админки
from string import ascii_letters  # Для генерации секретного кода
from random import randint  # Для генерации секретного кода

sep = '\\' if os.name == 'nt' else '/'

# Считывание важных переменных
s = input('Введите адрес папки для бота:\n')
BotKey = input('Введите ключ бота:\n')
n = int(input('Введите количество вершин в графе: '))
i = int(input('Введите число используемых полей инвентаря: '))

token = ''.join(map(lambda x: chr(int(x, 16)), open('TelegramBotGeneratorData/token', 'r').readlines()))
bot = telebot.TeleBot(token)

code = ''.join([ascii_letters[randint(0, len(ascii_letters) - 1)] for _ in range(randint(10, 30))])
print('Сейчас программа зафиксирует ваш TelegramID для корректной работы админки')
print(f'Секретный код: {code}')
print('Его нужно отправить боту @verification_4_bot_generator_bot')
AdminID = -1


@bot.message_handler(content_types=["text"])
def any_msg(message):
    if message.text == code:
        bot.send_message(message.chat.id, 'Аккаунт админа подтвержден')
        global AdminID
        AdminID = message.chat.id
        print('Аккаунт админа зафиксирован')
        print('Ожидайте создания всех необходимых файлов')
        bot.stop_polling()
    else:
        bot.send_message(message.chat.id, 'Возникли некоторые проблемы. Проверьте корректность введенного кода или '
                                          'перезапустите программу')


bot.stop_polling()
bot.polling()

# Создание всех файлов
# config.py
cfg = ''.join(open(f'TelegramBotGeneratorData{sep}config.py').readlines()).format(
    node=n, inventory_size=i, BotKey=BotKey, AdminId=AdminID)

# Переходиим в папку бота
d = os.getcwd()
os.chdir(s)
if len(os.listdir(path='.')):
    print('В папке назначения есть файлы')
    print('Создание бота в этой папке может их уничтожить')
    print('Или эти файлы могут помешать работе бота')
    sys.exit(1)
os.mkdir('TelegramBotData')
os.mkdir('TelegramBotData/logs')
os.mkdir('TelegramBotData/static')
os.mkdir('TelegramBotData/lib')
os.mkdir('TelegramBotData/save')
os.mkdir('TelegramBotData/graph')

# Копируем неизменяемые файлы
shutil.copy(d + f'{sep}TelegramBotGeneratorData{sep}inventory.py', f'TelegramBotData{sep}lib{sep}inventory.py')
shutil.copy(d + f'{sep}TelegramBotGeneratorData{sep}__init__.py', f'TelegramBotData{sep}lib{sep}__init__.py')
shutil.copy(d + f'{sep}TelegramBotGeneratorData{sep}pattern.py', 'bot.py')

open(f'TelegramBotData{sep}lib{sep}config.py', 'w').write(cfg)  # Сохранение конфига
open(f'TelegramBotData{sep}save{sep}save.json', 'w').write(json.dumps({}, indent=4, ensure_ascii=False))
# ^Пустой словарь для сохранений^

open(f'TelegramBotData{sep}static{sep}text.json', 'w').write(json.dumps([''] * n, indent=4, ensure_ascii=False))
# ^Заготовка для текстов вершин^

open(f'TelegramBotData{sep}static{sep}adjacency_list.json', 'w').write(
    json.dumps([[] for _ in range(n)], indent=4, ensure_ascii=False))
# ^Заготовка под список смежности^

open(f'TelegramBotData{sep}static{sep}button.json', 'w').write(
    json.dumps([['' for _ in range(n)] for _ in range(n)], indent=4, ensure_ascii=False))
# ^Заготовка под текста для кнопочек^

open(f'TelegramBotData{sep}static{sep}inventory_req_list.json', 'w').write(
    json.dumps([], indent=4, ensure_ascii=False))
# ^Заготовка под список требований по инвентарю^

open(f'TelegramBotData{sep}static{sep}visited_req_list.json', 'w').write(
    json.dumps([], indent=4, ensure_ascii=False))
# ^Заготовка под список требований по посещенным вершинам^

open(f'TelegramBotData{sep}static{sep}inventory_list.json', 'w').write(
    json.dumps([[] for _ in range(n)], indent=4, ensure_ascii=False))
# ^Заготовка под предметы инвенторя в вершинах^
