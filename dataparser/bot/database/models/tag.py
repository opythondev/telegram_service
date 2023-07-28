from sqlalchemy import Column, BigInteger, String, Table, MetaData
from pydantic import BaseModel
from database.main import Base

metadata = MetaData()


class TagData(BaseModel):
    id: int
    title: str


class Tag(Base):
    __table__ = Table(
        "tag",
        metadata,
        Column("id", BigInteger, primary_key=True),
        Column("title", String, nullable=False)
    )

    def __init__(self, tag: TagData):
        self.id = tag.id
        self.title = tag.title



