from fastapi import FastAPI
from random import choice
from kafka import KafkaProducer
import json

app = FastAPI()

# The list of stores
stores = [{"_id": 1, "stock": {"Apple": 50, "Orange": 30, "Bottle of water": 20}, "checkouts": [1, 2],
           "sellers": [1, 2]}]

# The list of checkouts
checkouts = [{"_id": 1}, {"_id": 2}]

# The list of sellers
sellers = [{"_id": 1, "name": "Nom d'un caissier"}, {"_id": 2, "name": "Nom d'un autre caissier"}]

# We choose randomly a specific store to simulate for the session
store = choice(stores)

# The list of checkouts of this store
store_checkouts = [checkout for checkout in checkouts if checkout["_id"] in store["checkouts"]]

# The list of sellers of this store
store_sellers = [seller for seller in sellers if seller["_id"] in store["sellers"]]
basket = {}


@app.get("/")
async def add_to_basket(product_name: str, quantity: int):
    """
    Add quantity unit(s) of the product product_name to the basket.
    """
    if product_name not in store["stock"] or quantity > store["stock"][product_name]:
        return "The product is not available or out of stock."

    store["stock"][product_name] -= quantity
    return "The product has been added to the basket."


@app.delete("/")
async def remove_from_basket(product_name: str):
    """
    Removes the product product_name from the basket.
    """
    if product_name not in basket.keys():
        return "The product is not included in the basket."

    store["stock"][product_name] += basket[product_name]
    del basket[product_name]
    return "The product has been removed from the basket."


@app.post("/")
async def validate_basket():
    """
    Validates the basket and sends the receipt.
    """
    checkout = choice(store_checkouts)
    seller = choice(store_sellers)

    # Insert the receipt corresponding to the basket in the collection "Receipts" of the database db
    db["Receipts"].insert_one({
        "store_id": store["_id"],
        "checkout_id": checkout["_id"],
        "seller_id": seller["_id"],
        "basket": basket,
        "total_price": sum(product["price"] for product in basket.values())
    })

    # Indicate that the basket was effectively validated
    return "The basket is validated, and the receipt has been added to the database."


@app.get("/stock")
async def get_stock():
    """
    Get the current stock of the store.
    """
    return store["stock"]


if __name__ == "__main__":
    # Run the FastAPI application
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
