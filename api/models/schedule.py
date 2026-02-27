from sqlalchemy import Column, Integer, DateTime, ForeignKey, String, ForeignKey
from sqlalchemy.sql import func
from db.database import Base



class Schedule(Base):
    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True, index=True)
    calendar_item_id = Column(Integer, ForeignKey("calendar_items.id"))
    status = Column(String(50), default="pending")  # pending, executed, failed
    executed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    organization_id = Column(Integer, ForeignKey("organizations.id"))