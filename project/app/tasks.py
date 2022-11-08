import asyncio

async def fibonacci_task(number: int) -> int:
    return number if number < 2 else await fibonacci_task(number - 1) + await fibonacci_task(number - 2)
