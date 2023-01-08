# Tratamiento de datos
# ==============================================================================
import numpy as np
import pandas as pd
import statsmodels.api as sm

# Gráficos
# ==============================================================================
import matplotlib.pyplot as plt
import matplotlib.font_manager
from matplotlib import style
style.use('ggplot') or plt.style.use('ggplot')

# Preprocesado y modelado
# ==============================================================================
from sklearn.metrics import pairwise_distances
from sklearn.preprocessing import scale

# Configuración warnings
# ==============================================================================
import warnings
warnings.filterwarnings('ignore')

#1. Carga el data set con los libros
# ==============================================================================
print('Cargando dataset...')
datos = pd.read_csv('data_all_books2.csv', index_col=0)
# Remplaza los NaN con 0
datos = datos.fillna(0)
datos.index.name = None


print(datos.head(4)) # muestra los primeros 4 ...

#2. # Escalado de las variables
# ==============================================================================
print('Escalando los valores ...')
datos_scaled = scale(X=datos, axis=0, with_mean=True, with_std=True) 
datos_scaled = pd.DataFrame(datos_scaled, columns=datos.columns, index=datos.index)
datos_scaled.replace([np.inf, -np.inf], np.nan, inplace=True)

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
distances.to_csv('data_all_books2_distancias.csv', index=False)

#distances = pd.read_csv('data_all_books2_distancias.csv', index_col=0)
#print(distances.iloc[:4,:4])

#4. Top n observaciones más similares
# ==============================================================================
# Se reestructura la matriz de distancias para poder ordenar los pares de observaciones por orden de distancia.

top_distances = distances.melt(ignore_index=False, var_name="libro_b", value_name='distancia') \
    .rename_axis("libro_a") \
    .reset_index() \
    .dropna() \
    .sort_values('distancia') \
    .head(3)

print(type(top_distances))

print(top_distances)