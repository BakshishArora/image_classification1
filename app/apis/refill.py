from flask import jsonify, request
from flask_restful import Resource
from keras.applications import inception_v3

from app.controller.image_controller import Controller
from app.database.db import db
from app.database.db_connection import DatabaseOperation
from app.service.image_service import Validations, generate_return_dictionary
from app.decorators.protect_route import protect_route

class Refill(Resource):
    @protect_route
    def post(self):
        # get posted data
        posted_data = request.get_json()

        # get credentials
        username = posted_data['username']
        password = posted_data['admin']
        amount = posted_data['amount']

        # check if user exists
        if not Validations().user_exists(username):
            return jsonify(generate_return_dictionary(301, "Invalid Username"))

        # check admin password
        if not Validations().validate_admin_password(password):
            return jsonify(generate_return_dictionary(302, "Incorrect Password"))

        # update the token and respond
        DatabaseOperation().update_token(username, amount)

        return jsonify(generate_return_dictionary(200, "Refilled"))
