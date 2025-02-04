# Fetch Receipt Processor Challenge

This is an API created for the Fetch Receipt Processor Challenge.

### Set up and usage information

Assuming Docker is already installed, start Docker with:

- `docker build -t receipt-processor .`
- `docker run -d -p 8000:8000 receipt-processor`
- Or all together: `docker build -t receipt-processor . && docker run -d -p 8000:8000 receipt-processor`

This will run the tests and then run the API. Requests can then be made to it.

To see the Docker container output:

- Find the container ID with `docker ps`
- `docker logs <container_id>`
- Or all together: `docker logs $(docker ps -n 1 -a -q)`

Visit http://127.0.0.1:8000/docs for more detailed API documentation.

Here are some request examples:

```
curl -X 'POST' 'http://127.0.0.1:8000/receipts/process' \
    -H 'Content-Type: application/json' \
    -d '{
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
    }'
```

```
curl \
-X 'GET' \
'http://127.0.0.1:8000/receipts/7520a7c1-f483-4246-9735-40f8d343f1c6/points'
```

Stop the container with `docker stop $(docker ps -n 1 -a -q)`
