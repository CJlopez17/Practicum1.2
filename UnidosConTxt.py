import csv
import pandas as pd
import requests
import itertools
import matplotlib.pyplot as plt

API_KEY = 'cdb359dbf111cba0ccc61d7f992d0235'

def procesar_csv(ruta_archivo):
    # Leer el archivo CSV utilizando csv.reader
    with open(ruta_archivo, encoding='latin-1') as f:
        reader = csv.reader(f)
        data = list(reader)

    # Filtrar las filas que contienen como único valor los ";;"
    data_filtrados = list(filter(lambda row: not all(cell == ";;" for cell in row), data))

    # Crear un DataFrame a partir de los datos filtrados
    df = pd.DataFrame(data_filtrados)

    # Guardar el DataFrame procesado en un nuevo archivo CSV
    df.to_csv('data/edxapp-feedBack-11-5-23_procesado_original.csv', index=False)

    print("Archivo procesado guardado exitosamente.")

def analizar_sentimientos(texto):
    # Parámetros de la solicitud a MeaningCloud
    parametros = {
        'key': API_KEY,
        'txt': texto,
        'lang': 'es',
        'model': 'general',
        'txtf': 'plain',
        'url': ''
    }

    try:
        # Realizar la solicitud POST a la API de MeaningCloud
        respuesta = requests.post('https://api.meaningcloud.com/sentiment-2.1', data=parametros)
        respuesta.raise_for_status()  # Lanzar una excepción si ocurre un error de solicitud

        # Verificar si la respuesta es válida
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

# Procesar el archivo CSV
ruta_archivo = 'data/edxapp-feedBack-11-5-23.csv'
procesar_csv(ruta_archivo)

# Abrir el archivo CSV procesado
with open('data/edxapp-feedBack-11-5-23_procesado_original.csv', encoding='latin-1') as archivo:
    lector_csv = csv.reader(archivo)

    # Limitar el procesamiento a las filas
    primeras_filas = itertools.islice(lector_csv, 30)


    # Inicializar contadores para los sentimientos
    positivo = 0
    negativo = 0
    neutro = 0

    # Abrir archivo para guardar los resultados
    with open('sentimientos_resultados.txt', 'w', encoding='utf-8') as resultados_file:
        # Iterar sobre las filas limitadas
        for fila in primeras_filas:
            comentario = fila[0]  # Suponiendo que la columna está en el índice 0

            # Realizar análisis de sentimientos del comentario utilizando MeaningCloud
            resultado = analizar_sentimientos(comentario)

            # Procesar el resultado
            if resultado is not None and 'score_tag' in resultado:
                sentimiento = resultado['score_tag']
                if sentimiento == 'P':
                    positivo += 1
                elif sentimiento == 'N':
                    negativo += 1
                else:
                    neutro += 1

                # Guardar el comentario y el sentimiento en el archivo
                resultados_file.write(f"Comentario: {comentario}\n")
                resultados_file.write(f"Sentimiento: {sentimiento}\n")
                resultados_file.write("---\n")

# Crear la gráfica de barras
sentimientos = ['Positivo', 'Negativo', 'Neutro']
conteos = [positivo, negativo, neutro]

plt.bar(sentimientos, conteos)
plt.xlabel('Sentimiento')
plt.ylabel('Número de comentarios')
plt.title('Distribución de sentimientos en los comentarios')
plt.show()
