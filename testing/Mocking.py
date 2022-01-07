import services.FileServices
from models.data_storage import Data


def mock_userdata():
    data_object = Data.Data()
    data_object.add_user(Data.User("12344", "myFunnyUsername", "myPrivateChatId"))
    services.FileServices.save_json_overwrite(data_object, "data.json")
