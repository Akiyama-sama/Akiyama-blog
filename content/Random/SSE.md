---
tags:
  - #pernamant
  - 前端实习挑战
  - 前端
  - AI
  - 工程化
---
服务器向浏览器发送信息，除了[[WebSocket]]之外，还有SSE（Server-Sent Events）。他只能服务器向浏览器发送数据，与之相对的是[[WebSocket]]，且这个数据不是一次性数据包，而是一个数据流

 Server-Sent Events（SSE）是 HTML5 提供的一种标准 API，用于建立从服务器到客户端的单向通信通道。客户端通过 EventSource 接口连接服务器，服务器以特定格式（text/event-stream）持续返回数据片段，浏览器自动解析并触发 message 事件。

核心特点：

- 基于 HTTP 协议，复用现有基础设施（如 HTTPS、代理、CDN）。
- 自动重连机制：断线后客户端会自动尝试重新连接。
- 支持事件类型区分（如 message、error、customEvent）。
- 内置 Last-Event-ID 机制，支持消息恢复。


**报文格式**
SSE 传输的数据必须是 **UTF-8** 编码的文本，每条消息以 `\n\n`（两个换行符）结束。

常见字段如下：
- `data:` 消息内容（必选）。
- `event:` 自定义事件名称。
- `id:` 消息 ID，用于断线重连时告知服务器上次接收的位置（`Last-Event-ID`）。
- `retry:` 建议浏览器重连的间隔时间（毫秒）。











# reference
[[Server-Sent Events 教程 - 阮一峰的网络日志]]