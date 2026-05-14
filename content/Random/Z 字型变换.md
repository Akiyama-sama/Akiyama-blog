---
date: 2026-01-21
tags:
  - 前端实习挑战
  - 前端
  - 算法
---
将一个给定字符串 `s` 根据给定的行数 `numRows` ，以从上往下、从左到右进行 Z 字形排列。

比如输入字符串为 `"PAYPALISHIRING"` 行数为 `3` 时，排列如下：

P   A   H   N
A P L S I I G
Y   I   R

之后，你的输出需要从左往右逐行读取，产生出一个新的字符串，比如：`"PAHNAPLSIIGYIR"`。

请你实现这个将字符串进行指定行数变换的函数：

string convert(string s, int numRows);


```ts
function convert(s: string, numRows: number): string {
    // 1. 特殊情况处理：如果行数只有 1 行，或者行数大于字符串长度，直接返回原字符串
    if (numRows < 2 || s.length <= numRows) return s;
    
	const rows: string[] = new Array(numRows).fill("");
	let currentRow = 0
	let goDown = false
	
	for(const char of s) {
		rows[currentRow] +=char
		//如果当前到达第一行或者最后一行的时候，改变前进方向
		
		if(currentRow === 0 || currentRow === numRows -1){
			goDown = !goDown
		}

		//根据前进方向来判断 currentRow + -
		currentRow += goDown ? 1 : -1
	}
	
	return rows.join("")
};
```






