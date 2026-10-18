from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.db.database import Base


class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    module = Column(String(40), nullable=False)
    person_name = Column(String(120), nullable=True)
    birth_date = Column(String(20), nullable=True)
    birth_time = Column(String(20), nullable=True)
    birth_city = Column(String(120), nullable=True)
    accuracy = Column(String(40), nullable=True)
    experience = Column(String(40), nullable=True)
    usefulness = Column(String(40), nullable=True)
    comments = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    user = relationship("User", back_populates="feedback_items")
