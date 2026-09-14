---
date: 2026-07-14
tags:
aliases:
---
[[磁力小牛重构技术方案]]
## 前言

这是一个绝佳的搞产出以及提升的机会，这段时间一定要认真搞这个，就算我接了一些UI组件的活儿，但我觉得要不能搞出差错，这个还是需要多花点时间的。

## vite开发体验升级

背景：
1. 开发调试费劲，不能热重载，mock数据也费劲
2. 本地构建很脆弱，经常改动一两行代码构建直接崩掉，又要重新pnpm preview，移动端的每次重新pnpm preview都要2-3分钟

解决方法：引入 Vite 作为本地开发构建工具，区分 pnpm dev（Vite HMR）和 pnpm build（drow 生产构建）。

收益：

- 代码改动 → 浏览器更新从 2~3 分钟 → 秒级（< 1s）
- 不再因构建崩溃中断开发节奏
- 支持同时开多个包的 HMR，开发体验对齐主流前端项目



## 首屏资源过大

背景：
- 首屏资源 25M+ 且持续劣化，包大小达临界值无法新增依赖
- 引入新的第三方组件只能用微前端形式，开发成本极高

![[Pasted image 20260714212152.png]]


解决方法：

- 卡片组件独立拆包 + React.lazy 按需加载
- svg 图片资源从 KCDN 获取，而非嵌入代码


设计团队的诉求：
1. 能够减少走查频率
2. 能够复用我们组件

目录：

|                                 |                           |
| ------------------------------- | ------------------------- |
| 包                               | 职责                        |
| @ad/esp-robot-core              | IM SDK 集成、标准化 IM 模型       |
| @ad/esp-robot-runtime           | 实例生命周期、宿主上下文、会话、请求和流式客户端  |
| @ad/esp-robot-ui                | L1/L2/L3 UI 组件库           |
| @ad/esp-robot-chat-content      | 消息解码和注册、会话渲染、输入区与欢迎页      |
| @ad/esp-robot-platform          | PC/Mobile 宿主装配            |
| @ad/esp-robot-devtools          | 本地环境配置、Chrome DevTools 扩展 |
| @ad/esp-robot-ecom-card-adapter | 电商场景卡片适配层和独立 CDN 产物       |

核心依赖方向：

```
platform      → runtime, chat-content, robot-ui
chat-content  → runtime, robot-ui
robot-ui      → runtime
runtime       → im-core
im-core       → IM SDK packages only
```

实际接需求时，可以这样定位：

- 🌟改已有卡片的展示、接口字段或交互 → 优先只改 robot-ui 对应 L3 目录。 
- 🌟新增消息卡片类型 → 通常改 robot-ui + chat-content；涉及共享协议再改 runtime。
- 改输入框、推荐问题、消息列表 → 优先看 chat-content。
- 改 PC / 移动端容器、宿主集成 → 优先看 platform。
改连接、底层通信协议 → 才进入 im-core。

## PC容器设计

[[快手 - 需求 - Pc 容器重构]]
[[无头样式组件库 Ant Design 组件能力对比]]

## 原子组件库设计

[[快手 - 需求 - 原子组件库从零设计]]