
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(
    title="Banking Transaction API",
    version="1.0.0"
)

# Temporary in-memory database
transactions = {}
next_transaction_id = 1

# Pydantic model
class TransactionCreate(BaseModel):
    customer: str = Field(min_length=1)
    amount: float = Field(gt=0)
    status: str = "Pending"

# Model used for full replacement
class TransactionReplace(BaseModel):
    customer: str = Field(min_length=1)
    amount: float = Field(gt=0)
    status: str

    # Model used for partial updates
class TransactionUpdate(BaseModel):
    customer: str | None = None
    amount: float | None = Field(default=None, gt=0)
    status: str | None = None

# Home endpoint
@app.get("/")
def home():
    return {"message": "Banking API is running Succesfully!"}

# Create a transaction
@app.post("/transactions", status_code=201)
def create_transaction(transaction: TransactionCreate):
    global next_transaction_id

    transaction_id = next_transaction_id
    next_transaction_id += 1

    transactions[transaction_id] = transaction.model_dump()

    return {
        "transaction_id": transaction_id,
        **transactions[transaction_id]
    }


# Get all transactions
@app.get("/transactions")
def list_transactions():
    return [
        {"transaction_id": tid, **data}
        for tid, data in transactions.items()
    ]


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


# Replace an entire transaction
@app.put("/transactions/{transaction_id}")
def replace_transaction(
    transaction_id: int,
    transaction: TransactionReplace
):
    if transaction_id not in transactions:
        raise HTTPException(
            status_code=404,
            detail="Transaction not found"
        )

    transactions[transaction_id] = transaction.model_dump()

    return {
        "transaction_id": transaction_id,
        **transactions[transaction_id]
    }


# Update selected fields
@app.patch("/transactions/{transaction_id}")
def update_transaction(
    transaction_id: int,
    update: TransactionUpdate
):
    if transaction_id not in transactions:
        raise HTTPException(
            status_code=404,
            detail="Transaction not found"
        )

    changes = update.model_dump(exclude_unset=True)

    transactions[transaction_id].update(changes)

    return {
        "transaction_id": transaction_id,
        **transactions[transaction_id]
    }


# Delete a transaction
@app.delete("/transactions/{transaction_id}", status_code=204)
def delete_transaction(transaction_id: int):
    if transaction_id not in transactions:
        raise HTTPException(
            status_code=404,
            detail="Transaction not found"
        )

    del transactions[transaction_id]
    return None
