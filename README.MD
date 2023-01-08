# Analisis de sentimientos con Python

El **análisis de sentimientos** es una herramienta poderosa que permite a los computadores comprender el tono subjetivo subyacente de un texto. Esto es algo con lo que los humanos tienen dificultades, tampoco es tan fácil para los computadores... Pero con las herramientas adecuadas y Python, se puede usar el análisis de sentimientos para comprender mejor el sentimiento de un texto.

## Uso del procesamiento del lenguaje natural para preprocesar y limpiar datos de texto
Cualquier flujo de trabajo de análisis de sentimientos comienza con la carga de datos. Pero, ¿qué haces una vez que se han cargado los datos? Debe procesarlo a través de una canalización de procesamiento de lenguaje natural antes de poder hacer algo interesante con él.

Los pasos necesarios incluyen (pero no se limitan a) los siguientes:

1.  Tokenización de oraciones para dividir el texto en oraciones, palabras u otras unidades.
2.  Eliminar palabras vacías como "si", "pero", "o", etc.
3.  Normalizar palabras condensando todas las formas de una palabra en una sola forma.
4.  Vectorización de texto convirtiendo el texto en una representación numérica para el consumo de su clasificador.
  
Todos estos pasos sirven para reducir el ruido inherente a cualquier texto legible por humanos y mejorar la precisión de los resultados de su clasificador.

Instalación de librerias
```bash
#bash
$ pip3 install spacy==2.3.5
$ python3 -m spacy download es_core_news_sm
```

Se inicia creando una clase para ordenar el trabajo sobre la lista de libros (Books), donde esta clase recibe como parametro el nombre del archivo. Además esta clase tienen los siguientes atributos:
+   tittle = titulo del libro en el que se esta trabajando.
+   path_books = el PATH de la carpeta donde se encuentran los libros ( books).
+   plan_text = es el txt representado como un gran string.
```python

class Book():
    # Los libros deben estár en la carpeta books dentro del proyecto
    def __init__(self, txt_file):
        self.tittle = txt_file[:-3]
        self.path_books = pathlib.Path().resolve() / "books"
        self.plan_text = Path(self.path_books / txt_file).read_text()
        # TOKENIZED_BOOK puede usar las funciones con y sin stopwords
        self.tokenized_book = self.pre_tokenize_book()
        # Using spacy
        self.spacy_tokenized_book = self.spacy_tokenize_book()
        self.lenght = self.lenght_book_func()
        self.set_of_words = self.create_set_words()
```



## Tokenizar
La tokenización es el proceso de dividir fragmentos de texto en partes más pequeñas. ***spaCy*** viene con una canalización de procesamiento predeterminada que comienza con la tokenización, lo que hace que este proceso sea muy sencillo. En spaCy, se pueden hacer tokenización de oraciones o tokenización de palabras:

+   La tokenización de palabras divide el texto en palabras individuales.
+   La tokenización de oraciones divide el texto en oraciones individuales.
  
En este trabajo, se usará tokenización de palabras para separar el texto en palabras individuales.

Se agrega la función **spacy_tokenize_book** a la clase. Esta retorna una lista que representa el texto con las palabras como elementos de esta lista.
```python
    # Usando la librerya spacy
    def spacy_tokenize_book(self):
        book = nlp(self.plan_text)
        tokens = [t.orth_ for t in book]
        return tokens
```
Se instancia un libro, pasando como parametro el libro en archivo txt.
```python
book_papelucho = Book('Papelucho.txt')
```
Este retorna una lista con las palabras dentro de ella.
```python
# CANTIDAD DE TOKENS QUE COMPONEN LA LISTA
print(len(book_papelucho.spacy_tokenize_book()))
# TIPO DE ELEMENTO QUE RETORNLA LA FUNCION
print(type(book_papelucho.spacy_tokenize_book()))
```
El retorno es:
```bash
20702
<class 'list'>
```
## Eliminar 'stop-words'
Las stop-words son palabras que pueden ser importantes en la comunicación humana pero tienen poco valor para las máquinas. spaCy viene con una lista predeterminada de palabras y esta se ocupa a continuación con el metodo is_stop(). 

```python
def spacy_rm_stop_words(self):
        filtered_tokens = [token for token in nlp(self.plan_text) if not token.is_stop]
        return filtered_tokens
```
El retorno de esta funcion es una lista de elementos sin las stop-words de la lista propia de spaCy.

```python
# CANTIDAD DE TOKENS QUE COMPONEN LA LISTA SIN STOP WORDS
print(len(book_papelucho.spacy_rm_stop_words()))
# TIPO DE ELEMENTO QUE RETORNLA LA FUNCION
print(type(book_papelucho.spacy_rm_stop_words()))
```
El retorno es:
```bash
9112
<class 'list'>
```

## Normalizar
El siguiente paso en el flujo de trabajo consiste en normalizar el texto. El tokenizador reconoce formas como caminar, Caminar y CAMINAR como formas distintas. Además, el documento puede tener números y palabras compuestas por caracteres alfanuméricos y otros símbolos tales como #Ar1anaG. Si no interesan estas palabras, y se quiere que en la lista aparezcan solamente las formas convencionales (por ejemplo, caminar, sólo en minúsculas) se debe normalizar el texto. Además se eliminan palabras con menos de 4 caracteres.
```python
    def normalize(self):
        book = nlp(self.plan_text)
        words = [t.orth_ for t in book if not t.is_punct | t.is_stop]
        lexical_tokens = [t.lower() for t in words if len(t) > 3 and     
        t.isalpha()]
        return lexical_tokens
```
Utilizando está función retorna una nueva lista de elemenetos con las palabras normalizadas y sin las que tienene menos de 4 caracteres.

```python
# CANTIDAD DE TOKENS QUE COMPONEN LA LISTA NORMALIZADA
print(len(book_papelucho.normalize()))
print(type(book_papelucho.normalize()))
```
Lo que retorn:
```bash
6980
<class 'list'>
```



