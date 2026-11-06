from fastapi import FastAPI
app=FastAPI()

@app.get("/")
def home():
    return {"message": "Banking API is running!"}


@app.get("/transactions/{transaction_id}")
def get_transaction(transaction_id: int):
    # Placeholder for fetching transaction details from a database or service
    return {
        "transaction_id": transaction_id,
        "amount": 100.0,
        "currency": "USD",
        "status": "completed"
    }
     