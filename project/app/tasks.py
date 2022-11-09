import asyncio
from typing import List
from cache import AsyncLRU

from fastapi import HTTPException

from app.models import FibonacciPair
from app.utils import handle_input
from app.db.dals.blacklist_dal import BlacklistDAL
from app.db.config import async_session


@AsyncLRU()
async def fibonacci(number: int) -> int:
    return number if number < 2 else await fibonacci(number - 1) + await fibonacci(number - 2)


async def fibonacci_task(number: int) -> int:
    handle_input(number)
    blacklist = [el.number for el in await fibonacci_blacklist_task()]
    if number in blacklist:
        raise HTTPException(status_code=404, detail="Number is blacklisted")
    return await fibonacci(number)


async def fibonacci_task_pairs(number: int) -> List[FibonacciPair]:
    handle_input(number=number, zero_allowed=False)
    blacklist = [el.number for el in await fibonacci_blacklist_task()]
    filtered_numbers = [n for n in range(1, number + 1) if n not in blacklist]

    if not filtered_numbers:
        raise HTTPException(
            status_code=404, detail="All numbers are blacklisted")

    results = await asyncio.gather(*[fibonacci(n) for n in filtered_numbers])
    return [
        FibonacciPair(number=filtered_numbers[i], fibonacci_number=results[i])
        for i in range(len(results))
    ]




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


async def fibonacci_blacklist_task() -> List[int]:
    async with async_session() as session:
        async with session.begin():
            blacklist_dal = BlacklistDAL(session)
            return await blacklist_dal.get_all_blacklist_numbers()
