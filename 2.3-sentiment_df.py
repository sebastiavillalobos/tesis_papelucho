#import parso
from book_class import Book
from librerias.books_files import LIST_OF_ALL_BOOKS
#from sentiment_analysis_spanish import sentiment_analysis
import pandas as pd
import json
from pysentimiento import SentimentAnalyzer
from pysentimiento import EmotionAnalyzer


analyzer = SentimentAnalyzer(lang="es")
emotion_analyzer = EmotionAnalyzer(lang="es")


# def create_sentiments_dataframe():
#     for book in LIST_OF_ALL_BOOKS:
#         book = Book(book) 
#         sentiment = sentiment_analysis.SentimentAnalysisSpanish()
#         sentimen_analysis = [sentiment.sentiment(phrase) for phrase in book.split_by_setences()]
#         # save to a file
#         df = pd.DataFrame(sentimen_analysis)
#         df.to_csv(f"dataframe_libros/sentiment_{book.tittle}.csv")


def get_phrase_sentiment_beto(frase_libro):
    frase = frase_libro
    response = analyzer.predict(frase)
    emotion_response = emotion_analyzer.predict(frase)

    if response.output == 'POS':
        sentiment = 'POSITIVE'
    elif response.output == 'NEG':
        sentiment = 'NEGATIVE'
    elif response.output == 'NEU':
        sentiment = 'NEUTRAL'
    else:
        sentiment = 'NONE'
    
    positive = response.probas['POS']
    negative = response.probas['NEG']
    neutral = response.probas['NEU']
    emotion = emotion_response.output

    sentiment_analysis = (sentiment, emotion, positive, negative, neutral)
    return sentiment_analysis

def get_phrase_emotions_beto(frase_libro):
    frase = frase_libro
    response = emotion_analyzer.predict(frase)
    return response.output

import os.path

def create_phrases_analysis():
    for book in LIST_OF_ALL_BOOKS:
        book = Book(book) 
        if os.path.exists(f"dataframe_libros/{book.tittle}_phrases_analysis.csv"):
            print(f"{book.tittle} analysed")
            pass
        else:
            print(f"{book.tittle} is being analysed")
            sentimen_analysis = [get_phrase_sentiment_beto(phrase) for phrase in book.split_by_setences()]
            df = pd.DataFrame(sentimen_analysis, columns = ['sentiment', 'emotion', 'positive', 'negative', 'neutral'])
            df.to_csv(f"dataframe_libros/{book.tittle}_phrases_analysis.csv")
            print(f"{book.tittle}_phrases_analysis.csv created")
    return "procces end"


if __name__=="__main__":
    create_phrases_analysis()
    #print(len(LIST_OF_ALL_BOOKS))
    
### FALTA APLICAR EL GET EMOTIONS!!! READY!!

# PIPELINE GRAFICADO, EXPLICADO PASO A PASO

# calcular la complejidad lexica, que tan diuverso es el lexico????
# CANTIDAD DE PALABRAS DISTINTAS  READY!!

# caracteristicas encontradas en los libros de papelucho! NI MIERDA

# realizar analisis de solo los libros de papelucho y luego realizar uno con todos!!!!
# WORD CLOUD
# 
# DISTANCIAS OK
# CLUSTERING OK
# COMPLEJIDAD LEXICA OK

