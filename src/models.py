from pyexpat import model
from pydantic import BaseModel
from typing import List

class Item(BaseModel):
    shortDescription: str
    price: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "shortDescription": "Gatorade",
                "price": "2.25"
            }
        }
    }

class Receipt(BaseModel):
    retailer: str
    purchaseDate: str
    purchaseTime: str
    items: List[Item]
    total: str

    model_config = {
        "json_schema_extra": {
            "example": {
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
        }
    }