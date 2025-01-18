from pymongo import MongoClient
from app.database.db import db


class DatabaseOperation:
    def __init__(self) -> None:
        self.db = db
        self.users = self.db.Users

    def insert_entry(self, username, hashed_password, tokens=0):
        try:
            res = self.users.insert_one({"Username": username,
                                         "Password": hashed_password,
                                         "Tokens": tokens
                                         }).acknowledged
            print(res)
        except Exception as e:
            print('err', e)

    def update_token(self, username, amount):
        self.users.update_one({
            "Username": username},
            {
                "$set": {
                    "Tokens": amount
                }
        })
