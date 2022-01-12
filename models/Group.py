import dataclasses
from typing import Set, Dict, List

from models.HabitEntry import HabitEntry
from models.User import GroupUserAccount


@dataclasses.dataclass
class Group:
    group_id: str
    active_users: Set[str]
    all_users: Set[str]
    user_accounts: Dict[str, GroupUserAccount]
    habit_tracking: List[HabitEntry]
    money_pool: int = 0

    def __init__(self, group_id: str):
        self.group_id = group_id
        self.active_users = set()
        self.all_users = set()
        self.user_accounts = dict()
        self.habit_tracking = list()
        self.money_pool = 0

    def add_habit_entry(self, new_habit_entry: HabitEntry):
        self.habit_tracking.append(new_habit_entry)

    def add_user_account_active(self, new_user: GroupUserAccount):
        if new_user.user_id not in self.user_accounts.keys():
            self.user_accounts[new_user.user_id] = new_user
            self.all_users.add(new_user.user_id)
        self.active_users.add(new_user.user_id) #outside of if-scope so that adding a already existing user: the user will be set to active.