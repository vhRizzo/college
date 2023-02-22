#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <time.h>
#include "sort_algorithm.h"

int main (int argc, char **argv) {
    clock_t ticks[4];
    ticks[0] = clock ();                                        //tempo inicial do programa

    if (argc != 3) {                                            //caso os argumentos passados sejam siferente de 3, quebra a execução
        printf ("\nQuantidade de argumentos invalido\n");
        return 0;
    }//if

    char type = argv[1][0];                                     //armazena o tipo do arquivo passado por argumento de entrada
    char out[31];
    FILE *a, *b;

    a = fopen(argv[2], "r");                                    //abre o arquivo passado pelo argumento para leitura

    if (a == NULL) {                                            //controle de erro para caso ocorra um erro ao abrir o arquivo
        printf("\nErro ao abrir o arquivo de entrada\n");
        return 0;
    }//if
    else {

        strcpy (out, argv[2]);                                  //copia o conteúdo da string de entrada para a string "out"
        bool extension;

        extension = search_char (out, '.');                     //verifica se existe um "." no nome do arquivo

        if (extension == true)                                  //se sim, remove o conteúdo do último ponto pra frente na string
            out[strlen(out) - strlen(strrchr(out, '.'))] = '\0';

        int i = 0, comp = 0, swap = 0, size, *V;

        fscanf (a, "%i", &size);                                //armazena a primeira linha do arquivo contendo o tamanho do vetor
        fgets (NULL, 0, a);                                     //pula a linha no arquivo
        V = (int*) calloc (size, sizeof (int));                 //aloca a memória do tamanho armazenado e inicializa todos os valores em 0

        while (!feof (a)) {                                     //armazena em um vetor os valores nas linhas seguintes até o final do arquivo
            fscanf (a, "%i", &V[i]);
            fgets (NULL, 0, a);                                 //utiliza-se a mesma técnica de leitura da primeira linha do arquivo
            i ++;
        }//while

        switch (type) {                                         //executa o algoritmo passado no argumento de entrada

            ////OS PASSOS REALIZADOS PARA OS DEMAIS ALGORITMOS SÃO PRATICAMENTE OS MESMOS
            ////DO BUBBLESORT, PORTANTO SEGUEM DE MANEIRA ANÁLOGA MUDANDO APENAS ALGUNS NOMES
            case 'b':
                if (extension) {                                //se o arquivo possui um "."
                    strcat(out, "_bubblesort");                 //concatena a string "_bubblesort" ao nome do arquivo sem a extensão
                    strcat(out, strrchr(argv[2], '.'));         //em seguida concatena a extensão
                }//if
                else
                    strcat(out, "_bubblesort");                 //se não possuir ".", concatena somente o "_bubblesort"

                b = fopen (out, "w");                           //abre o arquivo de saída "b" em modo de escrita

                if (b == NULL) {                                //controle de erro para caso ocorra um erro ao criar o arquivo de saída
                    printf ("\nErro ao criar o arquivo de saida\n");
                    return 0;
                }//if

                else {
                    ticks[2] = clock ();
                    bubble_sort(V, size, &comp, &swap);        //executa o algoritmo bubblesort
                    ticks[3] = clock ();
                    printf("\nTempo ordenacao: %6.3fms\n", (double)(ticks[3] - ticks[2])*1000 / (CLOCKS_PER_SEC));
                }

                break;

            case 'i':
                if (extension) {
                    strcat(out, "_insertionsort");
                    strcat(out, strrchr(argv[2], '.'));
                }//if
                else
                    strcat(out, "_insertionsort");

                b = fopen (out, "w");

                if (b == NULL) {
                    printf ("\nErro ao criar o arquivo de saida\n");
                    return 0;
                }//if

                else {
                    ticks[2] = clock ();
                    insertion_sort(V, size, &comp, &swap);     //executa o algoritmo insertionsort
                    ticks[3] = clock ();
                    printf("\nTempo ordenacao: %6.3fms\n", (double)(ticks[3] - ticks[2])*1000 / (CLOCKS_PER_SEC));
                }

                break;
            case 's':
                if (extension) {
                    strcat(out, "_selectionsort");
                    strcat(out, strrchr(argv[2], '.'));
                }//if
                else
                    strcat(out, "_selectionsort");

                b = fopen (out, "w");

                if (b == NULL) {
                    printf ("\nErro ao criar o arquivo de saida\n");
                    return 0;
                }//if

                else {
                    ticks[2] = clock ();
                    selection_sort(V, size, &comp, &swap);     //executa o algoritmo selectionsort
                    ticks[3] = clock ();
                    printf("\nTempo ordenacao: %6.3fms\n", (double)(ticks[3] - ticks[2])*1000 / (CLOCKS_PER_SEC));
                }
                break;

            case 'm':
                if (extension) {
                    strcat(out, "_mergesort");
                    strcat(out, strrchr(argv[2], '.'));
                }//if
                else
                    strcat(out, "_mergesort");

                b = fopen (out, "w");

                if (b == NULL) {
                    printf ("\nErro ao criar o arquivo de saida\n");
                    return 0;
                }//if

                else {
                    ticks[2] = clock ();
                    merge_sort (V, 0, size, &comp, &swap);      //executa o algoritmo mergesort
                    ticks[3] = clock ();
                    printf("\nTempo ordenacao: %6.3fms\n", (double)(ticks[3] - ticks[2])*1000 / (CLOCKS_PER_SEC));
                }
                break;

            case 'q':
                if (extension) {
                    strcat(out, "_quicksort");
                    strcat(out, strrchr(argv[2], '.'));
                }//if
                else
                    strcat(out, "_quicksort");

                b = fopen (out, "w");

                if (b == NULL) {
                    printf ("\nErro ao criar o arquivo de saida\n");
                    return 0;
                }//if

                else {
                    ticks[2] = clock ();
                    quick_sort(V, 0, size, &comp, &swap);       //executa o algoritmo quicksort
                    ticks[3] = clock ();
                    printf("\nTempo ordenacao: %6.3fms\n", (double)(ticks[3] - ticks[2])*1000 / (CLOCKS_PER_SEC));
                }
                break;

            case 'h':
                if (extension) {
                    strcat(out, "_heapsort");
                    strcat(out, strrchr(argv[2], '.'));
                }//if
                else
                    strcat(out, "_heapsort");

                b = fopen (out, "w");

                if (b == NULL) {
                    printf ("\nErro ao criar o arquivo de saida\n");
                    return 0;
                }//if

                else {
                    ticks[2] = clock ();
                    heap_sort (V, size, &comp, &swap);          //executa o algoritmo heapsort
                    ticks[3] = clock ();
                    printf("\nTempo ordenacao: %6.3fms\n", (double)(ticks[3] - ticks[2])*1000 / (CLOCKS_PER_SEC));
                }
                break;

            default:                                            //controle de erro para caso o usuário digite um argumento inválido para o tipo de "sort"
                printf ("\nAlgoritmo de sort invalido\n");
                return 0;
        }//switch

        fprint_v (V, size, b);                                  //copia o vetor no arquivo
        printf ("Numeros ordenados: %i\nQuantidade de comparacoes: %i\nQuantidade de trocas: %i\n", size, comp, swap);
    }//else

    if (fclose (a) == EOF) {                                    //fecha o arquivo de entrada "a"
        printf ("\nErro ao fechar o arquivo de entrada\n");
        return 0;
    }

    if (fclose (b) == EOF) {                                    //fecha o arquivo de saída "b"
        printf ("\nErro ao fechar o arquivo de saida\n");
        return 0;
    }
    printf("Arquivo %s gerado com sucesso!\n", out);
    ticks[1] = clock();
    printf("Tempo total %6.3lfms\n", (double)(ticks[1] - ticks[0])*1000 / (CLOCKS_PER_SEC));
    return 0;
}
