from book_class import Book
import pandas as pd
import spacy
import librerias.decoratos as dc

# Carga es_core_news_sm -> ESPAÑOL!!!!
nlp = spacy.load("es_core_news_sm")
nlp.max_length = 1500000


# ----------------------------------
# Create data set
@dc.timing
def create_books_dataset(lista_libros):
    df_all_books = pd.DataFrame(columns=['word', 'freq'])
    for book in lista_libros:
        df_new = pd.DataFrame(Book(book).word_frequency(), columns=['word', 'freq'])
       # df_new.columns = ['word', 'freq']
        df_all_books = pd.merge(df_all_books, df_new, on='word', how='outer')
        df_all_books.columns = df_all_books.columns = [*df_all_books.columns[:-1], Book(book).tittle]
        df_all_books = df_all_books.fillna(0)
    df_all_books.drop("freq_x", axis=1, inplace=True)
    df_all_books.sort_values("word", axis = 0, ascending = True,
                 inplace = True, na_position ='last')
    df_all_books.to_csv('clusteringFiles/data_all_books.csv', index=False)
    return df_all_books

# PARA CREAR EL DATASET DE TODOS LOS LIBROS
#create_books_dataset(list_of_books)

# Imprime el data sat creado
data_set = pd.read_csv('data_all_books.csv', index_col=0)
print(data_set.head(4))