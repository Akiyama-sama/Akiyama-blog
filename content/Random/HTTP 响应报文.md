---
tags:
  - '#pernamant'
  - 计算机网络
  - Web
---
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
[[HTTP报文]]