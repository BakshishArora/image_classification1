from pymongo import  MongoClient

client = MongoClient("mongodb://127.0.0.1:27017")
db = client.ImageRecognition
users = db["Users"]

__all__ = ['users']