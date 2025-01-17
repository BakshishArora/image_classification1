from pymongo import MongoClient

# Initailaize MongoClient

client = MongoClient("mongodb://127.0.0.1:27017")

# create a new db and collection 

db = client.ImageRecognition
users = db["Users"]

__all__ = ['db']