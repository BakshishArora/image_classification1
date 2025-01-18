from flask import jsonify, request
from flask_restful import Resource
from keras.applications import inception_v3

from app.controller.image_controller import Controller
from app.database.db import db
from app.database.db_connection import DatabaseOperation
from app.service.image_service import Validations, generate_return_dictionary


class Home(Resource):
    def get(self):
        return "Welcome to the HomePage."


class Register(Resource):
    def post(self):
        # We get the posted data from the user first
        posted_data = request.get_json()

        # get the username and password
        username = posted_data["username"]
        password = posted_data["password"]
        tokens = posted_data.get("token", 4)

        # check if the user already exists
        if Validations().user_exists(username):
            return jsonify({
                "status": 301,
                "message": "Invalid username, user alreday exists."
            })
        status = Controller.register_new_user(username, password, tokens)

        if status:
            # return success
            return jsonify({
                "status": 200,
                "message": "You have successfully signed up for the API."
            })

