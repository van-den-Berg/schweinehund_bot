import dataclasses
from typing import Set


@dataclasses.dataclass
class User:
    user_id: str
    tel_username: str
    private_chat_id: str
    active_groups: Set[str]


@dataclasses.dataclass
class GroupUserAccount:
    userid: str
    username: str
    current_points: int = 0
    balance: int = 0
