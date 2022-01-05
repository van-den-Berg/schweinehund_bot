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
