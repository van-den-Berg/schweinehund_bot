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


# Returns True if the msg type is group. Else: return False.
# sends an error to the group chat if flag is True.
def is_group_message(msg: message, bot: TeleBot, throw_error_message: bool = False) -> bool:
    ret = (msg.chat.type == 'group') or (msg.chat.type == 'supergroup')
    if ret:
        print("- message is a GroupMessage.")
    else:
        print("- Message is NOT a GroupMessage.")
        if throw_error_message: bot.send_message(msg.chat.id, Strings.Errors.this_command_only_in_groups)
    return ret


# Returns True if the msg type is private. Else: return False.
# sends an error to the group chat if flag is True.
def is_private_message(msg: message, bot: TeleBot, throw_error_message: bool = False) -> bool:
    ret = msg.chat.type == 'private'
    if ret:
        print("- message is a PrivateMessage.")
    else:
        print("- Message is NOT a PrivateMessage.")
        if throw_error_message: bot.send_message(msg.chat.id, Strings.Errors.this_command_only_in_private_chat)
    return ret


def group_is_whitelisted(msg: message, whitelist, bot: TeleBot, throw_error_message: bool = False) -> bool:
    group_id: str = get_group_id(msg)
    ret = group_id in whitelist
    if ret:
        print(f"- Group {group_id} is Whitelisted.")
    else:
        print(f"- Group {group_id} is NOT Whitelisted.")
        if throw_error_message: bot.send_message(group_id, Strings.Registration.GroupRegistration.group_not_allowed(msg.chat.id))
    return ret


def group_is_registered(msg: message, data_obj: Data, bot: TeleBot, throw_error_message: bool = False) -> bool:
    group_id = get_group_id(msg)
    ret = group_id in data_obj.groups
    if ret:
        print(f"- Group {group_id} is registered.")
    else:
        print(f"- Group {group_id} is not registered.")
        if throw_error_message: bot.send_message(group_id, Strings.Errors.group_not_registered)
    return ret


# Returns true if the message meets this specs:
# - is_group_message
# - group_is_whitelisted
# - group_is_registered
def is_valid_group_message(my_message: message, whitelist, data_obj: Data, bot: TeleBot, throw_error_message: bool = False) -> bool:
    ret = is_group_message(my_message, bot, throw_error_message)
    if ret:
        ret = group_is_whitelisted(my_message, whitelist, bot, True)
        if ret:
               ret = group_is_registered(my_message, data_obj, bot, True)
    print("- Message is a valid groupMessage.") if ret else print("- Message is NOT a valid GroupMessage.")
    return ret
