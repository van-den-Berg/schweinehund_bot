# -*- coding: utf-8 -*-
import json
import os.path
from typing import List

import telebot  # importing pyTelegramBotAPI library
import time
import sys
import datetime

# import telegram_send
import models.HabitEntry
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
    # the file should also be created with save_json_overwrite.
    # with open(data_json_path, 'a') as x:
    #    x.write("{}")
    print(Strings.init_no_data_at_location(data_json_path))
    data_obj = Data(users={}, groups={})
    FileServices.save_json_overwrite(json_data=data_obj, file_path=data_json_path)
    print("initializing data file, because the directory was empty.")
if not os.path.exists(group_whitelist_path):
    with open(group_whitelist_path, 'w') as x:
        x.write('')
        print("initializing whitelist file, because the directory was empty.")
group_whitelist: List[str] = FileServices.read_group_whitelist(group_whitelist_path)
print(group_whitelist)

if mocking:  # create new instance of mocked data, overwrite the old one.
    data_obj = Mocking.mock_userdata(data_json_path)
    FileServices.save_json_overwrite(json_data=data_obj, file_path=data_json_path)

# get data object, create if not existing.
if os.path.isfile(data_json_path):
    data_obj = FileServices.read_json(data_json_path)
else:
    print(Strings.init_no_data_at_location(data_json_path))
    data_obj = Data(users={}, groups={})
    FileServices.save_json_overwrite(json_data=data_obj, file_path=data_json_path)


@bot.message_handler(commands=['echo'])  # Prints the content of the sent message
def print_message(msg: message):
    print("[/echo]")
    bot.send_message(chat_id=msg.chat.id, text=str(msg))


@bot.message_handler(commands=['printUserId'])  # prints the userId
def print_user_id(msg: message):
    print("[/printUserId]")
    bot.send_message(chat_id=msg.chat.id, text=str(get_sender_id(msg)))


@bot.message_handler(commands=['printData'])  # prints the data_obj
def print_data(msg: message):
    print("[/printData]")
    data_obj = FileServices.read_json(data_json_path)
    bot.send_message(msg.chat.id, FileServices.data_to_str(data_obj))


@bot.message_handler(commands=['registerGroup'])
def register_group(msg: message):
    group_id: str = str(msg.chat.id)
    print(f"[/registerGroup] Group {group_id} wants to register. Whitelisted Groups are: {group_whitelist}")
    if MessageServices.is_group_message(msg, bot, throw_error_message=True):
        if MessageServices.group_is_whitelisted(msg, group_whitelist, bot, throw_error_message=True):
            if not MessageServices.group_is_registered(msg, data_obj, bot, False):
                print("-- not already registered.")
                group_name = msg.chat.title
                data_obj.add_group(Group(group_id, group_name))
                bot.send_message(group_id, Strings.Registration.GroupRegistration.welcome_text)
                FileServices.save_json_overwrite(data_obj, data_json_path)
                print(f"--- Group {group_id} successfully registered for habit tracking.\n")
            else:
                print(f"-- Group {group_id} is already registered.")
                bot.send_message(group_id, Strings.Registration.GroupRegistration.already_registered)
    print("finish [/registerGroup]")


@bot.message_handler(commands=['join'])
def join(msg: message):
    print("[/join]")
    #  es meckert, da: "shadows name from outer scope".
    #  =>>> in unserem Fall ist das meine ich egal. wir müssen halt aufpassen, wenn wir dinge umbenennen,
    #  dass wir das im local namespace machen, aber denke nicht, das wir data_obj nochmal umbenennen und
    #  selbst wenn wäre es kein Problem, weil es überall das gleiche Objekt ist (es sagt immer das gleiche aus).
    #  Aber hast schon Recht, schön ist das nicht. Am Liebsten würde ich eine Klasse machen und das als Objektvariable haben,
    #  aber hab das mit den @bot... decorators nicht hinbekommen (hab gestern ne Stunde probiert und dann zurück gedreht).

    data_obj: Data = FileServices.read_json(data_json_path)
    # print(msg)

    if not MessageServices.is_valid_group_message(msg, group_whitelist, data_obj, bot, True):
        return
    print(f"user {msg.from_user.id} wants to join a group.")

    # TODO: Update the deprecated checks for the implemented methods in MessageHandler
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


