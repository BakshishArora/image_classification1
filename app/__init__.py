from flask import Flask, render_template
from flask_restful import  Api, Resource
from app.apis.classify import Classify
from app.apis.register import Register, Home
from app.apis.refill import Refill
from app.apis.protect import Auth
import os

app = Flask(__name__, template_folder=os.path.abspath('..//templates'), static_folder=os.path.abspath('..//static'))
app.secret_key = 'your_secret_key'
api = Api(app)

api.add_resource(Home, '/')
api.add_resource(Register, '/register')
api.add_resource(Auth, '/auth')
api.add_resource(Classify, '/classify')
api.add_resource(Refill, '/refill')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True )
