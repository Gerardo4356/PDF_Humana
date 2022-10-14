import time
import os
from xml.dom.minidom import Element

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
#Webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#Para descargar imagen
import urllib
import base64


#Quitar notificaciones
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
#Para tensorflow
import pandas as pd
import numpy as np
import cv2
import imutils
from imutils import paths
import os
import os.path
import pickle
import matplotlib.pyplot as plt
from keras.models import load_model #requiere instalar CUDA (de nvidia) y además pip install tf-nightly-gpu (para que tensorflow reconozca CUDA 11)  Al parecer esta versión solo jala con CUDA 11.0
from sklearn.preprocessing import LabelBinarizer #pip install sklearn
import argparse


def captcha(input=r"unsolved_captcha\temp.jpg"):   


    ###################################################
    ###       Para usarlo como app externa          ###
    ###################################################
    # ap = argparse.ArgumentParser()
    # ap.add_argument("-i", "--input", required=True, help="/content/drive/MyDrive/Captcha/unsolved_captchas/2.jpg")
    # ap.add_argument("-o","--output", required=True, help="/content/drive/MyDrive/Captcha/output")
    # ap.add_argument("-m", "--model", required=True, help="/content/drive/MyDrive/Captcha/TRAINING_MODEL/my_model.h5")
    # ap.add_argument("-lb", "--labels", required=True, help="/content/drive/MyDrive/Captcha/TRAINING_MODEL/captcha_labels.pickle")
    # args = vars(ap.parse_args())
    ###################################################


    args = {
        'input' : input,
        'model' : "model\my_model2.h5",
        'labels' : "model\captcha_labels2.pickle"
            }

    print(args['input'])
    #Loading the model
    model = load_model(args['model'])
    with open(args['labels'], "rb") as f:
        lb = pickle.load(f)

    
    # Load the image and convert it to grayscale
    image = cv2.imread(args['input'])
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
    # Adding some extra padding around the image
    gray = cv2.copyMakeBorder(gray, 10, 10, 10, 10, cv2.BORDER_REPLICATE)

    # applying threshold
    thresh = cv2.threshold(gray, 220, 255, cv2.THRESH_BINARY, cv2.THRESH_OTSU)[1]
    gray = thresh #quitar
    # find the contours
    contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


        
    letter_image_regions = []

    # Now we can loop through each of the contours and extract the letter

    for contour in contours:
        # Get the rectangle that contains the contour
        (x, y, w, h) = cv2.boundingRect(contour)
        
        # checking if any counter is too wide
        # if countour is too wide then there could be two letters joined together or are very close to each other
        if w > 5:
            if w / h > 1.5:
                # Split it in half into two letter regions
                half_width = int(w / 2)
                letter_image_regions.append((x, y, half_width, h))
                letter_image_regions.append((x + half_width, y, half_width, h))
            else:
                letter_image_regions.append((x, y, w, h))
                

    # Sort the detected letter images based on the x coordinate to make sure
    # we get them from left-to-right so that we match the right image with the right letter  

    letter_image_regions = sorted(letter_image_regions, key=lambda x: x[0])

    # Create an output image and a list to hold our predicted letters
    output = cv2.merge([gray] * 3)
    predictions = []
        
    # Creating an empty list for storing predicted letters
    predictions = []
        
    # Save out each letter as a single image
    for letter_bounding_box in letter_image_regions:
        # Grab the coordinates of the letter in the image
        x, y, w, h = letter_bounding_box

        # Extract the letter from the original image with a 2-pixel margin around the edge
        letter_image = gray[y - 2:y + h + 2, x - 2:x + w + 2]

        letter_image = cv2.resize(letter_image, (30,30))
            
        # Turn the single image into a 4d list of images
        letter_image = np.expand_dims(letter_image, axis=2)
        letter_image = np.expand_dims(letter_image, axis=0)

        # making prediction
        pred = model.predict(letter_image)
            
        # Convert the one-hot-encoded prediction back to a normal letter
        letter = lb.inverse_transform(pred)[0]
        predictions.append(letter)


        # draw the prediction on the output image
        cv2.rectangle(output, (x - 2, y - 2), (x + w + 4, y + h + 4), (0, 255, 0), 1)
        cv2.putText(output, letter, (x - 5, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 0), 2)



    # Print the captcha's text
    captcha_text = "".join(predictions)
    return captcha_text

