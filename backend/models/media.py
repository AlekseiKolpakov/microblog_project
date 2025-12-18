from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship

from backend.core.db import Base


class Media(Base):
    __tablename__ = "medias"

    id = Column(Integer, primary_key=True)
    file_path = Column(String, nullable=False)

    tweet_id = Column(Integer, ForeignKey("tweets.id"), nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    created_at = Column(DateTime, default=func.now())

    tweet = relationship("Tweet", backref="medias")
    owner = relationship("User", backref="uploaded_medias")
