# --------------------------------------------------
#1. ReadBooks
""" 
list_of_books: contiene la lista con todos los titulos de libros en la carpeta books 
* Se limpian los titulos y se dejan solo el titulo del libro
"""

# --------------------------------------------------
import pathlib
import os
import re


books_path = pathlib.Path().resolve() / "books"
LIST_OF_ALL_BOOKS = os.listdir(books_path)
LIST_OF_PAPELUCHO = [papelucho for papelucho in LIST_OF_ALL_BOOKS if "Papelucho" in papelucho]
LIST_OF_HARRY = [harry for harry in LIST_OF_ALL_BOOKS if "Harry" in harry]

# Rename All book tittles
def clean_tittles(book_tittle):
    new_tittle = book_tittle
    # REMOVE NUM AND SPECIAL CHARS
    new_tittle = new_tittle.replace('á', 'a')
    new_tittle = new_tittle.replace('é', 'e')
    new_tittle = new_tittle.replace('í', 'i')
    new_tittle = new_tittle.replace('ó', 'o')
    new_tittle = new_tittle.replace('ú', 'u')
    new_tittle = new_tittle.replace('1', '')
    new_tittle = new_tittle.replace('2', '')
    new_tittle = new_tittle.replace('3', '')
    new_tittle = new_tittle.replace('4', '')
    new_tittle = new_tittle.replace('5', '')
    new_tittle = new_tittle.replace('6', '')
    new_tittle = new_tittle.replace('7', '')
    new_tittle = new_tittle.replace('8', '')
    new_tittle = new_tittle.replace('9', '')
    new_tittle = new_tittle.replace('0', '')
    new_tittle = new_tittle.replace('_', ' ')
    # REMOVE AUTHORS
    new_tittle = new_tittle.replace('Patrick Süskind ', '')
    new_tittle = new_tittle.replace('R A Salvatore ', '')
    new_tittle = new_tittle.replace('Rick Riordan ', '')
    new_tittle = new_tittle.replace('Stephen King ', '')
    new_tittle = new_tittle.replace('J M Barrie ', '')
    new_tittle = new_tittle.replace('J K Rowling ', '')
    new_tittle = new_tittle.replace('J M Barrie ', '')
    new_tittle = new_tittle.replace('Lisa Jane Smith ', '')
    new_tittle = new_tittle.replace('S D Perry ', '')
    new_tittle = new_tittle.replace('Stephanie Meyer ', '')
    new_tittle = new_tittle.replace('Scott Fitzgerald ', '')
    new_tittle = new_tittle.replace('S D Perry ', '')
    new_tittle = new_tittle.replace('Robert E Howard ', '')
    new_tittle = new_tittle.replace('Robert Ludlum ', '')
    new_tittle = new_tittle.replace('Justin Somper ', '')
    return re.sub('\W+', ' ', new_tittle[:-4])

def rename_books_tittles():
    book_path = format(books_path) + "/"
    count = 1
    for book_name in LIST_OF_ALL_BOOKS:
        source_book_name = book_path + book_name
        
        new_book_name = book_path + clean_tittles(book_name) + ".txt"
        os.rename(source_book_name, new_book_name)
        count += 1
    return os.listdir(book_path)

list_of_books = rename_books_tittles()
book_path = format(books_path) + "/"

if __name__ == "__main__":
    rename_books_tittles()