## Lematizar
Relaciona una palabra flexionada o derivada con su forma canónica o lema. Y un lema no es otra cosa que la forma que tienen las palabras cuando se buscas en el diccionario.
La lematización es un proceso clave en muchas tareas prácticas de PLN, pero tiene dos costos. Primero, es un proceso que consume recursos (sobre todo tiempo). Segundo, suele ser probabilística, así que en algunos casos obtendremos resultados inesperados.
```python
    def lematize(self):
        book = nlp(self.plan_text)
        return [tok.lemma_.lower() for tok in book if tok.pos_ != 'PRON']
```
Esta funcion retorna una nueva lista con los elementos lematizados.

El retorno es:

```python
# CANTIDAD DE TOKENS QUE COMPONEN LA LISTA NORMALIZADA
print(len(book_papelucho.lematize()))
print(type(book_papelucho.lematize()))
```
Lo que retorna:
```bash
18037
<class 'list'>
```
## Bag of words
La bolsa de palabras agrupa y ordena segun frecuencia de palabras en la lista de elementos del texo.

Esta función admite la entrada de 1 parametro que definen la lista de tokenes a ser avaluada.
+ "Default": utiliza la lista de tokens sin numeros ni caracteres especiales.
+ "lematized": utiliza la lista de tokens lematizados.
+ "normalized": utiliza la lista de tokens normalizados.
```python
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
```
Esta función retorna una lista de tuplas, con el primer valor como la palabra y el segundo la cantidad de veces que se encuentra en la lista de entrada, esta lista retornada es ordenada.

```python
print(book1.wordfreq("normalized")[-5:])
print(book1.wordfreq()[-5:])
print(book1.wordfreq("lematized")[-5:])
```
El retorno es:
```
[('resulta', 43), ('gomez', 44), ('javier', 48), ('papa', 57), ('mama', 93)]
[('a', 586), ('la', 603), ('de', 619), ('que', 1003), ('y', 1187)]
[('a', 586), ('de', 619), ('que', 678), ('y', 1187), ('el', 1360)]
```
## Bolsa de palabras de todos los libros.
Se ejecuta la funcion iterando sobre la lista de libros.

```bash
# Analisis de sentimientos con Python

El **análisis de sentimientos** es una herramienta poderosa que permite a los computadores comprender el tono subjetivo subyacente de un texto. Esto es algo con lo que los humanos tienen dificultades, tampoco es tan fácil para los computadores... Pero con las herramientas adecuadas y Python, se puede usar el análisis de sentimientos para comprender mejor el sentimiento de un texto.

## Uso del procesamiento del lenguaje natural para preprocesar y limpiar datos de texto
Cualquier flujo de trabajo de análisis de sentimientos comienza con la carga de datos. Pero, ¿qué haces una vez que se han cargado los datos? Debe procesarlo a través de una canalización de procesamiento de lenguaje natural antes de poder hacer algo interesante con él.

Los pasos necesarios incluyen (pero no se limitan a) los siguientes:

1.  Tokenización de oraciones para dividir el texto en oraciones, palabras u otras unidades.
2.  Eliminar palabras vacías como "si", "pero", "o", etc.
3.  Normalizar palabras condensando todas las formas de una palabra en una sola forma.
4.  Vectorización de texto convirtiendo el texto en una representación numérica para el consumo de su clasificador.
  
Todos estos pasos sirven para reducir el ruido inherente a cualquier texto legible por humanos y mejorar la precisión de los resultados de su clasificador.

Instalación de librerias
```bash
#bash
$ pip3 install spacy==2.3.5
$ python3 -m spacy download es_core_news_sm
```

Se inicia creando una clase para ordenar el trabajo sobre la lista de libros (Books), donde esta clase recibe como parametro el nombre del archivo. Además esta clase tienen los siguientes atributos:
+   tittle = titulo del libro en el que se esta trabajando.
+   path_books = el PATH de la carpeta donde se encuentran los libros ( books).
+   plan_text = es el txt representado como un gran string.
```python

class Book():
    # Los libros deben estár en la carpeta books dentro del proyecto
    def __init__(self, txt_file):
        self.tittle = txt_file[:-3]
        self.path_books = pathlib.Path().resolve() / "books"
        self.plan_text = Path(self.path_books / txt_file).read_text()
        # TOKENIZED_BOOK puede usar las funciones con y sin stopwords
        self.tokenized_book = self.pre_tokenize_book()
        # Using spacy
        self.spacy_tokenized_book = self.spacy_tokenize_book()
        self.lenght = self.lenght_book_func()
        self.set_of_words = self.create_set_words()
```



## Tokenizar
La tokenización es el proceso de dividir fragmentos de texto en partes más pequeñas. ***spaCy*** viene con una canalización de procesamiento predeterminada que comienza con la tokenización, lo que hace que este proceso sea muy sencillo. En spaCy, se pueden hacer tokenización de oraciones o tokenización de palabras:

+   La tokenización de palabras divide el texto en palabras individuales.
+   La tokenización de oraciones divide el texto en oraciones individuales.
  
En este trabajo, se usará tokenización de palabras para separar el texto en palabras individuales.

Se agrega la función **spacy_tokenize_book** a la clase. Esta retorna una lista que representa el texto con las palabras como elementos de esta lista.
```python
    # Usando la librerya spacy
    def spacy_tokenize_book(self):
        book = nlp(self.plan_text)
        tokens = [t.orth_ for t in book]
        return tokens
```
Se instancia un libro, pasando como parametro el libro en archivo txt.
```python
book_papelucho = Book('Papelucho.txt')
```
Este retorna una lista con las palabras dentro de ella.
```python
# CANTIDAD DE TOKENS QUE COMPONEN LA LISTA
print(len(book_papelucho.spacy_tokenize_book()))
# TIPO DE ELEMENTO QUE RETORNLA LA FUNCION
print(type(book_papelucho.spacy_tokenize_book()))
```
El retorno es:
```bash
20702
<class 'list'>
```
## Eliminar 'stop-words'
Las stop-words son palabras que pueden ser importantes en la comunicación humana pero tienen poco valor para las máquinas. spaCy viene con una lista predeterminada de palabras y esta se ocupa a continuación con el metodo is_stop(). 

```python
def spacy_rm_stop_words(self):
        filtered_tokens = [token for token in nlp(self.plan_text) if not token.is_stop]
        return filtered_tokens
