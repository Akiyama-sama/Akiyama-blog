---
tags:
  - '#pernamant'
  - 计算机网络
  - Web
---
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





# reference
[[HTTP报文]]