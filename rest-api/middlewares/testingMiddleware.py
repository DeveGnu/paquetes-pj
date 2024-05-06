from functools import wraps
from flask import request
from werkzeug.datastructures import ImmutableMultiDict

def testing_middleware(func):
    """
    Middleware que modifica la peticion para agregar una llave nueva al request
    """
    @wraps(func)
    def decorator_function(*args,**kwargs):
        #1 get info
        http = request.args.to_dict()
        #2 Modify data
        http['testingProperty'] = "Propiedad agregada en el middleware"
        http['estado'] = {
            "codigo":"1",
            "descripcion":"Guanajuato"
        }
        
        #3 Modify request making inmutable
        request.args = ImmutableMultiDict(http)
        
        #4 return
        return func(*args,**kwargs)
        
    return decorator_function