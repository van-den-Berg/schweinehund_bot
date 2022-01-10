class Help:
    help_text = "this is a dummy text for the help section"
    avail_commands = "die folgenden Commands sind verfügbar: ..."


def registration_succesfull_private(name: str) -> str:
    return "Hallo und Willkommen " + name + ", wir freuen uns dass du hier bist!"


def registration_succesfull_group(name: str) -> str:
    return "Woop Woop! Begrüßt " + name + " im Team!!"


def group_not_allowed(group_id: str):
    return f"Diese Gruppe steht nicht auf der whitelist. Bitte kontaktiere die Administratoren. Die fehlende GruppenID ist {group_id}."


def init_no_data_at_location(path: str):
    return "There is no file at provided path \n " \
           "'data_json_path': '{}'. \n " \
           "A empty file for storing the data will be generated. \n " \
           "If there should be a file with valid data, please check the config.json".format(path)


class Registration:
    welcome_text = "Hey, schön dass du auch versuchst, deinen Arsch hoch zu bekommen! " \
                   "Damit alle wissen mit wem sie sich anlegen, fehlt noch dein Name. " \
                   "Mit diesem Namen wirst du in Zukunft von mir angesprochen und in Zusammenfassungen auftauchen. " \
                   "\n \n Wie darf ich dich nennen?"
    first_need_to_open_chat = "Damit du mitmachen kannst, musst du mich bei dir starten. " \
                              "Gehe dazu auf mein Profil und beginne einen Chat. " \
                              "Anschließend kannst du hierher zurückkommen und dich registrieren."
    already_registered = "Du bist bereits mit im Team!"
