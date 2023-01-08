# FALTA ITERAR POR TODOS LOS LIBROS



import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from book_class import Book


book1 = Book("Papelucho.txt")
# Carga archivo
df_sentiments = pd.read_csv('dataframe_libros/sentiment_Papelucho.csv', index_col=0, names=["pos", "value"])


book_dict_df = pd.read_csv('dataframe_libros/df_Papelucho_with_dict.csv')
book_df = book1.book_df()



# 1. GRAFICOSs

# 1.1 word freq
def graph_wf(book):
    df = Book(book).freq_df()
    # transforma la serie a un dataframe
    df = pd.DataFrame(df)
    df.columns=['freq']
    df.reset_index(drop=False, inplace=True)
    # Solo los 10 más frecuentes
    df = df.head(10)
    df.plot(x='word',y='freq', kind='bar' )
    plt.show()




def filtra_por_lexicon():
    # Filtra por lexicon
    book_dict_df_nrc = book_dict_df[book_dict_df['lexicon'] == 'nrc'][book_dict_df['sentiment']== 'tristeza']
    book_dict_df_bing = book_dict_df[book_dict_df['lexicon'] == 'bing']


    book_dict_df_nrc.groupby(['word','sentiment']).size().unstack().plot(kind='bar',stacked=True)

    book_dict_df_bing.groupby(['sentiment','lexicon']).size().unstack().plot(kind='bar',stacked=True)



    # book_dict_df_bing.groupby(['word','sentiment']).size().unstack().plot(kind='bar',stacked=True)



    plt.show()



if __name__ == '__main__':
    graph_wf("Papelucho.txt")
    filtra_por_lexicon()