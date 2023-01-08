
# 1 Preparar ambiente

virtualenv -p python3 $PWD && source $PWD/bin/activate

# 2 Instalar librerias

pip3 install pandas
pip3 install spacy
pip3 install scipy
pip3 install matplotlib
pip3 install numpy
pip3 install bleach
pip3 install sklearn
pip3 install pysentimiento
pip3 install nltk

pip install -U transformers 
pip install -U huggingface_hub

python3 -m spacy download es_core_news_sm

## pyenchant

Para chequear si una palabra existe en el diccionario en español

https://pyenchant.github.io/pyenchant/install.html