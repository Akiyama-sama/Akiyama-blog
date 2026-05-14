---
date: 2025-12-01
tags:
  - 前端实习挑战
  - 前端
  - AI
  - 工程化
---

1. **底层通信机制：HTTP/1.1 分块传输编码（Chunked Transfer Encoding）** 在HTTP/1.1中，服务器可以通过设置响应头 `Transfer-Encoding: chunked` 来启用分块传输。这意味着服务器不需要预先知道响应体的总长度，可以一边生成数据，一边将其分成多个“块”发送给客户端。每个块包含一个十六进制的长度标识和实际数据，最后以长度为0的块表示结束。这种机制允许服务端在未完成全部计算时就开始传输数据，非常适合AI生成类任务——因为生成过程是顺序的、耗时的，且输出具有前缀依赖性（即下一个token依赖前面的上下文）。
2. **服务端实现：生成式模型的逐token输出** 大多数现代AI语言模型（如Transformer架构）采用自回归方式生成文本，即每次预测一个token，并将其作为输入的一部分继续生成下一个token。这个过程本质上是串行的，因此天然适合流式输出。例如，在调用模型的generate()函数时，可以通过回调函数或生成器模式（generator）捕获每一个新生成的token，并立即通过HTTP响应流发送出去。
3. **[[WebSocket]] 与 Server-Sent Events ([[SSE]])** 虽然分块传输可用于普通HTTP接口，但在实际AI应用中更常使用两种技术来实现流式返回：
    - **Server-Sent Events (SSE)**：基于HTTP长连接，服务器可以持续向客户端推送消息。它使用 `text/event-stream` 的MIME类型，每条消息以 `data: ...` 开头，支持自动重连。SSE简单轻量，适用于单向服务器到客户端的流式输出，广泛用于AI聊天接口。
    - **WebSocket**：提供全双工通信通道，适合需要双向交互的场景（如实时问答、中断生成）。但相比SSE更复杂，资源开销更大。
4. **后端框架支持** 现代Web框架普遍支持异步流式响应。例如：
    - Python Flask/FastAPI 中可使用生成器函数配合 `StreamingResponse`
    - Node.js Express 中可通过 `res.write()` 发送数据块
    - Java Spring WebFlux 支持响应式流（Reactive Streams）
5. **前端如何接收？** 前端通常使用 `fetch` API 或 `EventSource` 对象来接收流式数据。例如使用 fetch 时，可以从 response.body 获取 ReadableStream 并读取其内容：
    ```javascript
    const response = await fetch('/api/generate', { method: 'POST' });
    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    
    while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        const text = decoder.decode(value);
        // 解析并显示增量文本
        console.log(text);
    }
    ```

6. **性能与用户体验优化** 流式返回不仅提升了感知速度（用户无需等待完整响应），还能降低内存压力（避免缓冲大量中间结果）。同时，结合 token级延迟优化（如 speculative decoding）、缓存机制（KV Cache复用）也能进一步提升吞吐效率。