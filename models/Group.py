import dataclasses
from typing import Set, Dict, List

from models.Activity import Activity
from models.HabitEntry import HabitEntry
from models.User import GroupUserAccount


@dataclasses.dataclass
class Group:
    group_id: str
    group_name: str
    active_users: Set[str] = dataclasses.field(default_factory=set)
    all_users: Set[str] = dataclasses.field(default_factory=set)
    user_accounts: Dict[str, GroupUserAccount] = dataclasses.field(default_factory=dict)
    habit_tracking: List[HabitEntry] = dataclasses.field(default_factory=list)
    money_pool: int = 0

    def add_habit_entry(self, new_habit_entry: HabitEntry) -> bool:
        # check if the user already submitted the activity on the same day.
        if new_habit_entry in self.habit_tracking:
            return False
        self.habit_tracking.append(new_habit_entry)
        return True

    def add_user_account_active(self, new_user: GroupUserAccount):
        if new_user.user_id not in self.user_accounts.keys():
            self.user_accounts[new_user.user_id] = new_user
            self.all_users.add(new_user.user_id)
        self.active_users.add(new_user.user_id)  # outside of if-scope. so that adding an already existing user: the user will be set to active.
