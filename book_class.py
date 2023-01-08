from inspect import classify_class_attrs
from operator import index
from socketserver import StreamRequestHandler
from typing_extensions import dataclass_transform
from librerias.books_files import book_path, list_of_books 
import pandas as pd
import pathlib
import re
import spacy
import librerias.decoratos as dc
import numpy as np

# Carga es_core_news_sm -> ESPAÑOL!!!!
nlp = spacy.load("es_core_news_sm")
nlp.max_length = 2500000



class Book():
    def __init__(self, tittle_book):
        self.tittle = tittle_book[:-4]
        self.plan_text = pathlib.Path(book_path + tittle_book).read_text()
        self.cleaned_text = self.clean_text()

   # Carga el dataframe .csv 
    def book_df(self):
        dataframe = pd.read_csv(f'dataframe_libros/df_{self.tittle}_raw.csv', index_col=0)
        # set word as label
        dataframe.columns = ['word']
        return dataframe

    def sentiment_df(self):
        dataframe = pd.read_csv(f'dataframe_libros/sentiment_{self.tittle}.csv', index_col=0)
        dataframe.columns = ['value']
        return dataframe

    # Solo para testear, multiplica x 1000 los valores   
    def sentiment_df_1000(self):
        data_set_sentiments = self.sentiment_df()
        data_values = data_set_sentiments['value'].values.tolist()
        new_list = np.array_split(data_values, 1000)
        # new_list = [(sum(list_values)/len(list_values)) for list_values in new_list \
        #             if len(list_values) > 0 ]
        new_list = [np.median(np.array(list_values)) for list_values in new_list]
        #new_list = [0.0001 if x < 0.0005 else x for x in new_list]
        new_list = [n * 1000 for n in new_list]
        #new_list = [float(x) for x in new_list]
        new_list = pd.DataFrame(new_list)
        new_list.columns = [f'{self.tittle}']
        return new_list

    def sentiment_df_1(self):
        data_set_sentiments = self.sentiment_df()
        data_values = data_set_sentiments['value'].values.tolist()
        new_list = np.array_split(data_values, 1000)
        # new_list = [(sum(list_values)/len(list_values)) for list_values in new_list \
        #             if len(list_values) > 0 ]
        new_list = [np.median(np.array(list_values)) for list_values in new_list]
        #new_list = [0.0001 if x < 0.0005 else x for x in new_list]
        #new_list = [float(x) for x in new_list]
        new_list = pd.DataFrame(new_list)
        new_list.columns = [f'{self.tittle}']
        return new_list

    # str con tecto limpio
    def clean_text(self):
        self.plan_text = self.plan_text.replace('N°', 'numero')
        self.plan_text = self.plan_text.replace('n°', 'numero')
        self.plan_text = self.plan_text.lower()
        self.plan_text = self.plan_text.replace('á', 'a')
        self.plan_text = self.plan_text.replace('á', 'a')
        self.plan_text = self.plan_text.replace('é', 'e')
        self.plan_text = self.plan_text.replace('í', 'i')
        self.plan_text = self.plan_text.replace('ó', 'o')
        self.plan_text = self.plan_text.replace('ú', 'u')
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
        self.plan_text = self.plan_text.replace('0', '')
        self.plan_text = self.plan_text.replace('-', '')
        self.plan_text = self.plan_text.replace('...', '.')
        self.plan_text = self.plan_text.replace(']', '.')
        self.plan_text = self.plan_text.replace('[', '.')
        self.plan_text = self.plan_text.replace('', '.')
        self.plan_text = self.plan_text.replace(' $', '')
        self.plan_text = self.plan_text.replace('"', '')
        self.plan_text = self.plan_text.replace('\n', '')

        # palabras de otros idiomas
        self.plan_text = self.plan_text.replace('ça', '')
        self.plan_text = self.plan_text.replace('èl', '')
        self.plan_text = self.plan_text.replace('žbig', '')
        self.plan_text = self.plan_text.replace('', '')
        self.plan_text = self.plan_text.replace('aabaraka', '')
        self.plan_text = self.plan_text.replace('zzazz', '')
        self.plan_text = self.plan_text.replace('zxcvbnmlkj', '')
        self.plan_text = self.plan_text.replace('zxcvbnmasdfghjklñ', '')
        self.plan_text = self.plan_text.replace('aaaaaah', '')
        self.plan_text = self.plan_text.replace('aaaaaggghhhhh', '')
        self.plan_text = self.plan_text.replace('aaaaah', '')
        self.plan_text = self.plan_text.replace('aaaaahhh', '')
        self.plan_text = self.plan_text.replace('aaaaahhhhh', '')
        self.plan_text = self.plan_text.replace('aaaah', '')
        self.plan_text = self.plan_text.replace('aaaahh', '')
        self.plan_text = self.plan_text.replace('aaaahhhh', '')
        self.plan_text = self.plan_text.replace('aaaar', '')
        self.plan_text = self.plan_text.replace('aaaargh', '')
        self.plan_text = self.plan_text.replace('aaaarghh', '')
        self.plan_text = self.plan_text.replace('aaah', '')
        self.plan_text = self.plan_text.replace('aaahhh', '')
        self.plan_text = self.plan_text.replace('aaaja', '')
        self.plan_text = self.plan_text.replace('aag', '')
        self.plan_text = self.plan_text.replace('aalden', '')
        self.plan_text = self.plan_text.replace('aalgun', '')
        self.plan_text = self.plan_text.replace('aaay', '')
        self.plan_text = self.plan_text.replace('aaragog', '')
        self.plan_text = self.plan_text.replace('aaron', '')
        self.plan_text = self.plan_text.replace('aauu', '')
        self.plan_text = self.plan_text.replace('aay', '')
        self.plan_text = self.plan_text.replace('aaay', '')
        self.plan_text = self.plan_text.replace('aamarra', '')
        self.plan_text = self.plan_text.replace('aamir', '')
        self.plan_text = self.plan_text.replace('aahh', '')
        self.plan_text = self.plan_text.replace('aaip', '')
        self.plan_text = self.plan_text.replace('aak', '')
        self.plan_text = self.plan_text.replace('überstigen', '')
        self.plan_text = self.plan_text.replace('üld', '')
        self.plan_text = self.plan_text.replace('ünica', 'unica')
        self.plan_text = self.plan_text.replace('þcon', '')
        self.plan_text = self.plan_text.replace(' ños', '')
        self.plan_text = self.plan_text.replace('ños ', '')
        self.plan_text = self.plan_text.replace('ïciente', '')
        self.plan_text = self.plan_text.replace('•', '')
        self.plan_text = self.plan_text.replace('«', '')
        self.plan_text = self.plan_text.replace('*', '')
        self.plan_text = self.plan_text.replace('n°', 'numero')
        self.plan_text = self.plan_text.replace(' aba ', '')
        #self.plan_text = re.sub("\W+", ' ', self.plan_text)
        # Delete 3 equals chars
        self.plan_text = re.sub("\\b([a-zA-Z0-9])\\1\\b", ' ', self.plan_text)
        self.plan_text = re.sub("\\b([a-zA-Z0-9])\\1\\1+\\b", ' ', self.plan_text)
        return self.plan_text

    # lista de tokens sin stop words locales y de spacy nlp library
    @dc.timing
    def filtered_tokens(self):
        [token for token in nlp(self.cleaned_text) if not token.is_stop]

    # lista de tokens con el texto limpio y sin palabras con 1 char
    @dc.timing
    def tokenize_book(self):
        clean_tokens = [token for token in nlp(self.cleaned_text) if not token.is_stop | token.is_punct and len(token)>1]
        clean_tokens = format(clean_tokens).replace(',','').replace('[', '').replace(']','').split()
        return clean_tokens

    @dc.timing
    def word_frequency(self):
        wordfreq = {}
        text_without_stops = self.tokenize_book()
        for word_token in text_without_stops:
            if word_token in wordfreq.keys():
                wordfreq[word_token] += 1
            else:
                wordfreq[word_token] = 1
        wordfreq = sorted(wordfreq.items(), key = lambda kv:(kv[1], kv[0]))
        return wordfreq
    
    def freq_df(self):
        book = pd.DataFrame(self.book_df())   
        book.columns = ['word']
        book = book.groupby(['word'])['word'].count().sort_values(ascending=False)
        return book

    @dc.timing
    def split_by_setences(self):
        book_txt = self.cleaned_text
        alphabets= "([A-Za-z])"
        prefixes = "(sr|sra|señor|señora|mister)[.]"
        suffixes = "(Inc|Ltd|Jr|Sr|Co)"
        acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
        webs = "[.](com|net|org|io|gov)"
        book_txt = " " + book_txt + "  "
        book_txt = book_txt.replace("\n"," ")
        book_txt = re.sub(prefixes,"\\1<prd>",book_txt)
        book_txt = re.sub(webs,"<prd>\\1",book_txt)
        book_txt = re.sub("\s" + alphabets + "[.] "," \\1<prd> ",book_txt)
        book_txt = re.sub(alphabets + "[.]" + alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>\\3<prd>",book_txt)
        book_txt = re.sub(alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>",book_txt)
        book_txt = re.sub(" "+suffixes+"[.]"," \\1<prd>",book_txt)
        book_txt = re.sub(" " + alphabets + "[.]"," \\1<prd>",book_txt)
        if "”" in book_txt: book_txt = book_txt.replace(".”","”.")
        if "\"" in book_txt: book_txt = book_txt.replace(".\"","\".")
        if "?" in book_txt: book_txt = book_txt.replace("?\"","\"?")
        if "!" in book_txt: book_txt = book_txt.replace('\!"','\"!')
        book_txt = book_txt.replace(".",".<stop>")
        book_txt = book_txt.replace(" ¿","<stop>¿")
        book_txt = book_txt.replace("?","?<stop>")
        book_txt = book_txt.replace("!","!<stop>")
        book_txt = book_txt.replace("<prd>",".")
        sentences = book_txt.split("<stop>")
        sentences = sentences[:-1]
        sentences = [s.strip() for s in sentences]
        sentences = [i for i in sentences if i != "."]
        return sentences



if __name__ == "__main__":
    book_example = Book("Papelucho.txt")
    print(book_example.sentiment_df_1000())

