---
date: 2026-07-06
tags:
aliases:
---
虽然做这个需求只是改改样式，但是想写出亮点，或者说是想要讲好完整的一个故事肯定是不够的，因此得自己包装一下，可以包装成 Agent 前端相关

1. 首先得搞清楚整个小牛的收发消息以及卡片渲染的过程
2. 再是小牛是如何控制整个表单的，特别是这个小牛在低码里面，是如何与另外一个低码表单进行联动的


## Agent流式数据流转

完整数据流总结

 SSE → fetch/canalFetch (text/event-stream)
  → streamToUIMessageChunks (transport.ts)
    → parseSSEPayload: 解析外层 JSON
    → parseSSELine: messageType/contentType → StreamContentItem
    → createQueueEntry: 挂载 atom/status 副作用
    → Scheduler: batchSize/intervalMs 节奏派发
  → useChat 内部状态机: idle→submitted→streaming→ready
    → lastMessage.parts 实时更新
  → StreamingEngine 渲染 (engine/index.tsx:730-895)
    → preprocessParts: 折叠为 ThoughtBlock/SectionBlock/MessagePart
    → renderMessageParts:
      → ThoughtBlock → StreamingThoughtBlock (思考链折叠)
      → SectionBlock → StreamingSectionBlock → SectionHeader (标题)
      → MessagePart → StreamingCardController → cardComponentMap[contentType] (卡片)
  → StreamingStore.status 同步 (streamingInstance)
  → 稳态 800ms 后 onReady + reportAgentRenderSuccess


小牛是如何操控这个表单的，主要是依赖于“依赖注入”，低码运行时直接把修改表单的一个方法给注入到小牛里面，后端 SSE 仅需回填关键表单字段，再将这些字段给传给这个依赖注入的方法，其实就是setModelAndMarketingObjective这个方法，就能富裕小牛这个能力

至于低码组件的这个表单能力也需要深入阅读理解：



