from fastapi import FastAPI
import csv
import os
import pandas as pd
from pydantic import BaseModel
from datetime import date

app =FastAPI()
FILE = "expenses.csv"
HEADERS = ["id", "date", "amount", "category", "description"]

@app.get("/expenses")
def get_expenses():
    if not os.path.exists(FILE):
        return []
    df = pd.read_csv(FILE)
    return df.to_dict(orient="records")

class Expense(BaseModel):
    amount: float
    category:str
    description: str
    expense_date: str = str(date.today())

@app.post("/expenses")
def add_expense(expense:Expense):
    if os.path.exists(FILE):
        df = pd.read_csv(FILE)
        new_id = max(df["id"].astype(int), default=0) + 1
    else:
        new_id = 1

    file_exists = os.path.exists(FILE)
    with open(FILE, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=HEADERS)
        if not file_exists:
            writer.writeheader()

        writer.writerow({
            "id": new_id,
            "date": expense.expense_date,
            "amount": expense.amount,
            "category": expense.category,
            "description": expense.description
            
        })

    return {"message": "Expense added", "id":new_id }

@app.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int):
    if not os.path.exists(FILE):
        return {"message": "No expenses file found"}
    
    df = pd.read_csv(FILE)
    original_count = len(df)
    
    df = df[df["id"] != expense_id]
    
    if len(df) == original_count:
        return {"message": f"No expense with id {expense_id} found"}
    
    df.to_csv(FILE, index=False)
    return {"message": f"Deleted expense id {expense_id}"}
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

