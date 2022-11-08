from pydantic import BaseModel

class FibonacciPair(BaseModel):
    number: int
    fibonnaci_number: int