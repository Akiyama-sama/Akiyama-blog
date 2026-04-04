---
date: 2026-03-26
tags:
---
1. 通用头（General Headers）用于请求和响应的通用信息。

|   |   |   |
|---|---|---|
|头字段|作用|示例|
|Cache-Control|缓存控制，如是否缓存、缓存时长|Cache-Control: no-cache|
|Connection|管理连接方式（保持或关闭）|Connection: keep-alive|
|Date|请求发送的时间|Date: Wed, 27 Aug 2025 12:00:00 GMT|

2. 请求头（Request Headers）客户端向服务器发送请求时附带的信息。（1）客户端信息

|   |   |   |
|---|---|---|
|头字段|作用|示例|
|Host|指定请求的主机名和端口（HTTP/1.1 必须）|Host: www.example.com|
|User-Agent|客户端信息（浏览器、系统等）|User-Agent: Mozilla/5.0 ...|
|Referer|表示请求的来源页面 URL|Referer: https://example.com/page|
|Accept|告诉服务器客户端能接收的 MIME 类型|Accept: text/html,application/json|
|Accept-Language|客户端期望的语言|Accept-Language: zh-CN, en-US|
|Accept-Encoding|支持的压缩方式|Accept-Encoding: gzip, deflate, br|

（2）认证与安全

|   |   |   |
|---|---|---|
|头字段|作用|示例|
|Authorization|认证信息，如 Token、Basic Auth|Authorization: Bearer <token>|
|Cookie|携带客户端的 Cookie，用于会话保持|Cookie: sessionId=abc123|
|Origin|表示请求的来源（跨域时使用）|Origin: https://example.com|
|X-CSRF-Token|防止 CSRF 攻击的安全令牌|X-CSRF-Token: abc123|

（3）缓存控制

|   |   |   |
|---|---|---|
|头字段|作用|示例|
|If-Modified-Since|校验资源是否在指定时间后修改过|If-Modified-Since: Wed, 21 Oct 2015 07:28:00 GMT|
|If-None-Match|配合 ETag 校验资源是否变更|If-None-Match: "etag12345"|
|Pragma|HTTP/1.0 缓存控制，通常 no-cache|Pragma: no-cache|

（4）请求体相关

|   |   |   |
|---|---|---|
|头字段|作用|示例|
|Content-Type|请求体的 MIME 类型|Content-Type: application/json|
|Content-Length|请求体的字节长度|Content-Length: 123|

3. 自定义头（Custom Headers）

|   |   |   |
|---|---|---|
|头字段|作用|示例|
|X-Requested-With|标识 AJAX 请求|X-Requested-With: XMLHttpRequest|
|X-Forwarded-For|记录客户端真实 IP（经过代理时）|X-Forwarded-For: 203.0.113.195|
|X-Real-IP|表示客户端真实 IP|X-Real-IP: 203.0.113.195|

4. HTTP/2 专用伪头

|   |   |
|---|---|
|头字段|作用|
|:method|请求方法（GET、POST 等）|
|:path|请求路径|
|:authority|主机和端口|
|:scheme|协议（http/https）|

请求头面试常问问题总结Content-Type 和 Accept 区别？ Content-Type 表示请求体的格式，Accept 表示期望服务器返回的格式。If-Modified-Since 和 If-None-Match 区别？ 前者基于时间（Last-Modified），后者基于资源标识（ETag），后者更精确。Referer 的作用？ 表示请求来源页面 URL，用于防盗链、流量分析，但受 Referrer-Policy 控制，HTTPS → HTTP 时可能被移除