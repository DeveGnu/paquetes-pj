from flask import request, jsonify, Blueprint, current_app
from flask_jwt_extended import create_access_token

ApiController = Blueprint('api',__name__)

@ApiController.route('/create_access_token',methods=['GET'])
def create_access_toke_test():
    access_token = create_access_token(current_app.config['JWT_SECRET_KEY'])
    return jsonify({
        "status":True,
        "data":{
            "message": access_token
        }
    })

@ApiController.route('/app/testing_secure_ping',methods=['GET'])
def testing_secure_ping():
    return jsonify({
        "status":True,
        "data":{
            "message": "Tienes permiso de ver el endpoint"
        }
    })


# GET
@ApiController.route('/ping',methods=['GET'])
def ping():
    example_test = request.args.get('usuario')
    return jsonify({
        "status":True,
        "data":{
            "message": example_test
        }
    })
