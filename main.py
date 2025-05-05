from fastapi import FastAPI
from routes import (paper)
from db import Base, engine


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Система управления каталогом статей и рекомендаций",
    version="0.0.1",
    contact={
        "name": "Хромов Дмитрий",
        "email": "khromov.da@phystech.edu",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    }
)

app.include_router(paper.router)
