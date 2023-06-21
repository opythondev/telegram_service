import dataclasses
import datetime
import uuid
from typing import Any, Union


@dataclasses.dataclass
class _Task:
    """ task data unit """
    trigger: str
    task_id: uuid
    run_time: Union[datetime, None] = None
    kwargs: dict = None
    foo: Any = None

