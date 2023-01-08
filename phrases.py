# FUNCIONALIDAD AGREGADA A LA CLASE BOOK 28-05-2022

from book_class import Book
import re
import librerias.decoratos as dc

book1 = Book("Papelucho.txt")


alphabets= "([A-Za-z])"
prefixes = "(sr|sra|señor|señora|mister)[.]"
suffixes = "(Inc|Ltd|Jr|Sr|Co)"
acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
webs = "[.](com|net|org|io|gov)"

# retorna el texto separado por frases
@dc.timing
def split_into_sentences(text):
    text = " " + text + "  "
    text = text.replace("\n"," ")
    text = re.sub(prefixes,"\\1<prd>",text)
    text = re.sub(webs,"<prd>\\1",text)
    if "Ph.D" in text: text = text.replace("Ph.D.","Ph<prd>D<prd>")
    text = re.sub("\s" + alphabets + "[.] "," \\1<prd> ",text)
    #text = re.sub(acronyms+" "+starters,"\\1<stop> \\2",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>\\3<prd>",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>",text)
    text = re.sub(" "+suffixes+"[.]"," \\1<prd>",text)
    text = re.sub(" " + alphabets + "[.]"," \\1<prd>",text)
    if "”" in text: text = text.replace(".”","”.")
    if "\"" in text: text = text.replace(".\"","\".")
    if "?" in text: text = text.replace("?\"","\"?")
    if "!" in text: text = text.replace('\!"','\"!')
    text = text.replace(".",".<stop>")
    text = text.replace(" ¿","<stop>¿")
    text = text.replace("?","?<stop>")
    text = text.replace("!","!<stop>")
    text = text.replace("<prd>",".")
    sentences = text.split("<stop>")
    sentences = sentences[:-1]
    sentences = [s.strip() for s in sentences]
    sentences = [i for i in sentences if i != "."]
    return sentences

#print(split_into_sentences(book1.cleaned_text))

print(book1.split_by_setences)