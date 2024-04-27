# -*- coding: utf-8 -*-

from flask import Flask, jsonify


app_flask = Flask(__name__)

@app_flask.route('/ping')
def ping():
    
    return jsonify({
        "status":True,
        "data":{
            "message": 'pong'
        }
    })
    

#entry point 
if __name__ == '__main__':
    app_flask.run(host='0.0.0.0', port=3690)