import dataclasses
from datetime import datetime, timedelta, date

from models.Activity import Activity


def get_today() -> str:
    return datetime.today().date().isoformat()

def get_yesterday() -> str:
    return (datetime.today() - timedelta(days=1)).date().isoformat()

@dataclasses.dataclass
class HabitEntry:
    user_id: str
    activity: Activity
    date: str = datetime.today().isoformat()  # isoformated datetime. has to be a string in order to be serializable for JSON

    def get_date(self) -> datetime.date:
        return datetime.date.fromisoformat(self.date)
