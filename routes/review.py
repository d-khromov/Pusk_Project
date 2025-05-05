from fastapi import APIRouter, status, Depends, HTTPException, Query
from sqlmodel import Session, select
from db import engine, SessionLocal, get_session
from schemas import review as schema_review
from schemas import paper as schema_paper
from typing import Optional
from auth import auth_handler
#from ..api_docs import request_examples
from sqlalchemy import text

router = APIRouter(prefix="/reviews", tags=["Отзывы на статьи"])

@router.post("/", status_code=status.HTTP_201_CREATED,
             response_model=schema_review.ReviewModel)
def upload_review(review: schema_review.ReviewModel,
                 session: Session = Depends(get_session),
                 current_user: dict = Depends(auth_handler.get_current_user)):
    # if the paper was not even posted, user should first post and then review
    paper_posted = session.execute(
        select(schema_paper.PaperDb).where(
            (schema_paper.PaperDb.title == review.title) &
            (schema_paper.PaperDb.author == review.author) &
            (schema_paper.PaperDb.field == review.field)
        )
    ).first()

    if not paper_posted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Такая статья не найдена. Пожалуйста, загрузите ее или добавьте в wanted."
        )

    new_review = schema_review.ReviewDb(
        title =review.title,
        author = review.author,
        field = review.field,
        email=current_user.email,
        review = review.review,
        grade=review.grade
    )
    session.add(new_review)
    session.commit()
    session.refresh(new_review)
    return new_review


@router.get("/", response_model=list[schema_review.ReviewModel])
def get_reviews(
        title: Optional[str] = Query(None, description="Название статьи"),
        author: Optional[str] = Query(None, description="Автор статьи"),
        field: Optional[str] = Query(None, description="Тематика статьи"),
        limit: int = 100,
        session: Session = Depends(get_session)
    ):
    query = session.query(schema_review.ReviewDb)

    if title:
        query = query.filter(schema_review.ReviewDb.title.ilike(f"%{title}%"))
    if author:
        query = query.filter(schema_review.ReviewDb.author.ilike(f"%{author}%"))
    if field:
        query = query.filter(schema_review.ReviewDb.field.ilike(f"%{field}%"))

    reviews = query.limit(limit).all()

    if not reviews:
        raise HTTPException(
            status_code=404,
            detail="Отзывы не найдены"
        )

    return reviews



