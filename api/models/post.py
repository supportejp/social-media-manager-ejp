from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from db.database import Base

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    status = Column(String(50), default="draft")

    # 🔥 NUEVOS CAMPOS
    media_type = Column(String(50), nullable=True)      # "image"
    media_path = Column(Text, nullable=True)            # ruta local del archivo
    linkedin_post_urn = Column(String(255), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    organization_id = Column(Integer, ForeignKey("organizations.id"))