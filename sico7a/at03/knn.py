import numpy as np

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

def kNNC(training, query, k=3):
    n = len(training)           # armazena a quantidade de elementos treinados
    aux = len(training[0])      # armazena a quantidade de features
    features = [training[i][1:aux-2] for i in range(n)] # armazena as features em um array (ignorando o primeiro '[0]' elemento por ser apenas indice
                                                        # e o ultimo por ser a classe)
    for i in range(len(features)):
        features[i].append(training[i][aux-1])
    target = [training[i][aux-2] for i in range(n)]   # armazena as classes alvo em outro array
    queryAux = query[1:aux-1]   # cria um array auxiliar para a query sem o indice e classe para facilitar nas contas entre este array e o de features

    distances = []              # inicializa o array de distancias
    for i in range(n):          # salva as distancias em uma tupla para armazenar tambem seus indices no array original 
        distances.append((i,(sum(np.subtract(features[i], queryAux)**2))**0.5))
    
    distances.sort(key=lambda tup: tup[1])  # ordena o array de distancias baseado na tupla da distancia
    low = distances[0:k]        # armazena apenas as primeiras k distancias em um novo array

    rslt = []                   # inicializa um array de resultado
    for i in range(len(low)):   # a partir dos indices salvos no array com apenas os k elementos mais proximos...
        rslt.append(target[low[i][0]])  # ...insere no array de resultado, os elementos do array de classes

    return np.mean(rslt)        # retorna o elemento que mais se repete