---
date: 2026-09-28
tags:
aliases:
---
LeetCode 的核心是**核心代码模式**（只需实现一个函数），而笔试中的 **ACM 模式**（也称命令行交互模式）需要你**自己处理标准输入（stdio）和标准输出（stdout）**。

在 JavaScript (Node.js) 下写 ACM 模式，主要挑战在于处理读入数据的格式（尤其是多行、空格分隔的数组或矩阵）。

---

### 一、 ACM 模式的核心写法（模板）

在 Node.js 中，最主流且推荐的处理标准输入的方式是使用内置的 `readline` 模块。

#### 1. 单行输入 / 固定行数输入

处理每行读入的数据，在 `line` 事件中进行解析：

```javascript
const readline = require('readline');

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

rl.on('line', (line) => {
  // 1. 读取并处理单行输入
  // 比如输入: "1 2 3"
  const nums = line.trim().split(' ').map(Number);
  
  // 2. 调用算法函数计算结果
  const result = solve(nums);
  
  // 3. 打印输出
  console.log(result);
});

function solve(nums) {
  // 这里写你平时在 LeetCode 里的核心逻辑
  return nums.reduce((a, b) => a + b, 0);
}

```

#### 2. 多行输入（最常见：先读 N, M，再读数组/矩阵）

例如输入：

```text
3 2
1 2 3
4 5 6

```

可以通过维护一个全局变量记录行数或状态：

```javascript
const readline = require('readline');

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

const inputs = [];

rl.on('line', (line) => {
  if (line.trim() !== '') {
    inputs.push(line.trim());
  }
});

// 当所有输入读取完毕后统一处理（或在达到预期行数后处理）
rl.on('close', () => {
  if (inputs.length === 0) return;

  // 第一行：N 和 M
  const [n, m] = inputs[0].split(' ').map(Number);

  // 后续行：矩阵/数组
  const matrix = [];
  for (let i = 1; i <= n; i++) {
    matrix.push(inputs[i].split(' ').map(Number));
  }

  // 计算并输出结果
  const result = solve(n, m, matrix);
  console.log(result);
});

function solve(n, m, matrix) {
  // 算法核心代码
  return matrix[0][0];
}

```

---

### 二、 JS 处理 ACM 模式的常见坑点

1. **数值转换与字符串清理**：
* 输入的每行末尾可能带有隐式的 `\r` 或空字符，务必使用 `.trim()` 清理。
* 使用 `.split(/\s+/)` 替代 `.split(' ')`，以防输入数据中有连续多个空格。


2. **大数溢出**：
* JS 的 `Number.MAX_SAFE_INTEGER` 是 $2^{53} - 1$。如果题目要求处理超过 64 位整数的数据，需要改用 `BigInt`。


3. **输出格式**：
* 注意题目要求的输出格式（如“每组数据间换行”、“输出保留两位小数”等）。
* 保留小数可以使用 `.toFixed(2)`。


4. **内存与性能**：
* 如果输入数据极大（几十万行），将所有数据全部存入 `inputs` 数组可能会导致内存超限。建议在 `line` 事件中实时处理或分块处理。



---

### 三、 推荐练习平台

1. **牛客网（Nowcoder）**：
* 专门针对国内企业笔试题型，支持 Node.js ACM 模式。
* 首页搜索 **“JS(Node.js) V8 ACM模式专项练习”** 或在“输入输出输入练习”专题中直接进行训练。


2. **卡码网（KamaCoder）**：
* 由“代码随想录”作者打造，专为 ACM 模式设计，提供非常标准的输入输出测试环境。



---