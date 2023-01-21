import telebot  # Основная библиотека для бота
import logging  # Библиотека для логов
from telebot import types  # Для настройки кнопок
from json import load, dumps  # Для считывания и записи словарей и списков
from TelegramBotData.lib import *  # Инвентарь и конфиг бота

bot = telebot.TeleBot(config.BotKey)  # Создание объекта бота

# Настройка параметров инвентаря
inventory.Inventory.node = config.node
inventory.Inventory.size = config.inventory_size
inventory.Inventory.visit_req = [[] for _ in range(inventory.Inventory.node)]
inventory.Inventory.inventory_req = [[] for _ in range(inventory.Inventory.node)]

# Считывание всей необходимой для работы бота информации
reverse_button = [{} for _ in range(config.node)]

with open('TelegramBotData/static/text.json') as fp:
    text = load(fp)  # Текста для вершин
with open('TelegramBotData/static/adjacency_list.json') as fp:
    inventory.adjacency_list = load(fp)  # Список смежности
with open('TelegramBotData/static/button.json') as fp:
    button = load(fp)  # Текста кнопок перехода между вершинами
with open('TelegramBotData/save/save.json') as fp:
    save = {int(k): v for k, v in load(fp).items()}  # Сохраненные пользователи
with open('TelegramBotData/static/inventory_list.json', 'r') as fp:
    inventory_list = load(fp)  # Изменения инвентаря
with open('TelegramBotData/static/visited_req_list.json', 'r') as fp:
    for v, u in load(fp):
        inventory.Inventory.set_visit_req(v, u)  # Создание требований по посещенным вершинам
with open('TelegramBotData/static/inventory_req_list.json', 'r') as fp:
    for v, j in load(fp):
        inventory.Inventory.set_inventory_req(v, j)  # Создание требований по предметам инвентаря

# Создание словаря для определения пункта назначения по тексту кнопки и пункту отправлвния
for i, l in enumerate(button):
    for v, k in enumerate(l):
        reverse_button[i][k] = v

# Настройка формата логов
logging.basicConfig(level=logging.INFO, filename='TelegramBotData/logs/telegrambot.log',
                    format="%(asctime)s %(levelname)s %(message)s")


def save_wrapper(func):
    """
    Декоратор для сохранения
    """
    def wrapper(*args, **kwargs):
        func(*args, **kwargs)
        open('TelegramBotData/save/save.json', 'w').write(dumps(save, indent=4, ensure_ascii=False))

    return wrapper


@bot.message_handler(commands=['start'])
@save_wrapper
def any_msg(message):
    """
    Команда start
    """
    client_id = message.chat.id  # ID чата
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)  # Пустая клавиатура
    vertex = 0  # Текущая вершина
    inv = inventory.Inventory()  # Путсой инвентарь
    inv.visit_add(vertex)
    save[client_id] = [vertex, inv.__dict__]
    bot.send_message(message.chat.id, "Нажми на команду /restart", reply_markup=keyboard)
    logging.info(f"{client_id}: Started game")


@bot.message_handler(commands=['restart'])  # Начать заново
@save_wrapper
def any_msg(message):
    """
    Команда restart
    """
    client_id = message.chat.id  # ID чата
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)  # Пустая клавиатура
    keyboard_remove = telebot.types.ReplyKeyboardRemove()  # Удаление клавиатуры
    vertex = 0
    inv = inventory.Inventory()  # Пустой инвентарь
    inv.visit_add(vertex)
    bot.send_message(message.chat.id, text[0], reply_markup=keyboard_remove)  # Вывод текста начальной вершины
    for possible_vertex in inventory.adjacency_list[vertex]:  # Добавление всех кнопок
        if inv.check(vertex, possible_vertex):  # Если к вершине можно пройти
            keyboard.add(types.KeyboardButton(text=button[vertex][possible_vertex]))
    bot.send_message(message.chat.id, 'Что будете делать;)?', reply_markup=keyboard)
    save[client_id] = [vertex, inv.__dict__]
    logging.info(f"{client_id}: Restarted game")


@bot.message_handler(commands=['admin_bot_stop'])
@save_wrapper
def bot_stop(message):
    """
    Остановка бота админом
    """
    if message.chat.id == config.AdminID:
        bot.send_message(message.chat.id, 'Остановка бота')
        bot.stop_polling()
        logging.info(f"{message.chat.id}: Stopped bot")


@bot.message_handler(content_types=["text"])
@save_wrapper
def any_msg(message):
    """
    Посещение какой-то вершины
    """
    client_id = message.chat.id  # ID чата
    keyboard_remove = telebot.types.ReplyKeyboardRemove()  # Пустая клавиатура
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)  # Удаление клавиатуры
    current_vertex = save[client_id][0]  # Загрузка сейва
    inv = inventory.Inventory()
    inv.__dict__ = save[client_id][1]
    if message.text not in reverse_button[current_vertex].keys():
        bot.send_message(message.chat.id, "Жмякай кнопки падла!", reply_markup=keyboard)
        return
    new_vertex = reverse_button[current_vertex][message.text]  # Вершина в которую пришел пользователь
    if new_vertex not in inventory.adjacency_list[current_vertex]:
        # Дополнительная проверка на попадание не в ту вершину
        bot.send_message(message.chat.id, f"Жмякай кнопки падла!", reply_markup=keyboard)
        return
    if not inv.check(current_vertex, new_vertex):
        # Проверка на попадание в закрытую вершину (например ввод текста без кнопки)
        bot.send_message(message.chat.id, "Ты не можешь это сделать!", reply_markup=keyboard)
        return
    for item in inventory_list[new_vertex]:  # Добавление предметов инвентаря
        inv.inventory_add(item)
    bot.send_message(message.chat.id, text[new_vertex], reply_markup=keyboard_remove)  # Отправка текста вершины

    for possible_vertex in inventory.adjacency_list[new_vertex]:  # Добавление кнопок
        if inv.check(new_vertex, possible_vertex):
            keyboard.add(types.KeyboardButton(text=button[new_vertex][possible_vertex]))

    inv.visit_add(new_vertex)
    bot.send_message(message.chat.id, 'Что будете делать;)?', reply_markup=keyboard)
    save[client_id] = [new_vertex, inv.__dict__]
    logging.info(f"{client_id}: Move from {current_vertex} to {new_vertex}")


if __name__ == '__main__':
    logging.debug(f'{text=}')
    logging.debug(f'{inventory.adjacency_list=}')
    logging.debug(f'{save=}')
    logging.debug(f'{button=}')
    logging.debug(f'{reverse_button=}')
    logging.debug(f'{config.BotKey=}')
    logging.debug(f'{inventory_list=}')
    logging.debug(f'{inventory.Inventory.visit_req=}')
    logging.debug(f'{inventory.Inventory.inventory_req=}')
    logging.debug(f'{config.AdminID=}')
    logging.info('Bot started')
    bot.polling()
