from telegram import message


def get_sender_id(my_message: message) -> int:
    return my_message.from_user.id


def get_sender_information(my_message: message):
    return my_message.from_user
