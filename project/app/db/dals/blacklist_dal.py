import sqlalchemy
from sqlalchemy.orm import Session

from app.db.models.blacklist import Blacklist

class BlacklistDAL():
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def add_blacklist_number(self, number: int):
        blacklist_number = Blacklist(number = number)
        self.db_session.add(blacklist_number)
        try:
            await self.db_session.commit()
        except sqlalchemy.exc.IntegrityError:
            pass
