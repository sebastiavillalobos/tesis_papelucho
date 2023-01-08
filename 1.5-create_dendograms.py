import matplotlib.pyplot as plt
import scipy.cluster.hierarchy as shc
import pandas as pd
import librerias.decoratos as dc
import numpy as np

"""
https://docs.scipy.org/doc/scipy/reference/generated/scipy.cluster.hierarchy.linkage.html#scipy.cluster.hierarchy.linkage

Distancias euclidianas


Complete or Maximum: se calcula la distancia entre todos los posibles pares formados por una observación del cluster A y una del cluster B. La mayor de todas ellas se selecciona como la distancia entre los dos clusters. Se trata de la medida más conservadora (maximal intercluster dissimilarity).

Single or Minimum: se calcula la distancia entre todos los posibles pares formados por una observación del cluster A y una del cluster B. La menor de todas ellas se selecciona como la distancia entre los dos clusters. Se trata de la medida menos conservadora (minimal intercluster dissimilarity).

Average: Se calcula la distancia entre todos los posibles pares formados por una observación del cluster A y una del cluster B. El valor promedio de todas ellas se selecciona como la distancia entre los dos clusters (mean intercluster dissimilarity).

Centroid: Se calcula el centroide de cada uno de los clusters y se selecciona la distancia entre ellos como la distancia entre los dos clusters.

Ward: Se trata de un método general. La selección del par de clusters que se combinan en cada paso del agglomerative hierarchical clustering se basa en el valor óptimo de una función objetivo, pudiendo ser esta última cualquier función definida por el analista. El método Ward's minimum variance es un caso particular en el que el objetivo es minimizar la suma total de varianza intra-cluster. En cada paso, se identifican aquellos 2 clusters cuya fusión conlleva menor incremento de la varianza total intra-cluster. Esta es la misma métrica que se minimiza en K-means.
"""

#1. Carga el data set con los libros
# ==============================================================================
print('Cargando dataset...')

print('Dataset cargado.')
print('')
# lista los titulos de los libros

print("Creando dendogramas...")

def filter_by_value(csv_file, column, value):
    df = pd.read_csv(csv_file, index_col=0)
    df2 = df[df[column].str.contains(value)]
    #print(df2)
    return df2

#2. Dendograma
# ==============================================================================
@dc.timing
def create_dendograms(method, cut_height, dpi):
    df = pd.read_csv('clusteringFiles/data_all_books_scaled.csv', index_col=0)
    df1 = pd.read_csv('clusteringFiles/data_all_books_scaled_book.csv', index_col=0)
    df1 = pd.read_csv('clusteringFiles/data_all_books_transposed.csv', index_col=0)
    titulo_libros = list(df.index.values)    
    print(f"Metodo {method}")
    plt.figure(figsize=(11, 7))
    plt.title(f"Metodo {method}, frecuencia palabras")
    dend2 = shc.dendrogram(shc.linkage(df, method=method), labels=titulo_libros)
    plt.tight_layout()
    plt.xlabel("Libros")
    plt.ylabel("Distancia")
    plt.xticks(fontsize=7)
    plt.savefig(f'imagenes/dendogram-{method}.png', dpi=dpi)


@dc.timing
def create_dendograms_papelucho(method, cut_height, dpi):
    # FILTRO PAPELUCHO y luego cambio la columna al index para el clustering
    df = filter_by_value('clusteringFiles/data_all_books_scaled_book.csv', "book", 'Papelucho')
    df = df.set_index('book')

    titulo_libros = list(df.index.values)    
    print(f"Metodo {method}")
    #plt.figure(figsize=(11, 7))
    plt.title(f"Metodo {method} colección papelucho")
    dend2 = shc.dendrogram(shc.linkage(df, method=method), labels=titulo_libros)
    plt.xlabel("Libros")
    plt.ylabel("Distancia")
    plt.xticks(fontsize=7)
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig(f'imagenes/dendogram-papelucho-{method}.png', dpi=dpi)


@dc.timing
def create_dend_phrases(method, cut_height, dpi):
    print(f"Metodo {method}")
    meth = method
    dataframe = pd.read_csv("clusteringFiles/data_all_books_sentiments_median2.csv", index_col=0)
    print(dataframe)
    titulo_libros = list(dataframe.index.values)
    plt.figure(figsize=(13, 9))
    plt.title(f"Books Sentiment Dendograms Method:{method}")
    dend2 = shc.dendrogram(shc.linkage(dataframe, method=method), labels=titulo_libros)
    plt.axhline(y=cut_height, c = 'black', linestyle='--', label='altura corte')
    plt.savefig(f'clusteringFiles/dendogram-sentiment-{method}2.png')


def create_emotion_dendograms(method, cut_height, dpi):
    from sklearn.preprocessing import scale
    df = pd.read_csv("dataframe_libros/all_books_emotion_frequency.csv", index_col=0)

    datos_scaled = scale(X=df, axis=1, with_mean=True, with_std=True) 
    datos_scaled = pd.DataFrame(datos_scaled, columns=df.columns, index=df.index)
    # datos_scaled.reset_index(inplace=True)
    # datos_scaled.columns.values[0] = "book"

    print(datos_scaled.head(5))
    # FILTRAR QUE LIBROS MOSTRAR
    #datos_scaled = datos_scaled.query('book.str.contains("Papelucho")', engine='python')

    titulo_libros = list(df.index.values)    
    print(f"Metodo {method}")
    plt.figure(figsize=(11, 7))
    plt.title(f"Metodo {method}, frecuencia emociones")
    dend2 = shc.dendrogram(shc.linkage(datos_scaled, method=method), labels=titulo_libros)
    plt.tight_layout()
    plt.xlabel("Libros")
    plt.ylabel("Distancia")
    plt.xticks(fontsize=7)
    plt.savefig(f'imagenes/dendogram-emotion-7-{method}.png', dpi=dpi)


