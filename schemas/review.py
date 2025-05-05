from pydantic import (BaseModel, Field)
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean
from db import Base


class ReviewModel(BaseModel):
    title: str = Field(
        title="Название статьи",
        max_length=300
    )
    author: str = Field(
        title="Автор",
        max_length=300
    )
    field: str = Field(
        title="Область науки",
        max_length=300
    )
    review: str = Field(
        title="Ревью статьи",
    )
    grade:float


class ReviewDb(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True)
    title:str = Column(String, unique=True, index=True)
    author:str = Column(String, unique=False, index=True)
    field:str = Column(String, unique=False, index=True)
    email:str = Column(String, unique=False, index=True)
    review:str = Column(String, unique=False, index=True)
    grade:float = Column(Float, unique=False, index=True)