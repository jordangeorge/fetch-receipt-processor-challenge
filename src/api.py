from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder

from models import Receipt

import uuid
import sqlite3
import json
import math
import re
from datetime import datetime

app = FastAPI()

conn = sqlite3.connect("data.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS data (
        id TEXT PRIMARY KEY, json_data TEXT
    )
    """)
conn.commit()

@app.post("/receipts/process", status_code=201, responses={
    201: {
        "description": "Successful Response",
         "content": {
            "application/json": {
                "example": {
                    "id": "874ab0dc-d6d7-459a-be24-d324be2605a9"
                }
            }
        }
    }
})
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

@app.get("/receipts/{unique_id}/points", status_code=200, responses={
    200: {
        "description": "Successful Response",
         "content": {
            "application/json": {
                "example": {
                    "points": 109
                }
            }
        }
    },
    404: {
        "description": "Successful Response",
         "content": {
            "application/json": {
                "example": {
                    "status_code": 404,
                    "detail": "Data not found",
                    "headers": None
                }
            }
        }
    }
})
def get_points(unique_id: str):
    cursor.execute(
        """
        SELECT json_data
        FROM data
        WHERE id = ?
        """, 
        (unique_id,)
    )

    row = cursor.fetchone()

    if row:
        receipt = json.loads(row[0])
        pydantic_receipt = Receipt.model_validate(receipt)
        points = calculate_points(pydantic_receipt)
        return {"points": points}
    
    return HTTPException(status_code=404, detail="Data not found")

def calculate_points(receipt: Receipt) -> int:
    points = 0
    
    # One point for every alphanumeric character in the retailer name.
    pattern = r'[a-zA-Z0-9]'
    points += len(re.findall(pattern, receipt.retailer))

    # 50 points if the total is a round dollar amount with no cents.
    points += 50 if receipt.total.endswith(".00") else 0

    # 25 points if the total is a multiple of 0.25.
    if float(receipt.total) % 0.25 == 0:
        points += 25
    
    # 5 points for every two items on the receipt.
    points += len(receipt.items) // 2 * 5

    # If the trimmed length of the item description is a multiple of 3, multiply the price by 0.2 and round up to the nearest integer. The result is the number of points earned.
    for item in receipt.items:
        if len(item.shortDescription.strip()) % 3 == 0:
            points += math.ceil(float(item.price) * 0.2)
    
    # 6 points if the day in the purchase date is odd.
    if int(receipt.purchaseDate.split("-")[2]) % 2 == 1: points += 6
    
    # 10 points if the time of purchase is after 2:00pm and before 4:00pm.
    start = str_to_datetime("14:00")
    end = str_to_datetime("16:00")
    purchase_time = str_to_datetime(receipt.purchaseTime)
    if start < purchase_time < end:
        points += 10

    return points

def str_to_datetime(date_str: str) -> datetime:
    format = "%H:%M"
    return datetime.strptime(date_str, format)