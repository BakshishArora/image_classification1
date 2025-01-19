from flask import jsonify, request
from flask_restful import Resource
from keras.applications import inception_v3

from app.controller.image_controller import Controller
from app.database.db import db
from app.database.db_connection import DatabaseOperation
from app.service.image_service import Validations, generate_return_dictionary
from app.decorators.protect_route import protect_route 

class Classify(Resource):
    @protect_route
    def post(self):
        # get poseted data
        posted_data = request.get_json()

        username = posted_data.get('username')
        url = posted_data.get('url', '')
        file = posted_data.get('file', '')

        # check if the user has tokens
        users = db.Users
        tokens = users.find({"Username": username})[0]["Tokens"]
        if tokens <= 0:
            return jsonify(generate_return_dictionary(303, "Not Enough Tokens"))

        # classify
        if not url and not file:
            return jsonify(({"error": "No url or image provided"}), 400)

        if url:
            actual_prediction = Controller.url_based_image_classification(url)

        if file:
            actual_prediction = Controller.file_based_image_classification(
                file)

        # return classification response
        ret_json = {}
        for pred in actual_prediction[0]:
            ret_json[pred[1]] = float(pred[2]*100)

        # reduce token
        DatabaseOperation().update_token(username, tokens-1)

        return jsonify({"Classification": ret_json})
