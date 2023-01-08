import matplotlib.pyplot as plt
from operator import index
from book_class import Book
from librerias.books_files import LIST_OF_ALL_BOOKS
import pandas as pd
#import asyncio
import librerias.decoratos as dc


dc.timing
def create_book_df(book):
    book = Book(book)
    print(f"creating df_{book.tittle}_raw.csv")
    df = pd.DataFrame(book.tokenize_book())
    df.to_csv(f"dataframe_libros/df_{book.tittle}_raw.csv")
    print(f"df_{book.tittle}_raw.csv created")


def create_all_book_df_sentiment():
    new_dataframe = pd.DataFrame([float(0) for _ in range(1000)])
    new_dataframe.columns = ['EMPTY']
    for book in LIST_OF_ALL_BOOKS:
        book = Book(book)
        print(f"{book.tittle}")
        book = book.sentiment_df_1()
        new_dataframe = new_dataframe.join(book)
    new_dataframe.drop('EMPTY', inplace=True, axis=1)
    new_dataframe = new_dataframe.transpose()
    new_dataframe = new_dataframe.dropna()
    new_dataframe.to_csv(f"clusteringFiles/data_all_books_sentiments_median2.csv", index=True)
    return new_dataframe


def lex_complexity(book):
    df = pd.read_csv(f"dataframe_libros/df_{book}_raw.csv", index_col=0)
    df.columns = ["word"]
    total_words = len(df)
    frequency = df.groupby(['word']).count()
    frequency = pd.DataFrame(frequency)
    lex_complexity = len(frequency)
    print(f"{book} done")
    return (lex_complexity, total_words)

def all_books_lex_complexity():
    books_complexity = []
    for book in LIST_OF_ALL_BOOKS:
        book = Book(book)
        different_words, total_words = lex_complexity(book.tittle)

        books_complexity.append((book.tittle, different_words, total_words))
    df = pd.DataFrame(books_complexity, columns=["book", "complexity", "total_words"])
    df.to_csv("dataframe_libros/all_books_complexity.csv")
    print("dataframe_libros/all_books_complexity.csv created")

# ordena por columna
def sort_by_column(csv_file, column):
    df = pd.read_csv(csv_file, index_col=0)
    df = df.sort_values(by=[column], ascending=False)
    print(df.head(5))
    print(df.tail(5))
    return df

def filter_by_value(csv_file, column, value):
    df = pd.read_csv(csv_file, index_col=0)
    print(df.columns.tolist())
    df2 = df[df[column].str.contains(value)]
    print(df2)
    return df2

def word_frequency(book, column):
    book = Book(book)
    df = pd.read_csv(f"dataframe_libros/df_{book.tittle}_with_dict.csv", index_col=0)
    frequency = df[column].value_counts()
    frequency = pd.DataFrame(frequency)
    frequency.reset_index(inplace=True)
    frequency.columns.values[0] = "word"
    frequency.columns.values[1] = "frequency"
    print(frequency.head(5))
    return frequency


#LIST_OF_ALL_BOOKS = ["Papelucho.txt", "Harry Potter y la orden del fenix.txt", "Crepusculo Amanecer.txt"]
def main():
    
    word_frequency("Papelucho.txt", "word")



if __name__ == "__main__":
    import time
    s = time.perf_counter()
    main()
    elapsed = time.perf_counter() - s
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")

