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
