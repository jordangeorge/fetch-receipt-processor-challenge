from fastapi.testclient import TestClient
from api import app 

client = TestClient(app)

def process_receipt_and_get_points(payload: dict, expected_points: int) -> str:
    response = client.post("/receipts/process", json=payload)

    unique_id = response.json()["id"]

    assert response.status_code == 201
    assert unique_id != None
    assert len(unique_id.split("-")) == 5

    response = client.get(f"/receipts/{unique_id}/points")

    assert response.status_code == 200
    assert response.json()["points"] == expected_points

def test_mm():
    payload = {
        "retailer": "M&M Corner Market",
        "purchaseDate": "2022-03-20",
        "purchaseTime": "14:33",
        "items": [
            {
            "shortDescription": "Gatorade",
            "price": "2.25"
            },
            {
            "shortDescription": "Gatorade",
            "price": "2.25"
            },
            {
            "shortDescription": "Gatorade",
            "price": "2.25"
            },
            {
            "shortDescription": "Gatorade",
            "price": "2.25"
            }
        ],
        "total": "9.00"
    }

    process_receipt_and_get_points(payload, 109)

def test_target():
    payload = {
        "retailer": "Target",
        "purchaseDate": "2022-01-01",
        "purchaseTime": "13:01",
        "items": [
            {
            "shortDescription": "Mountain Dew 12PK",
            "price": "6.49"
            },
            {
            "shortDescription": "Emils Cheese Pizza",
            "price": "12.25"
            },
            {
            "shortDescription": "Knorr Creamy Chicken",
            "price": "1.26"
            },
            {
            "shortDescription": "Doritos Nacho Cheese",
            "price": "3.35"
            },
            {
            "shortDescription": "   Klarbrunn 12-PK 12 FL OZ  ",
            "price": "12.00"
            }
        ],
        "total": "35.35"
    }

    process_receipt_and_get_points(payload, 28)

def test_walgreens():
    payload = {
        "retailer": "Walgreens",
        "purchaseDate": "2022-01-02",
        "purchaseTime": "08:13",
        "total": "2.65",
        "items": [
            {
            "shortDescription": "Pepsi - 12-oz",
            "price": "1.25"
            },
            {
            "shortDescription": "Dasani",
            "price": "1.40"
            }
        ]
    }

    process_receipt_and_get_points(payload, 15)

def test_target_simple():
    payload = {
        "retailer": "Target",
        "purchaseDate": "2022-01-02",
        "purchaseTime": "13:13",
        "total": "1.25",
        "items": [
            {
            "shortDescription": "Pepsi - 12-oz",
            "price": "1.25"
            }
        ]
    }

    process_receipt_and_get_points(payload, 31)

def test_not_found():
    response = client.get("/receipts/1234/points")

    assert response.json()['status_code'] == 404
    assert response.json() == {'status_code': 404, 'detail': 'Data not found', 'headers': None}

def test_wrong_payload_type():
    payload = {
        "retailer": "Target",
        "purchaseDate": "2022-01-02",
        "purchaseTime": 3,
        "total": "1.25",
        "items": [
            {
            "shortDescription": "Pepsi - 12-oz",
            "price": "1.25"
            }
        ]
    }
    
    response = client.post("/receipts/process", json=payload)

    assert response.status_code == 422
    assert response.json() == {
        "detail": [
                {
                    "input": 3,
                    "loc": [
                        "body",
                        "purchaseTime"
                    ],
                    "msg": "Input should be a valid string",
                    "type": "string_type"
                }
            ]
    }