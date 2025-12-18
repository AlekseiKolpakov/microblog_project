from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from backend.core.db import Base


class Tweet(Base):
    __tablename__ = "tweets"

    id = Column(Integer, primary_key=True)
    text = Column(String)

    author_id = Column(Integer, ForeignKey("users.id"))

    author = relationship("User", backref="tweets")
