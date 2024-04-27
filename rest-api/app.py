# -*- coding: utf-8 -*-
#################################
# IMPORTS 
#################################
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from waitress import serve
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os
from datetime import timedelta
from flask_jwt_extended import JWTManager
from flask_jwt_extended import jwt_required
from flask_jwt_extended import create_access_token

#################################
# CONFIG 
#################################
app_flask = Flask(__name__)
app_flask.config['CORS_HEADERS'] = 'Content-Type'
app_flask.config['JWT_SECRET_KEY'] = os.getenv('PJ_TESTING_JWT_SECRET_KEY')
app_flask.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=120)

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

@app_flask.route('/app/create_access_token',methods=['GET'])
@limiter.limit('100/minute')
def create_access_toke_test():
    access_token = create_access_token(app_flask.config['JWT_SECRET_KEY'])
    return jsonify({
        "status":True,
        "data":{
            "message": access_token
        }
    })

@app_flask.route('/app/testing_secure_ping',methods=['GET'])
@limiter.limit('4/minute')
@jwt_required()
def testing_secure_ping():
    return jsonify({
        "status":True,
        "data":{
            "message": "Tienes permiso de ver el endpoint"
        }
    })


# GET
@app_flask.route('/app/ping',methods=['GET'])
@cross_origin()
@limiter.limit('10/day')
def ping():
    example_test = request.args.get('usuario')
    return jsonify({
        "status":True,
        "data":{
            "message": example_test
        }
    })
    
# POST
@limiter.limit('100/minute')
@app_flask.route('/data/example_post',methods=['POST'])
def example_post():
    try:
        data = request.json
        return jsonify({
            "status":True,
            "data":{
                "message": [data['id'],data['item']]
            }
        })
    # 1st catch 
    except ArithmeticError as aritmeticError:
        print(f"except #1 - aritmeticError: {aritmeticError}")
        return jsonify({
            "status":False,
            "data":str(aritmeticError)
        })
    # 1st catch 
    except NameError as nameError:
        print(f"except #2 - nameError: {nameError}")
    # last catch 
    except Exception as error:
        print(f"except #3 - Error: {error}")
    
#PUT
@app_flask.route('/data/example_put/<int:id>/<string:name>',methods=['PUT'])
def example_put(id,name):
    return jsonify({
        "status":True,
        "data":{
            "message": {
                "id":id,
                "name":name
            }
        }
    })
    
#DELETE
@app_flask.route('/data/example_delete/<int:id>',methods=['DELETE'])
def example_delete(id):
    return jsonify({
        "status":True,
        "data":{
            "message": 'Item deleted succefully'
        }
    })



#entry point 
if __name__ == '__main__':
    app_flask.run(port=3690)
    # serve(app_flask, host='0.0.0.0', port='3690', url_scheme='http')