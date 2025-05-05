from pydantic import (BaseModel, Field)
from sqlalchemy import Column, Integer, String, UniqueConstraint, ForeignKey, Boolean
from db import Base


class UserModel(BaseModel):
    username: str
    email:str
    password:str



class UserDb(Base):
    __tablename__ = "users"
    __table_args__ = (UniqueConstraint("email"),)
    id:int = Column(Integer, primary_key=True)
    username:str = Column(String, unique=True, index=True)
    email:str = Column(String, unique=True, index=True)
    password:str = Column(String, unique=False, index=True)