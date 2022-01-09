import dataclasses

from models.Activity import Activity


@dataclasses.dataclass
class HabitEntry:
    user_id: str
    activity: Activity
    date: str  # isoformated datetime. has to be a string in order to be serializable for JSON
