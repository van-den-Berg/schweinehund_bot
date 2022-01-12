# -*- coding: utf-8 -*-
import json
import os.path
from typing import List

import telebot  # importing pyTelegramBotAPI library
import time
import sys

# import telegram_send
from lib.Strings import registration_succesfull_group, registration_succesfull_private
from models.Activity import Activity
from models.Data import Data, Group, GroupUserAccount
from models.HabitEntry import HabitEntry
from services import FileServices, MessageServices
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

if not os.path.exists(data_json_path):
    x = open(data_json_path, 'a')
    x.write("{}")
    x.close()
    print(Strings.init_no_data_at_location(data_json_path))
    data_obj = Data(users={}, groups={})
    FileServices.save_json_overwrite(json_data=data_obj, file_path=data_json_path)
if not os.path.exists(group_whitelist_path):
    open(group_whitelist_path, 'a').close()
group_whitelist: List[str] = FileServices.read_group_whitelist(group_whitelist_path)
print(group_whitelist)

# get data
if mocking:  # create new instance of mocked data, overwrite the old one.
    # data_obj = Mocking.mock_userdata(data_json_path)
    # FileServices.save_json_overwrite(json_data=data_obj, file_path=data_json_path)

    if os.path.isfile(data_json_path):
        data_obj = FileServices.read_json(data_json_path)
    else:
        print(Strings.init_no_data_at_location(data_json_path))
        data_obj = Data(users={}, groups={})
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
    print("[/print]")
    bot.send_message(chat_id=msg.chat.id, text=str(msg))


@bot.message_handler(commands=['printUserId'])  # prints the userId
def print_user_id(msg: message):
    print("[/printUserId]")
    bot.send_message(chat_id=msg.chat.id, text=str(get_sender_id(msg)))


@bot.message_handler(commands=['registerGroup'])
def register_group(msg: message):
    group_id: str = str(msg.chat.id)
    print("[/registerGroup] Group {} wants to register. Whitelisted Groups are: {}".format(group_id, group_whitelist))
    if group_id in group_whitelist:
        print("- Group {} is on Whitelist.".format(group_id))
        if group_id not in data_obj.groups.keys():
            print("-- not already registered.")
            data_obj.add_group(Group(group_id))
            bot.send_message(group_id, Strings.Registration.GroupRegistration.welcome_text)
            FileServices.save_json_overwrite(data_obj, data_json_path)
            print("--- Group {} successfully registered for habit tracking.\n")
        else:
            print("-- Group {} is already registered.".format(group_id))
            bot.send_message(group_id, Strings.Registration.GroupRegistration.already_registered)
    else:
        print("- Group is not on Whitelist")
        bot.send_message(group_id, Strings.Registration.GroupRegistration.group_not_allowed(msg.chat.id))
    print("finish [/registerGroup]")


@bot.message_handler(commands=['join'])
def join(msg: message):
    print("[/join]")
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
    if not MessageServices.is_valid_group_message(msg, group_whitelist, data_obj, bot): return
    print("user {} wants to join a group.".format(msg.from_user.id))

    # this command is only appliciable if send in a group chat.
    if msg.chat.type != "group":
        bot.send_message(msg.chat.id, Strings.Errors.this_command_only_in_groups)

    # check if the group it is sent from is on whitelist
    group_chat_id: str = str(msg.chat.id)
    if group_chat_id not in group_whitelist:
        # print(group_chat_id, group_whitelist)
        bot.send_message(msg.chat.id, Strings.Errors.group_not_allowed(group_chat_id))
        return data_obj

    # Since the User will choose a new name for every group he is joining, it is one single controlflow.
    if get_sender_id(msg) in data_obj.users.keys():  # User already registered in the system, wants to join a group
        bot.send_message(msg.from_user.id, Strings.Registration.already_registered)
        return
    else:
        try:  # testing if user already opened chat with the bot
            echo = bot.send_message(msg.from_user.id, Strings.Registration.welcome_text)
            bot.register_next_step_handler(message=echo, callback=register_user_and_join_group,
                                           group_chat_id=str(msg.chat.id))
        except:
            bot.send_message(msg.chat.id, Strings.Registration.first_need_to_open_chat)


def register_user_and_join_group(msg: message, group_chat_id: str):
    data_obj: Data = FileServices.read_json(data_json_path)
    uid: str = get_sender_id(msg)
    if uid not in data_obj.users.keys():  # First time, a user joining a group, a new user-profile has to be created.
        new_user: User = User(user_id=uid,
                              username=msg.from_user.username,
                              private_chat_id=msg.chat.id, active_groups={group_chat_id})
        data_obj.add_user(new_user)
    data_obj.user_join_group(user_id=uid, group_id=group_chat_id,
                             chosen_username=msg.text)  # user is joining the group with given username for this specific group
    FileServices.save_json_overwrite(json_data=data_obj, file_path=data_json_path)
    bot.send_message(msg.chat.id, registration_succesfull_private(msg.text))
    bot.send_message(group_chat_id, registration_succesfull_group(msg.text))
    print(data_obj)


@bot.message_handler(commands=['sport'])
def add_habit_entry_sport(msg: message):
    print("[/sport]")
    user_id = str(msg.from_user.id)
    chatType = str(msg.chat.type)
    group_id = str(msg.chat.id)

    # check if user has a user account
    # if user_id not in data_obj.users:
    #    bot.send_message()

    # if send in group: add to group
    # check if group is existent and user is in group
    if chatType == 'group':
        if group_id in data_obj.groups and user_id in data_obj.users:
            data_obj.add_habit_entry(HabitEntry(user_id=user_id, activity=Activity.SPORT))
            FileServices.save_json_overwrite(data_obj, data_json_path)
            print("---saved entry")

    # if send in private chat: add to all groups that are active in user account
    # check if user is in group


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
