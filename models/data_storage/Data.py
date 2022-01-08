import datetime

from typing import List, Dict, Set

from models.Activity import Activity


class HabitEntry(dict):
    def __init__(self, user_id: str, activity: Activity, input_date: datetime.date):
        super().__init__()
        dict.__setitem__(self, "user_id", user_id)
        dict.__setitem__(self, "activity", activity)
        dict.__setitem__(self, "date", input_date.isoformat())


class GroupUserAccount(dict):

    def __init__(self, userid: str, username: str, current_points: int = 0, balance: int = 0):
        super().__init__()
        dict.__setitem__(self, "username", username)
        dict.__setitem__(self, "current_points", current_points)
        dict.__setitem__(self, "balance", balance)


class Group(dict):
    group_id: str

    def __init__(self, group_id: str, active_users: Set[str] = [], all_users: Set[str] = [], money_pool: int = 0,
                 user_accounts: Dict[str, GroupUserAccount] = {}, habit_tracking: List[HabitEntry] = []):
        super().__init__()
        self.group_id = group_id
        dict.__setitem__(self, "active_users", active_users)
        dict.__setitem__(self, "all_users", all_users)
        dict.__setitem__(self, "money_pool", money_pool)  # the current amount of money in the pool in cents
        dict.__setitem__(self, "user_accounts", user_accounts)
        dict.__setitem__(self, "habit_tracking", habit_tracking)

    def add_habit_entry(self, new_habit_entry: HabitEntry):
        habits: List[HabitEntry] = dict.get(self, "habit_tracking")
        habits.append(new_habit_entry)
        #dict.__setitem__(self, "habit_tracking", habits)


class User(dict):
    user_id: str

    def __init__(self, user_id: str, tel_username: str, private_chat_id: str, active_groups: List[str] = {}):
        super().__init__()
        self.user_id = user_id
        dict.__setitem__(self, "tel_username", tel_username)
        dict.__setitem__(self, "private_chat_id", private_chat_id)
        dict.__setitem__(self, "active_groups", active_groups)


class Data(dict):
    def __init__(self, users: Dict[str, User] = {}, groups: Dict[str, Group] = {}):
        super().__init__()
        dict.__setitem__(self, "users", users)
        dict.__setitem__(self, "groups", groups)

    def add_user(self, new_user: User):
        user_list: Dict[str, User] = dict.get(self, "users")
        if new_user.user_id not in user_list.keys():
            user_list[new_user.user_id] = new_user
            #user_list.__setitem__(new_user.user_id, new_user)
        #dict.__setitem__(self, "users", user_list)

    # TODO: needs testing
    def get_user(self, user_id: str) -> User:
        return dict.get(self, "users").get(user_id)

    def remove_user(self, user_id: str):
        user_list: Dict[str, User] = dict.get(self, "users")
        user_list.pop(user_id)
        #dict.__setitem__(self, "users", user_id)

    def add_habit_entry(self, new_habit_entry: HabitEntry):
        users: Dict[str, User] = dict.get(self, "users")
        groups: Dict[str, Group] = dict.get(self, "groups")
        userid: str = new_habit_entry.get("user_id")
        active_groups: List[str] = users.get(userid).get("active_groups")
        for group_id in active_groups:
            groups.get(group_id).add_habit_entry(new_habit_entry)

    #TODO: needs testing
    def add_group(self, new_group: Group):
        new_group_id: str = new_group.group_id
        new_group_active_users: List[str] = new_group.get("active_users")
        users: Dict[str, User] = dict.get(self, "users")
        groups: Dict[str, Group] = dict.get(self, "groups")
        if new_group_id in groups:
            #TODO: throw error: "group already exists"
            print("not implemented yet. ")
        else:
            groups[new_group_id] = new_group
            for user_id in new_group_active_users:
                users.get(user_id).get("active_groups").append(new_group_id)

    #TODO: need testing
    def get_group(self, group_id:str) -> Group:
        return dict.get(self, "groups").get(group_id)

    #TODO: need testing
    # returning True if succeeded
    def user_join_group(self, user_id: str, group_id: str) -> bool:
        users: Dict[str, User] = dict.get(self, "users")
        groups: Dict[str, Group] = dict.get(self, "groups")
        if (user_id in users) and (group_id in groups):
            group: Group = groups.get(group_id)
            active_users: List[str] = group.get("active_users")
            all_users: List[str] = group.get("all_users")

            if not user_id in all_users: all_users.append(user_id)
            if not user_id in active_users: active_users.append(user_id)

            users.get(user_id).get("active_groups").append(group_id)
            return True
        return False