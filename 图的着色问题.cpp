#include <iostream>
#include <cstdio>
#include<vector>
using namespace std;

int n, e, m;
int a = 1, b = 1;
int cou = 0;
int graph[20][20] = { 0 };
int color[20] = { 0 };


//用来判断节点c能否涂色
bool ok(int c) {
    for (int k = 1; k <= n; k++) {
        if (graph[c][k] && color[c] == color[k]) {
            return false;
        }
    }
    return true;
}

void backtrack(int cur) {
    if (cur > n) {
        for (int i = 1; i <= n; i++) {
            printf("%d ", color[i]);
        }
        cou++;
        printf("\n");
    }
    else {
        for (int i = 1; i <= m; i++) {
            color[cur] = i;
            if (ok(cur)) {
                backtrack(cur + 1);
            }
            color[cur] = 0;
        }
    }
}

int main()
{
    cout << "请输入点的数目边的数目和颜色数目:";
    cin >> n >> e >> m;
    cout << "输入每条边的两个点的下标;" << endl;

    for (size_t i = 0; i < e; i++)
    {
        cin >> a >> b;
        graph[a][b] = 1;
        graph[b][a] = 1;
    }

    backtrack(1);
    printf("Total=%d", cou);
    return 0;
}