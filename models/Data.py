import dataclasses

from typing import List, Dict, Set

from models.Activity import Activity
from models.Group import Group
from models.User import User, GroupUserAccount
from models.HabitEntry import HabitEntry


@dataclasses.dataclass
class Data:
    users: Dict[str, User]
    groups: Dict[str, Group]

    def add_user(self, new_user: User):
        self.users[new_user.user_id] = new_user

    def remove_user(self, user_id: str):
        self.users.pop(user_id)

    def is_user(self, user_id: str) -> bool:
        if user_id in self.users:
            return True
        return False

    def is_group(self, group_id: str) -> bool:
        if group_id in self.groups:
            return True
        return False

    def add_habit_entry(self, new_habit_entry: HabitEntry) -> bool:
        for group_id in self.users[new_habit_entry.user_id].active_groups:
            success: bool = self.groups[group_id].add_habit_entry(new_habit_entry)
            if success:
                print(
                    f"-Data_obj: user {new_habit_entry.user_id} added Habit entry {new_habit_entry.activity} to group {group_id}")
            return success
        return False

    # needs testing
    def add_group(self, new_group: Group):
        if new_group.group_id in self.groups.keys():
            print(f"The group with id {new_group.group_id} does already exist. It wasn't changed.")
        else:
            self.groups[new_group.group_id] = new_group
            for user_id in new_group.all_users:
                self.users[user_id].active_groups.add(new_group.group_id)

    # returning True if succeeded
    def user_join_group(self, user_id: str, group_id: str, chosen_username: str) -> bool:
        if (user_id in self.users.keys()) and (group_id in self.groups.keys()):
            user: User = self.users[user_id]
            group_user_account: GroupUserAccount = GroupUserAccount(user_id=user_id, chosen_name=chosen_username)
            self.groups[group_id].add_user_account_active(group_user_account)
            self.users[user_id].active_groups.add(group_id)
            return True
        return False

    def user_pause_group(self, user_id: str, group_id: str) -> bool:
        return self.users[user_id].user_pause_group(group_id) and self.groups[group_id].user_pause_group(user_id)

    def user_pause_all_groups(self, user_id: str) -> bool:
        check: bool = True
        for group_id in self.users[user_id].active_groups:
            check = self.groups[group_id].user_pause_group(user_id) and check
            check = self.users[user_id].user_pause_group(group_id) and check
        return check