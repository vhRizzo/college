import numpy as np
import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
from knn import kNND
from dwnn import DWNND

dataD = open("diabetes.dat", "r") # abre o arquivo

n = len(dataD.readlines())   # armazena a quantidade de elementos no arquivo
dataD.seek(0)                # retorna para o inicio
aux = dataD.read()           # le todo o arquivo e armazena uma variavel auxiliar
aux = aux.split()           # divide essa variavel, gerando assim uma lista separada pelas quebras de linha do arquivo
auxDataD = []                # cria um array auxiliar para armazenar os dados do arquivo
for i in range(n):          # percorre os elementos contidos no arquivo
    tmp = aux[i].split(',') # dividindo os elementos novamente, mas dessa vez separando pelas virgulas, gerando uma lista de listas
    tmp[-1] = 0 if tmp[-1] == "tested_negative" else 1 if tmp[-1] == "tested_positive" else tmp[-1]   # converte as classes nominais para numericas
    tmp = [*map(float,tmp[0:len(tmp)-1]),tmp[-1]]  # converte os dados dos elementos para float, e a classe para inteiro
    auxDataD.append([i, *tmp])   # insere os dados no array auxiliar

treino = []                     # inicializa o array de elementos treinados
teste = []                      # inicializa o array de elementos a serem testados
for i in range(0, n, 5):        # percorre os elementos do arquivo, onde a cada 5 elementos, 3 sao inseridos no array de elementos treinados...
    treino.append(auxDataD[i])   # ... e 2 sao inseridos no array de elementos a serem testados
    teste.append(auxDataD[i+1]) if i+1 < n else teste
    treino.append(auxDataD[i+2]) if i+2 < n else treino
    teste.append(auxDataD[i+3]) if i+3 < n else teste
    treino.append(auxDataD[i+4]) if i+4 < n else treino

k = [3, 9, 15, 21, 27, 33, 39]  # valores de k a serem testados

print("kNN:\n")
tx_suc = []
for j in range(len(k)):         # loop para testar varios k's
    predskNN = []               # inicializa o array de predicoes
    for i in range(len(teste)): # cria uma query pra cada array que sera testado, e roda a kNN
        query = teste[i]
        predskNN.append(kNND(treino, query, k=k[j]))

    successes = 0   # inicializa o contador de sucessos
    for i in range(len(predskNN)): # verifica se a classe dos elementos testados sao iguais ao seu valor real
        if teste[i][-1] == predskNN[i]:    # se sim, incrementa o contador
            successes += 1
    tx_suc.append(successes/len(predskNN)*100)
    print("Taxa de sucesso para k =", k[j], ":", tx_suc[j])  # printa o k utilizado e a taxa de sucesso

    knn = KNeighborsClassifier(algorithm='auto', 
                            leaf_size=30, 
                            metric='minkowski',
                            p=2,         # p=2 is equivalent to euclidian distance
                            metric_params=None, 
                            n_jobs=1, 
                            n_neighbors=k[j], 
                            weights='uniform')
    train_dataD = [treino[i][1:len(treino[0])] for i in range(len(treino))]
    train_labels = [treino[i][-1] for i in range(len(treino))]
    knn.fit(train_dataD, train_labels)
    test_dataD = [teste[i][1:len(teste[0])] for i in range(len(teste))]
    test_labels = [teste[i][-1] for i in range(len(teste))]
    test_dataD_predicted = knn.predict(test_dataD)
    print("Taxa de sucesso da literatura para k =", k[j], ":", accuracy_score(test_dataD_predicted, test_labels)*100)
# plt.plot(k, tx_suc)
# plt.xlabel("k")
# plt.ylabel("Taxa de sucesso")
# plt.title("kNN Discreto")
# plt.show()

print("\nDWNN:\n")
tx_suc = []
for j in range(len(k)):
    predsDWNN = []              # inicializa o array de predicoes
    for i in range(len(teste)): # cria uma query pra cada array que sera testado, e roda a DWNN
        query = teste[i]
        predsDWNN.append(DWNND(treino, query, k=k[j]))

    successes = 0   # inicializa o contador de sucessos
    for i in range(len(predsDWNN)): # verifica se a classe dos elementos testados sao iguais ao seu valor real
        if teste[i][-1] == predsDWNN[i]:    # se sim, incrementa o contador
            successes += 1
    tx_suc.append(successes/len(predskNN)*100)
    print("Taxa de sucesso para k =", k[j], ":", tx_suc[j])  # printa o k utilizado e a taxa de sucesso

    dwnn = KNeighborsClassifier(algorithm='auto', 
                            leaf_size=30, 
                            metric='minkowski',
                            p=2,         # p=2 is equivalent to euclidian distance
                            metric_params=None, 
                            n_jobs=1, 
                            n_neighbors=k[j], 
                            weights='distance')
    train_dataD = [treino[i][1:len(treino[0])] for i in range(len(treino))]
    train_labels = [treino[i][-1] for i in range(len(treino))]
    dwnn.fit(train_dataD, train_labels)
    test_dataD = [teste[i][1:len(teste[0])] for i in range(len(teste))]
    test_labels = [teste[i][-1] for i in range(len(teste))]
    test_dataD_predicted = dwnn.predict(test_dataD)
    print("Taxa de sucesso da literatura para k =", k[j], ":", accuracy_score(test_dataD_predicted, test_labels)*100)
# plt.plot(k, tx_suc)
# plt.xlabel("k")
# plt.ylabel("Taxa de sucesso")
# plt.title("DWNN Discreto")
# plt.show()