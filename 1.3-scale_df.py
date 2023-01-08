import numpy as np
import pandas as pd
from sklearn.preprocessing import scale
import librerias.decoratos as dc


@dc.timing
def scale_data():
    #1. Carga el data set con los libros
    # ==============================================================================
    print('Cargando dataset...')
    data_set = pd.read_csv('clusteringFiles/data_all_books_transposed.csv', index_col=0)

    #2. Escala los valores 
    # ==============================================================================
    print('Escalando los valores ...')
    datos_scaled = scale(X=data_set, axis=1, with_mean=True, with_std=True) 
    datos_scaled = pd.DataFrame(datos_scaled, columns=data_set.columns, index=data_set.index)
    datos_scaled.replace([np.inf, -np.inf], np.nan, inplace=True)

    print(datos_scaled.head(4))

    #3. Crea archivo csv con los valores escalados
    # ==============================================================================
    print("Creando archivo data_all_books_scaled.csv")
    datos_scaled.to_csv('clusteringFiles/data_all_books_scaled.csv')

#cale_data()


#  rename columna 0
df = pd.read_csv('clusteringFiles/data_all_books_scaled.csv')

df.columns.values[0] = "book"

df = pd.read_csv('clusteringFiles/data_all_books_scaled_book.csv')

print(df.head(4))