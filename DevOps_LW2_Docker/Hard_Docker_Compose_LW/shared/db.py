from sqlalchemy import Column, String, Integer
from typing import Type
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta  # type: ignore
from sqlalchemy import create_engine

Base: Type[DeclarativeMeta] = declarative_base()  # type: ignore
#engine = create_engine("sqlite:///data/news.db")
#session = sessionmaker(bind=engine)
class News(Base):  # type: ignore
    __tablename__ = "news"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    url = Column(String)
    complexity = Column(String)
    habr_id = Column(String)
    label = Column(String)


#Base.metadata.create_all(bind=engine)
