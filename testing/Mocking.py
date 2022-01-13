from models import Data
from models.Activity import Activity
from models.Group import Group
from models.HabitEntry import HabitEntry
from models.User import User
from services import FileServices

my_user = User(user_id="12222222344", username="myFunnyNewUsername2", private_chat_id="myPrivateChatId2", active_groups=set())
my_group = Group(group_id="Group1", group_name="MyGroup Name")

def mock_userdata(data_path: str) -> Data:
    data_object = Data.Data(users={}, groups={})
    #data_object.add_user(my_user)
    #data_object.add_group(new_group=my_group)
    #data_object.user_join_group(my_user.user_id, my_group.group_id, "myFancyUsername")
    #data_object.add_habit_entry(HabitEntry(user_id=my_user.user_id, activity=Activity.SPORT))
    #FileServices.save_json_overwrite(json_data=data_object, file_path=data_path)
    return data_object
