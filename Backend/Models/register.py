from sqlalchemy.dialects.postgresql import UUID
from Database.sql import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True,index=True)
    email = Column(String(255), unique=True, nullable=False,index=True)
    fullname = Column(String(255),nullable=False)
    hashpassword = Column(String, nullable=True,default="local",index=True)
    provider = Column(String(50),nullable=False,default="local",index=True)
    is_active = Column(Boolean, default=True,index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(),server_default=func.now())
    refresh_tokens = relationship("RefreshToken", back_populates="user", cascade="all, delete-orphan",lazy="select")

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', fullname='{self.fullname}', provider='{self.provider}')>"
    
class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id = Column(Integer,primary_key=True,index=True)
    token = Column(String(500),unique=True,nullable=False,index=True)
    user_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False,index=True)
    expires_at = Column(DateTime(timezone=True), nullable=False,index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_revoked = Column(Boolean, default=False,index=True)

    user = relationship("User",back_populates="refresh_tokens")

    def __repr__(self):
        return f"<RefreshToken(id={self.id}, user_id={self.user_id}, is_revoked={self.is_revoked})>"