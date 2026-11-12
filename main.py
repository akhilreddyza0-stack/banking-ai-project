
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(
    title="Banking Transaction API managemnet",
    version="1.0.0"
)

# Temporary in-memory database
transactions = {}

# Pydantic model
class Transaction(BaseModel):
    customer: str
    amount: float = Field(gt=0)
    status: str = "Pending"

# Home endpoint
@app.get("/")
def home():
    return {"message": "Banking API is running!"}

# Create a transaction
@app.post("/transactions", status_code=201)
def create_transaction(transaction: Transaction):

    transaction_id = len(transactions) + 1

    transactions[transaction_id] = transaction.model_dump()

    return {
        "transaction_id": transaction_id,
        **transactions[transaction_id]
    }

# Retrieve a transaction
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
