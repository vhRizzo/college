import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

########################################################################\/\/\/ kNN \/\/\/########################################################################

def kNND(training, query, k=3):
    n = len(training)           # armazena a quantidade de elementos treinados
    aux = len(training[0])      # armazena a quantidade de features
    features = [training[i][1:aux-1] for i in range(n)] # armazena as features em um array (ignorando o primeiro '[0]' elemento por ser apenas indice
                                                        # e o ultimo por ser a classe)
    target   = [training[i][aux-1] for i in range(n)]   # armazena as classes alvo em outro array
    queryAux = query[1:aux-1]   # cria um array auxiliar para a query sem o indice e classe para facilitar nas contas entre este array e o de features

    distances = []              # inicializa o array de distancias
    for i in range(n):          # salva as distancias em uma tupla para armazenar tambem seus indices no array original 
        distances.append((i,(sum(np.subtract(features[i], queryAux)**2))**0.5))
    
    distances.sort(key=lambda tup: tup[1])  # ordena o array de distancias baseado na tupla da distancia
    low = distances[0:k]        # armazena apenas as primeiras k distancias em um novo array

    rslt = []                   # inicializa um array de resultado
    for i in range(len(low)):   # a partir dos indices salvos no array com apenas os k elementos mais proximos...
        rslt.append(target[low[i][0]])  # ...insere no array de resultado, os elementos do array de classes

    return max(rslt, key=rslt.count)    # retorna o elemento que mais se repete

########################################################################/\/\/\ kNN /\/\/\########################################################################

########################################################################\/\/\/ DWNN \/\/\/#######################################################################

def DWNND(training, query, k=3):
    n = len(training)
    aux = len(training[0])
    features = [training[i][1:aux-1] for i in range(n)]
    target   = [training[i][aux-1] for i in range(n)]
    queryAux = query[1:aux-1]

    distances = []
    weights   = []
    for i in range(n):
        distances.append([i,(sum(np.subtract(features[i], queryAux)**2))**0.5, 0])  # ate aqui segue da mesma forma que o kNN, exceto que em vez de uma tupla...
        distances[i][2] = 1/(distances[i][1]**2) # utilizamos um array, agora com uma posicao a mais para armazenar tambem o peso
    
    distances.sort(key=lambda tup: tup[1])  # novamente ordena o array baseado na distancia
    low = distances[0:k]                    # e armazena as k mais proximas

    total = np.zeros(len(np.unique(target)))# gera um array de zeros com a quantidade de elementos unicos no array de classes
    for i in range(k):              # percorre o array de classes para acumular o peso dos elementos daquela respectiva classe
        index = target[low[i][0]]   # no array recentemente criado
        total[index] +=  low[i][2]

    return np.argmax(total)     # retorna o indice do maior peso

#######################################################################/\/\/\ DWNN /\/\/\########################################################################

#---------------------------------------------------------------------------------------------------------------------------------------------------------------#

########################################################################\/\/\/ MAIN \/\/\/#######################################################################

data = open("diabetes.dat", "r") # abre o arquivo

n = len(data.readlines())   # armazena a quantidade de elementos no arquivo
data.seek(0)                # retorna para o inicio
aux = data.read()           # le todo o arquivo e armazena uma variavel auxiliar
aux = aux.split()           # divide essa variavel, gerando assim uma lista separada pelas quebras de linha do arquivo
auxData = []                # cria um array auxiliar para armazenar os dados do arquivo
for i in range(n):          # percorre os elementos contidos no arquivo
    tmp = aux[i].split(',') # dividindo os elementos novamente, mas dessa vez separando pelas virgulas, gerando uma lista de listas
    tmp[-1] = 0 if tmp[-1] == "tested_negative" else 1 if tmp[-1] == "tested_positive" else tmp[-1]   # converte as classes nominais para numericas
    tmp = [*map(float,tmp[0:len(tmp)-1]),int(tmp[-1])]  # converte os dados dos elementos para float, e a classe para inteiro
    auxData.append([i, *tmp])   # insere os dados no array auxiliar

