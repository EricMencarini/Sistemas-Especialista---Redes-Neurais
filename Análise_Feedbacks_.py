##################################################################################################################################
#A ideia deste programa é fornecer uma análise a partir do feedback imposto pelo usuário a respeito das aulas da pós graduação.  #
#É feito a leitura do arquivo e em seguida o código fornece uma resposta classificando os graus de contetamento do usuário a     #
#respeito do feedback usando o processamento de linguagem natural.                                                                                    #
##################################################################################################################################

import string      
from collections import Counter  

from nltk.tokenize import word_tokenize                         
from nltk.sentiment.vader import SentimentIntensityAnalyzer    
from nltk.corpus import stopwords       
#nlkt.download()

import matplotlib.pyplot as plt


#Origem do arquivo : Chat-gpt4, a partir da pergunta: 
#P:Faça um texto com muitas emoções a respeito do feedback de um aluno sobre um módulo de pós graduação com 30 linhas


'''
Leio o arquivo de avaliações e faço a formatação do texto.
'''

texto = open('Avaliações/Avaliação_Curso.txt', encoding = 'utf-8').read()             
texto_minuscula = texto.lower()
texto_formatado = texto_minuscula.translate(str.maketrans('','',string.punctuation))
palavras_tokenizadas = word_tokenize(texto_formatado, "portuguese")
#print("Palavras Tokenizadas: \n" , palavras_tokenizadas)


'''
Verifico se a palavra não é uma stopword, e caso seja verdadeiro, adiciono ela na minha lista de palavra formatadas.
'''

palavras_formatadas =[]
for palavra in palavras_tokenizadas:
    if palavra not in stopwords.words('portuguese'):
        palavras_formatadas.append(palavra)


'''
Lê o arquivo que classifica as emoções, faz um tratamento e adiciona na lista de emoções existentes naquele texto.
'''

lista_emocoes = []
with open('Classificador_Emoções.txt', 'r', encoding = 'utf-8') as file:
    for line in file:
        formata_linha = line.replace("\n",'').replace(",",'').replace("'",'').strip()
        word, emotion = formata_linha.split(':')
        #print("Word :" + word + " " + "Emotion :" + emotion)

        if word in palavras_formatadas:
            lista_emocoes.append(emotion)

#print(lista_emocoes)


c = Counter(lista_emocoes)     ##Contabiliza a quantidade de emoçoes por palavras daquela categoria
print("Contadores:\n", c) 



#########################
##Parte de redes Neurais#
#########################

'''
Função utilizada para definir a pontuação das emoções avaliadas.
'''
def analise_sentimentos(sentimento_percebido):
    score = SentimentIntensityAnalyzer().polarity_scores(sentimento_percebido)
    print(score)
    neg = score['neg']
    pos = score['pos']
    if score['neg'] > score['pos']:
        print("Negative Sentiment")
    elif score['neg'] < score['pos']:
        print("Positive Sentiment")
    else:
        print("Neutral Sentiment")

analise_sentimentos(texto_formatado)     

#########################
##Plotando os gráficos###
#########################

fig, ax1 = plt.subplots()
ax1.bar(c.keys(), c.values())
fig.autofmt_xdate()

plt.bar(c.keys(), c.values())
plt.savefig('Gráficos/Gráfico de Barras.png')
plt.show()



