import time

def meture_execution_time(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"Tiempo: {func.__name__}: {end - start} segundos")
        return result
    return wrapper

@meture_execution_time
def testing():
    print('Funcion de prueba')
    print('Funcion de prueba')
    print('Funcion de prueba')
    print('Funcion de prueba')


