from operator import index, neg
from re import M
from book_class import Book
from librerias.books_files import LIST_OF_ALL_BOOKS, LIST_OF_PAPELUCHO, LIST_OF_HARRY
import pandas as pd
#import asyncio
import librerias.decoratos as dc
import matplotlib.pyplot as plt
import seaborn as sns

blue_colors = ['#00FFFF','#E0FFFF','#AFEEEE','#7FFFD4','#40E0D0','#48D1CC','#00CED1','#5F9EA0','#4682B4','#B0C4DE','#B0E0E6','#ADD8E6','#87CEEB','#87CEFA','#00BFFF','#1E90FF','#6495ED','#7B68EE','#4169E1','#0000FF','#0000CD','#00008B','#000080','#191970']
purple_colors = ['#DDA0DD','#EE82EE','#DA70D6','#FF00FF','#FF00FF','#BA55D3','#9370DB','#663399','#8A2BE2','#9400D3','#9932CC','#8B008B','#800080','#4B0082','#6A5ACD','#483D8B','#7B68EE']
red_colors = ['#CD5C5C','#F08080','#FA8072','#E9967A','#FFA07A','#DC143C','#FF0000','#B22222','#8B0000']
green_colors = ['#ADFF2F','#7FFF00','#7CFC00','#00FF00','#32CD32','#98FB98','#90EE90','#00FA9A','#00FF7F','#3CB371','#2E8B57','#228B22','#008000','#006400','#9ACD32','#6B8E23','#808000','#556B2F','#66CDAA','#8FBC8B','#20B2AA','#008B8B','#008080']

# ordena por columna
def sort_by_column(csv_file, column):
    df = pd.read_csv(csv_file, index_col=0)
    df = df.sort_values(by=[column], ascending=False)
    print(df.head(5))
    print(df.tail(5))
    return df

# agrupa por valor
def filter_by_value(csv_file, column, value):
    df = pd.read_csv(csv_file, index_col=0)
    print(df.columns.tolist())
    df2 = df[df[column].str.contains(value)]
    print(df2)
    return df2
    
def word_frequency(book):
    book = Book(book)
    df = pd.read_csv(f"dataframe_libros/df_{book.tittle}_with_dict.csv", index_col=0)
    frequency = df["word"].value_counts()
    frequency = pd.DataFrame(frequency)
    frequency.reset_index(inplace=True)
    frequency.columns.values[0] = "word"
    frequency.columns.values[1] = "frequency"
    frequency = frequency.sort_values(by=["frequency"], ascending=False)
    print(frequency.head(5))
    return frequency

# CAMBIAR EL DF QUE LEEEEEEEE. retorna un DF
def column_frequency(df, column):
    frequency = df
    frequency = frequency[column].value_counts()
    frequency = pd.DataFrame(frequency)
    frequency.reset_index(inplace=True)
    frequency.columns.values[0] = column
    frequency.columns.values[1] = "frequency"
    print(frequency.head(10))
    return frequency

def plot_frequency(book):
    df = word_frequency(book)
    df = df.head(10)
    #df.plot(x ='book', y='complexity', kind = 'bar', color = 'b', width = 0.9, figsize=(16, 9))
    df.plot(x ='word', y='frequency', kind = 'bar', color = 'c', width = 0.7)
    plt.title(f"top 10 palabras más frecuentes en {book[:-4]}")
    plt.xlabel("Palabras")
    #plt.ylabel("Cantidad")
    plt.xticks(fontsize=8)
    plt.tight_layout()
    plt.savefig(f"imagenes/frequency/freq_{book[:-4]}.png", bbox_inches='tight')


def plot_all_papeluchos():
    for book in LIST_OF_PAPELUCHO:
        plot_frequency(book)

