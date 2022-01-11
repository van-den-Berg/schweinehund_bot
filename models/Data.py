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
        self.users[new_user.id] = new_user

    ## TODO: read this
    # I don't think we need this one can just use data_object.users[user_id]
    # def get_user(self, user_id: str) -> User:
    #    return self.users[user_id]

    def remove_user(self, user_id: str):
        self.users.pop(user_id)

    def add_habit_entry(self, new_habit_entry: HabitEntry):
        for group_id in self.users[new_habit_entry.user_id].active_groups:
            self.groups[group_id].add_habit_entry(new_habit_entry)

    # TODO: needs testing
    def add_group(self, new_group: Group):
        if new_group.group_id in self.groups.keys():
            # TODO: throw error: "group already exists"
            # I think a print should suffice, otherwise the whole bot stops.
            print(f"The group with id {new_group.group_id} does already exist. It wasn't changed.")
        else:
            self.groups[new_group.group_id] = new_group
            for user_id in new_group.all_users:
                self.users[user_id].active_groups.add(new_group.group_id)

    # TODO: Read this
    # I don't think we need this, see above
    # def get_group(self, group_id: str) -> Group.py:
    #    return self.groups[group_id]

    # TODO: need testing
    # returning True if succeeded
    def user_join_group(self, user_id: str, group_id: str, chosen_username: str) -> bool:
        if (user_id in self.users.keys()) and (group_id in self.groups.keys()):
            user: User = self.users[user_id]
            group_user_account: GroupUserAccount = GroupUserAccount(id=user_id, calling_name=chosen_username)
            self.groups[group_id].add_user_account_active(group_user_account)
            self.users[user_id].active_groups.add(group_id)
            return True
        return False
