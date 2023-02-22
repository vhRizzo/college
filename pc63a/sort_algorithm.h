/**
* @file sort_algorithm.h
* @author Victor Hugo Rizzo Moura
* @date 17 Sep 2019
* @brief Implementacao dos metodos de ordenacao
* Implementa os metodos de ordenacao vistos na disciplina
* pesquisa e classificacao de dados.
*/
#ifndef ORDENADOR_SORT_ALGORITHM_H
#define ORDENADOR_SORT_ALGORITHM_H

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <math.h>

/**
 * \brief Verifica se um determinado caractere aparece pelo menos uma vez em determinada string
 *
 * \param str string a ser verificada
 * \param c caractere a ser procurado
 * \return true caso o caractere esteja presente na string
 * \return false caso o caractere não esteja presente na string
 *
 * Percorre a string até que se encontre, ou não, uma ocorrência de um determinado caractere
 */
bool search_char (char *str, char c) {
    for (unsigned int i = 0; i < strlen (str); i++)
        if (str[i] == c)
            return true;
    return false;
}//search_char

/**
 * \brief Ordena o vetor usando BubbleSort
 *
 * \param V vetor a ser ordenado
 * \param N tamanho do vetor
 * \param comp número de comparações realizadas pelo algoritmo
 * \param swap número de trocas realizadas pelo algoritmo
 *
 * Ordena o vetor usando o método Bubble Sort
 * Esse algorimo tem um comportamento assintótico O (N²)
 */
void bubble_sort (int *V, int N, int *comp, int *swap) {
    int end = N, aux;
    bool keep;
    do {
        keep = true;
        for (int i = 0; i < end - 1; i ++) {
            if (V[i] > V[i + 1]) {
                aux = V[i];
                V[i] = V[i + 1];
                V[i + 1] = aux;
                keep = false;
                (*swap) ++;
            }
            (*comp) ++;
        }
        end --;
    } while (keep != true);
}//bubble_sort

/**
 * \brief Ordena o vetor usando SelectionSort
 *
 * \param V vetor a ser ordenado
 * \param N tamanho do vetor
 * \param comp número de comparações realizadas pelo algoritmo
 * \param swap número de trocas realizadas pelo algoritmo
 *
 * Ordena o vetor usando o método Selection Sort
 * Esse algorimo tem um comportamento assintótico O (N²)
 */
void selection_sort (int *V, int N, int *comp, int *swap) {
    int lower, aux;
    for (int i = 0; i < N; i++) {
        lower = i;
        for (int j = i + 1; j < N; j++) {
            if (V[j] < V[lower])
                lower = j;
        }
        if (i != lower) {
            aux = V[i];
            V[i] = V[lower];
            V[lower] = aux;
            (*swap) ++;
        }
        (*comp) ++;
    }
}//selection_sort

/**
 * \brief Ordena o vetor usando InsertionSort
 *
 * \param V vetor a ser ordenado
 * \param N tamanho do vetor
 * \param comp número de comparações realizadas pelo algoritmo
 * \param swap número de trocas realizadas pelo algoritmo
 *
 * Ordena o vetor usando o método Insertion Sort
 * Esse algorimo tem um comportamento assintótico O (N²)
 */
void insertion_sort (int *V, int N, int *comp, int *swap) {
    int current, j;
    for (int i = 1; i < N; i++) {
        current = V[i];
        for (j = i; j > 0 && current < V[j - 1]; j--) {
            V[j] = V[j - 1];
            (*swap) ++;
        }
        V[j] = current;
        (*comp) ++;
    }
}//insertion_sort

/**
 * \brief Função que particiona um vetor dado pela função quick_sort
 *
 * \param V vetor a ser ordenado
 * \param start inicial do vetor
 * \param end posição final do vetor
 * \param comp número de comparações realizadas pelo algoritmo
 * \param swap número de trocas realizadas pelo algoritmo
 *
 * Organiza os dados a partir de um pivô pré-definido
 */
int partition (int *V, int start, int end, int *comp, int *swap) {
    int pivot = start, left = start, right = end, tmp;
    while (left <= right) {
        while (V[left] <= V[pivot]) {
            left++;
            (*comp) ++;
        }
        while (V[right] > V[pivot]) {
            right--;
            (*comp) ++;
        }
        if (right >= left) {
            tmp = V[left];
            V[left] = V[right];
            V[right] = tmp;
            (*swap) ++;
        }
    }
    tmp = V[right];
    V[right] = V[pivot];
    V[start] = tmp;
    (*swap) ++;
    return right;
}

/**
 * \brief Ordena o vetor usando QuickSort
 *
 * \param V vetor a ser ordenado
 * \param start inicial do vetor
 * \param end posição final do vetor
 * \param comp número de comparações realizadas pelo algoritmo
 * \param swap número de trocas realizadas pelo algoritmo
 *
 * Ordena o vetor usando o método Quick Sort
 * Esse algorimo tem um comportamento assintótico O (N*log(N))
 */
void quick_sort (int *V, int start, int end, int *comp, int *swap) {
    int pivot;
    if (start < end) {
        pivot = partition (V, start, end, comp, swap);
        quick_sort (V, start, pivot - 1, comp, swap);
        quick_sort (V, pivot + 1, end, comp, swap);
    }
}

