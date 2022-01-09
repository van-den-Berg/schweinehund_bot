# -*- coding: utf-8 -*-
import os.path

import telebot  # importing pyTelegramBotAPI library
import time
import sys

# import telegram_send
from lib.Strings import registration_succesfull_group, registration_succesfull_private
from models.Activity import Activity
from models.data_storage import Data
from services import FileServices
from telegram import message
from models.TelegramUser import User
from services.MessageServices import get_sender_id
from lib import Strings
from testing import Mocking

mocking = True

config_json_path: str = 'config.json'
data_json_path: str = 'data.json'
mock_data_json_path: str = 'mock_data.json'

config_dict = FileServices.read_json(config_json_path)
bot = telebot.TeleBot(token=config_dict["tel_api_token"])

list_of_items_scrap: list = []


# get data
if mocking:
    data_obj = Mocking.mock_userdata()
    data_json_path = mock_data_json_path
    FileServices.save_json_overwrite(json_data=data_obj, file_path=data_json_path)
else:
    if os.path.isfile(data_json_path):
        data_obj = FileServices.read_json(data_json_path)
    else:
        data_obj = Data.Data(users={}, groups={})
        FileServices.save_json_overwrite(json_data=data_obj, file_path=data_json_path)



@bot.message_handler(commands=["startBot"])
def echo_msg(msg: message):
    echo = bot.send_message(chat_id=msg.chat.id, text='Not implemented yet')

@bot.message_handler(commands=['define', 'Define'])
def echo_msg(msg: message):
    echo = bot.send_message(chat_id=msg.chat.id,
                            text='This is a dummy function. It will add an input into a list. \n '
                                 'What would you like to add?')
    bot.register_next_step_handler(message=echo, callback=extract_msg)

def extract_msg(msg: message):
    list_of_items_scrap.append(msg.text)
    print(list_of_items_scrap)

@bot.message_handler(commands=['printList'])
def print_list(msg: message):
    bot.send_message(chat_id=msg.chat.id,
                     text=str(list_of_items_scrap))

@bot.message_handler(commands=['printMessage'])  # Prints the content of the sent message
def print_message(msg: message):
    bot.send_message(chat_id=msg.chat.id, text=str(msg))

@bot.message_handler(commands=['printUserId'])  # prints the userId
def print_user_id(msg: message):
    bot.send_message(chat_id=msg.chat.id, text=str(get_sender_id(msg)))

@bot.message_handler(commands=['register'])
def register(msg: message):
    # data_dict = FileServices.read_json(data_json_path)
    print(msg)
    if get_sender_id(msg) in data_obj.users.keys():  # User already registered
        bot.send_message(msg.from_user.id, Strings.Registration.already_registered)
        return
    else:
        try:
            echo = bot.send_message(msg.from_user.id, Strings.Registration.welcome_text)
            bot.register_next_step_handler(message=echo, callback=register_user, group_chat_id=msg.chat.id)
        except:
            bot.send_message(msg.chat.id, Strings.Registration.first_need_to_open_chat)

def register_user(msg: message, group_chat_id: int):
    # data_dict = FileServices.read_json(data_json_path)
    uid = get_sender_id(msg)
    new_user: User = User(uid=uid, calling_name=msg.text)
    data_obj.users[uid] = new_user
    bot.send_message(msg.chat.id, registration_succesfull_private(new_user.get_callname()))

    bot.send_message(group_chat_id, registration_succesfull_group(new_user.get_callname()))
    print(data_obj.users)

def main_loop():
    bot.polling(none_stop=True)
    while True:
        time.sleep(1)


if __name__ == '__main__':
    try:
        print('starting main loop')
        main_loop()
    except KeyboardInterrupt:
        print(sys.stderr, '\nExiting by user request\n')
        sys.exit(0)
