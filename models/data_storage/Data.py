import dataclasses

from typing import List, Dict, Set

from models.Activity import Activity


@dataclasses.dataclass
class HabitEntry:
    user_id: str
    activity: Activity
    date: str  # isoformated datetime. has to be a string in order to be serializable for JSON


@dataclasses.dataclass
class GroupUserAccount:
    userid: str
    username: str
    current_points: int = 0
    balance: int = 0


@dataclasses.dataclass
class Group:
    group_id: str
    active_users: Set[str]
    all_users: Set[str]
    user_accounts: Dict[str:GroupUserAccount]
    habit_tracking: List[HabitEntry]
    money_pool: int = 0

    def add_habit_entry(self, new_habit_entry: HabitEntry):
        self.habit_tracking.append(new_habit_entry)


@dataclasses.dataclass
class User:
    user_id: str
    tel_username: str
    private_chat_id: str
    active_groups: List[str]


@dataclasses.dataclass
class Data:
    users: Dict[str, User]
    groups: Dict[str, Group]

    def add_user(self, new_user: User):
        self.users[new_user.user_id] = new_user

    ## TODO: read this
    # I don't think we need this one can just use data_object.users[user_id]
    #def get_user(self, user_id: str) -> User:
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
                self.users[user_id].active_groups.append(new_group.group_id)

    # TODO: Read this
    # I don't think we need this, see above
    #def get_group(self, group_id: str) -> Group:
    #    return self.groups[group_id]

    # TODO: need testing
    # returning True if succeeded
    def user_join_group(self, user_id: str, group_id: str) -> bool:

        if (user_id in self.users.keys()) and (group_id in self.groups.keys()):
            self.groups[group_id].all_users.add(user_id)
            self.groups[group_id].active_users.add(user_id)
            self.users[user_id].active_groups.append(group_id)
            return True
        return False
