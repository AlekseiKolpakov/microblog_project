from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from backend.core.db import Base


class Like(Base):
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True)

    liker_id = Column(Integer, ForeignKey("users.id"))
    tweet_id = Column(Integer, ForeignKey("tweets.id"))

    liker = relationship("User", backref="likes")
    tweet = relationship("Tweet", backref="likes")
