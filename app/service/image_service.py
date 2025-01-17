from app.database.db import users
import bcrypt
from app.config import Config
from keras.applications.inception_v3 import preprocess_input
from keras.preprocessing.image import img_to_array
import numpy as np


class Validations:

    @classmethod
    def user_exists(self, username):
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
    
    @classmethod 
    def validate_admin_password(self, admin):

        if admin == Config.ADMIN_PASSWORD:
            return True 
        
        return False
    
class ImageService:

    @classmethod
    def image_preprocess(img):

        img = img.resize((299,299))
        img_array = img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)

        return img_array

def generate_return_dictionary(status, message):
    ret_json = {
        "status": status,
        "message": message
    }
    return ret_json


