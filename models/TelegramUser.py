import dataclasses


@dataclasses.dataclass
class User:
    id: int
    username: str
    calling_name: str
    first_name: str
    last_name: str
    private_chat_id: int
