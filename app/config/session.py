from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config.config import settings

engine = create_engine(
    url=settings.sync_db_url,
    echo=False,#True для отладки
)

Session = sessionmaker(bind=engine)