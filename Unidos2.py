import csv
import pandas as pd
import requests
import itertools
import matplotlib.pyplot as plt

API_KEY = 'cdb359dbf111cba0ccc61d7f992d0235'

def procesar_csv(ruta_archivo):
    with open(ruta_archivo, encoding='latin-1') as f:
        reader = csv.reader(f)
        data = list(reader)

    data_filtrados = list(filter(lambda row: not all(cell == ";;" for cell in row), data))

    df = pd.DataFrame(data_filtrados)

    df.to_csv('data/edxapp-feedBack-11-5-23_procesado_original.csv', index=False)

    print("Archivo procesado guardado exitosamente.")

def analizar_sentimientos(texto):
    parametros = {
        'key': API_KEY,
        'txt': texto,
        'lang': 'es',
        'model': 'general',
        'txtf': 'plain',
        'url': ''
    }

    try:
        respuesta = requests.post('https://api.meaningcloud.com/sentiment-2.1', data=parametros)
        respuesta.raise_for_status()
        if respuesta.content:
            datos = respuesta.json()
            return datos
        else:
            print('La respuesta de la API está vacía.')
            return None

    except requests.exceptions.HTTPError as error_http:
        print('Error en la solicitud HTTP:', error_http)
        return None
    except requests.exceptions.RequestException as error:
        print('Error en la solicitud:', error)
        return None

ruta_archivo = 'data/edxapp-feedBack-11-5-23.csv'
procesar_csv(ruta_archivo)

with open(ruta_archivo, encoding='latin-1') as archivo:
    lector_csv = csv.reader(archivo)

    primeras_filas = itertools.islice(lector_csv, 10)

    positivo = 0
    negativo = 0
    neutro = 0

    for fila in primeras_filas:
        comentario = fila[0]

        resultado = analizar_sentimientos(comentario)

        if resultado is not None and 'score_tag' in resultado:
            sentimiento = resultado['score_tag']
            if sentimiento == 'P':
                positivo += 1
            elif sentimiento == 'N':
                negativo += 1
            else:
                neutro += 1

sentimientos = ['Positivo', 'Negativo', 'Neutro']
conteos = [positivo, negativo, neutro]

plt.bar(sentimientos, conteos)
plt.xlabel('Sentimiento')
plt.ylabel('Número de comentarios')
plt.title('Distribución de sentimientos en los comentarios')
plt.show()
