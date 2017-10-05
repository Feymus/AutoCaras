##@package docstring
#Created on Aug 20, 2017
#
#@author: Michael Choque
#@author: Nelson Gomez
#@author: William Espinoza

from flask import Flask
from flask import request
from flask import jsonify
from Controller.Controlador import Controlador


## Controlador de la aplicacion
controlador = Controlador()
## Servidor de la aplicacion
app = Flask(__name__, static_url_path='')


## Metodo main_index
#
# Este metodo manda el script principal de la pagina a la direccion http://127.0.0.1:5000/
@app.route('/')
def main_index():
    return app.send_static_file('index.html')

## Metodo submit_imgs_dir
#
# Recibe por POST la direccion local de los sujetos a cargar a la aplicacion
@app.route('/cargaimgs', methods=['GET', 'POST'])
def submit_imgs_dir():
    if request.method == 'POST':
        img_url = request.form['img_url']
        estado = controlador.CargarImagenes(img_url)
        
        respuesta = jsonify( 
            status=estado[0],
            msg=estado[1]
        )
        
        if estado[0] == 0:
            print(controlador.Entrenar())
            return respuesta
        return respuesta
    return app.send_static_file('index.html')



if __name__ == '__main__':
    app.run()