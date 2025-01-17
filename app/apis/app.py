from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from pymongo import MongoClient
from app.database.db import users

from keras.applications import inception_v3

from app.controller.image_controller import Controller
from app.service.image_service import Validations, generate_return_dictionary
from app.database.db_connection import Database_operation


# create APIs

class Register(Resource):
    def post(self):
        # We get the posted data from the user first
        posted_data = request.get_json()

        # get the username and password
        username = posted_data["username"]
        password = posted_data["password"]
        tokens = posted_data.get("token", 4)

        # check if the user already exists
        if Validations.user_exists(username):
            return jsonify({
                "status": 301,
                "message": "Invalid username, user alreday exists."
            })        
        status = Controller().register_new_user(username, password, tokens)

        if status:
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
        url = posted_data.get('url','')
        file = posted_data.get('file', '')


        # verify credentials
        ret_json, error = Validations.verify_credentials(username, password)
        if error:
            return jsonify(ret_json)

        # check if the user has tokens
        tokens = users.find({"Username": username})[0]["Tokens"]
        if tokens <= 0:
            return jsonify(generate_return_dictionary(303, "Not Enough Tokens"))

        # classify
        if not url or not file:
            return jsonify(({"error": "No url or image provided"}), 400)
        
        if url:
            actual_prediction = Controller.url_based_image_classification(url)

        if file:
            actual_prediction = Controller.file_based_image_classification(file)
        
        # return classification response
        ret_json = {}
        for pred in actual_prediction[0]:
            ret_json[pred[1]]= float(pred[2]*100)

        # reduce token
        Database_operation().update_token(username, tokens-1)
        
        
        return jsonify({"Classification": ret_json})
    
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
        if Validations.validate_admin_password(password):
            return jsonify(generate_return_dictionary(302, "Incorrect Password"))

        # update the token and respond
        Database_operation.update_token(username, amount)

        return jsonify(generate_return_dictionary(200, "Refilled"))
