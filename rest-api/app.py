# -*- coding: utf-8 -*-
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from waitress import serve
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os
from datetime import timedelta
from flask_jwt_extended import JWTManager

# Controllers section
from blueprints.apiController import ApiController
from blueprints.appController import AppController

JWT_SECRET_KEY = os.getenv('PJ_TESTING_JWT_SECRET_KEY')

# flask config
app_flask = Flask(__name__)
app_flask.app_context().push()

# flask config variables
app_flask.config['CORS_HEADERS'] = 'Content-Type'
app_flask.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY
app_flask.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=120)

# flask config packages
cors = CORS(app_flask,resources={
    r"/*": {
        "origins": [
            "https://hpwbf3p1-3690.usw3.devtunnels.ms/",
        ]
    }
})

limiter = Limiter(
    get_remote_address,
    app=app_flask,
    default_limits=['5/minute']
)

jwt = JWTManager(app_flask)

# Config DB

#Blueprints
app_flask.register_blueprint(ApiController, url_prefix='/api')
app_flask.register_blueprint(AppController, url_prefix='/app')

#entry point 
if __name__ == '__main__':
    app_flask.run(port=3690)
    # serve(app_flask, host='0.0.0.0', port='3690', url_scheme='http')