import enchant
import librerias.decoratos as dc
## lista los diccionarios de distintos idiomas soportados
#print(enchant.list_languages())


# revisa si existe
# @dc.timing
def word_exist():
    d = enchant.request_dict("es_ES")
    d.check("hoyo")

# print(d.suggest("ola"))


@dc.timing
def test_word_exist(n):
    [word_exist() for _ in list(range(n))]

test_word_exist(1000)

