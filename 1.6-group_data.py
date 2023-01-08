import matplotlib.pyplot as plt
import scipy.cluster.hierarchy as shc
import pandas as pd
import librerias.decoratos as dc
import numpy as np
from sklearn.cluster import AgglomerativeClustering

@dc.timing
def group_data(linkage, num_clusters):
    cluster = AgglomerativeClustering(n_clusters=num_clusters, affinity='euclidean', linkage=linkage)
    data = pd.read_csv('clusteringFiles/data_all_books_scaled.csv', index_col=0)
    cluster.fit_predict(data)
    print(cluster.labels_)
    plt.figure(figsize=(13, 9))
    plt.title(f"Data clustered with {linkage} ")
    plt.scatter(data.iloc[:,0], data.iloc[:,1], c=cluster.labels_, cmap='rainbow')
    plt.savefig(f'clustered-{linkage}.png', dpi=1200)
    print(f'clustered-{linkage}.png created')


# Numero de cluster obtenidos al dibujar una horizontal en los dendograms
group_data('ward', 10)
group_data('complete', 10)
group_data('average', 10)