---
tags:
  - #pernamant
  - #计算机网络
  - #Web
  - 前端实习挑战
  - 前端
  - CSS
---
### 1. [[HTTP 请求报文]]

HTTP 请求由三部分组成：[[请求行]]、[[请求头]]和[[请求体]]。

```
POST /customer HTTP/1.1 #请求行
Host: localhost:8080  #请求头
User-Agent: Mozilla/5.0
Content-Type: application/json
Content-Length: 34
#请求体：json格式的数据

{  
    "name": "John Doe",
    "age": 30

}
```
### 2. [[HTTP 响应报文]]

HTTP 响应也由三部分组成：[[状态行]]、[[响应头]]和[[响应体]]。

```
HTTP/1.1 200 OK #状态行
Content-Type: application/json #响应头
Content-Length: 34
{ #响应体

    "message": "请求成功",
    "data": {
        "name": "John Doe",
        "age": 30
    }

}
```


# reference
[[访问一个web服务器的过程是怎样的]]
[[主题9：Web应用和HTTP协议]]