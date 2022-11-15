import numpy as np
import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_squared_error
from knn import kNNC
from dwnn import DWNNC

dataC = open("liver-disorders.dat", "r") # abre o arquivo
out   = open("knnCont.dat", "w")

n = len(dataC.readlines())   # armazena a quantidade de elementos no arquivo
dataC.seek(0)                # retorna para o inicio
aux = dataC.read()           # le todo o arquivo e armazena uma variavel auxiliar
aux = aux.split()            # divide essa variavel, gerando assim uma lista separada pelas quebras de linha do arquivo
auxData = []                # cria um array auxiliar para armazenar os dados do arquivo
for i in range(n):           # percorre os elementos contidos no arquivo
    tmp = aux[i].split(',')  # dividindo os elementos novamente, mas dessa vez separando pelas virgulas, gerando uma lista de listas
    tmp = [*map(float,tmp[0:len(tmp)-1]),int(tmp[-1])]  # converte os dados dos elementos para float, e a classe para inteiro
    auxData.append([i, *tmp])  # insere os dados no array auxiliar

treino = []                     # inicializa o array de elementos treinados
teste = []                      # inicializa o array de elementos a serem testados
for i in range(0, n, 5):        # percorre os elementos do arquivo, onde a cada 5 elementos, 3 sao inseridos no array de elementos treinados...
    treino.append(auxData[i])   # ... e 2 sao inseridos no array de elementos a serem testados
    teste.append(auxData[i+1]) if i+1 < n else teste
    treino.append(auxData[i+2]) if i+2 < n else treino
    teste.append(auxData[i+3]) if i+3 < n else teste
    treino.append(auxData[i+4]) if i+4 < n else treino

k = [3, 9, 15, 21, 27, 33, 39]  # valores de k a serem testados

print("kNN:\n")
rmse = []
for j in range(len(k)):         # loop para testar varios k's
    aux = len(treino[0])
    train_dataC  = [treino[i][1:aux-2] for i in range(len(treino))]
    for i in range(len(train_dataC)):
        train_dataC[i].append(treino[i][aux-1])
    train_labels = [treino[i][aux-2] for i in range(len(treino))]
    aux = len(teste[0])
    test_dataC   = [teste[i][1:aux-2] for i in range(len(teste))]
    for i in range(len(test_dataC)):
        test_dataC[i].append(teste[i][aux-1])
    test_labels  = [teste[i][aux-2] for i in range(len(teste))]
    
    predskNN = []               # inicializa o array de predicoes
    for i in range(len(teste)): # cria uma query pra cada array que sera testado, e roda a kNN
        query = teste[i]
        predskNN.append(kNNC(treino, query, k=k[j]))
    mse = mean_squared_error(test_labels, predskNN)
    rmse.append((mse)**0.5)
    print("Erro quadratico medio para k =", k[j], ":", rmse[j])  # printa o k utilizado e a taxa de sucesso

    knn = KNeighborsRegressor(algorithm='auto', 
                            leaf_size=30, 
                            metric='minkowski',
                            p=2,         # p=2 is equivalent to euclidian distance
                            metric_params=None, 
                            n_jobs=1, 
                            n_neighbors=k[j], 
                            weights='uniform')
    knn.fit(train_dataC, train_labels)
    test_dataC_predicted = knn.predict(test_dataC)
    mse = mean_squared_error(test_labels, test_dataC_predicted)
    print("Erro quadratico medio da literatura para k =", k[j], ":", (mse)**0.5)
plt.plot(k, rmse)
plt.xlabel("k")
plt.ylabel("Erro quadrático médio")
plt.title("kNN Contínuo")
plt.show()

print("DWNN:\n")
rmse = []
for j in range(len(k)):         # loop para testar varios k's
    aux = len(treino[0])
    train_dataC  = [treino[i][1:aux-2] for i in range(len(treino))]
    for i in range(len(train_dataC)):
        train_dataC[i].append(treino[i][aux-1])
    train_labels = [treino[i][aux-2] for i in range(len(treino))]
    aux = len(teste[0])
    test_dataC   = [teste[i][1:aux-2] for i in range(len(teste))]
    for i in range(len(test_dataC)):
        test_dataC[i].append(teste[i][aux-1])
    test_labels  = [teste[i][aux-2] for i in range(len(teste))]

    predsDWNN = []               # inicializa o array de predicoes
    for i in range(len(teste)): # cria uma query pra cada array que sera testado, e roda a kNN
        query = teste[i]
        predsDWNN.append(DWNNC(treino, query, k=k[j]))
    mse = mean_squared_error(test_labels, predsDWNN)
    rmse.append((mse)**0.5)
    print("Erro quadratico medio para k =", k[j], ":", rmse[j])  # printa o k utilizado e a taxa de sucesso

    knn = KNeighborsRegressor(algorithm='auto', 
                            leaf_size=30, 
                            metric='minkowski',
                            p=2,         # p=2 is equivalent to euclidian distance
                            metric_params=None, 
                            n_jobs=1, 
                            n_neighbors=k[j], 
                            weights='distance')
    knn.fit(train_dataC, train_labels)
    test_dataC_predicted = knn.predict(test_dataC)
    mse = mean_squared_error(test_labels, test_dataC_predicted)
    print("Erro quadratico medio da literatura para k =", k[j], ":", (mse)**0.5)
plt.plot(k, rmse)
plt.xlabel("k")
plt.ylabel("Erro quadrático médio")
plt.title("DWNN Contínuo")
plt.show()