from app.constants import DESCRIPTION
from app.db.config import Base, async_session, engine
from app.models import FibonacciPair
from app.tasks import (add_to_blacklist_task, delete_from_blacklist_task,
                       fibonacci_blacklist_task, fibonacci_task_pairs_v2,
                       fibonacci_task_v2)
from fastapi import Depends, FastAPI
from fastapi_pagination import Page as BasePage
from fastapi_pagination import add_pagination, paginate
from sqlalchemy.orm import Session

app = FastAPI(
    title="Fibonacci",
    description=DESCRIPTION,
)

Page = BasePage.with_custom_options(size=100)


async def get_session():
    try:
        session = async_session()
        yield session
    finally:
        await session.close()


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@app.get("/fibonacci/")
async def fibonacci(number: int, session: Session = Depends(get_session)):
    fibonacci_number = await fibonacci_task_v2(number, session)
    return {"fibonacci_number": fibonacci_number}


@app.get("/fibonacci/list", response_model=Page[FibonacciPair])
async def fibonacci_list(number: int,  session: Session = Depends(get_session)):
    fibonacci_pairs = await fibonacci_task_pairs_v2(number, session)
    return paginate(fibonacci_pairs)


@app.post("/fibonacci/add_to_blacklist")
async def add_to_blacklist(number: int,  session: Session = Depends(get_session)):
    await add_to_blacklist_task(number, session)


@app.delete("/fibonacci/delete_from_blacklist")
async def delete_from_blacklist(number: int,  session: Session = Depends(get_session)):
    await delete_from_blacklist_task(number, session)


@app.get("/fibonacci/blacklist")
async def fibonacci_blacklist(session: Session = Depends(get_session)):
    return await fibonacci_blacklist_task(session)


add_pagination(app)
