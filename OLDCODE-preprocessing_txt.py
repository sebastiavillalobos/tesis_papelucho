from optparse import TitledHelpFormatter
import os
import re
from pathlib import Path
import pathlib
# Para usar el modulo en español de spacy
# python3 -m spacy download es_core_news_sm
import spacy
nlp = spacy.load("es_core_news_sm")
nlp.max_length = 1500000
# set path books
path_all_books = pathlib.Path().resolve() / "books"
# list all books on current path
all_books = os.listdir(path_all_books)

# def all_books_function(lista_libros):
#     dictionary = {}
#     k = 0
#     while k < len(lista_libros):
#         key = f'BOOK{k+1}'
#         value = lista_libros[k]
#         dictionary[key] = value
#         k += 1
#     return dictionary

# todos los libros
# for book in all_books:
#     open_book = open(path_all_books / book, mode="r", encoding="utf-8")
#     tittle_book = book
#     for line in open_book.readlines():

class Book():
    # Los libros deben estár en la carpeta books dentro del proyecto
    def __init__(self, txt_file):
        self.tittle = txt_file[:-4]
        self.path_books = pathlib.Path().resolve() / "books"
        self.plan_text = Path(self.path_books / txt_file).read_text()
        # TOKENIZED_BOOK puede usar las funciones con y sin stopwords
        #self.tokenized_book = self.pre_tokenize_book()
        self.tokenized_book = self.normalize()
        # lista de frecuencia
        self.word_freq = self.wordfreq()
        # Using spacy
        #self.spacy_tokenized_book = self.spacy_tokenize_book()
        self.lenght = self.lenght_book_func()
        self.set_of_words = self.create_set_words()
        
    # Limpia el texto 
    def clean_text(self):
        self.plan_text = self.plan_text.lower()
        self.plan_text = self.plan_text.replace('á', 'a')
        self.plan_text = self.plan_text.replace('é', 'e')
        self.plan_text = self.plan_text.replace('í', 'i')
        self.plan_text = self.plan_text.replace('ó', 'o')
        self.plan_text = self.plan_text.replace('ú', 'u')
        self.plan_text = self.plan_text.replace('1', '')
        self.plan_text = self.plan_text.replace('2', '')
        self.plan_text = self.plan_text.replace('3', '')
        self.plan_text = self.plan_text.replace('4', '')
        self.plan_text = self.plan_text.replace('5', '')
        self.plan_text = self.plan_text.replace('6', '')
        self.plan_text = self.plan_text.replace('7', '')
        self.plan_text = self.plan_text.replace('8', '')
        self.plan_text = self.plan_text.replace('9', '')
        # nombres
        self.plan_text = self.plan_text.replace('papelucho', '')
        # palabras de otros idiomas
        self.plan_text = self.plan_text.replace('aaa', 'a')
        self.plan_text = self.plan_text.replace('aaaa', 'a')
        self.plan_text = self.plan_text.replace('aaaaa', 'a')
        self.plan_text = self.plan_text.replace('aaaaaa', 'a')
        self.plan_text = self.plan_text.replace('aaaaaaa', 'a')
        self.plan_text = self.plan_text.replace('aaaaaaaa', 'a')
        self.plan_text = self.plan_text.replace('aaaaaaaaa', 'a')
        self.plan_text = self.plan_text.replace('aaaaaaaaaa', 'a')
        self.plan_text = self.plan_text.replace('aaaaaaaaaaa', 'a')
        self.plan_text = self.plan_text.replace('aaaaaaaaaaaa', 'a')
        self.plan_text = self.plan_text.replace('ça', '')
        self.plan_text = self.plan_text.replace('èl', '')
        self.plan_text = self.plan_text.replace('žbig', '')
        self.plan_text = self.plan_text.replace('', '')
        self.plan_text = self.plan_text.replace('aabaraka', '')
        self.plan_text = self.plan_text.replace('aaayyyy', '')
        self.plan_text = self.plan_text.replace('aaarrrgghh', '')
        self.plan_text = self.plan_text.replace('aaauuuggg', '')
        self.plan_text = self.plan_text.replace('zzazz', '')
        self.plan_text = self.plan_text.replace('zxcvbnmlkj', '')
        self.plan_text = self.plan_text.replace('zxcvbnmasdfghjklñ', '')
        self.plan_text = self.plan_text.replace('überstigen', '')
        self.plan_text = self.plan_text.replace('üld', '')
        self.plan_text = self.plan_text.replace('ünica', '')
        self.plan_text = self.plan_text.replace('þcon', '')
        self.plan_text = self.plan_text.replace('ños', '')
        self.plan_text = self.plan_text.replace('aba', '')
        self.plan_text = self.plan_text.replace('ïciente', '')
        return re.sub('\W+', ' ', self.plan_text)

    #
    # PRE_TOKENIZE  tokeniza el txt sin descartar las stop words
    #

    #  Usando la limpieza antes realizada por clean(), retorna una lista de strings
    def pre_tokenize_book(self):
        self.plan_text = self.clean_text()
        return self.plan_text.split()

    # Usando la librerya spacy
    def spacy_tokenize_book(self):
        book = nlp(self.plan_text)
        tokens = [t.orth_ for t in book]
        return tokens

    # TOKENIZED_BOOK usa esta funcioón que retorna una lista <class 'spacy.tokens.token.Token'>
    def spacy_rm_stop_words(self):
        filtered_tokens = [token for token in nlp(self.plan_text) if not token.is_stop]
        return filtered_tokens 


    def lenght_book_func(self):
        return len(self.tokenized_book)

    # crea una lista con diccionarios que representa el libro
    def create_set_words(self):
        book = []
        pos = 0
        for word in self.tokenized_book:
            book.append({"position":pos, "word":word, "book_tittle":self.tittle, "nrc":[]})
            pos += 1
        return book

