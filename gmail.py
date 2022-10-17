from __future__ import print_function

import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

#pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

from googleapiclient.errors import HttpError
# If modifying these scopes, delete the file token.json.
# SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
#Webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
# import scraping
import base64
from base64 import urlsafe_b64encode, urlsafe_b64decode


def access(printlabels=True):
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        # Call the Gmail API
        service = build('gmail', 'v1', credentials=creds)
        results = service.users().labels().list(userId='me').execute()
        labels = results.get('labels', [])
        
        if printlabels:
            if not labels:
                print('No labels found.')
                return
            print('Labels:')
            for label in labels:
                print(label['name'])

    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f'An error occurred: {error}')

    return service


def solicitar_constancias(access, driver):
    service = access(False)
    messages = service.users().messages().list(userId='me',q="label:humana is:unread subject:(Servicio Digital: Solicitud de Constancia de Semanas Cotizadas del Asegurado) ").execute()
    #Obtener id de mensajes
    if len(messages) > 1:    
        id_messages = []
        for message in messages['messages']:
            print(message['id'])
            id_messages.append(message['id']) 
            
        urls_tokens = []
        for i in range(len(id_messages)):
            print("---"+str(i)+"---")
            correo = service.users().messages().get(userId='me',id=id_messages[i],format='full').execute()['payload']['parts'][0]['parts'][0]['body']['data']        
            html = base64.b64decode(correo,"-_").decode()
            soup = BeautifulSoup(html, 'html.parser')
            enlace = soup.find_all("a")[1].get("href")
            urls_tokens.append(enlace)
            print(enlace)
    
        
            #Driver web para abrir los enlaces
        for url in urls_tokens:
            driver.get(url)
            time.sleep(1)
        driver.quit()

            #Marcas correos como leídos
        for i in id_messages:
            service.users().messages().modify(userId="me", id=i,body={"removeLabelIds": ['UNREAD']}).execute()

def descargar_adjunto(access,driver):
    service = access(False)
    messages = service.users().messages().list(userId='me',q="from:(historia.laboral@imss.gob.mx) has:attachment is:unread ").execute()
    
    if len(messages) > 1:    
        id_messages = []
        input(message)
        for message in messages['messages']:
            print(message['id'])
            id_messages.append(message['id']) 

        for i in range(len(id_messages)):
            correo = service.users().messages().get(userId='me',id=id_messages[i],format='full').execute()
            attachmentId = correo['payload']['parts'][1]['body']['attachmentId'] 
            attachment = service.users().messages().attachments().get(userId='me',messageId=id_messages[i],id=attachmentId).execute()['data']
            # attachment = "b'" + str(attachment) + "'"
            file = urlsafe_b64decode(attachment)
            #Falta extraer NSS y Nombre
            with open(r"PDF/test"+i+".pdf", "wb") as fh:
                fh.write(file)


def wdriver(headless=True):
    chrome_service = ChromeService(executable_path=ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    if headless: options.add_argument('headless')
    driver = webdriver.Chrome(service=chrome_service, options=options)
    return driver



if __name__ == '__main__':
    os.system('cls')
    driver = wdriver()
    descargar_adjunto(access,driver)



if __name__ == '__main_':
    os.system('cls')
    print("Cargando SCRAPING Y DRIVER...")
    #region Librerías
    import scraping
    driver = wdriver()
    #endregion
    while True:

        os.system('cls')
        print("Cargado, enter para comenzar...")
        #region DATOS
        # nss = "43836206698"
        # curp = "AIRL621115HCLRDP07"
        # nss = "43796036085"
        # curp = "LOVR600910HNLPLB02"
        # 43766025480 TOOF600118HNLRRR04
        correo = "ccantu@humana.mx"
        correo = "gerardocamarillodl@gmail.com"
        #endregion
        
        if input("Hacer scraping (Y/N):  ") == "Y":
            nss = input("NSS: ")
            curp = input("CURP: ")
            try: scraping.webscraping(nss,curp,correo,False)
            except: print("ERROR GRAVE")
            print("----Completada petición al sisec-----")
        
        input("Enter para proceso de correo ...")
        solicitar_constancias(access, driver)






        os.system("cls")
       