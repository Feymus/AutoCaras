##@package docstring
#Created on Aug 20, 2017
#
#@author: Michael Choque

from flask import Flask
from flask import request
from flask import jsonify
from Controller.Controlador import Controlador


controlador = Controlador()
app = Flask(__name__, static_url_path='')


@app.route('/')
def main_index():
    return app.send_static_file('index.html')

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