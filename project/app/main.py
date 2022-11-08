from fastapi import FastAPI
from fastapi_pagination import Page as BasePage, Params, paginate, add_pagination

from app.tasks import fibonacci_task, fibonacci_task_pairs
from app.models import FibonacciPair

app = FastAPI()

Page = BasePage.with_custom_options(size=100)

@app.get("/fibonacci/")
async def fibonacci(number: int):
    fibonacci_number = await fibonacci_task(number)
    return { "fibonacci_number" : fibonacci_number }

@app.get("/fibonacci/list", response_model=Page[FibonacciPair])
async def fibonacci_list(number: int):
    fibonacci_pairs = await fibonacci_task_pairs(number)
    return paginate(fibonacci_pairs)

@app.post("/fibonacci/blacklist")
async def add_to_blacklist(number: int):
    return

@app.delete("/fibonacci/delete_from_blacklist")
async def delete_from_blacklist(number: int):
    return

add_pagination(app)
