# -*- coding: utf-8 -*-
from flask import Flask, jsonify, request
from markupsafe import escape

app_flask = Flask(__name__)

# GET
@app_flask.route('/ping',methods=['GET'])
def ping():
    example_test = request.args.get('usuario')
    return jsonify({
        "status":True,
        "data":{
            "message": example_test
        }
    })
    
# POST
@app_flask.route('/example_post',methods=['POST'])
def example_post():
    data = request.json
    return jsonify({
        "status":True,
        "data":{
            "message": [data['id'],data['item']]
        }
    })
    
#PUT
@app_flask.route('/example_put/<int:id>/<string:name>',methods=['PUT'])
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
@app_flask.route('/example_delete/<int:id>',methods=['DELETE'])
def example_delete(id):
    return jsonify({
        "status":True,
        "data":{
            "message": 'Item deleted succefully'
        }
    })



#entry point 
if __name__ == '__main__':
    app_flask.run(host='0.0.0.0', port=3690)