from typing import List

import sqlalchemy
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from app.db.models.blacklist import Blacklist


class BlacklistDAL():
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def add_blacklist_number(self, number: int):
        blacklist_number = Blacklist(number=number)
        self.db_session.add(blacklist_number)
        try:
            await self.db_session.commit()
        except sqlalchemy.exc.IntegrityError:
            pass

    async def get_all_blacklist_numbers(self) -> List[int]:
        blacklist_all_entries = await self.db_session.execute(
            select(Blacklist).order_by(Blacklist.number)
        )
        return list(blacklist_all_entries.scalars().all())

    async def delete_blacklist_number(self, number: int):
        blacklist_entry = await self.db_session.get(Blacklist, number)
        if blacklist_entry:
            await self.db_session.delete(blacklist_entry)
            await self.db_session.commit()
