import csv
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

def eliminar_stop_words(texto):
    stop_words = set(stopwords.words('spanish'))

    tokens = word_tokenize(texto)

    tokens_filtrados = [token for token in tokens if token.lower() not in stop_words]

    texto_filtrado = ' '.join(tokens_filtrados)

    return texto_filtrado

with open('data/edxapp-feedBack-11-5-23.csv', encoding='latin-1') as archivo:
    lector_csv = csv.reader(archivo)

    for fila in lector_csv:
        comentario = fila[0]

        comentario_filtrado = eliminar_stop_words(comentario)

        print('Comentario filtrado:', comentario_filtrado)
        print('---')
