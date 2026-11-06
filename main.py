from fastapi import FastAPI
from pydantic import BaseModel, Field

app=FastAPI()

transactions = {}

class transactions(BaseModel):
    customer:str
    amount: float = Field(gt=0)
    status: str = "Pending"

@app.get("/")
def home():
    return {"message": "Banking API is running!"}


@app.post("/transactions", status_code=201)
def create_transaction(transaction: Transaction):
    transaction_id = len(transactions) + 1

    transactions[transaction_id] = transaction.model_dump()

    return {
        "transaction_id": transaction_id,
        **transactions[transaction_id]
    }

@app.get("/transactions/{transaction_id}")
def get_transaction(transaction_id: int):
    if transaction_id not in transactions:
        raise HTTPException(
            status_code=404,
            detail="Transaction not found"
        )

    return {
        "transaction_id": transaction_id,
        **transactions[transaction_id]
    }

    