```
El retorno de esta funcion es una lista de elementos sin las stop-words de la lista propia de spaCy.

```python
# CANTIDAD DE TOKENS QUE COMPONEN LA LISTA SIN STOP WORDS
print(len(book_papelucho.spacy_rm_stop_words()))
# TIPO DE ELEMENTO QUE RETORNLA LA FUNCION
print(type(book_papelucho.spacy_rm_stop_words()))
```
El retorno es:
```bash
9112
<class 'list'>
```

## Normalizar
El siguiente paso en el flujo de trabajo consiste en normalizar el texto. El tokenizador reconoce formas como caminar, Caminar y CAMINAR como formas distintas. Además, el documento puede tener números y palabras compuestas por caracteres alfanuméricos y otros símbolos tales como #Ar1anaG. Si no interesan estas palabras, y se quiere que en la lista aparezcan solamente las formas convencionales (por ejemplo, caminar, sólo en minúsculas) se debe normalizar el texto. Además se eliminan palabras con menos de 4 caracteres.
```python
    def normalize(self):
        book = nlp(self.plan_text)
        words = [t.orth_ for t in book if not t.is_punct | t.is_stop]
        lexical_tokens = [t.lower() for t in words if len(t) > 3 and     
        t.isalpha()]
        return lexical_tokens
```
Utilizando está función retorna una nueva lista de elemenetos con las palabras normalizadas y sin las que tienene menos de 4 caracteres.

```python
# CANTIDAD DE TOKENS QUE COMPONEN LA LISTA NORMALIZADA
print(len(book_papelucho.normalize()))
print(type(book_papelucho.normalize()))
```
Lo que retorn:
```bash
6980
<class 'list'>
```



## Lematizar
Relaciona una palabra flexionada o derivada con su forma canónica o lema. Y un lema no es otra cosa que la forma que tienen las palabras cuando se buscas en el diccionario.
La lematización es un proceso clave en muchas tareas prácticas de PLN, pero tiene dos costos. Primero, es un proceso que consume recursos (sobre todo tiempo). Segundo, suele ser probabilística, así que en algunos casos obtendremos resultados inesperados.
```python
    def lematize(self):
        book = nlp(self.plan_text)
        return [tok.lemma_.lower() for tok in book if tok.pos_ != 'PRON']
