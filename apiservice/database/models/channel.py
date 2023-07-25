from sqlalchemy import Column, BigInteger, String, Integer, Boolean, Table, MetaData
from pydantic import BaseModel
from database.main import Base

metadata = MetaData()


class ChannelData(BaseModel):
    id: int
    name: str
    phone: str = "null"
    email: str = "null"
    msg_id: int = 0
    is_active: bool = True


class Channel(Base):
    __table__ = Table(
        "Channel",
        metadata,
        Column("id", BigInteger, primary_key=True),
        Column("name", String, nullable=False),
        Column("phone", String, default="0", nullable=False),
        Column("email", String, default="null", nullable=False),
        Column("msg_id", Integer, default=0, nullable=False),
        Column("is_active", Boolean, default=True, nullable=False),
    )