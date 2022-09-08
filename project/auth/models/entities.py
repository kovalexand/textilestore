from uuid import uuid4

from sqlalchemy import Column, String, Boolean
from sqlalchemy.dialects.postgresql import UUID

from project.core.database import Base


class User(Base):
    __tablename__: str = "User"

    id: Column = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name: Column = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    key = Column(String)
    is_verified = Column(Boolean, default=False)
