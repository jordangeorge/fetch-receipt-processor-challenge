from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from typing import List
import uuid
import sqlite3
import json

app = FastAPI()

conn = sqlite3.connect("data.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS data (
               id TEXT PRIMARY KEY, json_data TEXT
               )
    """)
conn.commit()

class Item(BaseModel):
    shortDescription: str
    price: str

class Receipt(BaseModel):
    retailer: str
    purchaseDate: str
    purchaseTime: str
    items: List[Item]
    total: str

# @app.get("/")
# def read_root() -> dict[str, str]:
#     return {"Hello": "World"}

@app.post("/receipts/process")
def process_receipt(receipt: Receipt) -> dict[str, str]:
    # create unique id
    unique_id = str(uuid.uuid4())
    
    # convert in order to save in local sqlite db
    json_compatible_item_data = jsonable_encoder(receipt)
    
    # save id and receipt data to db
    cursor.execute("""
        INSERT INTO data
            (id, json_data)
        VALUES
            (?, ?)
        """, (
        unique_id,
        json.dumps(json_compatible_item_data)
    ))
    conn.commit()

    return {"id": unique_id}


@app.get("/receipts/{unique_id}/points")
def calculate_points(unique_id: str) -> dict:
    cursor.execute("SELECT json_data FROM data WHERE id=?", (unique_id,))
    row = cursor.fetchone()
    if row:
        receipt = json.loads(row[0])
        pydantic_receipt = Receipt.model_validate(receipt)
        points = calculate_points(pydantic_receipt)
        return {"points": points}
    return {"error": "Data not found"}


def calculate_points(receipt: str) -> int:
    points = 0
    
    # One point for every alphanumeric character in the retailer name.
    points += len(receipt.retailer)

    # 50 points if the total is a round dollar amount with no cents.
    points += 50 if receipt.total.endswith(".00") else 0

    # 25 points if the total is a multiple of 0.25.
    if float(receipt.total) % 0.25 == 0:
        points += 25

    # 5 points for every two items on the receipt.
    points += len(receipt.items) // 2 * 5

    # If the trimmed length of the item description is a multiple of 3, multiply the price by 0.2 and round up to the nearest integer. The result is the number of points earned.


    # 6 points if the day in the purchase date is odd.


    # 10 points if the time of purchase is after 2:00pm and before 4:00pm.


    return points


# http://127.0.0.1:8000/docs
# documentation 


