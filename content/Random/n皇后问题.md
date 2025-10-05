---
tags:
  - '#pernamant'
---
问题描述：根据国际象棋的规则，皇后可以攻击与同处一行、一列或一条斜线上的棋子。给定 n 个皇后和一个 n×n 大小的棋盘，寻找使得所有皇后之间无法相互攻击的摆放方案。

## 回溯算法

```js
/* 回溯算法：n 皇后 */
function backtrack(row, n, state, res, cols, diags1, diags2) {
    // 当放置完所有行时，记录解
    if (row === n) {
        res.push(state.map((row) => row.slice()));
        return;
    }
    // 遍历所有列
    for (let col = 0; col < n; col++) {
        // 计算该格子对应的主对角线和次对角线
        const diag1 = row - col + n - 1;
        const diag2 = row + col;
        // 剪枝：不允许该格子所在列、主对角线、次对角线上存在皇后
        if (!cols[col] && !diags1[diag1] && !diags2[diag2]) {
            // 尝试：将皇后放置在该格子
            state[row][col] = 'Q';
            cols[col] = diags1[diag1] = diags2[diag2] = true;
            // 放置下一行
            backtrack(row + 1, n, state, res, cols, diags1, diags2);
            // 回退：将该格子恢复为空位
            state[row][col] = '#';
            cols[col] = diags1[diag1] = diags2[diag2] = false;
        }
    }
}

/* 求解 n 皇后 */
function nQueens(n) {
    // 初始化 n*n 大小的棋盘，其中 'Q' 代表皇后，'#' 代表空位
    const state = Array.from({ length: n }, () => Array(n).fill('#'));
    const cols = Array(n).fill(false); // 记录列是否有皇后
    const diags1 = Array(2 * n - 1).fill(false); // 记录主对角线上是否有皇后
    const diags2 = Array(2 * n - 1).fill(false); // 记录次对角线上是否有皇后
    const res = [];

    backtrack(0, n, state, res, cols, diags1, diags2);
    return res;
}
```




# reference
https://www.hello-algo.com/chapter_backtracking/n_queens_problem/