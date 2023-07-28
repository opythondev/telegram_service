import datetime

from sqlalchemy import Column, BigInteger, Table, MetaData, TIMESTAMP
from pydantic import BaseModel
from database.main import Base

metadata = MetaData()


class UserChannelData(BaseModel):
    id: int
    user_id: int
    channel_id: int
    create_at: datetime.datetime


class UserChannel(Base):
    __table__ = Table(
        "userchannel",
        metadata,
        Column("id", BigInteger, primary_key=True),
        Column("user_id", BigInteger, nullable=False),
        Column("channel_id", BigInteger, nullable=False),
        Column("create_at", TIMESTAMP, nullable=False)
    )

    def __init__(self, user_channel: UserChannelData):
        self.id = user_channel.id
        self.user_id = user_channel.user_id
        self.channel_id = user_channel.channel_id
        self.create_at = user_channel.create_at
