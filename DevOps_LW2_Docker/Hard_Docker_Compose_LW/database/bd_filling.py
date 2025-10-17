from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from shared.scraputils import get_news  # type: ignore
from shared.db import News, Base  # type: ignore
import os
database_url = os.getenv('DATABASE_URL')
engine = create_engine(database_url)

session = sessionmaker(bind=engine)
s = session()

inspector = inspect(engine)
if not inspector.has_table('news'):
    Base.metadata.create_all(bind=engine)
    habr_info = get_news("https://habr.com/ru/articles/", 16)
    for article in habr_info[1:]:
        news = News(**article)
        s.add(news)
    s.commit()
s.close()