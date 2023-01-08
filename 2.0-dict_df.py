import enchant
import librerias.decoratos as dc
## lista los diccionarios de distintos idiomas soportados
#print(enchant.list_languages())

# revisa si existe, retorna true or false
# @dc.timing
def word_exist(word):
    d = enchant.request_dict("es_ES")
    return d.check(word)

# print(d.suggest("ola"))


@dc.timing
def test_word_exist(n):
    [word_exist("sebastian") for _ in list(range(n))]

# TEST DE 1000 palabras ...
#test_word_exist(1000)


print(word_exist("choriflay"))

# Se deja de lado, puesto que demora hrs !!!


# Filter spanish words on df

# 1. load book




