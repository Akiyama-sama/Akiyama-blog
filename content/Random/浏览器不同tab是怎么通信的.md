---
date: 2026-05-08
tags:
aliases:
---
1. LocalStorage，可以让不同的 tab 监听一个 storage来进行通信

```js
// 页面 A 写入数据
localStorage.setItem('update_time', Date.now());

// 页面 B 监听变化
window.addEventListener('storage', (e) => {
  if (e.key === 'update_time') {
    console.log('检测到数据更新:', e.newValue);
  }
});
```

2. BroadcastChannel API

一个页面发送消息，所有加入该频道的标签页都能收到。

```js
// 创建频道
const bc = new BroadcastChannel('my_channel');

// 发送消息
bc.postMessage('Hello Tabs!');

// 接收消息
bc.onmessage = (event) => {
  console.log('收到消息:', event.data);
};
```

3. Shared Worker
4. window.opener