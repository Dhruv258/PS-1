# Assign your MongoDB URI to the mongopass variable
from pymongo import MongoClient
mongopass = "mongodb+srv://admin:1password2@cluster0.ppse8zf.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(mongopass)
db = client["shipment_details"]
collection = db["test"]
