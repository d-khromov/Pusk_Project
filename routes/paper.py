from fastapi import APIRouter, status, Depends, HTTPException
from sqlmodel import Session, select
from db import engine, SessionLocal, get_db
from schemas import paper as schema_paper
#from ..api_docs import request_examples
from sqlalchemy import text

router = APIRouter(prefix="/papers", tags=["Управление БД статей"])

@router.post("/", status_code=status.HTTP_201_CREATED,
             response_model=schema_paper.PaperUpload)
def upload_paper(paper: schema_paper.PaperUpload,
                 session: Session = Depends(get_db)):
    new_paper = schema_paper.Paper(
        title =paper.title,
        author = paper.author,
        field = paper.field
    )
    session.add(new_paper)
    session.commit()
    session.refresh(new_paper)
    return new_paper
