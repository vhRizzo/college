#include <stdio.h>

void cria_heap (int *V, int parent, int end) {
    int aux = V[parent], child = parent * 2 + 1;
    while (child <= end) {
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
    V[parent] = aux;
}

void heap_sort (int *V, int n) {
    int i, tmp;
    for (i = (n - 1) / 2; i >= 0; i --)
        cria_heap (V, i, n - 1);
    for (i = n - 1; i >= 1; i --) {
        tmp = V[0];
        V[0] = V[i];
        V[i] = tmp;
        cria_heap (V, 0, i - 1);
    }
}

void print_v (int *V, int size) {
    printf ("\n");
    for (int i = 0; i < size; i ++)
        printf ("| %i ", V[i]);
    printf ("|\n");
}


int main() {
    int V[7] = {90, 23, 67, -8, 4, 54, 21};
    heap_sort (V, 7);
    print_v (V, 7);
    return 0;
}