/**
 * \brief Função auxiliar para a função merge_sort
 *
 * \param V vetor a ser ordenado
 * \param start inicial do vetor
 * \param end posição final do vetor
 * \param comp número de comparações realizadas pelo algoritmo
 * \param swap número de trocas realizadas pelo algoritmo
 *
 * Utiliza um vetor auxiliar para armazenar os
 * dados e em seguida organiza-os no vetor original
 */
void merge (int *V, int start, int mid, int end, int *comp, int *swap) {

    int *V_aux;
    int size = end - start + 1;
    V_aux = (int*) calloc (size, sizeof (int));
    int p1 = start, p2 = mid + 1, pV = 0;
    while ( (p1 <= mid) && (p2 <= end) ) {
        if ( V[p1] < V[p2] ) {
            V_aux[pV] = V[p1];
            p1 ++;
            pV ++;
            (*comp) ++;
        }
        else {
            V_aux[pV] = V[p2];
            p2 ++;
            pV ++;
            (*comp) ++;
        }
    }
    if ( p1 > mid ) {
        while ( p2 <= end ) {
            V_aux[pV] = V[p2];
            p2 ++;
            pV ++;
            (*comp) ++;
        }
    }
    else {
        while ( p1 <= mid ) {
            V_aux[pV] = V[p1];
            p1 ++;
            pV ++;
            (*comp) ++;
        }
    }
    for (int i = 0, j = start; j <= end; i ++, j ++) {
        V[j] = V_aux[i];
        (*swap) ++;
    }
    free (V_aux);
}//merge

/**
 * \brief Ordena o vetor usando MergeSort
 *
 * \param V vetor a ser ordenado
 * \param start inicial do vetor
 * \param end posição final do vetor
 * \param comp número de comparações realizadas pelo algoritmo
 * \param swap número de trocas realizadas pelo algoritmo
 *
 * Ordena o vetor usando o método Merge Sort
 * Esse algorimo tem um comportamento assintótico O (N*log(N))
 */
void merge_sort (int *V, int start, int end, int *comp, int *swap) {
    int mid;
    if (start < end) {
        mid = floor ((double) (start + end) / 2.0);
        merge_sort (V, start, mid, comp, swap);
        merge_sort (V, mid + 1, end, comp, swap);
        merge (V, start, mid, end, comp, swap);
    }
}

/**
 * \brief Função auxiliar para ordenar o vetor como um heap máximo
 *
 * \param V vetor a ser ordenado
 * \param parent índice do nó pai
 * \param end índice do último nó
 * \param comp número de comparações realizadas pelo algoritmo
 * \param swap número de trocas realizadas pelo algoritmo
 *
 * Organiza o vetor como um heap maximo para que possa ser realizado um Heap Sort
 */
void create_heap (int *V, int parent, int end, int *comp, int *swap) {
    int aux = V[parent], child = parent * 2 + 1;
    while (child <= end) {
        (*comp) ++;
        if (child < end) {
            if (V[child] < V[child + 1])
                child ++;
        }
        if (aux < V[child]) {
            V[parent] = V[child];
            parent = child;
            child = parent * 2 + 1;
        } else {

            break;
        }
    }
    (*swap) ++;
    V[parent] = aux;
}

/**
 * \brief Ordena o vetor usando HeapSort
 *
 * \param V vetor a ser ordenado
 * \param n tamanho do vetor
 * \param comp número de comparações realizadas pelo algoritmo
 * \param swap número de trocas realizadas pelo algoritmo
 *
 * Ordena o vetor usando o método Heap Sort
 * Esse algorimo tem um comportamento assintótico O (N*log(N))
 */
void heap_sort (int *V, int n, int *comp, int *swap) {
    int i, tmp;
    for (i = (n - 1) / 2; i >= 0; i --)
        create_heap (V, i, n - 1, comp, swap);
    for (i = n - 1; i >= 1; i --) {
        tmp = V[0];
        V[0] = V[i];
        V[i] = tmp;
        create_heap (V, 0, i - 1, comp, swap);
        (*swap) ++;
    }
}

/**
 * \brief Printa um determinado vetor no terminal
 *
 * \param V vetor a ser printado
 * \param size tamanho do vetor
 *
 * Mostra todos os elementos de um determinado vetor
 * delimitado por | item |, mais usado para fins de debug
 */
void print_v (int *V, int size) {
    printf ("\n");
    for (int i = 0; i < size; i ++)
        printf ("| %i ", V[i]);
    printf ("|\n");
}

/**
 * \brief Printa um determinado vetor em um arquivo
 *
 * \param V vetor a ser printado
 * \param size tamanho do vetor
 * \param file arquivo no qual o vetor será printado
 *
 * Printa todos os elementos de um vetor em um arquivo
 * saltando linhas entre cada elemento
 */
void fprint_v (int *V, int size, FILE *file) {
    for (int i = 0; i < size; i ++)
        fprintf (file, "%i\n", V[i]);
}

#endif //ORDENADOR_SORT_ALGORITHM_H
