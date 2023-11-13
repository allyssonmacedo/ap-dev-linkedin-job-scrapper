from pymongo import MongoClient
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
import nltk
#nltk.download('punkt')

import connectmongo

client = connectmongo.connectServer()

db_connection = client['jobs-in']

collection = db_connection.get_collection('jobs')

print(collection.count_documents(filter={}))

valores_unicos = collection.find()

# Imprimir os valores
print(f"Valores únicos para a chave")
print(valores_unicos)


# # Obter todas as frases da coleção
# frases = [documento["tags"] for documento in collection.find()]

# # Tokenizar as palavras nas frases
# palavras = [palavra.lower() for frase in frases for palavra in word_tokenize(frase)]

# # Calcular a frequência das palavras
# frequencia = FreqDist(palavras)

# # Imprimir as palavras mais frequentes
# print("Palavras mais frequentes:")
# for palavra, frequencia in frequencia.most_common(10):  # As 10 palavras mais frequentes
#     print(f"{palavra}: {frequencia} vezes")
