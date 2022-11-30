from sklearn.impute import SimpleImputer
from nb import naiveBayes
import pandas as pd
import numpy as np
import random

nsamples = 25       # quantidade de amostras para serem testadas
pred_index = 3      # indice da coluna que se deseja prever (irish = 3 | letter = 16)
isindexcol = None   # indice de qualquer coluna que apenas sirva como indice para os dados...
                    # ('None' se nao houver), nenhum dos dois datasets utilizados possuem...
                    # mas foi testado em datasets que possuiam, e funcionou corretamente

f = open("../datasets/irish.txt", "r") # abre o dataset
aux = f.read()      # le o dataset e armazena em uma variavel auxiliar
aux = aux.split()   # divide o que foi lido separado por espacos vazios e '\n'...
                    # obrigatoriamente o dataset nao pode conter espacos vazios
n = len(aux)        # armazena a quantidade de dados no dataset

dataset = []        # inicializa a lista do dataset
for i in range(n):  # percorre a variavel auxiliar
    dataset.append(aux[i].split(','))   # divide novamente os dados de cada elemento em 'aux'...
                                        # desta vez delimitado por ',' para obter os valores de cada dado...
                                        # o dataset deve obrigatoriamente possuir seus dados separados por virgula...
                                        # e ela nao pode ser usada para mais nada
imp = SimpleImputer(missing_values='?', strategy="most_frequent")   # inicializa o metodo de imputacao de dados faltantes se houver
                                        # dados faltantes obrigatoriamente devem ser marcados como '?'
dataset = imp.fit_transform(dataset)    # realiza a imputacao

aux = random.sample(range(n), nsamples) # gera, de forma aleatoria, indices de amostras

treino  = [x for i,x in enumerate(dataset) if i not in aux] # o que nao for amostra e utilizado para treino
samples = [x for i,x in enumerate(dataset) if i     in aux] # cria a lista de amostras baseado nos indices gerados

pred = pd.DataFrame()                   # inicializa um dataframe vazio do pandas para armazenar as predicoes
for sample in samples:                  # percorre a lista de amostras
    newpred = naiveBayes(treino, sample.tolist(), pred_index, isindexcol)
                                            # executa o algoritmo naiveBayes em cada amostra
    pred = pd.concat([pred, newpred])       # concatena a amostra testada ao dataframe de predicoes
pred.index=list(range(nsamples))        # mostra os indices corretamente (sem isso, como esse dataframe foi resultado de concatenacao...
                                        # ele mostraria os indices como 0, 0, 0, 0,...; isso fara ele mostrar 0, 1, 2, 3,...)
samplesdf = pd.DataFrame(samples)       # transforma a lista de amostras em um dataframe
print('\n\nAmostras testadas:\n\n', samplesdf)
print('\n\nPredicoes:\n\n', pred)
aux = pred.iloc[:,:-1].values.tolist()  # armazena em uma variavel auxiliar os valores de probabilidade, excluindo a ultima coluna...
                                        # pois se trata da coluna indicativa que exibe a coluna com maior probabilidade
nsuccess = len(np.where(pred[pred.columns[-1]] == samplesdf[pred_index])[0])  
                                        # np.where() retorna um vetor com os dados dada determinada condicao neste caso, a condicao...
                                        # sao os valores da ultima coluna do dataframe de predicao que sao iguais ao dataframe de amostras...
                                        # desta forma o resultado sera um vetor contendo todos os valores que o algoritmo "previu" corretamente...
                                        # pegando o 'len()' disso, se obtem a quantidade de acertos
successRate = nsuccess / nsamples       # calcula a taxa de acerto
print('\n\nSomatoria das predicoes (espera-se que seja igual a 1):\n')
for i in range(nsamples):               # percorre o vetor de resultados para calcular e exibir a soma das probabilidades, a fim de verificar...
                                        # que nao ha erros no algoritmo, pois o resultado do somatorio de todas as probabilidades deve ser 1
    soma = sum(aux[i])
    if soma != 1:
        print(i, '\t', soma)
    else:
        print(i, '\t', soma)
print("\n\nTaxa de predicoes onde a maior probabilidade era de fato o resultado: %.f%%\n" % (successRate*100))
