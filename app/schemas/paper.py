from pydantic import (BaseModel, Field)
from sqlalchemy import Column, Integer, String, Boolean
from app.db import Base


class PaperBaseModel(BaseModel):
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

class PaperModel(PaperBaseModel):
    status:bool


class PaperGet(PaperBaseModel):
    email: str = Field(
        title="Email загрузившего пользователя",
        max_length=300
    )

class PaperGetBest(PaperGet):
    grade: float

class PaperAsk(PaperBaseModel):
    email: str = Field(
        title="Email пользователя, которому нужна статья",
        max_length=300
    )


class PaperDb(Base):
    __tablename__ = "papers"
    id = Column(Integer, primary_key=True)
    title:str = Column(String, unique=True, index=True)
    author:str = Column(String, unique=False, index=True)
    field:str = Column(String, unique=False, index=True)
    status:bool = Column(Boolean, unique=False, index=True)
    email:str = Column(String, unique=False, index=True)