```
Esta funcion retorna una nueva lista con los elementos lematizados.

El retorno es:

```python
# CANTIDAD DE TOKENS QUE COMPONEN LA LISTA NORMALIZADA
print(len(book_papelucho.lematize()))
print(type(book_papelucho.lematize()))
```
Lo que retorna:
```bash
18037
<class 'list'>
```
## Bag of words
La bolsa de palabras agrupa y ordena segun frecuencia de palabras en la lista de elementos del texo.

Esta función admite la entrada de 1 parametro que definen la lista de tokenes a ser avaluada.
+ "Default": utiliza la lista de tokens sin numeros ni caracteres especiales.
+ "lematized": utiliza la lista de tokens lematizados.
+ "normalized": utiliza la lista de tokens normalizados.
```python
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
```
Esta función retorna una lista de tuplas, con el primer valor como la palabra y el segundo la cantidad de veces que se encuentra en la lista de entrada, esta lista retornada es ordenada.

```python
print(book1.wordfreq("normalized")[-5:])
print(book1.wordfreq()[-5:])
print(book1.wordfreq("lematized")[-5:])
```
El retorno es:
```
[('resulta', 43), ('gomez', 44), ('javier', 48), ('papa', 57), ('mama', 93)]
[('a', 586), ('la', 603), ('de', 619), ('que', 1003), ('y', 1187)]
[('a', 586), ('de', 619), ('que', 678), ('y', 1187), ('el', 1360)]
```
## Bolsa de palabras de todos los libros.
Se ejecuta la funcion iterando sobre la lista de libros.
```
Titulo: Alejando Pérez Visa - La saga de Darren Shan 01 - El Tenebroso Cirque du Freak.txt
Titulo: Alejando Pérez Visa - La saga de Darren Shan 02 - El Asistente del Vampiro.txt
Titulo: Alejando Pérez Visa - La saga de Darren Shan 03 - Túneles de Sangre.txt
Titulo: Alejando Pérez Visa - La saga de Darren Shan 04 - La Montaña de los Vampiros.txt
Titulo: Alejando Pérez Visa - La saga de Darren Shan 05 - La Ordalía de la Muerte.txt
Titulo: Alejando Pérez Visa - La saga de Darren Shan 06 - El Príncipe Vampiro.txt
Titulo: Alejando Pérez Visa - La saga de Darren Shan 07 - Cazadores del Crepúsculo.txt
Titulo: Alejando Pérez Visa - La saga de Darren Shan 08 - Aliados de la Noche.txt
Titulo: Alejando Pérez Visa - La saga de Darren Shan 09 - Asesinos del Alba.txt
Titulo: Alejando Pérez Visa - La saga de Darren Shan 10 - El Lago de las Almas.txt
Titulo: Alejando Pérez Visa - La saga de Darren Shan 11 - El Señor de las Sombras.txt
Titulo: Alejando Pérez Visa - La saga de Darren Shan 12 - Hijos del Destino.txt
Titulo: Arthur Conan Doyle - El signo de los cuatro.txt
Titulo: Arthur Conan Doyle - Estudio en Escarlata.txt
Titulo: C. S. Lewis - Las Crónicas de Narnia 1 - El León, la Bruja y el Ropero.txt
Titulo: C. S. Lewis - Las Crónicas de Narnia 2 - El Principe Caspian.txt
Titulo: C. S. Lewis - Las Crónicas de Narnia 3 - La Travesia del Explorador del Amanecer.txt
Titulo: C. S. Lewis - Las Crónicas de Narnia 4 - La Silla de Plata.txt
Titulo: C. S. Lewis - Las Crónicas de Narnia 5 - El Caballo y su Niño.txt
Titulo: C. S. Lewis - Las Crónicas de Narnia 6 - El Sobrino del Mago.txt
Titulo: C. S. Lewis - Las Crónicas de Narnia 7 - La Última Batalla.txt
Titulo: Christopher Paolini - El Legado 1 - Eragon.txt
Titulo: Christopher Paolini - El Legado 2 - Eldest.txt
Titulo: Christopher Paolini - El Legado 3 - Brisingr.txt
Titulo: Dan Brown - El Código Da Vinci.txt
Titulo: Dan Brown - El Símbolo Perdido.txt
Titulo: Dan Brown - La Conspiración.txt
Titulo: Dan Brown - La Fortaleza Digital.txt
Titulo: Dan Brown - Ángeles y Demonios.txt
Titulo: David Bischoff - Juegos de Guerra.txt
Titulo: Gabriel García Márquez - Vivir para contarla.txt
Titulo: George Norman Lippert - James Potter 1 - La Encrucijada de los Mayores.txt
Titulo: George Norman Lippert - James Potter 2 - La Maldición del Guardián.txt
Titulo: George R. R. Martin - Canción de Hielo y Fuego 1 - Juego de Tronos.txt
Titulo: George R. R. Martin - Canción de Hielo y Fuego 2 - Choque de Reyes.txt
Titulo: George R. R. Martin - Canción de Hielo y Fuego 3 - Tormenta de espadas I.txt
Titulo: George R. R. Martin - Canción de Hielo y Fuego 3 - Tormenta de espadas II.txt
Titulo: Isaac Asimov - Las Amenazas de Nuestro Mundo.txt
Titulo: J.K. Rowling - Harry Potter 1 - La Piedra Filosofal.txt
Titulo: J.K. Rowling - Harry Potter 2 - La Cámara Secreta.txt
Titulo: J.K. Rowling - Harry Potter 3 - El Prisionero de Azkaban.txt
Titulo: J.K. Rowling - Harry Potter 4 - El Cáliz de Fuego.txt
Titulo: J.K. Rowling - Harry Potter 5 - La Orden del Fenix.txt
Titulo: J.K. Rowling - Harry Potter 6 - El Misterio del Príncipe.txt
Titulo: J.K. Rowling - Harry Potter 7 - Las Reliquias de la Muerte.txt
Titulo: J.M. Barrie - Peter Pan.txt
Titulo: Julio Verne - Viaje al Centro de la Tierra.txt
Titulo: Justin Somper - Vampiratas 1 - Demonios del Oceano.txt
Titulo: Justin Somper - Vampiratas 2 - Una ola de Terror.txt
Titulo: Justin Somper - Vampiratas 3 - Emboscada en el Océano.txt
Titulo: Justin Somper - Vampiratas 4 - Sangre de Capitan.txt
Titulo: Katherine Neville - El Ocho.txt
Titulo: Laura Gallego García - Finis Mundi.txt
Titulo: Laura Gallego García - La emperatriz de los Etéreos.txt
Titulo: Lisa Jane Smith - Serie Diarios Vampiricos 1 - Despertar - Awakening.txt
Titulo: Lisa Jane Smith - Serie Diarios Vampiricos 2 - Conflicto - The Struggle.txt
Titulo: Lisa Jane Smith - Serie Diarios Vampiricos 3 - Furia - The Fury.txt
Titulo: Lisa Jane Smith - Serie Diarios Vampiricos 4 - Invocación - Dark Reunion.txt
Titulo: Lisa Jane Smith - Serie Diarios Vampiricos 5 - El regreso - Anochecer.txt
Titulo: Manel Loureiro - Apocalipsis Z.txt
Titulo: Max Brooks - Guerra Mundial Z.txt
Titulo: Michael Ende - La Historia Interminable.txt
Titulo: Neil Gaiman - Stardust.txt
Titulo: Patrick Süskind - El Perfume.txt
Titulo: Paulo Coelho - El Alquimista.txt
Titulo: R.A. Salvatore - 1. El Elfo Oscuro 1 - La Morada.txt
Titulo: R.A. Salvatore - 1. El Elfo Oscuro 2 - El Exilio.txt
Titulo: R.A. Salvatore - 1. El Elfo Oscuro 3 - El Refugio.txt
Titulo: R.A. Salvatore - 2. El valle del viento helado 1 - La Piedra de Cristal.txt
Titulo: R.A. Salvatore - 2. El valle del viento helado 2 - Ríos de Plata.txt
Titulo: R.A. Salvatore - 2. El valle del viento helado 3 - La Gema del Halfling.txt
Titulo: R.A. Salvatore - 3. El legado del drow 1 - El Legado.txt
Titulo: R.A. Salvatore - 3. El legado del drow 2 - Noche sin Estrellas.txt
Titulo: R.A. Salvatore - 3. El legado del drow 3 - Cerco de Oscuridad.txt
Titulo: R.A. Salvatore - 3. El legado del drow 4 - Luz en las Tinieblas.txt
Titulo: R.A. Salvatore - 4. Sendas de tinieblas 1 - El estigma de Errtu.txt
Titulo: R.A. Salvatore - 4. Sendas de tinieblas 2 - La columna del mundo.txt
Titulo: R.A. Salvatore - 4. Sendas de tinieblas 3 - El Siervo de La Piedra.txt
Titulo: R.A. Salvatore - 4. Sendas de tinieblas 4 - El mar de las espadas.txt
Titulo: R.A. Salvatore - 5. Las espadas del cazador 2 - Los Senderos de la Muerte.txt
Titulo: R.A. Salvatore - 5. Las espadas del cazador 3 - Las dos espadas.txt
Titulo: Rick Riordan - Percy Jackson y Los Olímpicos 1 - El ladrón del rayo.txt
Titulo: Rick Riordan - Percy Jackson y Los Olímpicos 2 - El mar de los monstruos.txt
Titulo: Rick Riordan - Percy Jackson y Los Olímpicos 3 - La maldicion del Titan.txt
Titulo: Rick Riordan - Percy Jackson y Los Olímpicos 4 - La batalla del laberinto.txt
Titulo: Robert E. Howard - Conan 01 - Conan.txt
Titulo: Robert Ludlum - El caso Bourne.txt
Titulo: S.D. Perry - Resident Evil 0 - Hora Cero.txt
Titulo: S.D. Perry - Resident Evil 1 - La conspiración Umbrella.txt
Titulo: Scott Fitzgerald - El extraño caso de Benjamin Button.txt
Titulo: Stephanie Meyer - Crepúsculo 0 - Sol de Medianoche.txt
Titulo: Stephanie Meyer - Crepúsculo 1 - Crepúsculo.txt
Titulo: Stephanie Meyer - Crepúsculo 2 - Luna Nueva.txt
Titulo: Stephanie Meyer - Crepúsculo 3 - Eclipse.txt
Titulo: Stephanie Meyer - Crepúsculo 4 - Amanecer.txt
Titulo: Stephen King - Cell.txt
Titulo: Stephen King - Historias fantásticas.txt
Titulo: Stephen King - La Expedición.txt
Titulo: Stephen King - La torre Oscura I.txt
Titulo: Stephen King - The Dead Zone.txt
Titulo: Umberto Eco - El Nombre de la Rosa.txt

