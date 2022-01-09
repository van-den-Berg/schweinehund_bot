import services.FileServices
from models import Data


def mock_userdata() -> Data:
    data_object = Data.Data(users={}, groups={})
    data_object.add_user(Data.User(id=12344, username='None', first_name='Karl', calling_name='MyFunnyName',
                                   last_name='Uwe', private_chat_id=123, active_groups={-781148698}))
    services.FileServices.save_json_overwrite(data_object, "data.json")
    return data_object
