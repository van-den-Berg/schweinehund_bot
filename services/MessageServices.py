from telebot import TeleBot
from telegram import message

from lib import Strings
from models.Data import Data


def get_sender_id(my_message: message) -> str:
    return str(my_message.from_user.id)


def get_group_id(my_message: message) -> str:
    return str(my_message.chat.id)


def get_sender_information(my_message: message):
    return my_message.from_user


def is_group_message(msg: message, bot: TeleBot, throw_error_message: bool = False) -> bool:
    ret = msg.chat.type == 'group'
    if ret:
        print("- message is a GroupMessage.")
    elif throw_error_message:
        print("- Message is no GroupMessage.")
        bot.send_message(msg.chat.id, Strings.Errors.this_command_only_in_groups)
    return ret


def is_private_message(msg: message, bot: TeleBot, throw_error_message: bool = False) -> bool:
    ret = msg.chat.type == 'private'
    if ret:
        print("- message is a PrivateMessage.")
    elif throw_error_message:
        print("- Message is no PrivateMessage.")
        bot.send_message(msg.chat.id, Strings.Errors.this_command_only_in_private_chat)
    return ret


def group_is_whitelisted(msg: message, whitelist, bot: TeleBot) -> bool:
    group_id: str = get_group_id(msg)
    ret = group_id in whitelist
    if ret:
        print("- Group {} is Whitelisted.".format(group_id))
    else:
        print("- Group {} is NOT Whitelisted.".format(group_id))
        bot.send_message(group_id, Strings.Registration.GroupRegistration.group_not_allowed(msg.chat.id))
    return ret


def group_is_registered(msg: message, data_obj: Data, bot: TeleBot) -> bool:
    group_id = get_group_id(msg)
    ret = group_id in data_obj.groups
    if ret:
        print("- Group {} is registered.".format(group_id))
    else:
        print("- Group {} is not registered.".format(group_id))
        bot.send_message(group_id, Strings.Errors.group_not_registered)
    return ret


def is_valid_group_message(my_message: message, whitelist, data_obj: Data, bot: TeleBot) -> bool:
    ret = is_group_message(my_message, bot) and group_is_whitelisted(my_message, whitelist,
                                                                     bot) and group_is_registered(my_message, data_obj,
                                                                                                  bot)
    print("- Message is a valid groupMessage.") if ret else print("- Message is NOT a valid GroupMessage.")
    return ret
