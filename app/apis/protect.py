from flask import jsonify, request
from flask_restful import Resource
from keras.applications import inception_v3

from app.controller.image_controller import Controller
from app.database.db import db
from app.database.db_connection import DatabaseOperation
from app.service.image_service import Validations, generate_return_dictionary
from app.service.auth import Authorize


class Auth(Resource):
    def post(self):
        posted_data = request.get_json()

        username = posted_data['username']
        password = posted_data['password']


        ret_json, error = Validations().verify_credentials(username, password)
        if error:
            return jsonify(ret_json)
        
        token = Authorize.encrypt(username)

        return jsonify(({"Token Enabled": token, "Valid for": "5m"}), 200)
        

