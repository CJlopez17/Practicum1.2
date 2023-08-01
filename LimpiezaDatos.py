import csv
import pandas as pd

def procesar_csv(ruta_archivo):
    with open(ruta_archivo, encoding='latin-1') as f:
        reader = csv.reader(f)
        data = list(reader)

    data_filtrados = list(filter(lambda row: not all(cell == ";;" for cell in row), data))

    df = pd.DataFrame(data_filtrados)

    df.to_csv('data/edxapp-feedBack-11-5-23_procesado_original.csv', index=False)

    print("Archivo procesado guardado exitosamente.")

ruta_archivo = 'data/edxapp-feedBack-11-5-23.csv'
procesar_csv(ruta_archivo)
