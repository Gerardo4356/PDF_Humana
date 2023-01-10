#Para py installer: pyinstaller -w -F --add-data "templates;templates" --add-data "static;static" app.py
from filecmp import DEFAULT_IGNORES
from re import I
from flask import Flask, render_template, request, redirect, url_for, flash, send_file
# import scraping
# import gmail
import diagnostico
import time
#Para detectar si no existe folder
import os

app = Flask(__name__)
verificaciones  = []
verificaciones_descarga = []
datos = ""

@app.route('/')
def Index():
    global verificaciones
    global verificaciones_descarga
    verificaciones  = []
    verificaciones_descarga  = []
    datos = ["","",""]

    return (render_template('manual.html', verificaciones=verificaciones, verificaciones_descarga=verificaciones_descarga))
    # return (render_template('home.html',datos=datos,verificaciones=verificaciones, verificaciones_descarga=verificaciones_descarga))

# @app.route('/diagnostico', methods=['GET', 'POST'])
# def general():
#     global verificaciones
#     global datos
#     global verificaciones_descarga
#     if request.method == "POST":
#         datos = []
#         if request.form.get('Descargar'):
#             print("Proceso SISEC..")
#             nss = request.form.get('nss')
#             curp = request.form.get('curp')
#             correo = request.form.get('correo')
#             print(correo)
#             print(curp)
#             print(nss)
#             try:
#                 res = scraping.webscraping(nss,curp,correo,headless=True)
#                 verificaciones_descarga.append(res)
#             except Exception as e:
#                 print(e)
#                 res = "Error con SISEC"
#                 verificaciones_descarga.append(res)

#         if request.form.get('Verificar'):
#             print("Proceso GMAIL..")
#             try:
#                 time.sleep(5)
#                 gmail.solicitar_constancias(gmail.access,gmail.wdriver())
#                 verificaciones.append("Gmail OK")
#                 print("Esperando a que lleguen los correos 5s")
#                 time.sleep(5)
#                 verificaciones.append(gmail.descargar_adjunto(gmail.access,gmail.wdriver()))
#                 verificaciones.append("PDF READY OK")
#             except Exception as e:
#                 verificaciones.append("Error en gmail")             
#                 print(e)

#             print("Verificar")

#         if request.form.get('Procesar'):
#             verificaciones = []
#             verificaciones_descarga = []
#             datos = []
#             print("Procesar")
#             diagnostico.diagnostico()
#             #something diferent
#         if request.form.get("Procesar_Manual"):
#             uploaded_file = request.files['ruta_pdf']
#             if uploaded_file.filename != '':
#                 uploaded_file.save(r"PDF/test0.pdf")
#                 diagnostico.diagnostico()

#     return render_template('home.html', verificaciones=verificaciones, datos=datos, verificaciones_descarga=verificaciones_descarga, check = 'checked="false"')

# @app.route('/automatico', methods=['GET', 'POST'])
# def automatico():
#     global verificaciones
#     global datos
#     global verificaciones_descarga
#     if request.method == "POST":
#         datos = []
#         if request.form.get('Descargar'):
#             print("Proceso SISEC..")
#             nss = request.form.get('nss')
#             curp = request.form.get('curp')
#             correo = request.form.get('correo')
#             print(correo)
#             print(curp)
#             print(nss)
#             try:
#                 res = scraping.webscraping(nss,curp,correo,headless=False)
#                 verificaciones_descarga.append(res)
#             except Exception as e:
#                 print(e)
#                 res = "Error con SISEC"
#                 verificaciones_descarga.append(res)

#         if request.form.get('Verificar'):
#             print("Proceso GMAIL..")
#             try:
#                 time.sleep(5)
#                 gmail.solicitar_constancias(gmail.access,gmail.wdriver())
#                 verificaciones.append("Gmail OK")
#                 print("Esperando a que lleguen los correos 5s")
#                 time.sleep(5)
#                 verificaciones.append(gmail.descargar_adjunto(gmail.access,gmail.wdriver()))
#                 verificaciones.append("PDF READY OK")
#             except Exception as e:
#                 verificaciones.append("Error en gmail")             
#                 print(e)

#             print("Verificar")

#         if request.form.get('Procesar'):
#             verificaciones = []
#             verificaciones_descarga = []
#             datos = []
#             print("Procesar")
#             diagnostico.diagnostico()

#     return render_template('automatico.html', verificaciones=verificaciones, datos=datos, verificaciones_descarga=verificaciones_descarga, check = 'checked="false"')



   
@app.route('/manual', methods=['GET', 'POST'])
def manual():
    global verificaciones
    global datos
    global verificaciones_descarga
    if request.method == "POST":
        datos = []

        if request.form.get("Procesar_Manual"):
            uploaded_file = request.files['ruta_pdf']
            if uploaded_file.filename != '':
                uploaded_file.save(r"PDF/test0.pdf")
                diagnostico.diagnostico()

    return render_template('manual.html', verificaciones=verificaciones, datos=datos, verificaciones_descarga=verificaciones_descarga, check = 'checked="false"')

    
if __name__ == "__main__":     # debug sirve en fase de pruebas para no tener que reiniciar a cada rato
    if not os.path.isdir("DIAGNOSTICOS"):
        os.makedirs("DIAGNOSTICOS")
        print("Creando carpeta DIAGNOSTICOS")
    if not os.path.isdir("PDF"):
        os.makedirs("PDF")
        print("Creando carpeta PDF")
    app.run(port=5000, debug=True)