# TODO: setze einen Nutzer auf "pausiert" (entferne ihn von entsprechenden active-listen)
# TODO: implement function
# Distinction between group chat and private chat:
# if sent in private chat with the bot, stall all active groups the user has.
# if sent in a active group: stall the user for only this particular group.
# Possible further improvements: Ask the user interactively with buttons which groups he wants to stall in private chat.
@bot.message_handler(commands=['urlaub'])
def pause_active_member(msg: message):
    print("[/urlaub]")
    data_obj: Data = FileServices.read_json(data_json_path)

    user_id = MessageServices.get_sender_id(msg)
    if not data_obj.is_user(user_id):
        bot.send_message(msg.chat.id, Strings.Errors.user_not_registered_at_all)
        return
    priv_chat_id = data_obj.users[user_id].private_chat_id
    chatType = str(msg.chat.type)
    group_id = str(msg.chat.id)

    # if sent in private chat with the bot, stall all active groups the user has.
    if MessageServices.is_private_message(msg, bot, False):
        check: bool = data_obj.user_pause_all_groups(user_id)
        if check:
            print(f"-- Pause wurde eingetragen.")
            FileServices.save_json_overwrite(data_obj, data_json_path)
            bot.send_message(priv_chat_id, Strings.GroupManagement.paused_groups_successful)
        else:
            print(f"-- Pause konnte nicht eingetragen werden.")
        return

    # if sent in an active group: stall the user for only this particular group.
    if MessageServices.is_valid_group_message(msg, group_whitelist, data_obj, bot, False):
        print(f"- User {user_id} möchte in Gruppe {group_id} eine Pause einlegen.")
        check: bool = data_obj.user_pause_group(user_id, group_id)
        if check:
            FileServices.save_json_overwrite(data_obj, data_json_path)
            print(f"-- Pause wurde eingetragen.")
            bot.send_message(priv_chat_id, Strings.GroupManagement.paused_single_group_successful(msg.chat.title))
        else:
            print(f"-- Pause konnte nicht eingetragen werden.")
        return
    print(f"-- Pause konnte nicht eingetragen werden, da die Message keinem ChatTypen zugeordnet werden konnte.")

    # TODO: implement Error handling for logging messages permanently that the bot didnt know what to do with.


# TODO: use a better command text.
# TODO: implement function
# reactivate stalled groups.
# if sent in private chat: reactivate all groups the user has stalled at the moment.
# if sent in active group chat: reactivate the user in that group if the user stalled the group.
# Possible further impovements: Ask the user interactively with buttons which groups he wants to rejoin in private chat.
@bot.message_handler(commands=['weiter'])
def reactivate_inactive_member(msg: message):
    data_obj: Data = FileServices.read_json(data_json_path)
    user_id = MessageServices.get_sender_id(msg)
    priv_chat_id = data_obj.users[user_id].private_chat_id
    chatType = str(msg.chat.type)
    group_id = str(msg.chat.id)

    if MessageServices.is_private_message(msg, bot, False):
        check: bool = data_obj.user_activate_all_passive_groups(user_id)
        if check:
            FileServices.save_json_overwrite(data_obj, data_json_path)
            print(f"-- erfolgreich alle Gruppen reaktiviert.")
            bot.send_message(priv_chat_id, Strings.GroupManagement.reactivated_groups_successful)
            return
        else:
            print(f"-- Für user {user_id} konnte keine Gruppe voll reaktiviert werden.")
            return
    if MessageServices.is_valid_group_message(msg, group_whitelist, data_obj, bot, False):
        check: bool = data_obj.user_reactivate_single_group(user_id, group_id)
        if check:
            FileServices.save_json_overwrite(data_obj, data_json_path)
            print(f"-- erfolgreich in Gruppe {group_id} reaktiviert.")
            bot.send_message(priv_chat_id,
                             Strings.GroupManagement.reactivated_single_group_successful(group_name=msg.chat.title))
            return
        else:
            print(f"-- Für user {user_id} konnte Gruppe {group_id} nicht reaktiviert werden.")
            return
    bot.send_message(priv_chat_id, "Das hat leider nicht funktioniert.")


# TODO: implement functionality to delete a message sent by a user.


