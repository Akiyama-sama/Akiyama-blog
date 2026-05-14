---
date: 2026-05-09
tags:
aliases:
---
## 1. 如何读取 `ReadableStream` 的 chunk

`fetch` 请求返回的 `response.body` 就是一个 `ReadableStream` 对象。我们需要通过一个“读号机”（Reader）来逐块获取数据。

```javascript
const response = await fetch('/api/stream');
const reader = response.body.getReader();

while (true) {
  // value 是 Uint8Array（二进制字节数组）
  // done 是一个布尔值，表示流是否结束
  const { value, done } = await reader.read();
  if (done) break;
  
  // 处理每一块 value
}

```

---

## 2. 如何使用 `TextDecoder` 解码

由于 `reader.read()` 返回的是二进制的 `Uint8Array`，直接转字符串会遇到乱码（特别是中文被截断时）。

`TextDecoder` 的优势在于它支持 **流式解码（Stream Decoding）**。通过传递 `{ stream: true }` 参数，它可以自动处理被拆分在两个 chunk 中的多字节字符（如 UTF-8 编码的汉字）。

```javascript
const decoder = new TextDecoder();
// 在循环中使用：
const textChunk = decoder.decode(value, { stream: true });
console.log(textChunk); 

```

---

## 3. 核心难点：如何处理“流拆包”（Splitting）

这是最考功力的地方。在网络传输中，一个完整的 SSE 消息（以 `data: ...\n\n` 结尾）可能会被拆分到不同的 TCP 包中。

### 拆包的情况分析：

1. **完整包：** 一个 chunk 恰好包含一个完整的 `data: ...\n\n`。
2. **粘包：** 一个 chunk 包含了多个消息，或者一个半消息。
3. **断包：** 一个消息的前半段在当前 chunk，后半段在下一个 chunk。

### 工程实现思路：

你需要维护一个**缓冲区（Buffer）**，将不完整的字符串暂存起来，直到遇到 SSE 的结束符 `\n\n`。

```javascript
let buffer = ""; // 用于缓存不完整的消息片段

async function parseSSE() {
  
const response = await fetch('/api/chat', {
  method: 'POST', // AI 场景多为 POST
  headers: {
    'Content-Type': 'application/json',
    // 明确告诉后端，我希望接收流式事件
    'Accept': 'text/event-stream', 
    // 如果有鉴权
    'Authorization': 'Bearer YOUR_TOKEN'
  },
  body: JSON.stringify({ prompt: "你好" })
});

  const reader = response.body.getReader();
  const decoder = new TextDecoder();

  while (true) {
    const { value, done } = await reader.read();
    if (done) break;

    // 1. 解码当前的二进制块并拼接到缓冲区
    buffer += decoder.decode(value, { stream: true });

    // 2. 根据 SSE 协议的分隔符 \n\n 拆分消息
    const parts = buffer.split('\n\n');

    // 3. 关键点：最后一部分可能是“半个消息”，留到下次处理
    buffer = parts.pop(); 

    // 4. 处理每一个完整的消息
    for (const message of parts) {
      if (message.startsWith('data:')) {
        const data = message.replace('data: ', '');
        console.log("收到完整消息:", data);
      }
    }
  }
}

```

---
