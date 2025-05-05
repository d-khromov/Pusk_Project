from pydantic import (BaseModel, Field)
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from db import Base


class PaperModel(BaseModel):
    title: str = Field(
        title="Название статьи",
        max_length=300
    )
    author: str = Field(
        author="Автор",
        max_length=300
    )
    field: str = Field(
        field="Область науки",
        max_length=300
    )
    status:str = Field(
        status="Требуется",
        max_length=300
    )



class PaperDb(Base):
    __tablename__ = "papers"
    id = Column(Integer, primary_key=True)
    title:str = Column(String, unique=True, index=True)
    author:str = Column(String, unique=False, index=True)
    field:str = Column(String, unique=False, index=True)
    status:str = Column(String, unique=False, index=True)
    #uploader:int = Column(Integer, ForeignKey("users.id"))