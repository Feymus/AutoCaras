"""Este modulo inicia una instancia del servidor Flask
en la cual se hospeda la pagina donde se ingresa el directorio con las imagenes
a utilzar

Created on Aug 20, 2017

@author: Michael Choque
@author: Nelson Gomez
@author: William Espinoza
"""
from __future__ import print_function
from flask import Flask
from flask import request
from flask import jsonify
from Controller.FacadeOperador import FacadeOperador
from Controller.FacadeUsuario import FacadeUsuario
from Controller.Facade import Facade
## Controlador de la aplicacion
FACADE = Facade()
CONTROLADOROP = FacadeOperador(FACADE)
CONTROLADORUC = FacadeUsuario(FACADE)
## Servidor de la aplicacion
APP = Flask(__name__, static_url_path='')
## Metodo main_index
#
@APP.route('/')
def main_index():
    """ Este metodo manda el script principal de la pagina a la direccion http://127.0.0.1:5000/"""
    return APP.send_static_file('index.html')
## Metodo submit_imgs_dir
#
@APP.route('/cargaimgs', methods=['GET', 'POST'])
def submit_imgs_dir():
    """ Recibe por POST la direccion local de los sujetos a cargar a la aplicacion"""
    if request.method == 'POST':
        ent_prefix = request.form['ent_prefix']
        energy_pct = request.form['energy_pct']
        img_url = request.form['img_url']
        estado = CONTROLADOROP.cargar_imagenes(img_url)
        respuesta = jsonify(
            status=estado[0],
            msg=estado[1]
        )
        if estado[0] == 0:
            CONTROLADOROP.entrenar(ent_prefix, int(energy_pct)/100)
            #sujeto = CONTROLADORUC.clasificar("../Images/s41/8.pgm", ent_prefix, False)
            #print("Sujeto: ", sujeto)
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
        estado = CONTROLADOROP.cargar_imagenes(img_url, num_entrenar)
        if estado[0] == 0:
            CONTROLADOROP.entrenar("PRUEBAS", 0.85)
            estado = CONTROLADOROP.get_precision()
            respuesta = jsonify(
                status=estado[0],
                msg=estado[1]
            )
            return respuesta
        return respuesta
    return APP.send_static_file('index.html')
if __name__ == '__main__':
    APP.run()
    