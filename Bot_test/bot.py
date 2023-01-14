import telebot
import logging
from telebot import types
from json import load, dumps3
from TelegramBotData import *

bot = telebot.TeleBot(config.BotKey)

inventory.Inventory.node = config.node
inventory.Inventory.size = config.inventory_size
inventory.Inventory.visit_req = [[] for _ in range(inventory.Inventory.node)]
inventory.Inventory.inventory_req = [[] for _ in range(inventory.Inventory.node)]

reverse_button = [{} for _ in range(config.node)]

with open('TelegramBotData/text.json') as fp:
    text = load(fp)
with open('TelegramBotData/adjacency_list.json') as fp:
    inventory.adjacency_list = load(fp)
with open('TelegramBotData/button.json') as fp:
    button = load(fp)
with open('TelegramBotData/save.json') as fp:
    save = {int(k): v for k, v in load(fp).items()}
with open('TelegramBotData/inventory_list.json', 'r') as fp:
    inventory_list = load(fp)
with open('TelegramBotData/visited_req_list.json', 'r') as fp:
    for v, u in load(fp):
        inventory.Inventory.set_visit_req(v, u)
with open('TelegramBotData/inventory_req_list.json', 'r') as fp:
    for v, j in load(fp):
        inventory.Inventory.set_inventory_req(v, j)

for i, l in enumerate(button):
    for v, k in enumerate(l):
        reverse_button[i][k] = v

logging.basicConfig(level=logging.INFO, filename='log.log',
                    format="%(asctime)s %(levelname)s %(message)s")

def save_wrapper(func):
    def wrapper(*args, **kwargs):
        func(*args, **kwargs)
        open('TelegramBotData/save.json', 'w').write(dumps(save, indent=4, ensure_ascii=False))

    return wrapper


@bot.message_handler(commands=['start'])
@save_wrapper
def any_msg(message):
    client_id = message.chat.id
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    vertex = 0
    inv = inventory.Inventory()
    inv.visit_add(vertex)
    save[client_id] = [vertex, inv.__dict__]
    bot.send_message(message.chat.id, "Нажми на команду /restart", reply_markup=keyboard)
    logging.debug(f"{client_id}: Started game")


@bot.message_handler(commands=['restart'])  # Начать заново
@save_wrapper
def any_msg(message):
    client_id = message.chat.id
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard_remove = telebot.types.ReplyKeyboardRemove()
    vertex = 0
    inv = inventory.Inventory()
    inv.visit_add(vertex)
    bot.send_message(message.chat.id, text[0], reply_markup=keyboard_remove)
    for possible_vertex in inventory.adjacency_list[vertex]:  # Добавление всех кнопок
        if inv.check(vertex, possible_vertex):
            keyboard.add(types.KeyboardButton(text=button[vertex][possible_vertex]))
    bot.send_message(message.chat.id, 'Что будете делать;)?', reply_markup=keyboard)
    save[client_id] = [vertex, inv.__dict__]
    logging.debug(f"{client_id}: Restarted game")


@bot.message_handler(commands=['admin_bot_stop'])
@save_wrapper
def bot_stop(message):
    if message.chat.id == config.AdminID:
        bot.send_message(message.chat.id, 'Остановка бота')
        print(f'Bot stopped by {message.chat.id}')
        bot.stop_polling()
        logging.debug(f"{client_id}: Stopped bot")


@bot.message_handler(content_types=["text"])
@save_wrapper
def any_msg(message):
    client_id = message.chat.id
    keyboard_remove = telebot.types.ReplyKeyboardRemove()
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    current_vertex = save[client_id][0]
    if message.text not in reverse_button[current_vertex].keys():
        bot.send_message(message.chat.id, "Жмякай кнопки падла!", reply_markup=keyboard)
        return
    new_vertex = reverse_button[current_vertex][message.text]
    inv = inventory.Inventory()
    inv.__dict__ = save[client_id][1]
    inv.visit_add(new_vertex)
    for item in inventory_list[new_vertex]:
        inv.inventory_add(item)
    if new_vertex not in inventory.adjacency_list[current_vertex]:
        bot.send_message(message.chat.id, f"Жмякай кнопки падла!", reply_markup=keyboard)
        return
    if not inv.check(current_vertex, new_vertex):
        bot.send_message(message.chat.id, "Ты не можешь это сделать!", reply_markup=keyboard)
        return
    bot.send_message(message.chat.id, text[new_vertex], reply_markup=keyboard_remove)

    for possible_vertex in inventory.adjacency_list[new_vertex]:
        if inv.check(new_vertex, possible_vertex):
            keyboard.add(types.KeyboardButton(text=button[new_vertex][possible_vertex]))

    inv.visit_add(new_vertex)
    bot.send_message(message.chat.id, 'Что будете делать;)?', reply_markup=keyboard)
    save[client_id] = [new_vertex, inv.__dict__]
    logging.debug(f"{client_id}:{current_vertex}->{new_vertex}")


print(f'{text=}')
print(f'{inventory.adjacency_list=}')
print(f'{save=}')
print(f'{button=}')
print(f'{reverse_button=}')
print(f'{config.BotKey=}')
print(f'{inventory_list=}')
print(f'{inventory.Inventory.visit_req=}')
print(f'{inventory.Inventory.inventory_req=}')
print(f'{config.AdminID}')
if __name__ == '__main__':
    bot.polling()