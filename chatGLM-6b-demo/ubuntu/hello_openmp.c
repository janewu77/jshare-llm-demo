#include <omp.h>
#include <stdio.h>

int main() {
    #pragma omp parallel
    printf("Hello, world!\n");
    return 0;
}