# IMPORTANT: THIS MESSAGE NEEDS TO BE THE LAST MESSAGE THAT HAS A BOT TRIGGER!
# This function triggers on every text message the bot receives. It handles the activity reports submitted by the
# users. It has to be assured that the function uses minimal computing time when no keyword is being detected.
@bot.message_handler(content_types=['text'])  # reacts to all text messages.
def scan_messages_for_habit_submissions(msg: message):
    # check if there is a Habbit in the msg
    msg_text = str(msg.text).lower()
    yesterday_flag: bool = "gestern" in msg_text
    today_flag: bool = "heute" in msg_text

    if yesterday_flag and today_flag:
        print(f"[message] in group {msg.chat.id}: {msg_text}")
        print(f"-- detected both 'gestern' and 'heute' in the message. This is an unhandled case and nothing will be saved. An error message will be thrown.")
        bot.send_message(msg.chat.id, Strings.HabitStrings.yesterday_and_today_in_message_error)
        return
    if yesterday_flag: print(f"-- keyword 'gestern' detected. Saving Habits for the last day.")
    if "/sport" in msg_text:
        print("[/sport]")
        add_habit_entry(msg, Activity.SPORT, yesterday_flag)
    if "/produktiv" in msg_text:
        print("[/produktiv]")
        add_habit_entry(msg, Activity.PRODUCTIVE_BY_10, yesterday_flag)
    if "/medienfrei" in msg_text:
        print("[/medienfrei]")
        add_habit_entry(msg, Activity.NO_MEDIA_DURING_WORK, yesterday_flag)
    if "/rausgegangen" in msg_text:
        print("[/rausgegangen]")
        add_habit_entry(msg, Activity.WENT_OUTSIDE, yesterday_flag)
    if "/guterabend" in msg_text:
        print("[/guterabend]")
        add_habit_entry(msg, Activity.GOOD_EVENING, yesterday_flag)
    print(f"[message] in group {msg.chat.id}: {msg_text}")
    return


def add_habit_entry(msg: message, activity: Activity, yesterday_flag: bool = False):
    data_obj: Data = FileServices.read_json(data_json_path)
    user_id = MessageServices.get_sender_id(msg)
    priv_chat_id = data_obj.users[user_id].private_chat_id
    chatType = str(msg.chat.type)
    group_id = str(msg.chat.id)

    date = models.HabitEntry.get_today()
    day_string: str = "heute"

    if yesterday_flag:
        date = (date - datetime.timedelta(days=1)).isoformat()
        day_string = "gestern"

    # check if user has a user account
    if not data_obj.is_user(user_id):
        print(f"-- User {user_id} has no user Account.")
        bot.send_message(group_id, Strings.Errors.user_not_registered_at_all)
        return

    # if send in group: add to group
    # check if group is existent and user is in group
    # check if user is active in the group.
    if MessageServices.is_group_message(msg, bot):
        if group_id in data_obj.groups and user_id in data_obj.users:
            if user_id in data_obj.groups[group_id].active_users:
                success = data_obj.add_habit_entry(HabitEntry(user_id=user_id, activity=activity, date=date))
                if success:
                    FileServices.save_json_overwrite(data_obj, data_json_path)
                    print(f"--- saved {activity.name} entry for {day_string} in group {group_id}")
                    ret_str = Strings.HabitStrings.get_habit_response(activity=activity)
                    print(f"--- Return Message: {ret_str}")
                    bot.send_message(priv_chat_id, ret_str)
                    return
                else:
                    print(
                        f"--- Could not save activity {activity} in group {group_id}. Activity for {day_string} already present.")

                    bot.send_message(priv_chat_id, Strings.HabitStrings.activity_already_logged_for_today(activity,
                                                                                                      data_obj.groups[
                                                                                                          group_id]))

            elif user_id in data_obj.groups[group_id].all_users:
                print(f"--- User {user_id} is not active in this group {group_id}. But he was active some time ago.")
                bot.send_message(group_id, Strings.Errors.user_not_active_in_this_group)
                return
            else:
                print(f"--- User {user_id} has not joined the group {group_id} yet.")
                bot.send_message(group_id, Strings.Errors.user_not_in_this_group)
                return
        return

    # if send in private chat: add to all groups that are active in user account
    if MessageServices.is_private_message(msg, bot):
        group_ids = set()
        for group_id in data_obj.users[user_id].active_groups:
            tmp_bool = data_obj.groups[str(group_id)].add_habit_entry(HabitEntry(user_id, activity, date=date))
            if tmp_bool:
                group_ids.add(group_id)
                print(f"---saved entry for {day_string} in group {group_id}")

        if len(group_ids) > 0:
            FileServices.save_json_overwrite(data_obj, data_json_path)
            bot.send_message(priv_chat_id, Strings.HabitStrings.get_habit_response(activity=activity))
            #bot.send_message(priv_chat_id, Strings.HabitStrings.added_to_groups(activity=activity, group_ids=group_ids, groups=data_obj.groups))
        else:
            bot.send_message(priv_chat_id, Strings.HabitStrings.activity_already_logged_for_today_private(activity))
        return


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
