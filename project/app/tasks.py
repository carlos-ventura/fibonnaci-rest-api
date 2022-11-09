import asyncio
from typing import List

from app.models import FibonacciPair
from app.utils import handle_input
from app.db.dals.blacklist_dal import BlacklistDAL
from app.db.config import async_session

async def fibonacci_task(number: int) -> int:
    return number if number < 2 else await fibonacci_task(number - 1) + await fibonacci_task(number - 2)

async def fibonacci_task_pairs(number: int) -> List[FibonacciPair]:
    results = await asyncio.gather(*[fibonacci_task(n) for n in range(1, number + 1)])
    return [ FibonacciPair(number=i+1, fibonacci_number=results[i]) for i in range(len(results))]

async def add_to_blacklist_task(number: int):
    handle_input(number)
    async with async_session() as session:
        async with session.begin():
            blacklist_dal = BlacklistDAL(session)
            await blacklist_dal.add_blacklist_number(number)

async def delete_from_blacklist_task(number: int):
    handle_input(number)
    async with async_session() as session:
        async with session.begin():
            blacklist_dal = BlacklistDAL(session)
            await blacklist_dal.delete_blacklist_number(number)