```

```bash
Titulo: R.A. Salvatore - 5. Las espadas del cazador 2 - Los Senderos de la Muerte
[('mithril', 248), ('bruenor', 250), ('orco', 270), ('brie', 277), ('catti', 277), ('nanfoodle', 300), ('obould', 438), ('drizzt', 548), ('orcos', 565), ('enanos', 592)]

Titulo: R.A. Salvatore - 1. El Elfo Oscuro 1 - La Morada
[('masoj', 313), ('do', 314), ('urden', 314), ('alton', 315), ('dinin', 328), ('zak', 438), ('matrona', 448), ('malicia', 474), ('casa', 550), ('drizzt', 1250)]

Titulo: Stephanie Meyer - Crepúsculo 2 - Luna Nueva
[('tenia', 272), ('cabeza', 279), ('rostro', 290), ('bella', 301), ('alice', 328), ('charlie', 362), ('ojos', 380), ('voz', 406), ('edward', 524), ('jacob', 653)]

Titulo: R.A. Salvatore - 4. Sendas de tinieblas 2 - La columna del mundo
[('priscilla', 229), ('pregunto', 234), ('jaka', 275), ('hombre', 286), ('lord', 320), ('barbaro', 329), ('feringal', 424), ('meralda', 671), ('morik', 703), ('wulfgar', 984)]

Titulo: Papelucho_soy_dislexo
[('cara', 23), ('perra', 23), ('iba', 26), ('puerta', 26), ('tenebrosa', 29), ('vaca', 33), ('dije', 35), ('tenia', 38), ('teniente', 54), ('teni', 76)]

Titulo: R.A. Salvatore - 5. Las espadas del cazador 3 - Las dos espadas
[('drow', 240), ('rey', 257), ('orco', 293), ('enano', 298), ('habian', 299), ('orcos', 300), ('enanos', 378), ('bruenor', 387), ('drizzt', 476), ('obould', 476)]

Titulo: J.K. Rowling - Harry Potter 7 - Las Reliquias de la Muerte
[('podia', 288), ('snape', 297), ('voz', 306), ('ojos', 336), ('voldemort', 440), ('dumbledore', 586), ('varita', 600), ('ron', 1167), ('hermione', 1233), ('harry', 3144)]

Titulo: Papelucho_historiador
[('realistas', 28), ('patriotas', 29), ('tierra', 32), ('colon', 36), ('carmen', 38), ('higgins', 41), ('indios', 44), ('dije', 47), ('chile', 58), ('españoles', 58)]

Titulo: R.A. Salvatore - 4. Sendas de tinieblas 3 - El Siervo de La Piedra
[('crenshinibon', 233), ('cristal', 235), ('piedra', 316), ('kimmuriel', 331), ('gy', 347), ('rai', 347), ('drow', 348), ('asesino', 361), ('jarlaxle', 769), ('entreri', 1137)]

Titulo: Justin Somper - Vampiratas 1 - Demonios del Oceano
[('li', 134), ('bart', 145), ('ojos', 150), ('tenia', 153), ('wrathe', 174), ('lorcan', 226), ('barco', 241), ('capitan', 427), ('grace', 578), ('connor', 611)]

Titulo: Katherine Neville - El Ocho
[('abadesa', 281), ('mano', 290), ('piezas', 311), ('ojos', 315), ('ajedrez', 318), ('juego', 331), ('tenia', 359), ('solarin', 456), ('mireille', 602), ('lily', 631)]

Titulo: Neil Gaiman - Stardust
[('pueblo', 94), ('señor', 98), ('cabeza', 100), ('dunstan', 106), ('muro', 111), ('pregunto', 113), ('ojos', 117), ('mano', 132), ('estrella', 221), ('tristran', 520)]

Titulo: Laura Gallego García - La emperatriz de los Etéreos
[('tenia', 104), ('maga', 116), ('opalo', 120), ('nieve', 122), ('ojos', 122), ('gelida', 130), ('emperatriz', 153), ('cristal', 190), ('aer', 413), ('bipa', 955)]

Titulo: Harry_Potter_y_el_misterio_del_principe
[('señor', 255), ('pregunto', 261), ('tenia', 291), ('malfoy', 331), ('snape', 335), ('slughorn', 337), ('hermione', 584), ('dumbledore', 721), ('ron', 739), ('harry', 2198)]

Titulo: Harry_Potter_y_la_orden_del_Fenix
[('hagrid', 447), ('profesora', 473), ('voz', 476), ('weasley', 486), ('umbridge', 501), ('dumbledore', 585), ('sirius', 613), ('ron', 1281), ('hermione', 1296), ('harry', 3959)]

Titulo: Umberto Eco - El Nombre de la Rosa
[('noche', 183), ('abadia', 190), ('iglesia', 193), ('habian', 196), ('monjes', 200), ('biblioteca', 221), ('dios', 237), ('libro', 256), ('abad', 322), ('guillermo', 768)]

