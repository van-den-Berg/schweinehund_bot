import dataclasses
import datetime
import time

from models.Activity import Activity


@dataclasses.dataclass
class HabitEntry:
    user_id: str
    activity: Activity
    date: str # isoformated datetime. has to be a string in order to be serializable for JSON

    def __init__(self, user_id: str, activity: Activity, date: str = str(time.time())):
        self.user_id = user_id
        self.activity = activity
        self.date = date

    # TODO: get datetime.date object from the millis date string
    def get_date(self) -> datetime.date:
        ret_date : datetime.date
        return ret_date