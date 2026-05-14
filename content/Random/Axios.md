---
tags:
  - #pernamant
  - 前端实习挑战
  - 前端
  - 计算机网络
---
Axios是基于Promise的 HTTP客户端，浏览器和Node.js都可以用

* 支持浏览器和Node.js
* 自动装换Json格式
* 可以拦截请求和响应
* 可以取消请求
* 客户端支持防御XSRF

示例
```js
axios.get('https://api.example.com/data')
  .then(response => {
    console.log(response.data);
  })
  .catch(error => {
    console.error('Error:', error);
  });

```

[[构建自己的Axios]]







# reference
