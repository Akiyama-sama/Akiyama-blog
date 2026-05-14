---
tags:
  - #pernamant
  - 前端实习挑战
  - 前端
  - 算法
---
问题描述：给出一个个元素的序列，求其中的第k小元素（即序列按升序排序后的第k个元素）。

中项（中间元素）：一个序列的中项为该序列的第「n/2 小元素。

## 快速选择

基本思路：将一个数组的第一个元素为基准元素（pivotIndex），将数组中小于基准元素的，放在左边，大于的放在右边，当基准元素的索引=k-1的时候，此时基准元素的值就是第k小元素。

如果pivotIndex>k-1 就在右边递归找
如果pivotIndex<k-1 就在左边递归找

递归出口为数组长度为1


```ts
function findKthLargest(nums: number[], k: number): number {
    // 随机选择一个基准值（pivot）
    const pivot = nums[Math.floor(Math.random() * nums.length)];
    
    const left: number[] = [];   // 存放大于 pivot 的数
    const mid: number[] = [];    // 存放等于 pivot 的数
    const right: number[] = [];  // 存放小于 pivot 的数

    for (const num of nums) {
        if (num > pivot) left.push(num);
        else if (num < pivot) right.push(num);
        else mid.push(num);
    }

    // 情况 1：第 k 大在左边（大于 pivot 的部分）
    if (k <= left.length) {
        return findKthLargest(left, k);
    }
    // 情况 2：第 k 大就在中间（等于 pivot 的部分）
    if (k <= left.length + mid.length) {
        return pivot;
    }
    // 情况 3：第 k 大在右边（小于 pivot 的部分）
    // 注意：k 也要相应减去左边和中间已经排除掉的个数
    return findKthLargest(right, k - left.length - mid.length);
}
```



# reference
