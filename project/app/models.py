from pydantic import BaseModel


class FibonacciPair(BaseModel):
    number: int
    fibonacci_number: int
