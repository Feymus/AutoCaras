"""Este modulo inicia una instancia del servidor Flask
en la cual se hospeda la pagina donde se ingresa el directorio con las imagenes
a utilzar"""
#Created on Aug 20, 2017
#
#@author: Michael Choque
#@author: Nelson Gomez
#@author: William Espinoza
from __future__ import print_function
from flask import Flask
from flask import request
from flask import jsonify
from Controller.Controlador import Controlador
## Controlador de la aplicacion
CONTROLADOR = Controlador()
## Servidor de la aplicacion
APP = Flask(__name__, static_url_path='')
## Metodo main_index
#
@APP.route('/')
def main_index():
    """# Este metodo manda el script principal de la pagina a la direccion http://127.0.0.1:5000/"""
    return APP.send_static_file('index.html')
## Metodo submit_imgs_dir
#
@APP.route('/cargaimgs', methods=['GET', 'POST'])
def submit_imgs_dir():
    """# Recibe por POST la direccion local de los sujetos a cargar a la aplicacion"""
    if request.method == 'POST':
        ent_prefix = request.form['ent_prefix']
        energy_pct = request.form['energy_pct']
        img_url = request.form['img_url']
        estado = CONTROLADOR.cargar_imagenes(img_url)
        respuesta = jsonify(
            status=estado[0],
            msg=estado[1]
        )
        if estado[0] == 0:
            CONTROLADOR.entrenar(ent_prefix, int(energy_pct)/100)
            return respuesta
        return respuesta
    return APP.send_static_file('index.html')
@APP.route('/precision', methods=['GET', 'POST'])
def get_precision():
    """ Recibe por POST la direccion local de los sujetos a cargar para pruebas """
    if request.method == 'POST':
        num_entrenar = request.form['num_entrenar']
        img_url = request.form['img_url']
        num_entrenar = 10 - (int(num_entrenar)//10)
        estado = CONTROLADOR.cargar_imagenes(img_url, _num_para_entrenar=num_entrenar)
        respuesta = jsonify(
            status=estado[0],
            msg=estado[1]
        )
        if estado[0] == 0:
            CONTROLADOR.entrenar("PRUEBAS", 0.85)
            CONTROLADOR.get_precision()
            return respuesta
        return respuesta
    return APP.send_static_file('index.html')
if __name__ == '__main__':
    APP.run()
    