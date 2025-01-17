from flask import Flask
from flask_restful import  Api
from app.apis.app import Register, Classify, Refill

app = Flask(__name__)
api = Api(app)


api.add_resource(Register, '/register')
api.add_resource(Classify, '/classify')
api.add_resource(Refill, '/refill')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug = True )
