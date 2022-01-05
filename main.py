# -*- coding: utf-8 -*-
from enum import Enum
from datetime import date
import json
import telebot  # importing pyTelegramBotAPI library
import time
import sys
import json

# import telegram_send
from models.Activity import Activity
from services.json_service import read_json
from models import User

configJson = read_json('config.json')

bot = telebot.TeleBot(
    token=configJson["tel_api_token"])  # supply your future bot with the token you have received
msg: list = []
userData: dict = {}
dataset: dict = {}


@bot.message_handler(commands=['define', 'Define'])
def echo_msg(message):
    echo = bot.send_message(chat_id=message.chat.id,
                            text='What word would you want me to extract, sir?')
    bot.register_next_step_handler(message=echo, callback=extract_msg)


def extract_msg(message):
    msg.append(message.text)
    print(msg)


@bot.message_handler(commands=['print'])
def print_list(message):
    bot.send_message(chat_id=message.chat.id,
                     text=str(msg))


@bot.message_handler(commands=['save'])
def save_to_json(message):
    bot.send_message(chat_id=message.chat.id, text=str(message))


# def add_user(user: User, chat_id):
#    user_doc: dict = {}
#    user_doc["chat_id"] = chat_id
#    user_doc["username"] =
#    dict[chat_id] = user_doc


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
