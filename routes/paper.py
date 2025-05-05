from fastapi import APIRouter, status, Depends, HTTPException, Query
from sqlmodel import Session, select
from db import engine, SessionLocal, get_session
from schemas import paper as schema_paper
from typing import Optional
from auth import auth_handler
#from ..api_docs import request_examples
from sqlalchemy import text

router = APIRouter(prefix="/papers", tags=["Управление БД статей"])

@router.post("/", status_code=status.HTTP_201_CREATED,
             response_model=schema_paper.PaperModel)
def upload_paper(paper: schema_paper.PaperModel,
                 session: Session = Depends(get_session),
                 current_user: dict = Depends(auth_handler.get_current_user)):
    new_paper = schema_paper.PaperDb(
        title =paper.title,
        author = paper.author,
        field = paper.field,
        status = paper.status,
        uploader_email=current_user.email
    )
    session.add(new_paper)
    session.commit()
    session.refresh(new_paper)
    return new_paper


@router.get("/", response_model=list[schema_paper.PaperGet])
def get_papers(
        title: Optional[str] = Query(None, description="Название статьи"),
        author: Optional[str] = Query(None, description="Автор статьи"),
        field: Optional[str] = Query(None, description="Тематика статьи"),
        limit: int = 100,
        session: Session = Depends(get_session)
    ):
    query = session.query(schema_paper.PaperDb)

    if title:
        query = query.filter(schema_paper.PaperDb.title.ilike(f"%{title}%"))
    if author:
        query = query.filter(schema_paper.PaperDb.author.ilike(f"%{author}%"))
    if field:
        query = query.filter(schema_paper.PaperDb.field.ilike(f"%{field}%"))

    papers = query.limit(limit).all()

    if not papers:
        raise HTTPException(
            status_code=404,
            detail="Статьи не найдены"
        )

    return papers
