from sklearn.metrics import pairwise_distances
from sklearn.preprocessing import scale
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#1. Carga el data set con los libros
# ==============================================================================
print('Cargando dataset...')
datos_scaled = pd.read_csv('clusteringFiles/data_all_books_scaled.csv', index_col=0)
#datos_scaled = pd.read_csv('data_all_books_transposed.csv', index_col=0)
print(datos_scaled.head(4)) 


#3. Cálculo de distancias
# ==============================================================================
print('------------------')
print('Distancia euclídea')
print('------------------')

distances = pairwise_distances(
                X      = datos_scaled,
                metric ='euclidean'
             )

# Se descarta la diagonal superior de la matriz
distances[np.triu_indices(n=distances.shape[0])] = np.nan

distances = pd.DataFrame(
                distances,
                columns=datos_scaled.index,
                index = datos_scaled.index
            )

print(distances.head(4)) 

# Crea archivo CSV
print("")

file_csv = "clusteringFiles/data_all_books_distances.csv"
print(f"Escribiendo archivo csv {file_csv}")
print("")
distances.to_csv(file_csv)
print(f"{file_csv} creado")


#4. Top n observaciones más similares
# ==============================================================================
# Se reestructura la matriz de distancias para poder ordenar los pares de observaciones por orden de distancia. MENOR = MÁS PARECIDO

top_distances = distances.melt(ignore_index=False, var_name="libro_b", value_name='distancia') \
    .rename_axis("libro_a") \
    .reset_index() \
    .dropna() \
    .sort_values('distancia') \
    #.head(3)


print(top_distances.head(4)) 
print("")
# Crea archivo CSV
file_csv = "clusteringFiles/top_distances.csv"
print(f"Escribiendo archivo csv {file_csv}")
print("")
top_distances.to_csv(file_csv, index=False)
print(f"{file_csv} creado")


#top_distances = pd.read_csv('top_distances.csv')



