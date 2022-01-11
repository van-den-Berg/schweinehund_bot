# -*- coding: utf-8 -*-
import json
import os.path
from typing import List

import telebot  # importing pyTelegramBotAPI library
import time
import sys

# import telegram_send
from lib.Strings import registration_succesfull_group, registration_succesfull_private
from models.Data import Data, Group, GroupUserAccount
from services import FileServices
from telegram import message
from models.User import User
from services.MessageServices import get_sender_id
from lib import Strings
from testing import Mocking

config_json_path: str = 'config.json'
data_json_path: str
group_whitelist_path: str

with open(config_json_path) as rf:
    config_dict = json.load(rf)

bot = telebot.TeleBot(token=config_dict["tel_api_token"])
mocking: bool = bool(config_dict["mocking"])
data_json_path = config_dict["mock_data_json_path"] if mocking else config_dict["data_json_path"]
group_whitelist_path = config_dict["group_whitelist_path"]

group_whitelist: List[str] = FileServices.read_group_whitelist(group_whitelist_path)

# get data
if mocking:  # create new instance of mocked data, overwrite the old one.
    data_obj = Mocking.mock_userdata(data_json_path)
    FileServices.save_json_overwrite(json_data=data_obj, file_path=data_json_path)

else:
    if os.path.isfile(data_json_path):
        data_obj = FileServices.read_json(data_json_path)
    else:
        print(Strings.init_no_data_at_location(data_json_path))
        data_obj = Data(users={}, groups={})
        FileServices.save_json_overwrite(json_data=data_obj, file_path=data_json_path)


@bot.message_handler(commands=['echo'])  # Prints the content of the sent message
def print_message(msg: message):
    bot.send_message(chat_id=msg.chat.id, text=str(msg))


@bot.message_handler(commands=['printUserId'])  # prints the userId
def print_user_id(msg: message):
    bot.send_message(chat_id=msg.chat.id, text=str(get_sender_id(msg)))


@bot.message_handler(commands=['join'])
def join(msg: message):
    # TODO: es meckert, da: "shadows name from outer scope".
    #  =>>> in unserem Fall ist das meine ich egal. wir müssen halt aufpassen wenn wir dinge umbenennen,
    #  dass wir das im local namespace machen, aber denke nicht, das wir data_obj nochmal umbenennen und
    #  selbst wenn wäre es kein Problem weil es überall das gleiche Objekt ist (es sagt immer das gleiche aus).
    #  Aber hast schon recht, schön ist das nicht. Am Liebsten würde ich eine Klasse machen und das als Objektvariable haben,
    #  aber hab das mit den @bot... decorators nicht hinbekommen (hab gestern ne Stunde probiert und dann zurück gedreht).
    #  ich kann bei Gelegenheit nochmal Niklas fragen was
    #  da der Trick ist, wahrscheinlich müsste die dann von telegram erben oderso.
    data_obj: Data = FileServices.read_json(data_json_path)
    # print(msg)
    print("user {} wants to join a group.".format(msg.from_user.id))

    # Since the User will choose a new name for every group he is joining, it is one single controlflow.
    # Not possible to make these distinctions.
    if get_sender_id(msg) in data_obj.users.keys():  # User already registered in the system, wants to join a group
        bot.send_message(msg.from_user.id, Strings.Registration.already_registered)
        return
    else:
        try:  # testing if user already opened chat with the bot
            echo = bot.send_message(msg.from_user.id, Strings.Registration.welcome_text)
            bot.register_next_step_handler(message=echo, callback=register_user_and_join_group, group_chat_id=str(msg.chat.id))
        except:
            bot.send_message(msg.chat.id, Strings.Registration.first_need_to_open_chat)


# DEPRECATED
def join_new_group(msg: message, group_chat_id: str) -> Data:
    data_obj: Data = FileServices.read_json(data_json_path)
    if group_chat_id not in group_whitelist:
        # print(group_chat_id, group_whitelist)
        bot.send_message(msg.from_user.id, Strings.group_not_allowed(group_chat_id))
        return data_obj
    if group_chat_id not in data_obj.groups.keys():
        group_user = GroupUserAccount(id=msg.from_user.id, calling_name=msg.text)
        data_obj.add_group(
            Group(group_id=group_chat_id, active_users={str(msg.from_user.id)}, all_users={str(msg.from_user.id)},
                  user_accounts={str(msg.from_user.id): group_user}, habit_tracking=[]))
        data_obj.user_join_group(user_id=str(msg.from_user.id), group_id=str(group_chat_id), chosen_username=msg.text)
        FileServices.save_json_overwrite(json_data=data_obj, file_path=data_json_path)
        return data_obj
    else:
        data_obj.user_join_group(user_id=str(msg.from_user.id), group_id=str(group_chat_id), chosen_username=msg.text)
        FileServices.save_json_overwrite(json_data=data_obj, file_path=data_json_path)
        return data_obj


def register_user_and_join_group(msg: message, group_chat_id: str):
    data_obj: Data = FileServices.read_json(data_json_path)
    uid: str = get_sender_id(msg)
    if uid not in data_obj.users.keys():  # First time, a user joining a group, a new user-profile has to be created.
        new_user: User = User(id=uid,
                              username=msg.from_user.username,
                              private_chat_id=msg.chat.id, active_groups={group_chat_id})
        data_obj.add_user(new_user)
    data_obj.user_join_group(user_id=uid, group_id=group_chat_id,
                             chosen_username=msg.text)  # user is joining the group with given username for this specific group
    FileServices.save_json_overwrite(json_data=data_obj, file_path=data_json_path)
    bot.send_message(msg.chat.id, registration_succesfull_private(msg.text))
    bot.send_message(group_chat_id, registration_succesfull_group(msg.text))
    print(data_obj)


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
