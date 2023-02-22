#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

int mergeSort (int *A, int inicio, int fim);
int combina (int *A, int inicio, int meio, int fim);
void geraRandVetor (int *A, int n);
void geraMelhorVetor (int *A, int n);
void geraPiorVetor (int *A, int n);
void printVetor (int *A, int n);

int main() {
    int n = 10;
    int A[n];
    int exec;
    
    geraMelhorVetor (A, n);
    
    clock_t begin = clock();
    exec = mergeSort (A, 0, n-1);
    clock_t end = clock();
    double time_spent = (double)(end - begin) / CLOCKS_PER_SEC;
    
    // printf("MELHOR\n\nEXEC: %d\nTEMPO: %.10f\n\n\n", exec, time_spent);
    
    geraRandVetor (A, n);
    printVetor(A, n);
    begin = clock();
    exec = mergeSort (A, 0, n-1);
    end = clock();
    time_spent = (double)(end - begin) / CLOCKS_PER_SEC;
    printVetor(A, n);
    // printf("MEDIO\n\nEXEC: %d\nTEMPO: %.10f\n\n\n", exec, time_spent);
    
    geraPiorVetor (A, n);
    
    begin = clock();
    exec = mergeSort (A, 0, n-1);
    end = clock();
    time_spent = (double)(end - begin) / CLOCKS_PER_SEC;
    
    // printf("PIOR\n\nEXEC: %d\nTEMPO: %.10f\n\n\n", exec, time_spent);
    
    return 0;
}

int mergeSort (int *A, int inicio, int fim)
{
    int exec = 0; // inicio da contagem
    int meio;
    
    if (inicio < fim) {
    	meio = floor( (inicio+fim)/2 );
    	mergeSort(A, inicio, meio);
    	mergeSort(A, meio+1, fim);
    	combina(A, inicio, meio, fim);
    }
    
    return exec;
}

int combina (int *A, int inicio, int meio, int fim)
{
	int n1 = meio - inicio + 1;
	int n2 = fim - meio;
	int B[n1];
	int C[n2];
	int i, j, k;
	
	for (i = 0; i < n1; i++)
		B[i] = A[inicio + i];
		
	for (j = 0; j < n2; j++)
		C[j] = A[meio + 1 + j];
	
	i = 0;
	j = 0;
	k = inicio;
	
	while (i <= n1 && j <= n2) {
		if (B[i] <= C[j]) {
			A[k] = B[i];
			i++;
		} else {
			A[k] = C[j];
			j++;
		}
		k++;
	}
	
	while (i <= n1) {
		A[k] = B[i];
		i++;
		k++;
	}
	
	while (j <= n2) {
		A[k] = C[j];
		j++;
		k++;
	}
}

void geraRandVetor (int *A, int n)
{
    for (int i = 0; i < n; i++)
        A[i] = rand() % n;
}

void geraMelhorVetor (int *A, int n)
{
    for (int i = 0; i < n; i++)
        A[i] = i;
}

void geraPiorVetor (int *A, int n)
{
    for (int i = 0; i < n; i++)
        A[i] = n - (i + 1);
}

void printVetor (int *A, int n)
{
    for (int i = 0; i < n; i++)
        printf ("| %i ", A[i]);
    printf ("|\n\n");
}

