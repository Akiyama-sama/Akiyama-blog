---
tags:
  - #pernamant
  - 前端实习挑战
  - 前端
  - JavaScript
---
- **增删类方法**：
    - push(item)：在数组末尾添加元素。时间复杂度平均O(1)。
    - pop()：移除并返回最后一个元素。O(1)。
    - unshift(item)：在开头插入元素，需要将所有元素后移一位。O(n)。
    - shift()：移除第一个元素，后续元素前移。O(n)。
    - splice(start, deleteCount, ...items)：从指定位置删除若干元素并可插入新元素。可用于任意位置增删。时间复杂度O(n)，因涉及元素移动。
- **截取与合并**：
    - slice(start, end)：返回子数组，不改变原数组。O(k)，k为返回长度。
    - concat(arr1, arr2)：连接多个数组，生成新数组。O(m+n)。
- **遍历与函数式方法**： 这些方法接受回调函数，常用于函数式编程风格。
    
    - forEach(callback)：遍历每个元素，无返回值。 实现伪代码：
    - map(callback)：返回新数组，每个元素是回调函数的返回值。 时间复杂度O(n)，空间复杂度O(n)。 伪代码：
    - filter(callback)：返回满足条件的元素组成的新数组。 伪代码：
    - reduce(callback, initialValue)：累积计算，将数组归约为单个值。 回调函数形式：(accumulator, current, index, array) => newValue 
    - some(callback)：只要有一个元素满足条件就返回true。短路求值，一旦发现即停止。
    - every(callback)：所有元素都满足才返回true。同样支持短路。
    - find(callback)：返回第一个满足条件的元素，否则undefined。
    - findIndex(callback)：返回对应索引。

- **搜索类方法**：
    - indexOf(value)：返回首次出现的索引，未找到返回-1。基于线性查找，O(n)。
    - includes(value)：判断是否包含某值，返回布尔值。
- **排序与重排**：
    
    - sort(compareFn)：原地排序。若无compareFn，则按字符串Unicode排序。 compareFn(a,b) 返回值决定顺序：
        - < 0: a 在 b 前
        - > 0: a 在 b 后
        - ==0: 顺序不变 JavaScript引擎通常使用Timsort（V8中）或混合排序算法，时间复杂度平均O(n log n)。
    - reverse()：反转数组，原地操作。
- **填充与转换**：
    
    - fill(value, start, end)：用指定值填充区间。O(k)，k为填充长度。
    - flat(depth)：扁平化嵌套数组。例如 [1,[2,3],[4,[5]]].flat(2) → [1,2,3,4,5] 实现依赖递归或栈结构遍历。
    - flatMap(callback)：先map再flat(1)。比map后调用flat更高效，因可流式处理。