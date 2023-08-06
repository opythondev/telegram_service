import datetime

from sqlalchemy import Column, BigInteger, Table, MetaData, TIMESTAMP
from pydantic import BaseModel
from bot.database.main import Base

metadata = MetaData()


class UserChannelData(BaseModel):
    user_id: int
    channel_id: int


class UserChannel(Base):
    __table__ = Table(
        "userchannel",
        metadata,
        Column("id", BigInteger, primary_key=True),
        Column("user_id", BigInteger, nullable=False),
        Column("channel_id", BigInteger, nullable=False),
        Column("create_at", TIMESTAMP, default=datetime.datetime.utcnow(),
               nullable=False)
    )

    def __init__(self, user_channel: UserChannelData):
        self.user_id = user_channel.user_id
        self.channel_id = user_channel.channel_id
