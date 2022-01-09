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

    def add_habit_entry(self, new_habit_entry: HabitEntry):
        self.habit_tracking.append(new_habit_entry)

