import csv

def procesar_csv(ruta_archivo):
    with open(ruta_archivo, encoding='latin-1') as f:
        reader = csv.reader(f)
        for row in reader:
            print(row)

ruta_archivo = 'data\edxapp-feedBack-11-5-23 - copia.csv'
procesar_csv(ruta_archivo)