#     Normalizar un texto con Python
# El siguiente paso en nuestro flujo de trabajo consiste en normalizar el texto. Nuestro tokenizador reconoce formas como caminar, Caminar y CAMINAR como formas distintas. Además, el documento puede tener números y palabras compuestas por caracteres alfanuméricos y otros símbolos tales como #Ar1anaG. Si no nos interesan estas palabras, y queremos que en nuestra lista aparezcan solamente las formas convencionales (por ejemplo, caminar, sólo en minúsculas) debemos normalizar nuestro texto. Aprovecharemos el momentum para descartar palabras muy cortas (menores a 3 caracteres) para filtrar aún más nuestros tokens.
    # retorna una lista
    def normalize(self):
        self.plan_text = self.clean_text()
        book = nlp(self.plan_text)
        words = [t.orth_ for t in book if not t.is_punct | t.is_stop]
        # normalización del texto descartando las palabras menores a 3 chars...
        lexical_tokens = [t.lower() for t in words if len(t) > 1 and     
        t.isalpha()]
        return lexical_tokens


# lematización: relaciona una palabra flexionada o derivada con su forma canónica o lema. Y un lema no es otra cosa que la forma que tienen las palabras cuando se buscas en el diccionario.
# La lematización es un proceso clave en muchas tareas prácticas de PLN, pero tiene dos costos. Primero, es un proceso que consume recursos (sobre todo tiempo). Segundo, suele ser probabilística, así que en algunos casos obtendremos resultados inesperados.
    def lematize(self):
        book = nlp(self.plan_text)
        return [tok.lemma_.lower() for tok in book if tok.pos_ != 'PRON']


###############
###############
# bag of words
###############
###############

    def wordfreq(self, type = "Default"):
        if type == "Default":
            tokens = self.tokenized_book
        if type == "lematized":
            tokens = self.lematize()
        if type == "normalized":
            tokens = self.normalize()
        wordfreq = {}
        for token in tokens:
            if token not in wordfreq.keys():
                wordfreq[token] = 1
            else:
                wordfreq[token] += 1
        wordfreq = sorted(wordfreq.items(), key = lambda kv:(kv[1], kv[0]))
        return wordfreq





###############
###############
# DISCCIONARIO
###############
###############

class DictionaryES():
    def __init__(self, txt_file):
        self.path_dict = pathlib.Path().resolve() / "diccionarios" / txt_file
        self.set_of_words = self.load_txt()
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
            word, sentiment, lexicon, value = line.split()
            dictionary.append({ "word":word, "sentiment":sentiment, "lexicon":lexicon,  "value":value})
        return dictionary

# _____________________________
# TODOS LOS LIBROS
# _____________________________
# Muestra las 10 palabras más frecuentes 
def print_all_books_function(lista_libros):
    dictionary = {}
    k = 0
    while k < len(lista_libros):
        book = Book(lista_libros[k])
        print(f'Titulo: {book.tittle}')
        print(book.wordfreq("normalized")
        [-10:])
        print('')
        k += 1




# Funcion que retorne cada X cantidad de palabras los sentimientos segun el lexicon.
# Parametros de entrada:
# Diccionario
# Libro
# Cantidad de palabras
# Lexicon

# 1 A cada apalabra agregar los valores del diccionario.


######## JOIN BOOK + DICT

# crea una lista con diccionarios que representa cada palabra de 1 libro
def create_set_words2(libro, diccionario):
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

def bow_dict(book, diccionario):
    list_of_words = book.word_freq
    full_book =[]
    current_word = ''
    nrc = []
    for n in range(len(list_of_words)):
        for dict_element in diccionario.set_of_words:
            if list_of_words[n][0] == dict_element['word'] and dict_element['lexicon'] == 'nrc':
                if current_word == dict_element['word']:
                    full_book[-1]['nrc'].append(dict_element['sentiment'])
                elif current_word == '':
                    full_book.append(create_full_word_info2(list_of_words[n][0],list_of_words[n][1], book.tittle, [dict_element['sentiment']], '', ''))
                    current_word = dict_element['word']
                else:
                    full_book.append(create_full_word_info2(list_of_words[n][0],list_of_words[n][1], book.tittle, [dict_element['sentiment']], '', ''))
                    current_word = dict_element['word'] 
            if list_of_words[n][0] == dict_element['word'] and dict_element['lexicon'] == 'bing':
                if current_word == dict_element['word']:
                    full_book[-1]['bing']= dict_element['sentiment']
                else:
                    full_book.append(create_full_word_info2(list_of_words[n][0],list_of_words[n][1], book.tittle, [], dict_element['sentiment'], ''))
                    current_word = dict_element['word']
            if list_of_words[n][0] == dict_element['word'] and dict_element['lexicon'] == 'AFINN':
                if current_word == dict_element['word']:
                    full_book[-1]['AFINN']= dict_element['value']
                else:
                    full_book.append(create_full_word_info2(list_of_words[n][0], list_of_words[n][1], book.tittle, [], '', dict_element['value']))
                    current_word = dict_element['word']
    return full_book

