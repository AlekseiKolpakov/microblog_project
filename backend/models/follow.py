from sqlalchemy import Column, DateTime, ForeignKey, Integer, func
from sqlalchemy.orm import relationship

from backend.core.db import Base


class Follow(Base):
    __tablename__ = "follows"

    id = Column(Integer, primary_key=True)

    follower_id = Column(Integer, ForeignKey("users.id"))
    followed_id = Column(Integer, ForeignKey("users.id"))

    created_at = Column(DateTime, default=func.now())

    follower = relationship("User", backref="followers")
    followed = relationship("User", backref="followings")
