import pathlib
from book_class import Book
import json
import re
import pandas as pd
import librerias.decoratos as dc
from librerias.books_files import LIST_OF_ALL_BOOKS

class DictionaryES():
    def __init__(self):
        self.path_dict = pathlib.Path().resolve() / "diccionarios/dict_es_sentiments.txt"
        self.set_of_words = self.load_txt()

    def data_frame_dict(self):
        dataframe = pd.read_csv('diccionarios/dictionary.csv')
        #dataframe = pd.DataFrame(dataframe)
        #dataframe = pd.DataFrame(dataframe, columns=dataframe.columns, index=dataframe.index)
        return dataframe

    def clean_text(self, line):
        line = line.lower()
        line = line.replace('á', 'a')
        line = line.replace('á', 'a')
        line = line.replace('é', 'e')
        line = line.replace('í', 'i')
        line = line.replace('ó', 'o')
        line = line.replace('ú', 'u')
        line = line.replace('á', 'a')
        line = line.replace('é', 'e')
        line = line.replace('í', 'i')
        line = line.replace('ó', 'o')
        line = line.replace('ú', 'u')
        return line

    # estructurar de diccionario, una lista de diccionarios
    # [{
    #    word: 'palabra1'
    #    sentiment: 'sentimiento1'
    #    lexicon: 'lex1'
    #    value: 'value1'
    # }, {
    #    word: 'palabra2'
    #    sentiment: 'sentimiento2'
    #    lexicon: 'lex2'
    #    value: 'value2'
    # }]
    def load_txt(self):
        dictionary = []
        file = open(self.path_dict, "r")
        for line in file:
            line = self.clean_text(line)
            word, sentiment, lexicon, value = line.split()
            dictionary.append({ "word":word, "sentiment":sentiment, "lexicon":lexicon,  "value":value})
        return dictionary

    def create_df(self):
        return pd.read_json(json.dumps(self.load_txt())).drop_duplicates().to_csv('diccionarios/dictionary.csv', index=False)


        # Funcion que retorne cada X cantidad de palabras los sentimientos segun el lexicon.
# Parametros de entrada:
# Diccionario
# Libro
# Cantidad de palabras
# Lexicon

# 1 A cada apalabra agregar los valores del diccionario.


######## JOIN BOOK + DICT

# crea una lista con diccionarios que representa cada palabra de 1 libro
def create_set_words(libro, diccionario):
    full_book =[]
    current_word = ''
    nrc = []
    for book_element in libro.set_of_words:
        for dict_element in diccionario.set_of_words:
            if book_element['word'] == dict_element['word'] and dict_element['lexicon'] == 'nrc':
                if current_word == dict_element['word']:
                    full_book[-1]['nrc'].append(dict_element['sentiment'])
                elif current_word == '':
                    full_book.append(create_full_word_info(book_element['position'], book_element['word'], book_element['book_tittle'], [dict_element['sentiment']], '', ''))
                    current_word = dict_element['word']
                else:
                    full_book.append(create_full_word_info(book_element['position'], book_element['word'], book_element['book_tittle'], [dict_element['sentiment']], '', ''))
                    current_word = dict_element['word'] 
            if book_element['word'] == dict_element['word'] and dict_element['lexicon'] == 'bing':
                if current_word == dict_element['word']:
                    full_book[-1]['bing']= dict_element['sentiment']
                else:
                    full_book.append(create_full_word_info(book_element['position'], book_element['word'], book_element['book_tittle'], [], dict_element['sentiment'], ''))
                    current_word = dict_element['word']
            if book_element['word'] == dict_element['word'] and dict_element['lexicon'] == 'AFINN':
                if current_word == dict_element['word']:
                    full_book[-1]['AFINN']= dict_element['value']
                else:
                    full_book.append(create_full_word_info(book_element['position'], book_element['word'], book_element['book_tittle'], [], '', dict_element['value']))
                    current_word = dict_element['word']
    return full_book

# Funcion constructora de una palabra
def create_full_word_info(position, word, book_tittle, nrc, bing, AFINN):
    return {'position':position, 'word':word, 'book_tittle':book_tittle, 'nrc':nrc, 'bing':bing, 'AFINN':AFINN}


## JOIN BAG OF WORD + DICT
@dc.timing
def create_book_df(book, diccionario):
    list_of_words = book.word_frequency()
    full_book =[]
    current_word = ''
    nrc = []
    for n in range(len(list_of_words)):
        for dict_element in diccionario.set_of_words:
            if list_of_words[n][0] == dict_element['word'] and dict_element['lexicon'] == 'nrc':
                if current_word == dict_element['word']:
                    full_book[-1]['nrc'].append(dict_element['sentiment'])
                elif current_word == '':
                    full_book.append(dict_structure(list_of_words[n][0],list_of_words[n][1], book.tittle, [dict_element['sentiment']], '', ''))
                    current_word = dict_element['word']
                else:
                    full_book.append(dict_structure(list_of_words[n][0],list_of_words[n][1], book.tittle, [dict_element['sentiment']], '', ''))
                    current_word = dict_element['word'] 
            if list_of_words[n][0] == dict_element['word'] and dict_element['lexicon'] == 'bing':
                if current_word == dict_element['word']:
                    full_book[-1]['bing']= dict_element['sentiment']
                else:
                    full_book.append(dict_structure(list_of_words[n][0],list_of_words[n][1], book.tittle, [], dict_element['sentiment'], ''))
                    current_word = dict_element['word']
            if list_of_words[n][0] == dict_element['word'] and dict_element['lexicon'] == 'AFINN':
                if current_word == dict_element['word']:
                    full_book[-1]['AFINN']= dict_element['value']
                else:
                    full_book.append(dict_structure(list_of_words[n][0], list_of_words[n][1], book.tittle, [], '', dict_element['value']))
                    current_word = dict_element['word']
    return full_book

def dict_structure(word, freq, book_tittle, nrc, bing, AFINN):
    return {'word':word, 'frec': freq, 'book_tittle':book_tittle, 'nrc':nrc, 'bing':bing, 'AFINN':AFINN}
# ----------------------------------

# USO



# book_papelucho = Book("Papelucho.txt")
# book_dictionary= create_book_df(book_papelucho, diccionario_español)

# json to dataframes
#pd.read_json(json.dumps(book_dictionary)).to_csv('list_to_csv.csv', index=False)
def old_book_with_dic():
    from librerias.books_files import LIST_OF_ALL_BOOKS
    diccionario_español = DictionaryES()
    def all_books_dict_df():
        for book in LIST_OF_ALL_BOOKS:
            book = Book(book)
            pd.read_json(json.dumps(create_book_df(Book(book), diccionario_español))).to_csv(f'dataframe_libros/df_{book.tittle}.csv', index=False)


# hace el join entre el libro y el diccionario
def  book_with_dic(book, dictionary):
    book = Book(book)
    book_df = book.book_df()
    dict_df = dictionary
    book_dict = pd.merge(book_df, dict_df, how='inner', left_on='word', right_on='word') 
    book_dict = book_dict.fillna(0)
    book_dict.to_csv(f"dataframe_libros/df_{book.tittle}_with_dict.csv")
    print(f"dataframe_libros/df_{book.tittle}_with_dict.csv created")

if __name__ == "__main__":
    # import time
    # s = time.perf_counter()
    # dictionary_df = DictionaryES().data_frame_dict()
    dictionary_df = DictionaryES().create_df()
    # for book in LIST_OF_ALL_BOOKS:
    #     book_with_dic(book, dictionary_df)
    # elapsed = time.perf_counter() - s
    # print(f"{__file__} executed in {elapsed:0.2f} seconds.")
