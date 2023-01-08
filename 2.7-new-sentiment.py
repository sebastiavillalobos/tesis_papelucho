from operator import ne
from book_class import Book
from librerias.books_files import LIST_OF_ALL_BOOKS
import pandas as pd
import requests
import json

def get_phrase_sentiment(frase_libro):
    frase = frase_libro
    url_sentiments = "https://nqjqfab6if.execute-api.us-east-2.amazonaws.com/sentiment"
    headers = {'Content-Type': "application/json"}
    payload = json.dumps({
        "frase": frase
    })
    response = requests.get(url_sentiments, headers=headers, data=payload)
   
    if response.status_code == 200:
        response = response.json()

        sentiment = response['sentiment']
        positive = response['score']['Positive']
        negative = response['score']['Negative']
        neutral = response['score']['Neutral']
        mixed = response['score']['Mixed']
        
        sentiment_analysis = (sentiment, positive, negative, neutral, mixed)
        return sentiment_analysis
    else:
        return ('NEUTRAL', 0, 0, 0)

def create_sentiments_dataframe_alexa():
    for book in LIST_OF_ALL_BOOKS:
        book = Book(book) 
        sentimen_analysis = [get_phrase_sentiment(phrase) for phrase in book.split_by_setences()]
        # save to a file
        df = pd.DataFrame(sentimen_analysis, columns = ['sentiment', 'positive', 'negative', 'neutral', 'mixed'])
        df.to_csv(f"dataframe_libros/alexa_sentiment_{book.tittle}.csv")
    return "procces end"



if __name__=="__main__":
    create_sentiments_dataframe_alexa()