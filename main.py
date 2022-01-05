# -*- coding: utf-8 -*-
from enum import Enum
from datetime import date
import json
import telebot  # importing pyTelegramBotAPI library
import time
import sys
import json

# import telegram_send
from lib.Strings import registration_succesfull_group, registration_succesfull_private
from models.Activity import Activity
from services import FileServices
from telegram import message
from models.User import User
from services.MessageServices import get_sender_id
from lib import Strings

configJson = FileServices.read_json('config.json')

bot = telebot.TeleBot(
    token=configJson["tel_api_token"])  # supply your future bot with the token you have received
list_of_items_scrap: list = []
users: dict[int, User] = {-1: User(uid=-1, calling_name="dummy")}


@bot.message_handler(commands=['define', 'Define'])
def echo_msg(msg: message):
    echo = bot.send_message(chat_id=msg.chat.id,
                            text='What word would you want me to save, sir?')
    bot.register_next_step_handler(message=echo, callback=extract_msg)


def extract_msg(msg: message):
    list_of_items_scrap.append(msg.text)
    print(list_of_items_scrap)


@bot.message_handler(commands=['print'])
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
    if users is not None and get_sender_id(msg) in users:
        bot.send_message(msg.from_user.id, Strings.Registration.already_registered)
        return
    else:
        try:
            echo = bot.send_message(msg.from_user.id, Strings.Registration.welcome_text)
            bot.register_next_step_handler(message=echo, callback=register_user, group_chat_id=msg.chat.id)
        except:
            bot.send_message(msg.chat.id, Strings.Registration.first_need_to_open_chat)


def register_user(msg: message, group_chat_id: int):
    uid = get_sender_id(msg)
    new_user: User = User(uid=uid, calling_name=msg.text)
    users[uid] = new_user
    bot.send_message(msg.chat.id, registration_succesfull_private(new_user.get_callname()))
    bot.send_message(group_chat_id, registration_succesfull_group(new_user.get_callname()))
    print(str(users))


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
