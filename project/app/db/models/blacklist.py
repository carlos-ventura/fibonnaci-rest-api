from app.db.config import Base
from sqlalchemy import Column, Integer


class Blacklist(Base):
    __tablename__ = 'blacklist'

    number = Column(Integer, primary_key=True)
