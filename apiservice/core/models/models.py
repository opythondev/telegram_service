from pydantic import BaseModel
from typing import List


class TaskInput(BaseModel):
    from_user: int
    channels: List[str]
