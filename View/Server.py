##@package docstring
#Created on Aug 20, 2017
#
#@author: Michael Choque

import os
from flask import Flask
from flask import request
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
        controlador.CargarImagenes(img_url)
        return "Okay"
    return app.send_static_file('index.html')



if __name__ == '__main__':
    app.run()