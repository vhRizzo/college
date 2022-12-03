import sys
import subprocess

pipV = 'pip'    # altere para 'pip3' caso seu sistema apenas suporte este comando

subprocess.check_call([sys.executable, '-m', pipV, 'install', 'scikit-learn']) # instala o scikit-learn se já não tiver instalado
subprocess.check_call([sys.executable, '-m', pipV, 'install', 'pandas'])       # o mesmo para o pandas,
subprocess.check_call([sys.executable, '-m', pipV, 'install', 'numpy'])        # para o numpy,
subprocess.check_call([sys.executable, '-m', pipV, 'install', 'scipy'])        # e para o scipy

from sklearn.naive_bayes import MultinomialNB
from sklearn.impute import SimpleImputer
from nb import naiveBayes, encode
import pandas as pd
import numpy as np
import random

nsamples = 25       # quantidade de amostras para serem testadas
pred_index = 3      # indice da coluna que se deseja prever (irish = 3 | letter = 16)
isindexcol = None   # indice de qualquer coluna que apenas sirva como indice para os dados...
                    # ('None' se nao houver), nenhum dos dois datasets utilizados possuem...
                    # mas foi testado em datasets que possuiam, e funcionou corretamente
df = pd.read_csv("../datasets/irish.txt", header=None)  # le o arquivo e o armazena em um dataframe do pandas
                    # o criterio para o dataset e que ele tenha somente dados, sem linha de cabecalho, os dados devem ser separados...
                    # por quebra de linha, e os atributos dos dados separados por virgula

if nsamples > len(df)/2:
    print("\n\nQuantidade de amostras excede a quantidade de elementos no dataset\n\n")
    sys.exit()
imp = SimpleImputer(missing_values='?', strategy="most_frequent")   # inicializa o metodo de imputacao de dados faltantes se houver
                                        # dados faltantes obrigatoriamente devem ser marcados como '?'
dataset = imp.fit_transform(df)         # realiza a imputacao

aux = random.sample(range(len(dataset)), nsamples) # gera, de forma aleatoria, indices de amostras

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
print('\n\nIMPLEMENTADO:\n\nPredicoes:\n\n', pred)
aux = pred.iloc[:,:-1].values.tolist()  # armazena em uma variavel auxiliar os valores de probabilidade, excluindo a ultima coluna...
                                        # pois se trata da coluna indicativa que exibe a coluna com maior probabilidade
nsuccess = len(np.where(pred[pred.columns[-1]] == samplesdf[pred_index])[0])  
                                        # np.where() retorna um vetor com os dados dada determinada condicao neste caso, a condicao...
                                        # sao os valores da ultima coluna do dataframe de predicao que sao iguais ao dataframe de amostras...
                                        # desta forma o resultado sera um vetor contendo todos os valores que o algoritmo "previu" corretamente...
                                        # pegando o 'len()' disso, se obtem a quantidade de acertos
successRate = nsuccess / nsamples       # calcula a taxa de acerto
print("\n\nTaxa de acerto das predicoes: %.f%%\n" % (successRate*100))

# IMPLEMENTACAO DA LITERATURA REALIZADA UTILIZANDO SCIKIT-LEARN BASEADO NOS CODIGOS-FONTE:
# https://scikit-learn.org/stable/modules/generated/sklearn.naive_bayes.MultinomialNB.html
# https://www.kaggle.com/code/guruprasad91/titanic-naive-bayes/notebook

df_train = pd.DataFrame(treino)
X_train = df_train.drop(pred_index, axis=1)
X_train.columns = list(range(len(X_train.columns)))
X_train = encode(X_train)
y_train = df_train[pred_index]
mnb = MultinomialNB()
mnb.fit(X_train, y_train)

df_test = pd.DataFrame(samples)
X_test = df_test.drop(pred_index, axis=1)
X_test.columns = list(range(len(X_test.columns)))
X_test = encode(X_test)
y_test = df_test[pred_index]
lit_pred = mnb.predict(X_test)

print("SCIKIT-LEARN:\n\nPredicoes:\n\n", pd.DataFrame(lit_pred, columns=['Maior prob']))

nsuccess = len(np.where(lit_pred == y_test)[0])
successRate = nsuccess / nsamples
print("\n\nTaxa de acerto das predicoes: %.f%%\n" % (successRate*100))
