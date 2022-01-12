import dataclasses
from typing import Set


@dataclasses.dataclass
class User:
    user_id: str  # user_id
    username: str  # tel_username
    private_chat_id: str
    active_groups: Set[str]

    def __init__(self, user_id: str, username: str, private_chat_id: str, active_groups: Set[str] = None):
        if active_groups is None:
            active_groups = set()
        else:
            self.active_groups = active_groups
        self.user_id = user_id
        self.username = username
        self.private_chat_id = private_chat_id


@dataclasses.dataclass
class GroupUserAccount:
    user_id: str  # user_id
    calling_name: str  # chosen_username
    current_points: int
    balance: int

    def __init__(self, user_id: str, calling_name: str, current_points: int = 0, balance: int = 0):
        self.user_id = user_id
        self.calling_name = calling_name
        self.current_points = current_points
        self.balance = balance
