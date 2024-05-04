from flask import Blueprint,current_app,jsonify,request
from bson.objectid import ObjectId

MongoController = Blueprint('mongo',__name__)

# CREATE
@MongoController.route('/usuario',methods=['POST'])
def create_usr():
    try:    
        mongo_connection = current_app.config['mongo_connection']

        new_user = {
            "nombre":request.json['nombre'],
            "correo":request.json['correo']
        }
        try:
            mongo_connection.db.usuarios.insert_one(new_user)
            return jsonify({
                "status":True,
                "data":{
                    "message": 'El usuario se registró exitosamente'
                }
            })
        except Exception as insertError:
            return jsonify({
                "status":False,
                "data":{
                    "message": str(insertError)
                }
            })

    except Exception as endpointError:
        return jsonify({
            "status":False,
            "data":{
                "message": str(endpointError)
            }
        })
        
# READ ALL
@MongoController.route('/usuarios',methods=['GET'])
def read_usrs():
    try:    
        mongo_connection = current_app.config['mongo_connection']

        try:
            # result = list(mongo_connection.db.usuarios.find({},{'_id':False}))
            result = list(mongo_connection.db.usuarios.find({}))
            
            new_result = []
            
            for item in result:
                # print(f"ObjectId: {type(ObjectId(str(item['_id'])))}")
                # print(f"StringId: {type(str(item['_id']))}")
                temp_user ={
                    "_id": str(item['_id']),
                    "nombre":item['nombre'],
                    "correo":item['correo']
                }
                print(f"temp_user: {temp_user}")
                new_result.append(temp_user)
            return jsonify({
                "status":True,
                "data":{
                    "message": "Se obtuvieron la lista de los usuarios exitosamente",
                    "data":new_result
                }
            })
        except Exception as insertError:
            return jsonify({
                "status":False,
                "data":{
                    "message": str(insertError)
                }
            })

    except Exception as endpointError:
        return jsonify({
            "status":False,
            "data":{
                "message": str(endpointError)
            }
        })

# READ ONE
@MongoController.route('/usuario/<string:id>',methods=['GET'])
def read_usr(id):
    try:    
        mongo_connection = current_app.config['mongo_connection']
        try:
            print(f"id: {id}")
            
            # result = list(mongo_connection.db.usuarios.find_one({'_id':id},{'_id':False}))
            result = mongo_connection.db.usuarios.find_one({'_id':ObjectId(id)})
            
            user = {}
            
            if result:
                for item in result:
                    user[item] = str(result[item])
                
            return jsonify({
                "status":True,
                "data":{
                    "message": "Se obtuvieron la lista de los usuarios exitosamente",
                    "data":user
                }
            })
        except Exception as insertError:
            return jsonify({
                "status":False,
                "data":{
                    "message": str(insertError)
                }
            })
    except Exception as endpointError:
        return jsonify({
            "status":False,
            "data":{
                "message": str(endpointError)
            }
        })
        
#UPDATE
@MongoController.route('/usuario/<string:id>',methods=['PUT'])
def update_usr(id):
    try:    
        mongo_connection = current_app.config['mongo_connection']
        try:
            print(f"id: {id}")
            print(f"new name: {request.json['name']}")
            
            result = mongo_connection.db.usuarios.update_one({
                    '_id':ObjectId(id)
                },{
                    '$set':{
                        "nombre":request.json['name']
                    }
                }
            )
            
            print(f"result: {result.modified_count}")
            
            if result.modified_count >= 1:
                return jsonify({
                    "status":True,
                    "data":{
                        "message": "El usuario fue modificado exitosamente",
                        "data":True
                    }
                })
            else:
                return jsonify({
                    "status":False,
                    "data":{
                        "message": "El usuario no fue modificado exitosamente porque no hubo cambios que realizar",
                        "data":False
                    }
                })
        except Exception as updateError:
            return jsonify({
                "status":False,
                "data":{
                    "message": str(updateError)
                }
            })
    except Exception as endpointError:
        return jsonify({
            "status":False,
            "data":{
                "message": str(endpointError)
            }
        })

# DELETE
@MongoController.route('/usuario/<string:id>',methods=['DELETE'])
def delete_usr(id):
    try:    
        mongo_connection = current_app.config['mongo_connection']
        try:
            result = mongo_connection.db.usuarios.delete_one({'_id':ObjectId(id)})

            if result.deleted_count >= 1:
                return jsonify({
                    "status":True,
                    "data":{
                        "message": "El usuario fue eliminado exitosamente",
                        "data":True
                    }
                })
            else:
                return jsonify({
                    "status":False,
                    "data":{
                        "message": "El usuario no fue eliminado exitosamente",
                        "data":False
                    }
                })
        except Exception as updateError:
            return jsonify({
                "status":False,
                "data":{
                    "message": str(updateError)
                }
            })
    except Exception as endpointError:
        return jsonify({
            "status":False,
            "data":{
                "message": str(endpointError)
            }
        })
