# -*- coding: utf-8 -*-
from enum import Enum
from datetime import date
import json
import telebot  # importing pyTelegramBotAPI library
import time
import sys
import json

# import telegram_send


configFile = open('config.json', 'r')
configJson = json.load(configFile)
configFile.close()

bot = telebot.TeleBot(
    token=configJson["tel_api_token"])  # supply your future bot with the token you have received
msg: list = []
userData: dict = {}
dataset: dict = {}


class User:
    id: int
    username: str
    first_name: str
    last_name: str
    private_chat_id: int

    def __init__(self, id: int, username=None, first_name=None, last_name=None, private_chat_id=None):
        self.private_chat_id = private_chat_id
        self.id = id
        self.last_name = last_name
        self.first_name = first_name
        self.username = username

    def update_user(self, id: int = None, username=None, first_name=None,
                    last_name=None, private_chat_id=None):
        self.id = self.id if id is None else id
        self.username = self.username if username is None else username
        self.first_name = self.first_name if first_name is None else first_name
        self.last_name = self.last_name if last_name is None else last_name
        self.private_chat_id = self.private_chat_id if private_chat_id is None else private_chat_id


class Activity(Enum):
    SPORT = 1
    CHILL_EVENING = 2


class UserProgressData:
    user_id: int
    training_data: dict = {Activity.SPORT: [], Activity.CHILL_EVENING: []}

    def __init__(self, user_id: int, training_data=None):
        self.training_data = self.training_data if training_data is None else training_data
        self.user_id = user_id

    def add_activity_now(self, activity: Activity) -> bool:
        today = date.today()
        if today in self.training_data[activity]:
            self.training_data[activity].append(date.today())
            return True
        return False


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