treino = []                     # inicializa o array de elementos treinados
teste = []                      # inicializa o array de elementos a serem testados
for i in range(0, n, 5):        # percorre os elementos do arquivo, onde a cada 5 elementos, 3 sao inseridos no array de elementos treinados...
    treino.append(auxData[i])   # ... e 2 sao inseridos no array de elementos a serem testados
    teste.append(auxData[i+1]) if i+1 < n else teste
    treino.append(auxData[i+2]) if i+2 < n else treino
    teste.append(auxData[i+3]) if i+3 < n else teste
    treino.append(auxData[i+4]) if i+4 < n else treino

k = [1, 5, 9, 13, 17, 21, 25, 29, 33, 37]     # valores de k a serem testados

print("kNN:\n")
for j in range(len(k)):     # loop para testar varios k's
    predskNN = []              # inicializa o array de predicoes
    for i in range(len(teste)): # cria uma query pra cada array que sera testado, e roda a kNN
        query = teste[i]
        predskNN.append(kNND(treino, query, k=k[j]))

    successes = 0   # inicializa o contador de sucessos
    for i in range(len(predskNN)): # verifica se a classe dos elementos testados sao iguais ao seu valor real
        if teste[i][-1] == predskNN[i]:    # se sim, incrementa o contador
            successes += 1
    print("Taxa de sucesso para k =", k[j], ":", successes/len(predskNN))  # printa o k utilizado e a taxa de sucesso

    knn = KNeighborsClassifier(algorithm='auto', 
                            leaf_size=30, 
                            metric='minkowski',
                            p=2,         # p=2 is equivalent to euclidian distance
                            metric_params=None, 
                            n_jobs=1, 
                            n_neighbors=k[j], 
                            weights='uniform')
    train_data = [treino[i][1:len(treino[0])] for i in range(len(treino))]
    train_labels = [treino[i][-1] for i in range(len(treino))]
    knn.fit(train_data, train_labels)
    test_data = [teste[i][1:len(teste[0])] for i in range(len(teste))]
    test_labels = [teste[i][-1] for i in range(len(teste))]
    test_data_predicted = knn.predict(test_data)
    print("Taxa de sucesso da literatura para k =", k[j], ":", accuracy_score(test_data_predicted, test_labels))

print("\nDWNN:\n")
for j in range(len(k)):
    predsDWNN = []              # inicializa o array de predicoes
    for i in range(len(teste)): # cria uma query pra cada array que sera testado, e roda a DWNN
        query = teste[i]
        predsDWNN.append(DWNND(treino, query, k=k[j]))

    successes = 0   # inicializa o contador de sucessos
    for i in range(len(predsDWNN)): # verifica se a classe dos elementos testados sao iguais ao seu valor real
        if teste[i][-1] == predsDWNN[i]:    # se sim, incrementa o contador
            successes += 1
    print("Taxa de sucesso para k =", k[j], ":", successes/len(predsDWNN))  # printa o k utilizado e a taxa de sucesso

    dwnn = KNeighborsClassifier(algorithm='auto', 
                            leaf_size=30, 
                            metric='minkowski',
                            p=2,         # p=2 is equivalent to euclidian distance
                            metric_params=None, 
                            n_jobs=1, 
                            n_neighbors=k[j], 
                            weights='distance')
    train_data = [treino[i][1:len(treino[0])] for i in range(len(treino))]
    train_labels = [treino[i][-1] for i in range(len(treino))]
    dwnn.fit(train_data, train_labels)
    test_data = [teste[i][1:len(teste[0])] for i in range(len(teste))]
    test_labels = [teste[i][-1] for i in range(len(teste))]
    test_data_predicted = dwnn.predict(test_data)
    print("Taxa de sucesso da literatura para k =", k[j], ":", accuracy_score(test_data_predicted, test_labels))

#######################################################################/\/\/\ MAIN /\/\/\########################################################################