Titulo: R.A. Salvatore - 3. El legado del drow 3 - Cerco de Oscuridad
[('casa', 211), ('drows', 221), ('bruenor', 259), ('habian', 277), ('matrona', 318), ('drow', 327), ('brie', 357), ('catti', 357), ('baenre', 479), ('drizzt', 556)]

Titulo: J.M. Barrie - Peter Pan
[('noche', 88), ('señora', 90), ('tenia', 98), ('michael', 109), ('darling', 117), ('niños', 127), ('john', 134), ('garfio', 178), ('wendy', 357), ('peter', 400)]

Titulo: Papelucho_casi_huerfano
[('dije', 32), ('tenia', 37), ('chilecomparte', 42), ('cl', 42), ('www', 42), ('xstar', 42), ('señor', 47), ('tia', 48), ('mama', 52), ('cura', 67)]

Titulo: Rick Riordan - Percy Jackson y Los Olímpicos 1 - El ladrón del rayo
[('dioses', 115), ('madre', 119), ('ares', 120), ('ojos', 147), ('chiron', 162), ('tenia', 202), ('dije', 242), ('percy', 256), ('annabeth', 399), ('grover', 442)]

Titulo: Papelucho_misionero
[('avion', 41), ('diamantes', 46), ('dije', 47), ('tenia', 49), ('juanito', 50), ('africa', 61), ('siku', 64), ('papa', 98), ('mama', 109), ('tucu', 132)]

Titulo: Justin Somper - Vampiratas 3 - Emboscada en el Océano
[('cabeza', 45), ('agua', 46), ('tenia', 46), ('flynn', 47), ('pez', 49), ('joao', 53), ('cali', 99), ('jez', 129), ('bart', 182), ('connor', 234)]

Titulo: Robert Ludlum - El caso Bourne
[('tenia', 246), ('ojos', 264), ('mano', 267), ('puerta', 278), ('marie', 305), ('cain', 306), ('carlos', 481), ('jason', 565), ('bourne', 690), ('hombre', 849)]

Titulo: Max Brooks - Guerra Mundial Z
[('sabia', 120), ('tenian', 125), ('muertos', 139), ('teniamos', 156), ('mundo', 163), ('podia', 213), ('tenia', 232), ('habian', 237), ('gente', 255), ('guerra', 271)]

Titulo: Harry_Potter_y_la_piedra_filosofal
[('podia', 120), ('malfoy', 123), ('dudley', 136), ('tenia', 150), ('dumbledore', 156), ('snape', 166), ('hermione', 272), ('hagrid', 364), ('ron', 417), ('harry', 1301)]

Titulo: Rick Riordan - Percy Jackson y Los Olímpicos 3 - La maldicion del Titan
[('parecia', 126), ('ojos', 130), ('dije', 146), ('artemisa', 160), ('tenia', 161), ('bianca', 163), ('annabeth', 202), ('grover', 266), ('zoë', 336), ('thalia', 373)]

Titulo: Stephen King - The Dead Zone
[('cabeza', 204), ('ojos', 207), ('años', 215), ('hombre', 223), ('greg', 236), ('habian', 257), ('stillson', 263), ('tenia', 264), ('sarah', 372), ('johnny', 1530)]

Titulo: Papelucho_perdido
[('beleundez', 25), ('señor', 26), ('dije', 29), ('tenia', 29), ('mama', 30), ('iba', 31), ('tren', 31), ('avion', 38), ('papa', 40), ('ji', 71)]

Titulo: Harry_Potter_y_la_camara_ecreta
[('pregunto', 159), ('ojos', 164), ('weasley', 180), ('señor', 186), ('voz', 188), ('malfoy', 217), ('lockhart', 234), ('hermione', 322), ('ron', 691), ('harry', 1607)]

Titulo: Lisa Jane Smith - Serie Diarios Vampiricos 5 - El regreso - Anochecer
[('ojos', 259), ('podia', 275), ('caroline', 292), ('tenia', 304), ('meredith', 525), ('matt', 529), ('stefan', 571), ('bonnie', 740), ('damon', 879), ('elena', 1049)]

Titulo: Stephanie Meyer - Crepúsculo 3 - Eclipse
[('rostro', 236), ('mano', 262), ('tenia', 284), ('charlie', 297), ('voz', 341), ('bella', 361), ('alice', 391), ('ojos', 433), ('jacob', 706), ('edward', 992)]

Titulo: R.A. Salvatore - 2. El valle del viento helado 3 - La Gema del Halfling
[('puerta', 231), ('drow', 247), ('pook', 304), ('brie', 309), ('catti', 309), ('regis', 311), ('entreri', 389), ('bruenor', 541), ('wulfgar', 542), ('drizzt', 792)]

Titulo: Rick Riordan - Percy Jackson y Los Olímpicos 4 - La batalla del laberinto
[('rachel', 144), ('percy', 152), ('ojos', 154), ('parecia', 154), ('laberinto', 159), ('nico', 181), ('tyson', 210), ('tenia', 213), ('grover', 217), ('annabeth', 449)]

Titulo: Lisa Jane Smith - Serie Diarios Vampiricos 3 - Furia - The Fury
[('rostro', 106), ('voz', 129), ('alaric', 143), ('matt', 173), ('ojos', 195), ('meredith', 202), ('bonnie', 229), ('damon', 259), ('stefan', 445), ('elena', 655)]

Titulo: Patrick Süskind - El Perfume
[('mundo', 93), ('nariz', 94), ('vida', 94), ('fragancia', 134), ('tenia', 143), ('olor', 144), ('podia', 146), ('perfume', 170), ('baldini', 235), ('grenouille', 388)]

Titulo: R.A. Salvatore - 3. El legado del drow 4 - Luz en las Tinieblas
[('duende', 208), ('harkle', 211), ('errtu', 242), ('bruenor', 279), ('mar', 293), ('drow', 366), ('deudermont', 411), ('brie', 537), ('catti', 537), ('drizzt', 912)]

Titulo: Papelucho_mi_hermana_Ji
[('tenia', 34), ('casa', 41), ('com', 42), ('lectulandia', 42), ('pagina', 42), ('www', 42), ('jolly', 45), ('papa', 58), ('mama', 120), ('ji', 134)]

