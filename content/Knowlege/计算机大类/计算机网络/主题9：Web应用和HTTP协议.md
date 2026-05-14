---
tags:
  - #literature
  - 计算机网络
  - 前端实习挑战
  - 前端
  - CSS
---
# 概述
1. 在http1.0 中，一次请求就要进行一次完整的[[TCP连接]]，即连接，传输，断开，这样的效率非常低下，而http1.1使用[[流水线方式]]的持续连接，可以在一次[[TCP连接]]中传输多份数据
2. [[Cookie]]
3. 当与暂时存放的请求相同的新请求到达时，万维网高速缓存就把暂存的响应发送出去，而不需要按 URL 的地址再去因特网访问该资源。

# 原文摘要

1、  http1.1默认采用[[流水线方式]]的持久[[TCP连接]]。解释其含义

2、  **[[Cookie]]的工作原理

3、  **[[代理服务器]]（web高速缓存）的作用和应用价值？（见期中简答题）**

**访问Web应用的过程

(1) 浏览器分析超链指向页面的 URL。
(2) 浏览器向 DNS 请求解析 www.tsinghua.edu.cn 的 IP 地址。
(3) 域名系统 DNS 解析出清华大学服务器的 IP 地址。
(4) 浏览器与服务器建立 TCP 连接
(5) 浏览器发出取文件命令：
      GET /chn/yxsz/index.htm。
(6) 服务器给出响应，把文件 index.htm 发给浏览器。
(7) TCP 连接释放。
(8) 浏览器显示“清华大学院系设置”文件 index.htm 中的所有文本。

## [[HTTP协议]]（超文本传输协议）
现在主要使用1.1的版本
可参考[[HTTP报文]]

请求报文：
![file-20241203131244734](https://obsidian-picgo-mio.oss-cn-hangzhou.aliyuncs.com/file-20241203131244734.png)
响应报文
![file-20241203131305563](https://obsidian-picgo-mio.oss-cn-hangzhou.aliyuncs.com/file-20241203131305563.png)