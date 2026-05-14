---
date: 2026-01-14
tags:
  - 算法
  - 前端实习挑战
  - 前端
---
给你一个整数数组 `citations` ，其中 `citations[i]` 表示研究者的第 `i` 篇论文被引用的次数。计算并返回该研究者的 **`h` 指数**。

根据维基百科上 [h 指数的定义](https://baike.baidu.com/item/h-index/3991452?fr=aladdin)：`h` 代表“高引用次数” ，一名科研人员的 `h` **指数** 是指他（她）至少发表了 `h` 篇论文，并且 **至少** 有 `h` 篇论文被引用次数大于等于 `h` 。如果 `h` 有多种可能的值，**`h` 指数** 是其中最大的那个。


# 排序法
排序：将引用次数数组 citations 按 从大到小（降序）排列。
遍历与比较：遍历排序后的数组，下标为 $i$ 的论文是第 $i+1$ 篇高引用论文。如果当前论文的引用次数 $citations[i] \ge i + 1$，说明我们至少有 $i+1$ 篇论文引用次数大于等于 $i+1$。我们继续向后看，直到不满足这个条件为止。结论：最大的符合条件的 $i+1$ 就是 h 指数。

```js
/**
 * @param {number[]} citations
 * @return {number}
 */
var hIndex = function(citations) {
    const sorted = citations.sort((a,b)=>b-a)

    let i = 0
    while(sorted[i]>=i+1){
        i++
    }
    return i
};
```





