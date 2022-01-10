import services.FileServices
from models import Data


def mock_userdata(data_path: str) -> Data:
    data_object = Data.Data(users={}, groups={})
    data_object.add_user(Data.User(user_id="12344", tel_username="Thomas Müller: Krumfuß", chosen_name='myFunnyUsername',
                                   private_chat_id="myPrivateChatId", active_groups=set()))
    services.FileServices.save_json_overwrite(data_object, data_path)
    return data_object
