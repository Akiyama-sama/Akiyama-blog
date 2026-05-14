---
tags:
  - #pernamant
  - 前端实习挑战
  - 前端
  - 计算机网络
---
Ajax是 Asyncchronous JavaScript and XML的缩写，指的是通过JS的异步通信，获取XML文档再获取其中的数据，更新部分网页，而不用刷新整个网页


创建AJAX请求的步骤：

- **创建一个 XMLHttpRequest 对象。**
- 在这个对象上 **使用 open 方法创建一个 HTTP 请求** ，open 方法所需要的参数是请求的方法、请求的地址、是否异步和用户的认证信息。
- 在发起请求前，可以为这个对象 **添加一些信息和监听函数** 。比如说可以通过 setRequestHeader 方法来为请求添加头信息。还可以为这个对象添加一个状态监听函数。一个 XMLHttpRequest 对象一共有 5 个状态，当它的状态变化时会触发onreadystatechange 事件，可以通过设置监听函数，来处理请求成功后的结果。当对象的 readyState 变为 4 的时候，代表服务器返回的数据接收完成，这个时候可以通过判断请求的状态，如果状态是 2xx 或者 304 的话则代表返回正常。这个时候就可以通过 response 中的数据来对页面进行更新了。
- 当对象的属性和监听函数设置完成后，最后调 **用 sent 方法来向服务器发起请求** ，可以传入参数作为发送的数据体。
```javascript
function makeAjaxRequest(url, method, data, callback) {
  const xhr = new XMLHttpRequest();
  
  xhr.onreadystatechange = function() {
    if (xhr.readyState === XMLHttpRequest.DONE) {
      if (xhr.status === 200) {
        callback(null, xhr.responseText);
      } else {
        callback(new Error('请求失败: ' + xhr.status));
      }
    }
  };
  
  xhr.open(method, url, true);
  
  if (method.toUpperCase() === 'POST') {
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify(data));
  } else {
    xhr.send();
  }
}

// 使用示例
makeAjaxRequest('https://api.example.com/data', 'GET', null, function(error, response) {
  if (error) {
    console.error('出错了:', error);
  } else {
    console.log('收到响应:', response);
  }
});
```




# reference
