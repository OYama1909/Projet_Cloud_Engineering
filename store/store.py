from fastapi import FastAPI
from random import choice
from pymongo import MongoClient


app = FastAPI()

#Get the mongo client from the Docker container used for Mongo DB
client = MongoClient("mongodb://root:example@mongo")

#Get the database that we will use
db = client["Commerce"]

#Products are identified by name, so there cannot be two products with the same
#name !
referenced_products = {
	"Apple": {"price": 1},
	"Orange": {"price": 1},
	"Bottle of water": {"price": 0.8}
}

#The list of stores
stores = [{"_id":1, "stock":{"Apple":50, "Orange":30, "Bottle of water": 20}, "checkouts":[1, 2], "sellers":[1, 2]}]

#The list of checkouts
checkouts = [{"_id":1}, {"_id":2}]

#The list of sellers
sellers = [{"_id":1, "name":"Nom d'un caissier"}, {"_id":2, "name":"Nom d'un autre caissier"}]

#We choose randomly a specific store to simulate for the session
store = choice(stores)

#The list of checkouts of this store
store_checkouts = [checkout for checkout in checkouts if checkout["_id"] in store["checkouts"]]

#The list of sellers of this store
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
    #Insert the receipt corresponding to the basket in the collection "Receipts" of the database db
    db["Receipts"].insert_one({"store_id": store["_id"], "checkout_id": choice(store_checkouts)["_id"], "seller_id": choice(store_sellers)["_id"], "basket": basket, "total_price": sum(product["price"] for product in basket.values())})
    #Indicate that the basket was effectively validated
    return "The basket is validated and the receipt has been added to the database."
