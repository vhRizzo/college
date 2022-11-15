import numpy as np

def DWNND(training, query, k=3):
    n = len(training)
    aux = len(training[0])
    features = [training[i][1:aux-1] for i in range(n)]
    target   = [training[i][aux-1] for i in range(n)]
    queryAux = query[1:aux-1]

    distances = []
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

def DWNNC(training, query, k=3):
    n = len(training)
    aux = len(training[0])
    features = [training[i][1:aux-2] for i in range(n)]
    for i in range(len(features)):
        features[i].append(training[i][aux-1])
    target = [training[i][aux-2] for i in range(n)]
    queryAux = query[1:aux-1]

    distances = []
    weights   = []
    for i in range(n):
        distances.append([i,(sum(np.subtract(features[i], queryAux)**2))**0.5, 0])  # ate aqui segue da mesma forma que o kNN, exceto que em vez de uma tupla...
        distances[i][2] = 1/(distances[i][1]**2) if distances[i][1] != 0 else -1 # utilizamos um array, agora com uma posicao a mais para armazenar tambem o peso
    
    distances.sort(key=lambda tup: tup[1])  # novamente ordena o array baseado na distancia
    low = distances[0:k]                    # e armazena as k mais proximas

    if distances[0][1] == 0:    # se a distancia da primeira posicao for 0 (fazendo o peso tender ao infinito)
        return target[distances[0][0]]  # retorna o proprio target desse elemento

    candidates = [target[low[i][0]] for i in range(len(low))]
    weights = [low[i][2] for i in range(len(low))]
    rslt = sum(np.multiply(candidates,weights)) / sum(weights)

    return rslt     # retorna o indice do maior peso