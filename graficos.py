from tarfile import TarFile
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# Carga archivo
data_set_sentiments = pd.read_csv('dataframe_libros/sentiment_Papelucho.csv', index_col=0, names=["pos", "value"])
data_set = pd.read_csv('dataframe_libros/df_Papelucho.csv')

# 1. GRAFICOS DE FRECUENCIA DE PALABRAS Y SENTIMIENTOS
data_set.groupby(['bing','nrc']).size().unstack().plot(kind='bar',stacked=True)



plt.show()
print(data_set.tail(4))



# 2. 
# Set un maximo de valores por libro
data_set_sentiments = data_set_sentiments.reset_index()
# Pasa los valores a una lista
data_values = data_set_sentiments['value'].values.tolist()
# Divide el arreglo en N partes, retorna una lista con los segmentos y su mediana
def prom_values_by_n(lista, n):
    new_list = np.array_split(lista, n)
    new_list = [(sum(list_values)/len(list_values)) for list_values in new_list]
    return new_list

# Genera una lista con 100 valores
print(prom_values_by_n(data_values, 100))

# Transforma la lista a un dataframe
data_set_sentiments = pd.DataFrame(prom_values_by_n(data_values, 100))

print(data_set_sentiments.head(4))
print(data_values)
#data_set_sentiments.plot(kind='bar',x='pos',y='value', color='blue')
data_set_sentiments.plot(kind='bar', color='blue')
plt.title("Papelucho FRASES")
plt.subplots_adjust(hspace=0.0) 
plt.show()