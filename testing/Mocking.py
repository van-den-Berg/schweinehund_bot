import services.FileServices
from models.data_storage import Data


def mock_userdata() -> Data:
    data_object = Data.Data(users={}, groups={})
    data_object.add_user(Data.User(user_id="12344", tel_username="myFunnyUsername", private_chat_id="myPrivateChatId", active_groups=[]))
    services.FileServices.save_json_overwrite(data_object, "data.json")
    return data_object
