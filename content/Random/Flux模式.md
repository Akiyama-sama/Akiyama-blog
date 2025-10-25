---
date: 2025-10-25
tags: 
---
Flux模式的核心思想为单项数据流，解决了MVC模式中数据混乱的问题。

有四大组件：

- Action：动作，描述发生了什么的动作
- Dispatcher：调度器，负责广播Action
- Stores：各自存储，并包含更新逻辑
- VIew：视图，从Store中获取数据并渲染