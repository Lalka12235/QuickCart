from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config.config import settings

engine = create_engine(
    url=settings.sync_db_url,
    echo=False,#True для отладки
)

SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()