# Agregar a la misma columna la info
def sum_words_of_books(LIST_OF_BOOKS):
    df1 = pd.DataFrame(columns=['word'])
    for book in LIST_OF_BOOKS:
        book = Book(book)
        df2 = pd.read_csv(f"dataframe_libros/df_{book.tittle}_with_dict.csv", index_col=0)
        # usa la columna [word] y la retorna como una df
        df2 = df2[["word"]]
        # agrega en la misma columna la data
        df1 = pd.concat([df1, df2], ignore_index = True, axis = 0)
    # DESCOMENTAR PARA QUE SUME 
    df1 = column_frequency(df1, 'word')
    print(df1)
    df1.to_csv("dataframe_libros/all_books_frequency.csv", index=False)
    return(df1)

def plot_papelucho_freq(df):
    df = df.head(20)
    print(df)
    #df.plot(x ='book', y='complexity', kind = 'bar', color = 'b', width = 0.9, figsize=(16, 9))
    df.plot(x ='word', y='frequency', kind = 'bar', color = 'b', width = 0.7)
    plt.title(f"top 20 palabras más frecuentes")
    plt.xlabel("Palabras")
    #plt.ylabel("Cantidad")
    plt.xticks(fontsize=8)
    plt.tight_layout()
    plt.savefig(f"imagenes/frequency/freq_all_books.png", bbox_inches='tight')



# -----------------------------------------
# FRECUENCIA EMOCIONES Y SENTIMIENTOS
# -----------------------------------------

def get_bing_sentiment_df(book):
    book = Book(book)
    df = pd.read_csv(f"dataframe_libros/df_{book.tittle}_with_dict.csv", index_col=0)
    df = df.query('lexicon=="bing"')
    print(df.head(5))
    return df

def get_nrc_emotion_df(book):
    book = Book(book)
    df = pd.read_csv(f"dataframe_libros/df_{book.tittle}_with_dict.csv", index_col=0)
    df = df.query('lexicon=="nrc" & sentiment != "positivo" & sentiment != "negativo"')
    return df

def get_nrc_sentiment_df(book):
    book = Book(book)
    df = pd.read_csv(f"dataframe_libros/df_{book.tittle}_with_dict.csv", index_col=0)
    df = df.query('lexicon=="nrc" & sentiment == "positivo" | sentiment == "negativo"')
    return df

def plot_nrc_frequency(book, analisys):
    df = pd.DataFrame()
    if analisys=="emotion":
        df = get_nrc_emotion_df(book)
    if analisys=="sentiment":
        df = get_nrc_sentiment_df(book)
    #df.plot(x ='book', y='complexity', kind = 'bar', color = 'b', width = 0.9, figsize=(16, 9))
    df = column_frequency(df, "sentiment")
    df.plot(x ='sentiment', y='frequency', kind = 'bar', color = 'c', width = 0.7)
    plt.title(f"top emociones más frecuentes en {book[:-4]}")
    plt.legend(['Frecuencia'])
    plt.xlabel("Emociones")
    plt.ylabel("Frequencia")
    plt.xticks(fontsize=8)
    plt.tight_layout()
    plt.savefig(f"imagenes/frequency/freq_{book[:-4]}_{analisys}_.png", bbox_inches='tight')

# Agregar a las mismas columnas la info de los libros
def sum_sentiments_of_books(LIST_OF_BOOKS, analisys):
    df1 = pd.DataFrame(columns=[analisys, 'frequency'])
    df2 = pd.DataFrame()
    file_name = 'ERROR'

    if LIST_OF_BOOKS == LIST_OF_ALL_BOOKS:
        file_name = "all_books"
    if LIST_OF_BOOKS == LIST_OF_PAPELUCHO:
        file_name = "all_papelucho"
    if LIST_OF_BOOKS == LIST_OF_HARRY:
        file_name = "all_harry_potter"

    for book in LIST_OF_BOOKS:
        #book = Book(book)
        if analisys=="emotion":
            df2 = get_nrc_emotion_df(book)
        if analisys=="sentiment":
            df2 = get_nrc_sentiment_df(book)
        # agrega en la misma columna la data
        df1 = pd.concat([df1, df2], ignore_index = True, axis = 0)
    # SUMA LAS FRECUENCIAS
    df1 = column_frequency(df1, "sentiment")
    print(df1)
    df1.to_csv(f"dataframe_libros/{file_name}_{analisys}_frequency.csv", index=False)
    return(df1)


