---
tags:
  - '#pernamant'
---
服务器向浏览器发送信息，除了[[WebSocket]]之外，还有SSE（Server-Sent Events）。他只能服务器向浏览器发送数据，与之相对的是[[WebSocket]]，且这个数据不是一次性数据包，而是一个数据流

 Server-Sent Events（SSE）是 HTML5 提供的一种标准 API，用于建立从服务器到客户端的单向通信通道。客户端通过 EventSource 接口连接服务器，服务器以特定格式（text/event-stream）持续返回数据片段，浏览器自动解析并触发 message 事件。

核心特点：

- 基于 HTTP 协议，复用现有基础设施（如 HTTPS、代理、CDN）。
- 自动重连机制：断线后客户端会自动尝试重新连接。
- 支持事件类型区分（如 message、error、customEvent）。
- 内置 Last-Event-ID 机制，支持消息恢复。












# reference
[[Server-Sent Events 教程 - 阮一峰的网络日志]]