Titulo: R.A. Salvatore - 4. Sendas de tinieblas 1 - El estigma de Errtu
[('bruenor', 206), ('jarlaxle', 225), ('brie', 229), ('catti', 229), ('hombre', 246), ('drow', 256), ('asesino', 280), ('drizzt', 468), ('wulfgar', 486), ('entreri', 631)]

Titulo: Lisa Jane Smith - Serie Diarios Vampiricos 1 - Despertar - Awakening
[('cabeza', 101), ('tyler', 106), ('damon', 107), ('matt', 109), ('voz', 148), ('meredith', 156), ('bonnie', 202), ('ojos', 225), ('stefan', 366), ('elena', 586)]

Titulo: S.D. Perry - Resident Evil 0 - Hora Cero
[('cabeza', 91), ('podia', 93), ('suelo', 96), ('volvio', 100), ('habian', 122), ('tren', 124), ('tenia', 166), ('puerta', 236), ('rebecca', 493), ('billy', 515)]

Titulo: Stephanie Meyer - Crepúsculo 0 - Sol de Medianoche
[('chica', 131), ('jessica', 131), ('pensamientos', 131), ('voz', 132), ('cabeza', 134), ('alice', 164), ('tenia', 195), ('ojos', 224), ('podia', 235), ('bella', 419)]

Titulo: R.A. Salvatore - 2. El valle del viento helado 1 - La Piedra de Cristal
[('ciudad', 172), ('podia', 177), ('ciudades', 203), ('regis', 243), ('drow', 244), ('habian', 310), ('bruenor', 321), ('kessell', 353), ('wulfgar', 458), ('drizzt', 568)]

Titulo: Stephanie Meyer - Crepúsculo 1 - Crepúsculo
[('parecia', 192), ('mano', 195), ('tenia', 197), ('charlie', 210), ('bella', 213), ('alice', 218), ('rostro', 227), ('voz', 370), ('ojos', 416), ('edward', 554)]

Titulo: Robert E. Howard - Conan 01 - Conan
[('mano', 99), ('suelo', 101), ('cabeza', 105), ('puerta', 105), ('tenia', 107), ('espada', 125), ('ojos', 137), ('hombre', 147), ('cimmerio', 163), ('conan', 544)]

Titulo: Harry_Potter_y_las_reliquias_de_la_muerte
[('podia', 288), ('snape', 297), ('voz', 306), ('ojos', 336), ('voldemort', 440), ('dumbledore', 586), ('varita', 600), ('ron', 1167), ('hermione', 1233), ('harry', 3144)]

Titulo: Papelucho
[('ganas', 34), ('padre', 36), ('domitila', 40), ('casa', 42), ('mañana', 43), ('resulta', 43), ('gomez', 44), ('javier', 48), ('papa', 57), ('mama', 93)]

Titulo: R.A. Salvatore - 3. El legado del drow 1 -  El Legado
[('enano', 183), ('vierna', 259), ('regis', 263), ('wulfgar', 303), ('entreri', 310), ('brie', 319), ('catti', 319), ('drow', 353), ('bruenor', 433), ('drizzt', 933)]

Titulo: Stephen King - Historias fantásticas
[('hombre', 73), ('años', 74), ('rand', 74), ('shapiro', 77), ('podia', 79), ('tio', 88), ('ojos', 94), ('mano', 103), ('tenia', 105), ('rocky', 106)]

Titulo: R.A. Salvatore - 1. El Elfo Oscuro 2 - El Exilio
[('capataz', 204), ('zaknafein', 213), ('enano', 217), ('clak', 223), ('casa', 251), ('matrona', 262), ('drow', 319), ('malicia', 406), ('belwar', 609), ('drizzt', 1069)]

Titulo: Laura Gallego García - Finis Mundi
[('pregunto', 93), ('tenia', 95), ('habian', 98), ('monje', 107), ('alinor', 114), ('mundo', 120), ('juglar', 194), ('lucia', 275), ('michel', 559), ('mattius', 560)]

Titulo: R.A. Salvatore - 3. El legado del drow 2 - Noche sin Estrellas
[('ojos', 188), ('tenia', 207), ('baenre', 269), ('joven', 278), ('jarlaxle', 286), ('entreri', 337), ('drow', 355), ('brie', 567), ('catti', 567), ('drizzt', 864)]

Titulo: Michael Ende - La Historia Interminable
[('respondio', 178), ('puerta', 186), ('ojos', 199), ('podia', 199), ('voz', 199), ('tenia', 213), ('fujur', 219), ('fantasia', 268), ('atreyu', 804), ('bastian', 1178)]

Titulo: Papelucho_detective
[('señor', 32), ('pensaba', 34), ('iba', 38), ('chirigüe', 39), ('tenia', 48), ('domi', 63), ('dije', 70), ('casa', 79), ('papa', 91), ('mama', 103)]

Titulo: Papelucho_en_vacaciones
[('lectulandia', 46), ('pagina', 46), ('www', 46), ('amos', 52), ('teni', 52), ('pelli', 55), ('habi', 78), ('an', 79), ('ma', 88), ('bartolo', 96)]

Titulo: R.A. Salvatore - 4. Sendas de tinieblas 4 - El mar de las espadas
[('pregunto', 231), ('drow', 257), ('regis', 313), ('elfo', 321), ('lorinel', 345), ('bruenor', 386), ('brie', 388), ('catti', 402), ('wulfgar', 585), ('drizzt', 696)]

Titulo: Manel Loureiro - Apocalipsis Z
[('seguro', 128), ('casa', 138), ('entrada', 138), ('enorme', 154), ('punto', 157), ('cabeza', 172), ('podia', 180), ('par', 189), ('puerta', 213), ('tenia', 246)]

Titulo: Harry_Potter_y_el_caliz_de_fuego
[('moody', 350), ('tenia', 354), ('hagrid', 362), ('weasley', 380), ('voz', 383), ('dumbledore', 564), ('señor', 642), ('hermione', 835), ('ron', 980), ('harry', 2840)]

