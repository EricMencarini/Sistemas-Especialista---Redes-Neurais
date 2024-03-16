##################################################################################################################################
#A ideia deste código é fornecer uma análise a partir do feedback de uma palestra ou evento.                                     #
#É feito a leitura do arquivo e em seguida o código fornece uma resposta classificando os graus de contetamento do usuário a     #
#respeito do feedback usando o processamento de linguagem natural.                                                               #
##################################################################################################################################

import string      
from collections import Counter  

from nltk.tokenize import word_tokenize                         
from nltk.sentiment.vader import SentimentIntensityAnalyzer    
from nltk.corpus import stopwords       
#nlkt.download()
from googletrans import Translator

import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf
from matplotlib.backends.backend_pdf import PdfPages


#Origem do arquivo : Chat-gpt4, a partir da pergunta: 
#P:Faça um texto com muitas emoções a respeito do feedback de um aluno sobre um evento de T.I com 30 linhas

#%%
'''
Leio o arquivo de avaliações e faço a formatação do texto.
'''

texto = open('Avaliações/Avaliação_Curso.txt', encoding = 'utf-8').read()             
texto_minuscula = texto.lower()
texto_formatado = texto_minuscula.translate(str.maketrans('','',string.punctuation))
palavras_tokenizadas = word_tokenize(texto_formatado, "portuguese")
print(texto)
#print(texto_minuscula)
#print(texto_formatado)
#print("Palavras Tokenizadas: \n" , palavras_tokenizadas)
#%%

'''
Verifico se a palavra não é uma stopword, e caso seja verdadeiro, adiciono ela na minha lista de palavra formatadas.
'''

palavras_formatadas =[]
for palavra in palavras_tokenizadas:
    if palavra not in stopwords.words('portuguese'):
        palavras_formatadas.append(palavra)

print(palavras_formatadas)
#%%
'''
Lê o arquivo que classifica as emoções, faz um tratamento e adiciona na lista de emoções existentes naquele texto.
'''

lista_emocoes = []
with open('Classificador_Emoções.txt', 'r', encoding = 'utf-8') as file:
    for line in file:
        formata_linha = line.replace("\n",'').replace(",",'').replace("'",'').strip()
        palavra, emocao = formata_linha.split(':')
        #print("Palavra :" + palavra + " " + "Emocao :" + emocao)

        if palavra in palavras_formatadas:
            lista_emocoes.append(emocao)

#print(lista_emocoes)

#%%
c = Counter(lista_emocoes)     ##Contabiliza a quantidade de emoçoes por palavras daquela categoria
print("Contadores:\n", c) 
#%%
#########################
##Parte de redes Neurais#
#########################

'''
Traduz o texto para inglês para melhor funcionamento do NLTK
'''
def translate_to_english(texto):
    translator = Translator()
    traducao = translator.translate(texto, src='pt', dest='en')
    return traducao.text

'''
Função utilizada para definir a pontuação das emoções avaliadas.
'''
def analise_sentimentos(sentimento_percebido):
    score = SentimentIntensityAnalyzer().polarity_scores(sentimento_percebido)
    print(score)
    
    compound = score['compound']
    if compound > 0.5:
        print("A apresentação foi um sucesso, parabéns!")
    elif compound > 0.2:
        print("Foi uma apresentação positiva, continue assim!")
    elif compound > -0.2:
        print("Sua apresentação não causou nenhum tipo de impacto.")
    elif compound > -0.5:
        print("Sua apresentação gerou sentimentos negativos no público.")
    else:
        print("Você está demitido!!")

converte_texto_ingles = translate_to_english(texto_formatado)    
analise_sentimentos(converte_texto_ingles)




#%%
#########################
##Plotando os gráficos###
#########################
'''
Crio um arquivo PDF com as análises para serem enviadas por email.
'''
with PdfPages('Gráficos/Gráficos.pdf') as pdf:
    
    # Gráfico de barras
    fig, ax1 = plt.subplots()
    ax1.bar(c.keys(), c.values())
    fig.autofmt_xdate()
    pdf.savefig()  
    plt.close()

    # Gráfico de pizza
    plt.figure(figsize=(8, 6))
    plt.pie(c.values(), labels=c.keys(), autopct='%1.1f%%', colors=['red', 'green', 'blue', 'yellow'])
    plt.title('Gráfico de Pizza')
    pdf.savefig()
    plt.close()

    # Gráfico de dispersão
    fig, ax2 = plt.subplots()
    ax2.scatter(c.keys(), c.values(), color='red')
    fig.autofmt_xdate()
    plt.title('Gráfico de Dispersão')
    pdf.savefig()
    plt.close()

    # Gráfico de linha
    plt.figure(figsize=(8, 6))
    plt.plot(list(range(len(c))), list(c.values()), color='green', marker='o')
    plt.title('Gráfico de Linha')
    plt.xlabel('Categoria')
    plt.ylabel('Valores')
    plt.xticks(range(len(c)), c.keys())
    pdf.savefig()
    plt.close()

    pdf.close
# %%
