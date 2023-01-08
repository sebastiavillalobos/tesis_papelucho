# Intercambia las columnas por filas
import pandas as pd
import librerias.decoratos as dc
#1. Carga el data set con los libros
# ==============================================================================
@dc.timing
def load_data():
    print('Cargando dataset...')
    data_set = pd.read_csv('clusteringFiles/data_all_books.csv', index_col=0)
    # Remplaza los NaN con 0
    data_set = data_set.fillna(0)
    data_set.index.name = None

    print(data_set.head(4)) # muestra los primeros 4 ...

    #2. Filas a columnas
    # ==============================================================================
    print('Despues de aplicar transpose')
    tdf1 = data_set.transpose()
    tdf1.to_csv('clusteringFiles/data_all_books_transposed.csv')
    print(tdf1.head(4))

load_data()