from sqlalchemy import Column, BigInteger, String, Table, MetaData, Integer
from pydantic import BaseModel
from bot.database.main import Base

metadata = MetaData()


class PostData(BaseModel):
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
        self.channel_id = post.channel_id
        self.message_id = post.message_id
        self.date = post.date
        self.photo = post.photo
        self.title = post.title
        self.text = post.text
        self.reactions_count = post.reactions_count
        self.views_count = post.views_count
        self.comments_channel_id = post.comments_channel_id
