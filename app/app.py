from flask import Flask, request, jsonify
from flask_restful import Api, Resource
import bcrypt 
import numpy as np
import requests

from keras.applications import inception_v3
from keras.applications.inception_v3 import preprocess_input
from keras.applications import imagenet_utils
from keras.preprocessing.image import img_to_array
from PIL import Image
from io import BytesIO

from service import Validations, generate_return_dictionary
from db_connection import db


app = Flask(__name__)
api = Api(app)

#Load the pretrained model 
pretrained_model = inception_v3.InceptionV3(weights="imagenet")

users = db["Users"]
# create APIs

class Register(Resource):
    def post(self):
        # We get the posted data from the user first
        posted_data = request.get_json()

        # get the username and password
        username = posted_data["username"]
        password = posted_data["password"]
        tokens = posted_data.get('token', 4)

        # check if the user already exists
        if Validations.user_exists(username):
            return jsonify({
                "status": 301,
                "message": "Invalid username, user alreday exists."
            })
        
        # if user is new hash password
        hashed_pw = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

        # store the new user in database
        users.insert_one({"Username": username,
                          "Password": hashed_pw,
                          "Tokens": tokens
                          })

        # return success 
        return jsonify({
            "status": 200,
            "message": "You have successfully signed up for the API."
        })
    
class Classify(Resource):
    def post(self):
        # get poseted data
        posted_data = request.get_json()

        # get credentials
        username = posted_data['username']
        password = posted_data['password']
        url = posted_data['url']

        # verify credentials
        ret_json, error = Validations.verify_credentials(username, password)
        if error:
            return jsonify(ret_json)

        # check if the user has tokens
        tokens = users.find({"Username": username})[0]["Tokens"]
        if tokens <= 0:
            return jsonify(generate_return_dictionary(303, "Not Enough Tokens"))

        # classify
        if not url:
            return jsonify(({"error": "No url provided"}), 400)
        
        # Load image from url
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))

        # pre process the image 
        img = img.resize((299,299))
        img_array = img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)

        # make predictions
        prediction = pretrained_model.predict(img_array)
        actual_prediction = imagenet_utils.decode_predictions(prediction, top=5)

        # return classification response
        ret_json = {}
        for pred in actual_prediction[0]:
            ret_json[pred[1]]= float(pred[2]*100)

        # reduce token
        users.update_one({
            "Username": username},
            {
                "$set":{
                    "Tokens": tokens-1
                }
            })
        
        return jsonify(ret_json)
    
class Refill(Resource):
    def post(self):
        # get posted data 
        posted_data = request.get_json()

        # get credentials
        username = posted_data['username']
        password = posted_data['admin']
        amount = posted_data['amount']

        # check if user exists
        if not Validations.user_exists(username):
            return jsonify(generate_return_dictionary(301, "Invalid Username"))
        

        #check admin password
        correct_pw = 'abc123'
        if not password == correct_pw:
            return jsonify(generate_return_dictionary(302, "Incorrect Password"))

        # update the token and respond
        users.update_one({
            "Username": username
        },{
            "$set": {
                "Tokens": amount
            }
        })

        return jsonify(generate_return_dictionary(200, "Refilled"))


api.add_resource(Register, '/register')
api.add_resource(Classify, '/classify')
api.add_resource(Refill, '/refill')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug = True )