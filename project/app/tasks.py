import asyncio
from typing import List

from app.db.dals.blacklist_dal import BlacklistDAL
from app.models import FibonacciPair
from app.utils import handle_input
from cache import AsyncLRU
from fastapi import HTTPException
from sqlalchemy.orm import Session


@AsyncLRU()
async def fibonacci(number: int) -> int:
    return number if number < 2 else await fibonacci(number - 1) + await fibonacci(number - 2)


async def fibonacci_v2(number: int) -> int:
    start_n, next_n = 0, 1
    for _ in range(number):
        start_n, next_n = next_n, next_n+start_n
    return start_n


async def fibonacci_task_v2(number: int) -> int:
    handle_input(number)
    blacklist = [el.number for el in await fibonacci_blacklist_task()]
    if number in blacklist:
        raise HTTPException(status_code=404, detail="Number is blacklisted")
    return await fibonacci_v2(number)


async def fibonacci_task(number: int) -> int:
    handle_input(number)
    blacklist = [el.number for el in await fibonacci_blacklist_task()]
    if number in blacklist:
        raise HTTPException(status_code=404, detail="Number is blacklisted")
    result = 0
    try:
        result = await fibonacci(number)
    except RecursionError as e:
        raise HTTPException(
            status_code=500, detail=str(e)) from e
    return result


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


async def fibonacci_task_pairs_v2(number: int) -> List[FibonacciPair]:
    handle_input(number=number, zero_allowed=False)
    fibonacci_list: List[FibonacciPair] = []
    blacklist = [el.number for el in await fibonacci_blacklist_task()]

    if len(blacklist) >= number:
        raise HTTPException(
            status_code=404, detail="All numbers are blacklisted")

    start_n, next_n = 1, 1
    for i in range(number):
        if i + 1 not in blacklist:
            fibonacci_list.append(FibonacciPair(
                number=i + 1, fibonacci_number=start_n))
        start_n, next_n = next_n, next_n+start_n
    return fibonacci_list


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
