from app.constants import DESCRIPTION
from app.db.config import Base, async_session, engine
from app.models import FibonacciPair
from app.tasks import (add_to_blacklist_task, delete_from_blacklist_task,
                       fibonacci_blacklist_task, fibonacci_task,
                       fibonacci_task_pairs)
from fastapi import Depends, FastAPI
from fastapi_pagination import Page as BasePage
from fastapi_pagination import add_pagination, paginate
from sqlalchemy.orm import Session

app = FastAPI(
    title="Fibonacci",
    description=DESCRIPTION,
)

Page = BasePage.with_custom_options(size=100)


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@app.get("/fibonacci/")
async def fibonacci(number: int):
    fibonacci_number = await fibonacci_task(number)
    return {"fibonacci_number": fibonacci_number}


@app.get("/fibonacci/list", response_model=Page[FibonacciPair])
async def fibonacci_list(number: int):
    fibonacci_pairs = await fibonacci_task_pairs(number)
    return paginate(fibonacci_pairs)


@app.post("/fibonacci/add_to_blacklist")
async def add_to_blacklist(number: int):
    await add_to_blacklist_task(number)


@app.delete("/fibonacci/delete_from_blacklist")
async def delete_from_blacklist(number: int):
    await delete_from_blacklist_task(number)


@app.get("/fibonacci/blacklist")
async def fibonacci_blacklist():
    return await fibonacci_blacklist_task()


add_pagination(app)
