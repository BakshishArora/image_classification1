from flask import jsonify
import bcrypt

from app.database.db_connection import DatabaseOperation
from app.service.image_service import generate_return_dictionary
from app.service.image_service import ImageService

import bcrypt
import numpy as np
import requests

from PIL import Image
from io import BytesIO

from app.classification.model_operation import ImageClassification


class Controller:

    @classmethod
    def register_new_user(self, username, password, tokens):
        try:
            hashed_pw = bcrypt.hashpw(
                password.encode('utf8'), bcrypt.gensalt())

            # store the new user in database
            DatabaseOperation().insert_entry(username, hashed_pw, tokens)
            return True

        except Exception as e:
            return jsonify(generate_return_dictionary(503, "Database Not Connected"))

    @classmethod
    def url_based_image_classification(self, url):

        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        # pre process the image
        img_array = ImageService.image_preprocess(img)
        # make predictions
        actual_prediction = ImageClassification.classify(img_array)

        return actual_prediction

    @classmethod
    def file_based_image_classification(self, file):
        pass
