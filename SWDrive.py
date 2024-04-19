import requests
import webbrowser
from socket import AF_INET, socket, SOCK_STREAM
import json
import re


#-- coding: utf-8 --
import urllib.parse


def compartir(ID,email):
    id_archivo = ID
    url = f"https://www.googleapis.com/drive/v3/files/{id_archivo}/permissions"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    role = input("Introduce el rol del usuario (writer, commenter, reader): ")
    data = {
        "role": role,
        "type": "user",
        "emailAddress": email
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        print("Archivo compartido exitosamente.")
    else:
        print("Error al compartir el archivo.")    

def getIDArchivo(file_name):
    # Endpoint para buscar archivos por nombre
    search_url = f"https://www.googleapis.com/drive/v3/files?q=name='{file_name}'&fields=files(id)&access_token={access_token}"

    # Realizar la solicitud GET para buscar el archivo
    response = requests.get(search_url)

    # Verificar si la solicitud fue exitosa
    if response.status_code == 200:
        # Parsear la respuesta JSON
        response_json = response.json()
        # Obtener la lista de archivos que coinciden con el nombre
        files = response_json.get('files', [])
        # Verificar si se encontró algún archivo
        if files:
        # Retornar el ID del primer archivo encontrado
            return files[0]['id']
        else:
            print("No se encontraron archivos con ese nombre.")
            return None
    else:
        print("Error al buscar el archivo.")
        return None

def descargar(file_id4, archdescargar):  
    if file_id4:
        print(f"El ID del archivo '{archdescargar}' es: {file_id4}")
    else:
        print("No se pudo obtener el ID del archivo.")

        
    #descargar drive
    file_id = file_id4  
    download_url = f"https://www.googleapis.com/drive/v3/files/{file_id}?alt=media"

    download_response = requests.get(download_url, headers=headers)

    if download_response.status_code == 200:
        with open(archdescargar, "wb") as file:
            file.write(download_response.content)
        print("Descargado exitosamente")
    else:
        print("Error al descargar")

def subir(archsubir):
    if not archsubir.startswith("./"):
        archsubir = "./" + archsubir

    upload_url = "https://www.googleapis.com/upload/drive/v3/files?uploadType=resumable"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    try:
        metadata = {
            "name": re.search(r"/([^/]+)$", archsubir).group(1)  
        }

        response = requests.post(upload_url, headers=headers, json=metadata) 


        if response.status_code == 200:
            upload_location = response.headers["Location"]
            with open(archsubir, "rb") as file:
                file_content = file.read()
            response = requests.put(upload_location, data=file_content)
            if response.status_code == 200:
                print("Archivo subido exitosamente a Google Drive.")
            else:
                print("Error al subir el archivo a Google Drive.")
        else:
            print("Error al obtener la URL de carga para el archivo.")
    except AttributeError:
        print("Error al obtener el nombre del archivo.")

auth_code = ""
print("###################################")
print("OAuth 2.0 for Mobile & Desktop Apps")
print("###################################")
# https://developers.google.com/identity/protocols/oauth2/native-app

print("\nStep 1.- Prerequisites on Google Cloud Console")
print("\tEnable APIs for your project")
print("\tIdentify access scopes")
print("\tCreate authorization credentials")
print("\tConfigure OAuth consent screen")
print("\tAdd access scopes and test users")

client_id = "709685891477-ksuenm1c47n43jqr7rnct69mabe4eegq.apps.googleusercontent.com"
client_secret = "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"
scope = "https://www.googleapis.com/auth/drive"

redirect_uri = "http://127.0.0.1:8090"

print("\nStep 2.- Send a request to Google's OAuth 2.0 server")
uri = "https://accounts.google.com/o/oauth2/v2/auth"
datos = { 'client_id': client_id,
          'redirect_uri': redirect_uri,
          'response_type': 'code',
          'scope': scope}
datos_encoded = urllib.parse.urlencode(datos)

print("\tOpening browser...")
webbrowser.open_new ((uri +'?' + datos_encoded))

print("\nStep 3.- Google prompts user for consent")

print("\nStep 4.- Handle the OAuth 2.0 server response")

# Create a local server that listens on port 8090
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind(('localHost', 8090))
server_socket.listen(1)
print("\tLocal server listening on port 8090")

# Receive the 302 request from the browser
client_connection, client_address = server_socket.accept()
peticion = client_connection.recv(1024)
print("\tRequest from the browser received at local server:")

# Extract the "auth_code" from the request
primera_linea = peticion.decode('UTF8').split('\n')[0]
aux_auth_code = primera_linea.split(' ')[1]
auth_code = aux_auth_code[7:].split('&')[0]
print ("\tauth_code: " + auth_code)

# Send a response to the user
http_response = "HTTP/1.1 200 OK\r\n\r\n" \
                "<html>" \
                "<head><title>Prueba</title></head>" \
                "<body>The authentication flow has completed. Close this window.</body>" \
                "</html>"
client_connection.sendall(http_response.encode(encoding="utf-8"))
client_connection.close()
server_socket.close()

print("\nStep 5.- Exchange authorization code for refresh and access tokens")

uri = 'https://oauth2.googleapis.com/token'
cabeceras = {'Host': 'oauth2.googleapis.com',
             'Content-Type': 'application/x-www-form-urlencoded'}

datos = {'code': auth_code,
          'client_id': client_id,
          'client_secret': client_secret,
          'redirect_uri': redirect_uri,
          'grant_type': 'authorization_code'}
respuesta = requests.post(uri, headers=cabeceras, data=datos, allow_redirects=False)
status = respuesta.status_code
print("\tStatus: " + str(status))


contenido = respuesta.text
print("\tContenido:")
print(contenido)
contenido_json = json.loads(contenido)
access_token = contenido_json['access_token']
print("\taccess_token: " + access_token)

archsubir = input("Introduce la ruta del archivo a subir: ")
subir(archsubir)

archdescargar = input("Introduce el nombre del archivo a descargar: ") 
file_id4 = getIDArchivo(archdescargar)
descargar(file_id4, archdescargar)
archcompartir = input("Introduce el nombre del archivo a compartir: ")
email = input("Introduce el correo del usuario con el que deseas compartir el archivo: ")
compartir(getIDArchivo(archcompartir),email)
    
    
 