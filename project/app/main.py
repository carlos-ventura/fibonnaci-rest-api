from fastapi import FastAPI
from app.tasks import fibonacci_task

app = FastAPI()


@app.get("/fibonacci/")
async def fibonacci(number: int):
    fibonacci_number = await fibonacci_task(number)
    return { "fibonacci_number" : fibonacci_number }

@app.get("/fibonacci/list")
async def fibonacci_list(number: int):
    return

@app.post("/fibonacci/blacklist")
async def add_to_blacklist(number: int):
    return

@app.delete("/fibonacci/delete_from_blacklist")
async def delete_from_blacklist(number: int):
    return
