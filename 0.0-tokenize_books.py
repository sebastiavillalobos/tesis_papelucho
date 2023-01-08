from book_class import Book
from librerias.books_files import LIST_OF_ALL_BOOKS, LIST_OF_PAPELUCHO, LIST_OF_HARRY
import pandas as pd
import matplotlib.pyplot as plt
import spacy

nlp = spacy.load("es_core_news_sm")
nlp.max_length = 2500000


def tokenize_book(book):
    book = Book(book)
    cleaned_book = book.clean_text().replace('.', '')
    cleaned_book = cleaned_book.split(" ")
    df = pd.DataFrame(cleaned_book, columns=['word'])
    df.to_csv(f"dataframe_libros/df_{book.tittle}_dirty.csv")
    return df

def frequency_of_book(book):
    df = tokenize_book(book)
    book = Book(book)
    frequency = df["word"].value_counts()
    frequency = pd.DataFrame(frequency)
    frequency.reset_index(inplace=True)
    frequency.columns.values[0] = "word"
    frequency.columns.values[1] = "frequency"
    frequency = frequency.sort_values(by=["frequency"], ascending=False)
    return frequency

def plot_frequency_raw(book):
    df = frequency_of_book(book)
    df = df.head(10)
    #df.plot(x ='book', y='complexity', kind = 'bar', color = 'b', width = 0.9, figsize=(16, 9))
    df.plot(x ='word', y='frequency', kind = 'bar', color = '#50C878', width = 0.7, legend=None, figsize=(6, 4))
    plt.title(f"top 10 palabras más frecuentes en {book[:-4]}")
    plt.xlabel("Palabras")
    plt.ylabel("Frecuencia")
    plt.xticks(fontsize=8)
    plt.tight_layout()
    plt.savefig(f"imagenes/frequency/freq_{book[:-4]}_raw.png", bbox_inches='tight')
    plt.close()



def tokenized_without_stopwords(book):
        book = Book(book)
        clean_tokens = [token for token in nlp(book.cleaned_text) if not token.is_stop | token.is_punct and len(token)>1]
        clean_tokens = format(clean_tokens).replace(',','').replace('[', '').replace(']','').split()

        df = pd.DataFrame(clean_tokens, columns=['word'])
        df.to_csv(f"dataframe_libros/df_{book.tittle}_without_stopwords.csv")
        return df


def frequency_without_stopwords(book):
    df = tokenized_without_stopwords(book)
    frequency = df["word"].value_counts()
    frequency = pd.DataFrame(frequency)
    frequency.reset_index(inplace=True)
    frequency.columns.values[0] = "word"
    frequency.columns.values[1] = "frequency"
    frequency = frequency.sort_values(by=["frequency"], ascending=False)
    return frequency

def plot_frequency_without_stopwords(book):
    df = frequency_without_stopwords(book)
    df = df.head(10)
    #df.plot(x ='book', y='complexity', kind = 'bar', color = 'b', width = 0.9, figsize=(16, 9))
    df.plot(x ='word', y='frequency', kind = 'bar', color = '#FA8072', width = 0.7, legend=None, figsize=(6, 4))
    plt.title(f"top 10 palabras más frecuentes en {book[:-4]} sin Stop Words")
    plt.xlabel("Palabras")
    plt.ylabel("Frecuencia")
    plt.xticks(fontsize=8)
    plt.tight_layout()
    plt.savefig(f"imagenes/frequency/freq_{book[:-4]}_without_stopwords.png", bbox_inches='tight')
    plt.close()


# for book in LIST_OF_ALL_BOOKS:
#     plot_frequency_without_stopwords(book)
#     plot_frequency_raw(book)
#     print(f"{book} terminado")

def concat_freq_dataframe(LIST_OF_BOOKS):
    df = pd.DataFrame()
    for book in LIST_OF_BOOKS:
        book = Book(book)
        df1= pd.read_csv(f"dataframe_libros/df_{book.tittle}_dirty.csv", index_col=0)
        df = pd.concat([df, df1], ignore_index = True, axis = 0)
    df.to_csv(f"dataframe_libros/df_coleccion_papelucho_dirty.csv")
    return df

def concat_freq_dataframe_without_stopwords(LIST_OF_BOOKS):
    df = pd.DataFrame()
    for book in LIST_OF_BOOKS:
        book = Book(book)
        df1= pd.read_csv(f"dataframe_libros/df_{book.tittle}_without_stopwords.csv", index_col=0)
        df = pd.concat([df, df1], ignore_index = True, axis = 0)
    df.to_csv(f"dataframe_libros/df_coleccion_papelucho_without_stopwords.csv")
    return df


# CARGO EL DF y GENERO LAS FRECUENCIAS. DESPUES TOMO EL CSV CREADO Y LO CARGO EN https://www.wordclouds.com/

df = pd.read_csv("dataframe_libros/df_coleccion_papelucho_without_stopwords.csv", index_col=0)
#df = pd.read_csv("dataframe_libros/df_coleccion_papelucho_dirty.csv", index_col=0)
print(df.columns.tolist())
print(df.head(5))
frequency = df["word"].value_counts()
frequency = pd.DataFrame(frequency)
frequency.reset_index(inplace=True)
frequency.columns.values[0] = "word"
frequency.columns.values[1] = "frequency"
frequency = frequency.sort_values(by=["frequency"], ascending=False)
frequency = frequency.head(50)
#frequency.to_csv(f"dataframe_libros/frequency_coleccion_papelucho_dirty.csv")
frequency.to_csv(f"dataframe_libros/frequency_coleccion_papelucho_without_stopwords.csv")
frequency = frequency.head(10)
green_colors = ['#ADFF2F','#7FFF00','#7CFC00','#00FF00','#32CD32','#98FB98','#90EE90','#00FA9A','#00FF7F','#3CB371','#2E8B57','#228B22','#008000','#006400','#9ACD32','#6B8E23','#808000','#556B2F','#66CDAA','#8FBC8B','#20B2AA','#008B8B','#008080']
purple_colors = ['#DDA0DD','#EE82EE','#DA70D6','#FF00FF','#FF00FF','#BA55D3','#9370DB','#663399','#8A2BE2','#9400D3','#9932CC','#8B008B','#800080','#4B0082','#6A5ACD','#483D8B','#7B68EE']
#df.plot(x ='book', y='complexity', kind = 'bar', color = 'b', width = 0.9, figsize=(16, 9))
frequency.plot(x ='word', y='frequency', kind = 'bar', color = purple_colors, width = 0.7, legend=None, figsize=(6, 4))
plt.title(f"top 10 palabras más frecuentes en la colección papelucho sin Stop Words")
plt.xlabel("Palabras")
plt.ylabel("Frecuencia")
plt.xticks(fontsize=8)
plt.tight_layout()
plt.show()



































































































