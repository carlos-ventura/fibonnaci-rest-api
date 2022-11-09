from fastapi import HTTPException

def handle_input(number: int, zero_allowed = True):
    if number < 0:
        raise HTTPException(status_code=400, detail="Number should be positive")
    if not zero_allowed and number==0:
        raise HTTPException(status_code=400, detail="Number should be between 1 and N")