import dataclasses
import datetime
import uuid
from typing import Any, Union


@dataclasses.dataclass
class _Task:
    """ task data unit """
    task_id: uuid
    trigger: str = "date"
    run_time: Union[datetime.datetime, None] = None
    kwargs: dict = None
    foo: Any = None

