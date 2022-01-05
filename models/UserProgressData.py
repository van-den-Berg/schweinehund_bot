from datetime import date
from models.Activity import Activity


class UserProgressData:
    user_id: int
    training_data: dict = {Activity.SPORT: [], Activity.CHILL_EVENING: []}

    def __init__(self, user_id: int, training_data=None):
        self.training_data = self.training_data if training_data is None else training_data
        self.user_id = user_id

    def add_activity_now(self, activity: Activity) -> bool:
        today = date.today()
        if today in self.training_data[activity]:
            self.training_data[activity].append(date.today())
            return True
        return False
