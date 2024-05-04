from flask import Blueprint,current_app,jsonify,request
import csv

MysqlController = Blueprint('mysql',__name__)

# CREATE
@MysqlController.route('/usuario',methods=['POST'])
def create_usr():
    try:    
        print(request.json)
        usrname = request.json['nombre']
        email = request.json['correo']
        dictionary_cursor = current_app.config['mysq_dictionary_cursor']

        query = f"INSERT INTO usuarios (nombre, correo) VALUES ('{usrname}','{email}')"
        print(f"query: {query}")
        
        dictionary_cursor.execute(query)
        result = dictionary_cursor.fetchall()
        print(f"result: {result}")
        if len(result) == 0:    
            return jsonify({
                "status":True,
                "data":{
                    "message": 'El usuario se registró exitosamente'
                }
            })
        else:
            return jsonify({
                "status":False,
                "data":{
                    "message": 'El usuario no se registró'
                }
            })
    except Exception as endpointError:
        return jsonify({
                "status":False,
                "data":{
                    "message": str(endpointError)
                }
            })
        
# READ 
@MysqlController.route('/usuarios',methods=['GET'])
def get_usrs():
    #1 cursor
    # cursor = current_app.config['mysql_cursor']
    dictionary_cursor = current_app.config['mysq_dictionary_cursor']
    #2 query    
    query = f"SELECT * FROM usuarios"
    #3 execution
    # cursor.execute(query)
    #4 fetch
    # userList: [('Mariano', 'mariano@gmail.com')]
    # user_list = cursor.fetchall()
    
    dictionary_cursor.execute(query)
    # userList: [{'nombre': 'Mariano', 'correo': 'mariano@gmail.com'}]
    user_list = dictionary_cursor.fetchall()
    
    new_user_list = []
    
    for user in user_list:
        print(f"user: {user}")
        user['status'] = True
        new_user_list.append(user)

    print(f"userList: {user_list}")
    return jsonify({
        "status":True,
        "data":{
            "message": new_user_list
        }
    })

# UPDATE
@MysqlController.route('usuario/<string:name>/<string:email>',methods=['PUT'])
def update_user(name,email):
    try:
        dictionary_cursor = current_app.config['mysq_dictionary_cursor']

        query = f"UPDATE usuarios SET nombre = '{name}' WHERE correo = '{email}'"
        
        dictionary_cursor.execute(query)
        
        result = dictionary_cursor.fetchall()
        
        if len(result) == 0:    
            return jsonify({
                "status":True,
                "data":{
                    "message": 'El usuario se modificó exitosamente'
                }
            })
        else:
            return jsonify({
                "status":False,
                "data":{
                    "message": 'El usuario no se modificó'
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
@MysqlController.route('usuario/<string:email>',methods=['DELETE'])
def user_delete(email):
    try:
        dictionary_cursor = current_app.config['mysq_dictionary_cursor']

        query = f"DELETE FROM usuarios WHERE correo = '{email}'"
        
        dictionary_cursor.execute(query)
        result = dictionary_cursor.fetchall()
        print(f"result: {result}")
        if len(result) == 0:    
            return jsonify({
                "status":True,
                "data":{
                    "message": 'El usuario se eliminó exitosamente'
                }
            })
        else:
            return jsonify({
                "status":False,
                "data":{
                    "message": 'El usuario no se eliminó'
                }
            })
    except Exception as endpointError:
        return jsonify({
            "status":False,
            "data":{
                "message": str(endpointError)
            }
        })
        

@MysqlController.route('/cargaMasiva',methods=['POST'])
def upload_csv():
    if 'users' not in request.files:
        return jsonify({
            "status":False,
            "data":{
                "message": "No existe la llave 'users' en el formData"
            }
        })
    file = request.files['users']
    extension = file.filename.split('.')[1]
    if extension != 'csv':
        return jsonify({
            "status":False,
            "data":{
                "message": "La extension del archivo no es correcta, suba un archivo .csv"
            }
        })
        
    try:
        
        data = file.read().decode('utf-8').splitlines()
        csv_users = csv.reader(data)
        
        for row in csv_users:
            print(f"Nombre: {row[0]} - Correo: {row[1]}")
            
        return jsonify({
            "status":True,
            "data":{
                "message": "Debugging..."
            }
        })
        
    except Exception as fileError:
        return jsonify({
            "status":False,
            "data":{
                "message": f"Error en el archivo: {str(fileError)}"
            }
        })