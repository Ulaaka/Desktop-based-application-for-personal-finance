#include <stdio.h>

int main() {
    int N, M, K;
    scanf("%d %d %d", &N, &M, &K);

    int a[100][100];
    int i, j, k,  toot = 1;

    for(k = 0; k < K; k++){
        for(i = 0; i < N; i++) {
            for(j = 0; j < M; j++) {
            a[i][j] = toot++;
            }
        }

    }


    for(i = 0; i < N; i++) {
        for(j = 0; j < M; j++) {
            printf("%4d", a[i][j]);
        }
        printf("\n");
    }

    return 0;
}