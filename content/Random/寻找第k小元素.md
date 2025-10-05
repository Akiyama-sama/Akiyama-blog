---
tags:
  - '#pernamant'
---
问题描述：给出一个个元素的序列，求其中的第k小元素（即序列按升序排序后的第k个元素）。

中项（中间元素）：一个序列的中项为该序列的第「n/2 小元素。

## 快速选择

基本思路：将一个数组的第一个元素为基准元素（pivotIndex），将数组中小于基准元素的，放在左边，大于的放在右边，当基准元素的索引=k-1的时候，此时基准元素的值就是第k小元素。

如果pivotIndex>k-1 就在右边递归找
如果pivotIndex<k-1 就在左边递归找

递归出口为数组长度为1


```js
const arr = [5, 3, 8, 4, 2];

function quickSelect(arr, k) {
  // 增加边界检查
  if (k < 1 || k > arr.length) {
    return null; 
  }
  return _quickSelect(arr, k);
}

function _quickSelect(arr, k) {
  // 递归的终止条件
  if (arr.length === 1) {
    return arr[0];
  }
  
  const { result, pivotIndex } = partition(arr);
  
  const targetIndex = k - 1; // 目标索引

  if (pivotIndex === targetIndex) {
    return result[pivotIndex];
  } else if (pivotIndex > targetIndex) {
    // 目标在左边
    return _quickSelect(result.slice(0, pivotIndex), k);
  } else { // pivotIndex < targetIndex
    // 目标在右边，更新 k 值
    const newK = k - (pivotIndex + 1);
    return _quickSelect(result.slice(pivotIndex + 1), newK);
  }
}

function partition(arr) {
  const pivot = arr[0];
  const left = [];
  const right = [];
  const mid = [];

  for (let i = 1; i < arr.length; i++) {
    const e = arr[i];
    if (e < pivot) {
      left.push(e);
    } else if (e > pivot) {
      right.push(e);
    } else {
      mid.push(e);
    }
  }

  // 修正：将 pivot 自身放回数组
  const result = [...left, pivot, ...mid, ...right];
  const pivotIndex = left.length; // pivot 的最终索引
  return { result, pivotIndex };
}

const result = quickSelect(arr, 2);
console.log(result); // 正确输出: 3
```



# reference
