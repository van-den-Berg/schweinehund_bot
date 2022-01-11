import dataclasses
from typing import Set


@dataclasses.dataclass
class User:
    id: str #user_id
    username: str #tel_username
    private_chat_id: str
    active_groups: Set[str]


@dataclasses.dataclass
class GroupUserAccount:
    id: str #user_id
    calling_name: str #chosen_username
    current_points: int = 0
    balance: int = 0
