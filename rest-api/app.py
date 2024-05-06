# -*- coding: utf-8 -*-
from flask import Flask
from flask_cors import CORS
# from waitress import serve
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os
from datetime import timedelta
from flask_jwt_extended import JWTManager
import mysql.connector
from flask_pymongo import PyMongo

# Controllers section
from blueprints.apiController import ApiController
from blueprints.appController import AppController
from blueprints.mysqlController import MysqlController
from blueprints.mongoController import MongoController

JWT_SECRET_KEY = os.getenv('PJ_TESTING_JWT_SECRET_KEY')

# Mysql
MYSQL_HOST= os.getenv('MYSQL_HOST')
MYSQL_PORT= os.getenv('MYSQL_PORT')
MYSQL_USERNAME= os.getenv('MYSQL_USERNAME')
MYSQL_PASSWORD= os.getenv('MYSQL_PASSWORD')
MYSQL_DB= os.getenv('MYSQL_DB')
#MongoDB
MONGO_HOST= os.getenv('MONGO_HOST')
MONGO_PORT= os.getenv('MONGO_PORT')
MONGO_USERNAME= os.getenv('MONGO_USERNAME')
MONGO_PASSWORD= os.getenv('MONGO_PASSWORD')
MONGO_DB= os.getenv('MONGO_DB')


# flask config
app_flask = Flask(__name__)
app_flask.app_context().push()

# flask config variables
app_flask.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY
app_flask.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=120)
app_flask.config['CORS_HEADERS'] = 'Content-Type'
app_flask.config['MONGO_URI'] = f"mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB}?authSource=admin"

# flask config packages
cors = CORS(app_flask,resources={
    r"/*": {
        "origins": [
            "http://localhost:3690",
        ]
    }
})

limiter = Limiter(
    get_remote_address,
    app=app_flask,
    default_limits=['5/minute']
)

jwt = JWTManager(app_flask)
mongo_connection = PyMongo(app_flask)
# mongo_connection = PyMongo(app_flask,f"mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB}?authSource=admin")

# Mysql
mysql_connection = mysql.connector.connect(
    host=MYSQL_HOST,
    user=MYSQL_USERNAME,
    password=MYSQL_PASSWORD,
    database=MYSQL_DB,
    port=MYSQL_PORT,
    charset='utf8'
)

#cursor
mysql_cursor = mysql_connection.cursor()
mysq_dictionary_cursor = mysql_connection.cursor(dictionary=True)

app_flask.config['mysql_cursor'] = mysql_cursor
app_flask.config['mysq_dictionary_cursor'] = mysq_dictionary_cursor
app_flask.config['mongo_connection'] = mongo_connection

#Blueprints
app_flask.register_blueprint(ApiController, url_prefix='/api')
limiter.limit('400/minute')(ApiController)

app_flask.register_blueprint(AppController, url_prefix='/app')
limiter.limit('200/minute')(AppController)

app_flask.register_blueprint(MysqlController, url_prefix='/mysql')
limiter.limit('200/minute')(MysqlController)

app_flask.register_blueprint(MongoController, url_prefix='/mongo')
limiter.limit('200/minute')(MongoController)

#entry point 
if __name__ == '__main__':
    app_flask.run(port=3690)
    # serve(app_flask, host='0.0.0.0', port='3690', url_scheme='http')