def create_full_word_info2(word, freq, book_tittle, nrc, bing, AFINN):
    return {'word':word, 'frec': freq, 'book_tittle':book_tittle, 'nrc':nrc, 'bing':bing, 'AFINN':AFINN}


# Agregar la cantidad de palabras.


############################## TESTING ##############################

# Lista todas las bag of words de cada txt en la carpeta books
# all_books_function(all_books)




# Instancia book and dict para pruebas de funciones
# book1 = Book('Papelucho.txt')
# book2 = Book('Harry_Potter_y_el_prisionero_de_Azkaban.txt')
# book3 = Book('Stephen King - The Dead Zone.txt')
# dict1 = DictionaryES('diccionario.txt')


#print(book1.word_freq)
# book_papelucho = Book('Papelucho.txt')

# # con spacy y con mi metodo llego a la misma cantidad de palabras :)
# print(len(book1.pre_tokenize_book()))
# print(len(book1.spacy_tokenized_book))



#print(book_papelucho.normalize())
# print(len(book_papelucho.lematize()))
# print(type(book_papelucho.lematize()))


# Tratamiento de datos
# ==============================================================================
import numpy as np
import pandas as pd
import statsmodels.api as sm

# # bag of words
# data = book1.word_freq
# df = pd.DataFrame(data)
# df.columns = ['word', 'freq']
# #print(df)
# data2 = book2.word_freq
# df2 = pd.DataFrame(data2)
# df2.columns = ['word', 'freq']
# #print(df2)
# data3 = book3.word_freq
# df3 = pd.DataFrame(data3)
# df3.columns = ['word', 'freq']

# df_merge = pd.merge(df, df2, on='word', how='outer')
# df_merge.columns = ['word',book1.tittle, book2.tittle]
# print(df_merge)

# Crea el dataset con todos los libros y los guarda en el archivo data_all_books.csv
def all_books_dataset(lista_libros):
    df1 = pd.DataFrame(Book('Papelucho.txt').word_freq ,columns=['word', 'freq'])
    for book in lista_libros:
        df2 = pd.DataFrame(Book(book).word_freq)
        df2.columns = ['word', 'freq']
        df_all_books = pd.merge(df1, df2, on='word', how='outer')
        df_all_books.columns = df_all_books.columns = [*df_all_books.columns[:-1], Book(book).tittle]
        df1 = df_all_books
    df1.drop("freq_x", axis=1, inplace=True)
    df1.sort_values("word", axis = 0, ascending = True,
                 inplace = True, na_position ='last')
    df1.to_csv('data_all_books2.csv', index=False)
    return df1



# four_books = ['Harry_Potter_y_la_camara_ecreta.txt']
four_books = ['R.A. Salvatore - 2. El valle del viento helado 1 - La Piedra de Cristal.txt', 'Papelucho_mi_hermana_Ji.txt', 'Lisa Jane Smith - Serie Diarios Vampiricos 4 - Invocación - Dark Reunion.txt', 'Harry_Potter_y_la_camara_ecreta.txt']
all_books_dataset(four_books)

# Gráficos
# ==============================================================================
# import matplotlib.pyplot as plt
# import matplotlib.font_manager
# from matplotlib import style
# style.use('ggplot') or plt.style.use('ggplot')

# Preprocesado y modelado
# ==============================================================================
# from sklearn.metrics import pairwise_distances
# from sklearn.preprocessing import scale

# # Configuración warnings
# # ==============================================================================
# import warnings
# warnings.filterwarnings('ignore')


# #book2 = Book('Justin Somper - Vampiratas 4 - Sangre de Capitan.txt')
# # print data frame
# df_book1 = pd.DataFrame(bow_dict(book1,dict1))
# df_book1.columns = ['word', 'freq', 'book_tittle', 'nrc', 'bing', 'AFINN']
# # 
# df_book1 = df_book1.sort_values(by='freq', ascending=False)
# ## IMPTIME EL DATAFRAME!

# print(df_book1)
#df_book2 = pd.DataFrame(bow_dict(book2,dict1))
# data_fram_1 = data_fram_1.to_string(index=False) ## SIN EL INDEX

# bing = positivo, solo columnas word, freq, bing
# df_book1_positivo = df_book1.query("bing == 'positivo'")
# df_book1_positivo = df_book1_positivo.filter(items=['word', 'freq', 'bing'])
# print(df_book1_positivo)
## DATA FRAME FROM WORD FREW
#df_book1_wf = pd.DataFrame(book1.word_freq)
#print(df_book1_wf)