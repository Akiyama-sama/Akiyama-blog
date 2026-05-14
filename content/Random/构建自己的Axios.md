---
date: 2025-11-29
tags:
  - 前端实习挑战
  - 前端
  - 计算机网络
---
这是一个利用浏览器API中的XMLHttpRequest的实现

```ts
export type Method = 'get' | 'GET' | 'delete' | 'DELETE' | 'head' | 'HEAD' | 'options' | 'OPTIONS' | 'post' | 'POST' | 'put' | 'PUT' | 'patch' | 'PATCH';

export interface AxiosRequestConfig {
  method:Method
  url:string
  data:any
}

function axios(config:AxiosRequestConfig) {
  return new Promise((resolve, reject) => {
    const xhr = new XMLHttpRequest();

    // 1. 初始化请求 (配置 method 和 url)
    // 在此处编写代码...
    xhr.open(config.method,config.url)
    // 2. 监听状态变化 (处理响应)
    xhr.onreadystatechange = function() {
        if(xhr.readyState ==4){
          if(xhr.status >= 200 && xhr.status <300){
            resolve(JSON.parse(xhr.response))
          }else{
            reject(Error(`错误状态码：${xhr.status},错误提示：${xhr.statusText}`))
          } 
        }
    };
    xhr.setRequestHeader('Content-Type','application/json')
    // 3. 发送请求
    // 在此处编写代码...
    xhr.send(config.data ? JSON.stringify(config.data):null)
  });
}

axios({ method: 'GET', url: 'https://jsonplaceholder.typicode.com/todos/1',data:null })
  .then(response => console.log(response));
```