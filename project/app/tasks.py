import asyncio
from typing import List

from app.models import FibonacciPair

async def fibonacci_task(number: int) -> int:
    return number if number < 2 else await fibonacci_task(number - 1) + await fibonacci_task(number - 2)

async def fibonacci_task_pairs(number: int) -> List[FibonacciPair]:
    results = await asyncio.gather(*[fibonacci_task(n) for n in range(1, number + 1)])
    return [ FibonacciPair(number=i+1, fibonacci_number=results[i]) for i in range(len(results))]
