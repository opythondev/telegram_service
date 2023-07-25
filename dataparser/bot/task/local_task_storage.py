import dataclasses
from .task import _Task


@dataclasses.dataclass
class LocalTaskStorage:
    """ Task storage"""
    storage: dict[_Task]