def webscraping(nss,curp,correo, headless = True):
    
    respuesta = "SISEC OK"
    
    
    service = ChromeService(executable_path=ChromeDriverManager().install())

    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    if headless: options.add_argument('headless')
    driver = webdriver.Chrome(service=service, options=options)
    # driver.maximize_window()

    driver.get("https://serviciosdigitales.imss.gob.mx/semanascotizadas-web/usuarios/IngresoAsegurado")

    
    #curp_campo
    campo = driver.find_element(By.XPATH, '//*[@id="CURP"]')
    campo.send_keys(curp)

    #nss_campo
    campo = driver.find_element(By.XPATH, '//*[@id="NSS"]')
    campo.send_keys(nss)
    
    #correo_campo
    campo = driver.find_element(By.XPATH, '//*[@id="Correo"]')
    campo.send_keys(correo)
    
    
    captcha_error = True    #Temp
    while captcha_error == True:
    #region captcha
        # get the image source
        img = driver.find_element(By.XPATH, '//*[@id="captchaImg"]')
        #save temp as base64
        img_captcha_base64 = driver.execute_async_script("""
        var ele = arguments[0], callback = arguments[1];
        ele.addEventListener('load', function fn(){
        ele.removeEventListener('load', fn, false);
        var cnv = document.createElement('canvas');
        cnv.width = this.width; cnv.height = this.height;
        cnv.getContext('2d').drawImage(this, 0, 0);
        callback(cnv.toDataURL('image/jpeg').substring(22));
        }, false);
        ele.dispatchEvent(new Event('load'));
        """, img)
        #download base64 image and transform to jpg
        with open(r"unsolved_captcha/"+str("temp")+".jpg", 'wb') as f:
            f.write(base64.b64decode(img_captcha_base64))

        try:
            captcha_text = captcha()
            campo = driver.find_element(By.XPATH, '//*[@id="captcha"]')
            campo.click()
            campo.send_keys(captcha_text)
        except:
            pass
        campo = driver.find_element(By.XPATH, '//*[@id="btnContinuar"]')
        campo.click()



        #Detectar error con captcha
        try:
            x = driver.find_element(By.XPATH, '//*[@id="divErrorCampos"]/p').text
            print(x)
            if x == "El NSS capturado no coincide con la CURP.":
                print("NSS: " + nss)
                print("CURP: " + curp)
                print("Cerrando proceso")
                driver.quit()
                respuesta = "El NSS capturado no coincide con la CURP."
        except:
            pass
        #Error en curp
        try:
            x = driver.find_element(By.XPATH, '//*[@id="mensajesError"]/div/p').text
            print(x)
            if x == "¡Error! CURP incorrecto. Por favor verifique.":
                print("NSS: " + nss)
                print("CURP: " + curp)
                print("Cerrando proceso")
                driver.quit()
                respuesta = x
        except:
            pass







        #endregion captcha
       
        #Mensaje de error 
        
        try:
            driver.find_element(By.XPATH, '//*[@id="formTurnar"]/h2')
            captcha_error = False
            continue
        except:
            #Hay un error, repite
            captcha_error = True
















    os.system('cls')
    
    #Click en constancia de semanas cotizadas
    campo = driver.find_element(By.XPATH, '//*[@id="formTurnar"]/div[2]/div/div[1]/h4/button')
    campo.click()
       

   
    try:
        campo = driver.find_element(By.XPATH, '//*[@id="detalle"]')
        driver.execute_script("arguments[0].click();", campo)
    except Exception as e: input(e)
    captcha_error = True
    while captcha_error == True:
    #region captcha
        # get the image source
        img = driver.find_element(By.XPATH, '//*[@id="captchaImg"]')
        #save temp as base64
        img_captcha_base64 = driver.execute_async_script("""
        var ele = arguments[0], callback = arguments[1];
        ele.addEventListener('load', function fn(){
        ele.removeEventListener('load', fn, false);
        var cnv = document.createElement('canvas');
        cnv.width = this.width; cnv.height = this.height;
        cnv.getContext('2d').drawImage(this, 0, 0);
        callback(cnv.toDataURL('image/jpeg').substring(22));
        }, false);
        ele.dispatchEvent(new Event('load'));
        """, img)
        #download base64 image and transform to jpg
        with open(r"unsolved_captcha/"+str("temp")+".jpg", 'wb') as f:
            f.write(base64.b64decode(img_captcha_base64))

        try:
            captcha_text = captcha()
            print("Captcha text: " + captcha_text)
            campo = driver.find_element(By.XPATH, '//*[@id="captcha"]')
            driver.execute_script("arguments[0].click();", campo)
            campo.send_keys(captcha_text)
        except Exception as e:
            input("Error en encontrar el campo del segundo captcha")
            pass
        
        

        
        
        
        
        campo = driver.find_element(By.XPATH, '//*[@id="btnContinuar"]')
        campo.click()
        #endregion captcha
        
        print("Esperando elemento")
        try:
            captcha_error = False
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="modEncuestaSatisfaccion"]/div/div'))).click()
        except Exception as e:
            
            print("Captcha tiene error")
            # print(e)
            captcha_error = True
        
        #Si se detecto el error, repetir, si hay otro error en esto, quiere decir que no se está introduciendo el captcha
        if captcha_error:
            print("Intentando procesar el error")
            try:
                driver.find_element(By.XPATH, '//*[@id="divErrorCampos"]/p/b')                              #Campo de error
                driver.find_element(By.XPATH, '//*[@id="btnCerrar"]').click()                               #Click en reintentar
                driver.find_element(By.XPATH, '//*[@id="formTurnar"]/div[2]/div/div[1]/h4/button').click()  #Click en constancia otra vez
            
            except:
                print("ERROR RARO AL ENVIAR EL SEGUNDO CAPTCHA, PUEDE SER DEL SITIO")
                respuesta = "SISEC ANORMAL"
                driver.quit()
                return respuesta

    
    
    #Si ya está presente el elemento
    print("Se realizó correctamente")
    driver.quit()
    return respuesta
    
    
    
    
    
if __name__ == "__main__":
    



    nss = "43796036085"
    curp = "LOVR600910HNLPLB02"
    correo = "gerardocamarillodl@gmail.com"
   
    webscraping(nss,curp,correo, headless =False)
    print("Listo")

