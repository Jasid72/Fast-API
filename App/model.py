from App.Database import Base
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, text


class Post(Base):
    __tablename__ = "post"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String(100), nullable=False)
    content = Column(String(100), nullable=False)
    published = Column(Boolean, default="True")
    created_at = Column(TIMESTAMP(timezone=True), nullable=True, server_default=text('now()'))