#all_books_analisys_df(LIST_OF_ALL_BOOKS, "emotion")
#all_books_analisys_df(LIST_OF_ALL_BOOKS, "sentiment")

def all_books_analisys_df(LIST_OF_BOOKS, analisys):
    for book in LIST_OF_BOOKS:
        df = pd.DataFrame()
    #book = Book(book)
        if analisys=="emotion":
            df = get_nrc_emotion_df(book)
        if analisys=="sentiment":
            df = get_nrc_sentiment_df(book)
        book = Book(book)
        print(book.tittle)
        df = column_frequency(df, "sentiment")
        print(df.head(5))
        df = df.sort_values(by=['sentiment'])
        print(df.head(5))
        df.to_csv(f"dataframe_libros/df_{book.tittle}_{analisys}_frequency.csv", index=False)


# CREA DF CON CADA LIBRO
# analisis_list = [LIST_OF_ALL_BOOKS, LIST_OF_PAPELUCHO, LIST_OF_HARRY]
#     for analysis in analisis_list:
#         merge_sentiments_df(analysis, "emotion")
#         merge_sentiments_df(analysis, "sentiment")
def merge_sentiments_df(LIST_OF_BOOKS, analisys):
    file_name = ''
    if LIST_OF_BOOKS == LIST_OF_ALL_BOOKS:
        file_name = "all_books"
    if LIST_OF_BOOKS == LIST_OF_PAPELUCHO:
        file_name = "all_papelucho"
    if LIST_OF_BOOKS == LIST_OF_HARRY:
        file_name = "all_harry_potter"

    df_all_books = pd.DataFrame(columns=['sentiment', 'freq'])
    for book in LIST_OF_BOOKS:
        df_new = pd.read_csv(f"dataframe_libros/df_{Book(book).tittle}_{analisys}_frequency.csv", index_col=0)
        df_new.sort_values(by=['sentiment'])
       # df_new.columns = ['word', 'freq']
        df_all_books = pd.merge(df_all_books, df_new, on='sentiment', how='outer')
        df_all_books.columns = df_all_books.columns = [*df_all_books.columns[:-1], Book(book).tittle]
        df_all_books = df_all_books.fillna(0)
    #df_all_books.drop("freq_x", axis=1, inplace=True)
    df_all_books.drop(columns=df_all_books.columns[0], axis=1, inplace=True)
    df_all_books.drop(columns=df_all_books.columns[0], axis=1, inplace=True)
    if analisys == "emotion":
        df_all_books = df_all_books.transpose()
        df_all_books.columns = ["alegría", "asombro", "confianza", "disgusto", "ira", "miedo", "premonición", "tristeza"]
        print(df_all_books.head(5))
    if analisys == "sentiment":
        df_all_books = df_all_books.transpose()
        df_all_books.columns = ["negativo", "positivo"]
        print(df_all_books.head(5))
    df_all_books.to_csv(f'dataframe_libros/{file_name}_{analisys}_frequency.csv', index=True)
    print(df_all_books.columns.tolist())
    return df_all_books

# SACAR FOTO Y PEGAR EN DRAW.IO
# plot_emociones("Papelucho")
# plot_emociones("")   -> todos los libros
def plot_emociones(coleccion):
    from sklearn.preprocessing import scale
    df = pd.read_csv("dataframe_libros/all_books_emotion_frequency.csv", index_col=0)

    datos_scaled = scale(X=df, axis=1, with_mean=True, with_std=True) 
    datos_scaled = pd.DataFrame(datos_scaled, columns=df.columns, index=df.index)
    datos_scaled.reset_index(inplace=True)
    datos_scaled.columns.values[0] = "book"

    # FILTRAR QUE LIBROS MOSTRAR
    datos_scaled = datos_scaled.query(f'book.str.contains("{coleccion}")', engine='python')
    print(datos_scaled.head(5))

    # https://htmlcolorcodes.com/
    colors = ['#922B21','#76448A','#1F618D', '#148F77', '#B7950B', '#A04000', '#BB8FCE', '#566573']
    datos_scaled.plot(x ='book', y=['alegría', 'asombro', 'confianza', 'disgusto', 'ira', 'miedo', 'premonición', 'tristeza'], kind = 'bar', color=colors, width = 0.9)
    plt.legend(loc='upper left',fontsize = 10, bbox_to_anchor=(1, 0.8))
    plt.title(f"Emociones colección {coleccion}")
    plt.xlabel("Colección de libros")
    #plt.ylabel("Palabras diferentes")
    plt.xticks(fontsize=8)
    plt.tight_layout()
    #plt.savefig('imagenes/complejidad_lexica_coleccion}.png', bbox_inches='tight')
    plt.show()

