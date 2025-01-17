from keras.applications import inception_v3
from keras.applications import imagenet_utils
from flask import jsonify

#Load the pretrained model 
pretrained_model = inception_v3.InceptionV3(weights="imagenet")

class ImageClassification:

    @classmethod
    def classify(self, img_array):
        try:
            prediction = pretrained_model.predict(img_array)
            actual_prediction = imagenet_utils.decode_predictions(prediction, top=5)

            return actual_prediction
        
        except Exception as e:
            return jsonify({"message": e})
