from flask import request, jsonify, Blueprint, current_app
from flask_jwt_extended import create_access_token

AppController = Blueprint('app',__name__)

@AppController.route('/data/example_post',methods=['POST'])
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
    
@AppController.route('/data/example_put/<int:id>/<string:name>',methods=['PUT'])
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
    
@AppController.route('/data/example_delete/<int:id>',methods=['DELETE'])
def example_delete(id):
    return jsonify({
        "status":True,
        "data":{
            "message": 'Item deleted succefully'
        }
    })

