import datetime

from sqlalchemy import Column, BigInteger, String, Table, MetaData, Integer
from pydantic import BaseModel
from database.main import Base

metadata = MetaData()

"""
id bigint pk increments
	channel_id bigint *> Channels.id
	message_id int null
	date text null
	text text null
	photo text null
	reactions_count integer def(0)
	views_count integer def(0)
	comments_channel_id integer 
"""

class PostData(BaseModel):
    id: int
    channel_id: int
    message_id: int
    date: str
    text: str
    title: str
    views_count: int
    reactions_count: int = 0
    comments_channel_id: int = 0
    photo: str = "null"


class Post(Base):
    __table__ = Table(
        "post",
        metadata,
        Column("id", BigInteger, primary_key=True),
        Column("channel_id", BigInteger, nullable=False),
        Column("message_id", BigInteger, nullable=False),
        Column("date", String, nullable=False),
        Column("photo", String),
        Column("title", String, nullable=False),
        Column("text", String, nullable=False),
        Column("reactions_count", Integer),
        Column("views_count", Integer, nullable=False),
        Column("comments_channel_id", BigInteger, nullable=False)
    )

    def __init__(self, post: PostData):
        self.id = post.id
        self.channel_id = post.channel_id
        self.message_id = post.message_id
        self.date = post.date
        self.photo = post.photo
        self.title = post.title
        self.text = post.text
        self.message_id = post.message_id
        self.message_id = post.message_id
        self.message_id = post.message_id
        self.message_id = post.message_id
