from fastapi import FastAPI
from random import choice
from operator import getitem
from functools import partial

app = FastAPI()

#Products are identified by name, so there cannot be two products with the same
#name !
referenced_products = {
	"Apple": {"price": 1},
	"Orange": {"price": 1},
	"Bottle of water": {"price": 0.8}
}

stores = [{"_id":1, "stock":{"Apple":50, "Orange":30, "Bottle of water": 20}, "checkouts":[1, 2], "sellers":[1, 2]}]
checkouts = [{"_id":1}, {"_id":2}]
sellers = [{"_id":1, "name":"Nom d'un caissier"}, {"_id":2, "name":"Nom d'un autre caissier"}]

store = choice(stores)
store_checkouts = [checkout for checkout in checkouts if checkout["_id"] in store["checkouts"]]
store_sellers = [seller for seller in sellers if seller["_id"] in store["sellers"]]
basket = {}

@app.get("/")
async def add_to_basket(product_name: str, quantity: int):
    """
    Add quantity unit(s) of the product product_name to the basket.
    """
    if not product_name in referenced_products.keys():
    	return "The product is not referenced."
    if quantity>store["stock"][product_name]:
    	return "The product is out of stock."
    store["stock"][product_name]-=quantity
    basket[product_name] = basket.get(product_name, {"quantity":0, "price":0})
    basket[product_name]["quantity"]+=quantity
    basket[product_name]["price"]+=quantity*referenced_products[product_name]["price"]
    return "The product has been added to the basket."

@app.delete("/")
async def remove_from_basket(product_name: str):
    """
    Removes the product product_name from the basket.
    """
    if not product_name in basket.keys():
    	return "The product is not included in the basket."
    del basket[product_name]
    return "The product has been removed from the basket."

@app.post("/")
async def validate_basket():
    """
    Validates the basket and sends the receipt.
    """
    return {"store_id": store["_id"], "checkout_id": choice(store_checkouts)["_id"], "seller_id": choice(store_sellers)["_id"], "basket": basket, "total_price": sum(product["price"] for product in basket.values())}
