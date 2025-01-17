from app.database.db import users

class Database_operation:

    @classmethod
    def insert_entry(username, hashed_password, tokens=0):
        users.insert_one({"Username": username,
                            "Password": hashed_password,
                            "Tokens": tokens
                            })

    @classmethod 
    def update_token(username,amount):
        users.update_one({
            "Username": username},
            {
                "$set":{
                    "Tokens": amount
                }
            })
