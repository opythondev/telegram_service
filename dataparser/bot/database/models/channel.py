from sqlalchemy import Column, BigInteger, String, Integer, Table, MetaData
from pydantic import BaseModel
from database.main import Base

metadata = MetaData()


class ChannelData(BaseModel):
    id: int
    name: str
    link: str
    description: str
    user_count: int


class Channel(Base):
    __table__ = Table(
        "channel",
        metadata,
        Column("id", BigInteger, primary_key=True),
        Column("name", String, nullable=False),
        Column("link", String, nullable=False),
        Column("description", String, nullable=False),
        Column("user_count", Integer, nullable=False)
    )

    def __init__(self, channel: ChannelData):
        self.id = channel.id
        self.name = channel.name
        self.link = channel.link
        self.description = channel.description
        self.user_count = channel.user_count