Titulo: Paulo Coelho - El Alquimista
[('hombre', 73), ('viento', 79), ('hombres', 86), ('vida', 98), ('ovejas', 105), ('viejo', 124), ('mundo', 125), ('alquimista', 151), ('desierto', 172), ('muchacho', 383)]

Titulo: Scott Fitzgerald - El extraño caso de Benjamin Button
[('padre', 21), ('voz', 21), ('hildegarde', 23), ('roscoe', 24), ('edad', 26), ('hijo', 39), ('años', 58), ('señor', 63), ('button', 97), ('benjamin', 98)]

Titulo: Rick Riordan - Percy Jackson y Los Olímpicos 2 - El mar de los monstruos
[('ojos', 95), ('campamento', 121), ('luke', 130), ('percy', 149), ('clarisse', 151), ('dije', 151), ('grover', 153), ('tenia', 181), ('tyson', 329), ('annabeth', 437)]

Titulo: Papelucho_y_mi_hermano_hippie
[('dije', 52), ('soto', 52), ('iba', 55), ('chori', 56), ('mama', 57), ('domi', 63), ('neron', 65), ('javier', 84), ('chorizo', 93), ('xstar', 119)]

Titulo: Papelucho_y_el_marciano
[('urquieta', 29), ('ji', 30), ('tenia', 39), ('domi', 41), ('casa', 42), ('choclo', 46), ('dije', 58), ('papa', 61), ('mama', 72), ('det', 110)]

Titulo: Stephen King - Cell
[('mujer', 158), ('mano', 176), ('director', 178), ('habian', 184), ('tenia', 210), ('hombre', 271), ('jordan', 460), ('alice', 521), ('tom', 836), ('clay', 1565)]

Titulo: Lisa Jane Smith - Serie Diarios Vampiricos 2 - Conflicto - The Struggle
[('matt', 95), ('caroline', 102), ('casa', 107), ('voz', 112), ('meredith', 183), ('damon', 187), ('ojos', 192), ('bonnie', 308), ('stefan', 395), ('elena', 666)]

Titulo: Justin Somper - Vampiratas 2 - Una ola de Terror
[('cabeza', 187), ('jacoby', 188), ('kuo', 190), ('ojos', 195), ('barco', 304), ('cheng', 360), ('li', 403), ('capitan', 495), ('grace', 811), ('connor', 847)]

Titulo: R.A. Salvatore - 1. El Elfo Oscuro 3 - El Refugio
[('tenia', 168), ('pantera', 177), ('guenhwyvar', 192), ('vigilante', 205), ('elfo', 213), ('podia', 242), ('roddy', 336), ('montolio', 340), ('drow', 599), ('drizzt', 1039)]

Titulo: Stephen King - La torre Oscura I
[('habian', 92), ('luz', 101), ('ojos', 110), ('cort', 112), ('cabeza', 113), ('jake', 154), ('negro', 173), ('chico', 220), ('hombre', 239), ('pistolero', 615)]

Titulo: ejemplo_harry
[('harry', 8), ('tenia', 8), ('colagusano', 10), ('habian', 10), ('puerta', 10), ('señor', 10), ('mansion', 14), ('voz', 14), ('ryddle', 24), ('frank', 32)]

Titulo: S.D. Perry - Resident Evil 1 - La conspiración Umbrella
[('stars', 103), ('habian', 135), ('equipo', 142), ('rebecca', 153), ('tenia', 177), ('wesker', 239), ('jill', 326), ('barry', 329), ('puerta', 363), ('chris', 404)]

Titulo: Julio Verne - Viaje al Centro de la Tierra
[('duda', 71), ('preciso', 73), ('axel', 80), ('pies', 93), ('tierra', 94), ('agua', 103), ('mar', 112), ('hans', 162), ('profesor', 174), ('tio', 410)]

Titulo: Harry_Potter_y_el_prisionero_de_Azkaban
[('voz', 222), ('pregunto', 226), ('profesor', 243), ('snape', 245), ('hagrid', 253), ('black', 307), ('lupin', 401), ('hermione', 656), ('ron', 769), ('harry', 1935)]

Titulo: Papelucho_en_la_clinica
[('domi', 41), ('iba', 43), ('rubilar', 46), ('profeta', 48), ('dije', 53), ('señor', 53), ('tenia', 58), ('casa', 68), ('mama', 90), ('papa', 149)]

Titulo: J.K. Rowling - Harry Potter 6 - El Misterio del Príncipe
[('señor', 255), ('pregunto', 261), ('tenia', 291), ('malfoy', 331), ('snape', 335), ('slughorn', 337), ('hermione', 584), ('dumbledore', 721), ('ron', 739), ('harry', 2198)]

Titulo: Stephen King - La Expedición
[('buddy', 63), ('cabeza', 63), ('mami', 64), ('mujer', 68), ('casa', 76), ('carune', 80), ('tenia', 128), ('reg', 132), ('george', 143), ('abuela', 173)]

Titulo: Justin Somper - Vampiratas 4 - Sangre de Capitan
[('mano', 254), ('bart', 260), ('pregunto', 264), ('cabeza', 332), ('lorcan', 381), ('zu', 385), ('mosh', 388), ('capitan', 439), ('connor', 841), ('grace', 878)]

Titulo: R.A. Salvatore - 2. El valle del viento helado 2 - Ríos de Plata
[('amigos', 207), ('habian', 218), ('enano', 236), ('brie', 252), ('catti', 252), ('entreri', 359), ('regis', 371), ('wulfgar', 486), ('drizzt', 646), ('bruenor', 684)]

Titulo: Stephanie Meyer - Crepúsculo 4 - Amanecer
[('cara', 313), ('tenia', 343), ('carlisle', 365), ('renesmee', 368), ('podia', 377), ('alice', 396), ('jacob', 511), ('ojos', 548), ('bella', 563), ('edward', 1155)]

Titulo: Lisa Jane Smith - Serie Diarios Vampiricos 4 - Invocación - Dark Reunion
[('voz', 131), ('tyler', 148), ('vickie', 155), ('damon', 190), ('ojos', 204), ('matt', 279), ('elena', 295), ('meredith', 432), ('stefan', 559), ('bonnie', 745)]
```