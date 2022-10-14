from filecmp import DEFAULT_IGNORES
from re import I
from flask import Flask, render_template, request, redirect, url_for, flash, send_file
import scraping

app = Flask(__name__)
verificaciones  = []


@app.route('/')
def Index():
    global verificaciones
    verificaciones  = []
    datos = ["","",""]

    return (render_template('home.html',datos=datos))

@app.route('/diagnostico', methods=['GET', 'POST'])
def contact():
    global verificaciones
    if request.method == "POST":
        if request.form.get('Verificar'):
            datos = []
            nss = request.form.get('nss')
            curp = request.form.get('curp')
            correo = request.form.get('correo')
            print(correo)
            print(curp)
            print(nss)
            try:
                res = scraping.webscraping(nss,curp,correo,True)
            except:
                res = "Error con SISEC"
            datos.append(correo)
            datos.append(curp)
            datos.append(nss)
            verificaciones.append(res)
            print("Verificar")

        if request.form.get('Procesar'):
            verificaciones = []
            datos = []
            print("Procesar")

            #something diferent
            pass
    return render_template('home.html', verificaciones=verificaciones, datos=datos)

    
if __name__ == "__main__":     # debug sirve en fase de pruebas para no tener que reiniciar a cada rato
    app.run(port=5000, debug=True)