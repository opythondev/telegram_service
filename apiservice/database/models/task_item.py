import datetime

from sqlalchemy import Column, BigInteger, String, Table, MetaData, TIMESTAMP
from pydantic import BaseModel
from database.main import Base

metadata = MetaData()


class TaskItemData(BaseModel):
    task_id: int
    target_url: str
    channel_id: int
    id: int = None
    status: str = "create"
    create_at: datetime.datetime = datetime.datetime.utcnow()
    finished_at: datetime.datetime = datetime.datetime.utcnow()


class TaskItem(Base):
    __table__ = Table(
        "taskitem",
        metadata,
        Column("id", BigInteger, primary_key=True),
        Column("task_id", BigInteger, nullable=False),
        Column("channel_id", BigInteger, nullable=False),
        Column("target_url", String, nullable=False),
        Column("status", String, nullable=False),
        Column("create_at", TIMESTAMP, nullable=False),
        Column("finished_at", TIMESTAMP, nullable=False),
    )

    def __init__(self, task_item: TaskItemData):
        self.task_id = task_item.task_id
        self.channel_id = task_item.channel_id
        self.target_url = task_item.target_url
        self.status = task_item.status
        self.create_at = task_item.create_at
        self.finished_at = task_item.finished_at
        if task_item.id is not None:
            self.id = task_item.id
