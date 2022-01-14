import dataclasses
from typing import Set, Dict, List

from models.Activity import Activity
from models.HabitEntry import HabitEntry
from models.User import GroupUserAccount


@dataclasses.dataclass
class Group:
    group_id: str
    active_users: Set[str]
    all_users: Set[str]
    user_accounts: Dict[str, GroupUserAccount]
    habit_tracking: List[HabitEntry]
    group_name: str
    money_pool: int = 0

    def __init__(self, group_id: str, group_name: str):
        self.group_name = group_name
        self.group_id = group_id
        self.active_users = set()
        self.all_users = set()
        self.user_accounts = dict()
        self.habit_tracking = list()
        self.money_pool = 0

    def add_habit_entry(self, new_habit_entry: HabitEntry) -> bool:
        # check if the user already submitted the activity on the same day.
        # 1. get all the habits of the selected activity
        # 2. check if they are on a different day.
        invalid:bool = False
        new_activity: Activity = new_habit_entry.activity
        new_date = new_habit_entry.date
        for habit_entry in self.habit_tracking:
            if habit_entry.activity == new_activity:
                if habit_entry.get_date() != new_habit_entry.get_date():
                    self.habit_tracking.append(new_habit_entry)
                    return True
        return False

    def add_user_account_active(self, new_user: GroupUserAccount):
        if new_user.user_id not in self.user_accounts.keys():
            self.user_accounts[new_user.user_id] = new_user
            self.all_users.add(new_user.user_id)
        self.active_users.add(
            new_user.user_id)  # outside of if-scope so that adding a already existing user: the user will be set to active.
