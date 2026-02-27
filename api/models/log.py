from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from db.database import Base
from sqlalchemy import ForeignKey

organization_id = Column(Integer, ForeignKey("organizations.id"))

class Log(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)
    level = Column(String(50), nullable=False)  # info, error
    event = Column(String(100), nullable=False)  # schedule_executed, schedule_failed, etc
    message = Column(Text, nullable=True)

    schedule_id = Column(Integer, ForeignKey("schedules.id"), nullable=True)
    calendar_item_id = Column(Integer, ForeignKey("calendar_items.id"), nullable=True)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=True)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    organization_id = Column(Integer, ForeignKey("organizations.id"))