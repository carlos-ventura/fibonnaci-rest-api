from sqlalchemy import Column, Integer

from app.db.config import Base


class Blacklist(Base):
    __tablename__ = 'blacklist'

    number = Column(Integer, primary_key=True)