# CAMBIAR LA QUERY PARA FILTRAR QUE LIBROS REVISAR
def plot_sentimientos():
    from sklearn.preprocessing import scale
    df = pd.read_csv("dataframe_libros/all_books_sentiment_frequency.csv", index_col=0)


    df.reset_index(inplace=True)
    df.columns.values[0] = "book"

    # FILTRAR QUE LIBROS MOSTRAR
    df = df.query(f'book.str.contains("Papelucho")', engine='python')
    print(df.head(5))

    # https://htmlcolorcodes.com/
    colors = ['#8E44AD', '#F39C12']
    df.plot(x ='book', y=['negativo', 'positivo'], kind = 'bar', color=colors, width = 0.9)
    plt.legend(loc='upper left',fontsize = 10, bbox_to_anchor=(1, 0.8))
    plt.title(f"Sentimientos en colección Harry Potter")
    plt.xlabel("Colección de libros")
    plt.ylabel("Frecuencia de sentimientos")
    plt.xticks(fontsize=8)
    plt.tight_layout()
    #plt.savefig('imagenes/complejidad_lexica_coleccion}.png', bbox_inches='tight')
    plt.show()
# -----------------------------------------
# -----------------------------------------


# -----------------------------------------
# PHRASES PLOT
# -----------------------------------------
# CREAR DF CON LOS SENTIMIENTOS POSITIVOS/NEGATIVOS desde el df de cada libro 
# {book}_phrases_analysis.csv
# con las columnas [sentiment,emotion,positive,negative,neutral]


#get_positive_values_from_book("Papelucho")
def get_positive_values_from_book(book, split_n_times):
    import numpy as np
    df = pd.read_csv(f"dataframe_libros/{book}_phrases_analysis.csv", index_col=0)
    df = df[["positive"]]

    df_list = df.values.tolist()
    new_list = np.array_split(df_list, split_n_times)
    #new_list = [np.median(np.array(df_list)) for df_list in new_list]
    new_list = [np.mean(np.array(df_list)) for df_list in new_list]
    #new_list = [max(df_list) for df_list in new_list]

    df = pd.DataFrame(new_list)
    df.columns = ["positive"]
    return df

def merge_positives_values():
    df2 = pd.DataFrame([float(0) for _ in range(100)])
    df2.columns = ['book']
    for book in LIST_OF_ALL_BOOKS:
        book = Book(book)
        df1 = get_positive_values_from_book(book.tittle, 100)
        df1.columns = [f"{book.tittle}"]
        df2 = df2.join(df1)
    df2 = df2.fillna(0)
    df2.drop(columns=df2.columns[0], axis=1, inplace=True)
    df2 = df2.transpose()  
     
    df2.to_csv(f'dataframe_libros/all_books_positive_phrases_analysis_100.csv', index=True)
    print('dataframe_libros/all_books_positive_phrases_analysis_100.csv created')



#get_positive_values_from_book("Papelucho")
def get_negative_values_from_book(book, split_n_times):
    import numpy as np
    df = pd.read_csv(f"dataframe_libros/{book}_phrases_analysis.csv", index_col=0)
    df = df[["negative"]]

    df_list = df.values.tolist()
    new_list = np.array_split(df_list, split_n_times)
    new_list = [np.median(np.array(df_list)) for df_list in new_list]

    df = pd.DataFrame(new_list)
    df.columns = ["negative"]
    return df

