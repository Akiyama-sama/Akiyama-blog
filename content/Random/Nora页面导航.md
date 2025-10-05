---
tags:
  - '#pernamant'
---

## NavigationHistory（单个页面信息）

```typescript
interface NavigationHistory {
  pageTitle: PageTitles;  // 页面标题/类型，如'Home'、'Lyrics'等
  data?: PageData;        // 可选的页面数据，传递给页面组件的参数
  onPageChange?: (changedPageTitle: PageTitles, changedPageData?: PageData) => void; // 页面切换回调
}
```

每个`NavigationHistory`对象代表用户访问过的一个页面状态，包含该页面的标题、数据和可能的页面切换回调函数。

## NavigationHistoryData（整体导航状态）

```typescript
interface NavigationHistoryData {
  pageHistoryIndex: number;    // 当前激活页面的索引
  history: NavigationHistory[]; // 历史页面记录数组
}
```

`NavigationHistoryData`包含了两个关键部分：
1. `history`数组：按时间顺序存储用户访问过的所有页面
2. `pageHistoryIndex`：指向当前显示的页面在数组中的位置

## 实际工作模式

类似浏览器的历史导航机制：

1. **添加新页面**：当用户导航到新页面时，将新页面信息添加到`history`数组末尾，并将`pageHistoryIndex`指向新添加的项

   ```javascript
   navigationHistory.history.push(pageData);
   navigationHistory.pageHistoryIndex += 1;
   ```

2. **前进/后退**：通过改变`pageHistoryIndex`的值实现页面的前进/后退，无需重新构建页面状态

3. **处理分支导航**：当用户从历史记录中间位置导航到新页面时，会截断此后的历史记录（就像浏览器一样）

   ```javascript
   navigationHistory.history = navigationHistory.history.slice(
     0, 
     navigationHistory.pageHistoryIndex + 1
   );
   ```

这种设计非常优雅，它使应用能够维护完整的导航历史，支持前进/后退功能，同时保留页面状态和数据，提供类似浏览器的用户体验，但完全在应用内部管理而不依赖浏览器历史API。






# reference
