from sqlalchemy import Column, BigInteger, String, Table, MetaData
from pydantic import BaseModel
from database.main import Base

metadata = MetaData()


class ChannelTagData(BaseModel):
    channel_id: int
    title: str
    id: int = None


class ChannelTag(Base):
    __table__ = Table(
        "channeltag",
        metadata,
        Column("id", BigInteger, primary_key=True),
        Column("channel_id", BigInteger, nullable=False),
        Column("title", String, nullable=False)
    )

    def __init__(self, channel_tag: ChannelTagData):
        self.channel_id = channel_tag.channel_id
        self.title = channel_tag.title