def create_phrases_positive_dendogram(method,cut_height,dpi):
    from sklearn.preprocessing import scale
    df = pd.read_csv("dataframe_libros/all_books_positive_phrases_analysis_100.csv", index_col=0)

    datos_scaled = scale(X=df, axis=1, with_mean=True, with_std=True) 
    datos_scaled = pd.DataFrame(datos_scaled, columns=df.columns, index=df.index)

    print(datos_scaled.head(5))
    # FILTRAR QUE LIBROS MOSTRAR
    #datos_scaled = datos_scaled.query('book.str.contains("Papelucho")', engine='python')

    titulo_libros = list(df.index.values)    
    print(f"Metodo {method}")
    plt.figure(figsize=(11, 7))
    plt.title(f"Metodo {method}, intensidad frases positivas")
    dend2 = shc.dendrogram(shc.linkage(datos_scaled, method=method), labels=titulo_libros)
    plt.tight_layout()
    plt.xlabel("Libros")
    plt.ylabel("Distancia")
    plt.xticks(fontsize=7)
    plt.show()
    plt.savefig(f'imagenes/dendogram_positive_phrases_{method}.png', dpi=dpi)

def create_phrases_negative_dendogram(method,cut_height,dpi):
    from sklearn.preprocessing import scale
    df = pd.read_csv("dataframe_libros/all_books_negative_phrases_analysis_100.csv", index_col=0)

    datos_scaled = scale(X=df, axis=1, with_mean=True, with_std=True) 
    datos_scaled = pd.DataFrame(datos_scaled, columns=df.columns, index=df.index)

    print(datos_scaled.head(5))
    # FILTRAR QUE LIBROS MOSTRAR
    #datos_scaled = datos_scaled.query('book.str.contains("Papelucho")', engine='python')

    titulo_libros = list(df.index.values)    
    print(f"Metodo {method}")
    plt.figure(figsize=(11, 7))
    plt.title(f"Metodo {method}, intensidad frases negativas")
    dend2 = shc.dendrogram(shc.linkage(datos_scaled, method=method), labels=titulo_libros)
    plt.tight_layout()
    plt.xlabel("Libros")
    plt.ylabel("Distancia")
    plt.xticks(fontsize=7)
    plt.show()
    plt.savefig(f'imagenes/dendogram_negative_phrases_{method}.png', dpi=dpi)

create_phrases_positive_dendogram('ward', 420 , 600)
create_phrases_negative_dendogram('ward', 420 , 600)
# create_emotion_dendograms('ward', 420 , 600)
# create_dendograms('ward', 420 , 600)
# create_dendograms('complete', 420 , 600)
# create_dendograms('average', 420 , 600)
# create_dend_phrases('ward', 420 , 1200)
# create_dend_phrases('complete', 420 , 1200)
# create_dend_phrases('average', 420 , 1200)


    # # Metodo ward
    # print("Metodo ward")
    # # normal
    # plt.figure(figsize=(13, 9))
    # plt.title("Books Dendograms Ward")
    # dend = shc.dendrogram(shc.linkage(data_set, method='ward'), labels=titulo_libros)
    # plt.savefig('dendogram-ward-normal.png', dpi=1200)

    # # scaled
    # plt.figure(figsize=(13, 9))
    # plt.title("Books Dendograms Ward Scaled")
    # dend2 = shc.dendrogram(shc.linkage(data_set_scaled, method='ward'), labels=titulo_libros)
    # plt.axhline(y=8, c = 'black', linestyle='--', label='altura corte')
    # plt.savefig('dendogram-ward-scaled.png', dpi=1200)

    # # Metodo average
    # print("Metodo average")
    # # normal
    # plt.figure(figsize=(13, 9))
    # plt.title("Books Dendograms Average")
    # dend = shc.dendrogram(shc.linkage(data_set, method='average'), labels=titulo_libros)
    # plt.savefig('dendogram-average-normal.png', dpi=1200)

    # # scaled
    # plt.figure(figsize=(13, 9))
    # plt.title("Books Dendograms Average Scaled")
    # dend2 = shc.dendrogram(shc.linkage(data_set_scaled, method='average'), labels=titulo_libros)
    # plt.axhline(y=10, c = 'black', linestyle='--', label='altura corte')
    # plt.savefig('dendogram-average-scaled.png', dpi=1200)

    # # Metodo complete
    # print("Metodo complete")
    # # normal
    # plt.figure(figsize=(13, 9))
    # plt.title("Books Dendograms Complete")
    # dend = shc.dendrogram(shc.linkage(data_set, method='complete'), labels=titulo_libros)
    # plt.savefig('dendogram-complete-normal.png', dpi=1200)

    # # scaled
    # plt.figure(figsize=(13, 9))
    # plt.title("Books Dendograms Complete Scaled")
    # dend2 = shc.dendrogram(shc.linkage(data_set_scaled, method='complete'), labels=titulo_libros)
    # plt.axhline(y=6, c = 'black', linestyle='--', label='altura corte')
    # plt.savefig('dendogram-complete-scaled.png', dpi=1200)

print('Proceso finalizado')