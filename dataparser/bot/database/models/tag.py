from sqlalchemy import Column, BigInteger, String, Table, MetaData
from pydantic import BaseModel
from bot.database.main import Base

metadata = MetaData()


class TagData(BaseModel):
    title: str


class Tag(Base):
    __table__ = Table(
        "tag",
        metadata,
        Column("id", BigInteger, primary_key=True),
        Column("title", String, nullable=False)
    )

    def __init__(self, tag: TagData):
        self.title = tag.title
