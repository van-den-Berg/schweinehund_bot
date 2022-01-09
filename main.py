# -*- coding: utf-8 -*-
import json
import os.path
from typing import List

import telebot  # importing pyTelegramBotAPI library
import time
import sys

# import telegram_send
from lib.Strings import registration_succesfull_group, registration_succesfull_private
from models.data_storage.Data import Data, Group, GroupUserAccount
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
group_whitelist_path: str = 'group_whitelist.csv'

with open(config_json_path) as rf:
    config_dict = json.load(rf)
bot = telebot.TeleBot(token=config_dict["tel_api_token"])

with open(group_whitelist_path) as rf:
    group_whitelist: List[int] = [int(i) for i in rf.read().replace(',', '').split()]

# get data
if mocking:
    data_obj = Mocking.mock_userdata()
    data_json_path = mock_data_json_path
    os.remove(data_json_path)
    FileServices.save_json_overwrite(json_data=data_obj, file_path=data_json_path)
else:
    if os.path.isfile(data_json_path):
        data_obj = FileServices.read_json(data_json_path)
    else:
        data_obj = Data(users={}, groups={})
        FileServices.save_json_overwrite(json_data=data_obj, file_path=data_json_path)


@bot.message_handler(commands=['echo'])  # Prints the content of the sent message
def print_message(msg: message):
    bot.send_message(chat_id=msg.chat.id, text=str(msg))


@bot.message_handler(commands=['printUserId'])  # prints the userId
def print_user_id(msg: message):
    bot.send_message(chat_id=msg.chat.id, text=str(get_sender_id(msg)))


@bot.message_handler(commands=['register'])
def register(msg: message):
    data_obj = FileServices.read_json(data_json_path)
    print(msg)
    if get_sender_id(msg) in data_obj.users.keys():  # User already registered
        if msg.from_user.id in data_obj.users[msg.from_user.id].active_groups:  # User already registered
            bot.send_message(msg.from_user.id, Strings.Registration.already_registered)
            return
        else:  # user wants to join new group
            data_obj = join_new_group(msg=msg, group_chat_id=msg.chat.id)

    else:  # User registers for the first time
        try:
            echo = bot.send_message(msg.from_user.id, Strings.Registration.welcome_text)
            bot.register_next_step_handler(message=echo, callback=register_user, group_chat_id=msg.chat.id)
        except:
            bot.send_message(msg.chat.id, Strings.Registration.first_need_to_open_chat)


def join_new_group(msg: message, group_chat_id: int) -> Data:
    data_obj: Data = FileServices.read_json(data_json_path)

    if group_chat_id not in group_whitelist:
        bot.send_message(msg.from_user.id, Strings.group_not_allowed(msg.chat.id))
        return data_obj

    if group_chat_id not in data_obj.groups.keys():
        group_user = GroupUserAccount(userid=msg.from_user.id, username=data_obj.users[msg.from_user.id].calling_name)

        data_obj.add_group(
            Group(group_id=group_chat_id, active_users=set(msg.from_user.id), all_users=set(msg.from_user.id),
                  user_accounts={msg.from_user.id: group_user}, habit_tracking=[]))
        data_obj.user_join_group(user_id=msg.from_user.id, group_id=group_chat_id)

        FileServices.save_json_overwrite(json_data=data_obj, file_path=data_json_path)
        return data_obj



def register_user(msg: message, group_chat_id: int) -> Data:
    data_obj: Data = FileServices.read_json(data_json_path)

    new_user: User = User(id=msg.from_user.id, calling_name=msg.text, first_name=msg.from_user.first_name,
                          last_name=msg.from_user.last_name, username=msg.from_user.username,
                          private_chat_id=msg.chat.id, active_groups={group_chat_id})
    data_obj.users[msg.from_user.id] = new_user

    data_obj.user_join_group(user_id=msg.from_user.id, group_id=group_chat_id)

    FileServices.save_json_overwrite(json_data=data_obj, file_path=data_json_path)

    bot.send_message(msg.chat.id, registration_succesfull_private(new_user.calling_name))

    bot.send_message(group_chat_id, registration_succesfull_group(new_user.calling_name))

    print(data_obj)
    return data_obj


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
