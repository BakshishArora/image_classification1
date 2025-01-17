from db_connection import db
import bcrypt

users = db["Users"]

class Validations:

    @classmethod
    def user_exists(self,username):
        if users.count_documents({"Username": username}) == 0:
            return False 
        else:
            return True
        
    @classmethod
    def verify_pw(self,username, password):
        if not self.user_exists(username):
            return False
        
        hashed_pw = users.find({
            "Username": username
        })[0]["Password"]

        if bcrypt.hashpw(password.encode('utf8'), hashed_pw) == hashed_pw:
            return True
        else:
            return False
    
    @classmethod
    def verify_credentials(self,username, password):
        if not self.user_exists(username):
            return generate_return_dictionary(301, "Invalid Username"), True
        
        correct_pw = self.verify_pw(username, password)

        if not correct_pw:
            return generate_return_dictionary(302, "Incorrect Password"), True
        
        return None, False
    

def generate_return_dictionary(status, message):
    ret_json = {
        "status": status,
        "message": message
    }
    return ret_json


