import dataclasses
import datetime

from models.Activity import Activity


@dataclasses.dataclass
class HabitEntry:
    user_id: str
    activity: Activity
    date: str = datetime.date.today().isoformat()  # isoformated datetime. has to be a string in order to be serializable for JSON

    def get_date(self) -> datetime.date:
        return datetime.date.fromisoformat(self.date)
