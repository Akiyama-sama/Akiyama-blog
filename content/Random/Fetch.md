---
tags:
  - '#pernamant'
---
Fetch这个较新的API是意在替代XMLHttpRequest，他是基于Promise的

* 基于Promise，支持async/await
* 原生支持
* 不会自动拒绝HTTP错误状态

示例
```js
fetch('https://api.example.com/data')
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error('Error:', error));

```





# reference
