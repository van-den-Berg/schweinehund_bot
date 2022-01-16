import dataclasses
from typing import Set


@dataclasses.dataclass
class User:
    user_id: str  # user_id
    tel_username: str  # tel_username
    private_chat_id: str
    active_groups: Set[str]

    def __init__(self, user_id: str, username: str, private_chat_id: str, active_groups: Set[str] = None):
        if active_groups is None:
            active_groups = set()
        else:
            self.active_groups = active_groups
        self.user_id = user_id
        self.tel_username = username
        self.private_chat_id = private_chat_id

    def user_pause_group(self, group_id) -> bool:
        if group_id in self.active_groups:
            self.active_groups.remove(group_id)
            return True
        return False

@dataclasses.dataclass
class GroupUserAccount:
    user_id: str  # user_id
    chosen_name: str  # chosen_username
    current_points: int
    balance: int

    def __init__(self, user_id: str, chosen_name: str, current_points: int = 0, balance: int = 0):
        self.user_id = user_id
        self.chosen_name = chosen_name
        self.current_points = current_points
        self.balance = balance