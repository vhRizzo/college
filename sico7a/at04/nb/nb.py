from sklearn.preprocessing import OrdinalEncoder
from scipy.stats import norm
import pandas as pd
import numpy as np
import statistics

def isnumber(s: str):
    """
    Verifica se o conteudo de uma string e qualquer tipo de numero

    Parametros
    ----------
    s : string
        string a ser verificada
    
    Retorna
    -------
    True
        se o conteudo da string for um numero
    False
        se o conteudo da string nao e um numero
    """

    try:
        complex(s)      # tenta converter a string para complexo...
                        # foi utilizado complexo pois englobara qualquer tipo de numero...
                        # inteiro ou float, positivo ou negativo
    except ValueError:  # se a convercao apresentou erro
        return False    # retorna falso
    return True         # caso contrario retorna verdadeiro

def encode(df: pd.DataFrame):
    """
    Substitui atributos categoricos de um dataframe por um codificador numerico

    Parametros
    ----------
    df: pd.DataFrame
        dataframe para ser codificado
    
    Retorna
    -------
        dataframe codificado
    """

    ret = pd.DataFrame(df.values.tolist())  # inicializa o dataframe de retorno (utilizo .tolist() aqui pois sem isso o dataframe de origem...
                                            # tambem se altera por algum tipo de comportamento de ponteiro)
    oenc = OrdinalEncoder()                 # inicializa o codificador
    aux = []                                # inicializa uma lista auxiliar para armazenar os indices de colunas categoricas
    for i in range(len(ret.columns)):       # percorre os atributos do primeiro dado no dataframe
        if not(isnumber(ret[i][0])):            # se ele nao for numerico
            aux.append(i)                           # adiciona o indice a lista auxiliar
    ret[aux] = pd.DataFrame(oenc.fit_transform(ret[aux]))
                                            # realiza a codificacao das colunas
    return ret

def naiveBayes(dataset: list, sample: list, pred_index: int, index_col: int):
    """
    Realiza a predicao da probabilidade de um evento ocorrer dado determinado dataset
    atraves do metodo de Naive Bayes

    Parametros
    ----------
    dataset : list
        dataset armazenado como lista de listas, onde cada linha possui um dado,
        e cada dado e uma lista de strings contendo as caracteristicas desses dados
    sample : list
        amostra que se deseja prever; e.g.: dadas as caracteristicas de uma amostra,
        qual a probabilidade dela ser X ou Y ao comparar suas caracteristicas com as
        caracteristicas dos dados do dataset que sao X ou que sao Y
    pred_index : int
        indice da coluna contendo a caracterista "alvo"; e.g.: supondo que se deseja
        verificar se a amostra e X ou Y, a coluna deste indice sera uma coluna de X e Y
    index_col : int
        indice da coluna que serve o unico proposito de ser indice para um dado;
        alguns datasets possuem colunas pra este propósito, como esta coluna nao
        serve em nada para o calculo da probabilidade, indique seu indice para que
        seja ignorada pelo algoritmo
    
    Retorna
    -------
    Pandas DataFrame, onde cada coluna possui a probabilidade de algo ocorrer
    """

    df = pd.DataFrame(dataset)                  # cria um dataframe baseado no dataset
    if index_col != None:                       # verifica se o dataset possui coluna de indice
        sample.pop(index_col)                       # se houver, remove esta coluna da lista de amostras
        df = df.drop(index_col, axis=1)             # remove tambem do dataframe
        dataset = df.values.tolist()                # reconstroi o dataset
        df = pd.DataFrame(dataset)                  # reconstroi o dataframe do dataset
        if pred_index > index_col:                  # se o indice da coluna de 'alvos' for maior que a coluna de indices
            pred_index -= 1                             # decrementa o indice da coluna de 'alvos'
    sample.pop(pred_index)                      # remove a coluna de 'alvos' da amostra
    possible_hyp = df[pred_index].unique()      # gera as hipoteses possiveis verificando todos os valores unicos nesta coluna
    answers = np.zeros(np.shape(possible_hyp))  # inicializa um vetor de zeros com o tamanho do vetor de hipoteses possiveis

    for j in range(len(possible_hyp)):          # percorre as hipoteses possiveis
        answers[j] = sum(df[pred_index] == possible_hyp[j]) / len(dataset)
                                                    # calcula a probabilidade de cada hipotese, somando a quantidade de vezes que esta hipotese...
                                                    # se repete, e dividindo pelo total de elementos na coluna de hipoteses do dataset (peso)
        rows   = np.where(df[pred_index] == possible_hyp[j])
                                                    # armazena o indice dos elementos que possuem a hipotese atual
        subset = pd.DataFrame()                     # inicializa um subset como um dataframe vazio
        for i in range(len(rows[0])):               # percorre os elementos com aquela hipotese
            subset = pd.concat([subset, df.iloc[[rows[0][i]]]]) # adiciona esses elemento ao subset

        prod = 1                                    # inicializa o produtorio em 1
        for i in range(len(sample)):                # percorre as caracteristicas da amostra
            if i < pred_index:                          # como a coluna de hipoteses foi removida da amostra...
                k = i
            else:                                       # se o indice atual for maior que o indice de hipoteses, o indice a ser comparado no...
                k = i+1                                 # subset deve ser 1 unidade maior
            if isnumber(subset.iloc[[0]][k]):           # se a caracteristica da coluna atual for um valor numerico...
                mean = statistics.mean(subset[k].astype(float)) # armazena sua media...
                sd = statistics.stdev(subset[k].astype(float))  # e seu desvio padrao...
                x = norm(mean, sd)                              # normaliza os valores...
                prob = x.pdf(float(sample[i]))                  # e gera a a distribuicao normal destes valores
            else:                                       # se nao for um numero
                prob = sum(sample[i] == subset[k]) / len(subset)# retorna a taxa de frequencia desta caracteristica no subset
            prod = prod * prob                          # calcula o produtorio
        
        answers[j] = answers[j] * prod              # aplica o peso da resposta atual ao produtorio calculado
    
    answers = answers / sum(answers)            # normaliza as respostas (dividindo cada valor pelo somatorio dos valores)
    ret = pd.DataFrame(answers, index=possible_hyp) # cria um dataframe para as respostas
    ret = ret.transpose()                       # transpoe o dataframe para ficar com cada resposta em uma coluna
    ret['Maior prob'] = ret.idxmax(axis=1)      # indica qual a coluna com a maior probabilidade

    return ret