def merge_negatives_values():
    df2 = pd.DataFrame([float(0) for _ in range(100)])
    df2.columns = ['book']
    for book in LIST_OF_ALL_BOOKS:
        book = Book(book)
        df1 = get_negative_values_from_book(book.tittle, 100)
        df1.columns = [f"{book.tittle}"]
        df2 = df2.join(df1)
    df2 = df2.fillna(0)
    df2.drop(columns=df2.columns[0], axis=1, inplace=True)
    df2 = df2.transpose()  
     
    df2.to_csv(f'dataframe_libros/all_books_negative_phrases_analysis_100.csv', index=True)
    print('dataframe_libros/all_books_negative_phrases_analysis_100.csv created')


    # for book in LIST_OF_PAPELUCHO:
    #     book = book[:-4]
    #     plot_analsys_story_type(book, "negative", 50)
    #     plot_analsys_story_type(book, "positive", 50)
def plot_analsys_story_type(book, sentiment, n_values):
    if sentiment == "positive":
        df = get_positive_values_from_book(book, n_values)
        df = df['positive']
        sentimientos = "positivos"
        colors = red_colors
    if sentiment == "negative":
        df = get_negative_values_from_book(book, n_values)
        df = df['negative']
        sentimientos = "negativos"
        colors = blue_colors

    df.plot(kind='bar', color=colors , width=0.9, legend=None)
    #plt.legend(loc='upper left',fontsize = 10, bbox_to_anchor=(1, 0.8))
    plt.title(f"Sentiemientos {sentimientos} en funcion del libro {book}")
    plt.xlabel(f"Tiempo de la historia")
    plt.ylabel("Intensidad de sentimiento")
    plt.xticks(fontsize=8)
    plt.tight_layout()
    plt.savefig(f'imagenes/{book}_{sentiment}_forma_relato.png', bbox_inches='tight')
    plt.close()
    print(f"imagenes/{book}_{sentiment}_forma_relato.png created")
    #plt.show()

# -------------------------------------
# PLOT INTERVALOS DE CONFIANZA

        # for book in LIST_OF_ALL_BOOKS:
        #     book = book[:-4]
        #     create_plot_df_with_ci(book, "negative", 100)
        #     create_plot_df_with_ci(book, "positive", 100)
def create_plot_df_with_ci(book, sentiment, split_n_times):
    import numpy as np
    df = pd.read_csv(f"dataframe_libros/{book}_phrases_analysis.csv", index_col=0)
    

    # agrega una columna con los intervalos 
    positions = len(df) / split_n_times
    position_list = [0]
    m = 1
    for n in list(range(len(df))):
        if n < positions * m:
            position_list.append(m-1)
        else:
            m = m + 1
            position_list.append(m-1)

    if len(df) < len(position_list):
        position_list.pop()


    df["position"] = position_list
    
    if sentiment == "positive":
        color_plot = 'darkorange'
        color_title = 'navy'
        sentimiento = "positivo"
    if sentiment == "negative":
        color_plot = 'darkturquoise'
        color_title = 'steelblue'
        sentimiento = "negativo"

    sns.lineplot(x = "position", y = sentiment, data = df, color=color_plot)

    plt.title(f"Sentiemientos {sentimiento} libro {book}", color=color_title, weight="bold")
    plt.xlabel(f"Tiempo de la historia")
    plt.ylabel(f"Intensidad de {sentimiento}")
    plt.xticks(fontsize=8)
    plt.tight_layout()
   
    plt.ylim(0 , 1)
    plt.xlim(0 , split_n_times)

    plt.savefig(f'imagenes/{book}_{sentiment}_intervalo_confianza.png', bbox_inches='tight')
    print(f"imagenes/{book}_{sentiment}_intervalo_confianza.png created")

    plt.close()
    #plt.show()

def main():
    merge_negatives_values()
    merge_positives_values()


if __name__ == "__main__":
    import time
    s = time.perf_counter()
    main()
    elapsed = time.perf_counter() - s
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")


