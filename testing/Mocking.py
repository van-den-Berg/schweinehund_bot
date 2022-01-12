import services.FileServices
from models import Data
from models.Activity import Activity
from models.Group import Group
from models.HabitEntry import HabitEntry
from models.User import User


def mock_userdata(data_path: str) -> Data:
    data_object = Data.Data(users={}, groups={})
    data_object.add_user(User(id="12222222344", username="myFunnyNewUsername2", private_chat_id="myPrivateChatId2", active_groups=set()))
    #data_object.add_group(new_group=(Group(group_id="Group1")))
    #data_object.add_habit_entry(HabitEntry(user_id="12222222344", activity=Activity.SPORT))
    return data_object
