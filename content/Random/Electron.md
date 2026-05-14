---
date: 2026-04-30
tags:
  - '#pernamant'
  - Javascript
  - 桌面端
  - 跨端
  - Node.js
---

`Electron` 是一个用 **Web 技术构建桌面应用**的框架。它把：

- Chromium
- Node.js

打包到一起，让前端可以用：

- HTML
- CSS
- JavaScript / TypeScript
- React / Vue 等前端框架

开发 Windows、macOS、Linux 上运行的桌面应用。

一句话理解：

> Electron 就是“浏览器壳 + Node.js 能力 + 桌面应用外壳”，让前端代码不只跑在网页里，也能跑成桌面客户端。

## 为什么前端会用它

很多前端同学熟悉 Web 开发，但要做桌面端时，如果改用原生：

- Windows 要学 C# / C++
- macOS 要学 Swift / Objective-C

成本会很高。

Electron 的价值就在于：

- 前端团队能沿用已有技术栈
- 一套代码覆盖多平台
- 可以访问文件系统、系统托盘、菜单、通知、快捷键等桌面能力

所以像：

- 聊天客户端
- 笔记软件
- AI 桌面应用
- 音视频工具
- 内部效率工具

都很适合用 Electron。

## Electron 的本质架构

理解 Electron，最重要的是理解它不是一个“单进程网页”，而是一个**多进程桌面应用**。

这里可以和 [[浏览器包含哪些进程]]、[[渲染进程]] 一起看。

因为 Electron 底层基于 Chromium，所以它继承了浏览器的多进程思想；同时又额外把 Node.js 的桌面能力接进来了。

最核心的三个角色是：

1. 主进程（Main Process）
2. 渲染进程（Renderer Process）
3. 预加载脚本（Preload Script）

## 1. 主进程 Main Process

主进程相当于 Electron 应用的“后台总控”。

它主要负责：

- 应用生命周期管理
- 创建窗口
- 创建菜单、托盘
- 处理系统级能力
- 文件访问
- 原生对话框
- 与操作系统交互

典型代码一般从这里开始：

```js
const { app, BrowserWindow } = require("electron")

function createWindow() {
  const win = new BrowserWindow({
    width: 1200,
    height: 800,
  })

  win.loadURL("http://localhost:5173")
}

app.whenReady().then(createWindow)
```

这里的 `BrowserWindow` 本质上就是创建一个桌面窗口，然后在里面装一个 Chromium 页面。

你可以把主进程理解成：

- 会管应用
- 会管窗口
- 会管系统资源
- 但**不负责具体页面 UI 渲染**

## 2. 渲染进程 Renderer Process

渲染进程就是窗口里真正跑前端页面的地方。

它和浏览器里的网页环境很像，负责：

- 页面渲染
- DOM 操作
- 事件处理
- 运行前端框架代码

所以你在 Electron 里写 React/Vue 页面，本质上仍然是在一个 Chromium 的渲染进程里运行。

这里就能直接连到：

- [[渲染进程]]
- [[事件循环 Event loop]]
- [[浏览器环境下事件循环与渲染进程之间的关系]]

也就是说，Electron 里的前端页面，很多运行机制和普通网页并没有本质区别。

## 3. Preload Script 预加载脚本

这是 Electron 非常关键的一层。

它运行在：

- 页面加载前
- 但又比普通渲染进程拥有更高权限的桥接位置

你可以把它理解成：

> preload 是主进程能力和前端页面之间的一层“受控中间层”。

它最常见的职责是：

- 暴露安全的 API 给渲染进程
- 屏蔽危险的 Node 原始能力
- 做 `ipcRenderer` 的封装

例如：

```js
const { contextBridge, ipcRenderer } = require("electron")

contextBridge.exposeInMainWorld("electronAPI", {
  selectFile: () => ipcRenderer.invoke("dialog:openFile"),
})
```

这样前端页面里就可以调用：

```js
window.electronAPI.selectFile()
```

而不是直接拿到完整 Node.js 权限。

## 为什么 Electron 不建议“渲染进程直接开 Node 能力”

这是 Electron 面试最爱问的点之一。

如果你在渲染进程直接开启：

- `nodeIntegration: true`

那页面里的脚本就能直接访问：

- `fs`
- `child_process`
- `path`
- 甚至执行系统命令

如果页面里存在 XSS，攻击者就不只是能改页面，而是可能直接拿到本机能力。

这比普通 Web 的 XSS 严重得多。

所以 Electron 里更推荐：

- 关闭 `nodeIntegration`
- 开启 `contextIsolation`
- 用 preload + `contextBridge` 暴露最小必要能力

这本质上就是一种“最小授权”设计。

## IPC：进程间通信

因为主进程和渲染进程职责不同，所以它们之间必须通信。

Electron 提供的核心通信方式是 IPC（Inter-Process Communication）。

主要有两组：

- `ipcRenderer`
- `ipcMain`

常见模式有两种：

### 1. 单向通知

```js
ipcRenderer.send("channel-name", payload)
ipcMain.on("channel-name", (event, payload) => {
  console.log(payload)
})
```

### 2. 请求-响应

```js
ipcMain.handle("dialog:openFile", async () => {
  return "mock-file-path"
})
```

```js
const result = await ipcRenderer.invoke("dialog:openFile")
```

实际项目里，一般更推荐 `invoke/handle` 这种“像 RPC 一样”的写法，因为语义更清晰。

## 一个典型调用链

比如前端页面上点一个“选择文件”按钮：

1. React 页面点击按钮
2. 调用 `window.electronAPI.selectFile()`
3. preload 用 `ipcRenderer.invoke()` 发请求
4. 主进程 `ipcMain.handle()` 接收请求
5. 主进程调用系统对话框
6. 结果返回给渲染进程
7. 页面展示文件路径

这个链路就是 Electron 的核心心智模型。

## Electron 和普通 Web 的区别

### 普通 Web

- 运行在浏览器里
- 权限较受限
- 不能直接随意访问本地文件系统
- 更偏“页面应用”

### Electron

- 运行成桌面应用
- 既有 Chromium 页面渲染能力
- 又可以通过主进程调用系统能力
- 更偏“桌面客户端”

所以 Electron 本质上不是“网页加个壳那么简单”，而是：

**把 Web 页面放进桌面应用架构里，并补上系统级能力。**

## Electron 和 [[Node.js]] 的关系

Electron 不是单纯的 Node 应用，也不是单纯的浏览器页面。

可以这样看：

- 主进程更接近 `Node.js + 桌面应用控制层`
- 渲染进程更接近 `浏览器页面`
- preload 是它们之间的桥

也正因为如此，Electron 项目里经常要同时理解：

- 浏览器渲染模型
- Node.js 模块与系统 API
- 进程通信
- 安全边界

## 为什么说前端做 Electron，会特别考验“边界感”

因为 Electron 最难的不是把页面渲染出来，而是知道：

- 什么逻辑该放主进程
- 什么逻辑该放渲染进程
- 什么能力必须通过 preload 暴露
- 什么权限绝不能直接给页面

一般来说：

### 适合放主进程

- 窗口管理
- 托盘、菜单
- 本地文件操作
- 原生通知
- 系统快捷键
- 调用本机程序

### 适合放渲染进程

- 页面 UI
- 状态管理
- 表单与交互
- 前端路由
- 组件渲染

### 适合放 preload

- 白名单式桥接 API
- 对 IPC 的统一封装
- 对渲染层暴露最小权限接口

## Electron 的安全重点

Electron 的安全不是可选项，而是核心工程问题。

常见原则：

1. 不开启不必要的 Node 集成
2. 开启 `contextIsolation`
3. preload 暴露最小 API 面
4. IPC 通道做白名单和参数校验
5. 不随便加载不可信远程页面
6. 对外部输入继续防 XSS

因为普通 Web 的 XSS，影响往往在页面内；但 Electron 里如果边界没控好，XSS 可能升级成本机能力泄漏。

## 性能上要关注什么

Electron 虽然开发效率高，但也有代价：

- 安装包通常更大
- 内存占用比纯原生应用高
- 多窗口、多 WebView、多复杂页面时资源压力更明显

所以优化时要关注：

- 窗口数量
- 渲染进程数量
- 页面性能
- 是否有长期占用内存的后台任务
- 是否把重计算丢给主线程导致卡顿

这也能和 [[React性能优化]]、[[渲染进程]]、[[事件循环 Event loop]] 一起理解。

## 结合我的简历，Electron 应该怎么讲

我简历里写的是：

[[前端简历 - v1.2.0#技术栈]]

> 掌握 Electron 跨端开发及 Java/Go/Node 后端 CRUD，能够深度参与全链路协作流程。

如果面试官追问“你会 Electron，具体会什么”，比较好的回答方向不是只说：

- 我能用 Electron 起项目

而是说清楚：

- 我理解主进程、渲染进程、preload 的职责边界
- 我知道如何通过 IPC 做安全通信
- 我知道为什么不能把 Node 能力直接暴露给页面
- 我知道桌面端能力应该如何抽象给前端页面使用

如果再结合项目表达，可以讲成：

> 我把 Electron 理解成一套桌面应用架构，而不是单纯前端页面。页面渲染逻辑仍然放在渲染进程里，系统能力放在主进程，通过 preload 和 IPC 做桥接，并优先保证 `contextIsolation` 和最小权限暴露，这样功能和安全边界才不会混在一起。

## 面试版本

- Electron 是基于 Chromium 和 Node.js 的桌面应用框架，可以用前端技术开发跨平台桌面应用。
- 它的核心架构是主进程、渲染进程和 preload。
- 主进程负责窗口和系统能力，渲染进程负责页面 UI，preload 负责安全桥接。
- 主进程和渲染进程通过 IPC 通信，常用的是 `ipcMain` / `ipcRenderer`。
- 安全上通常要关闭 `nodeIntegration`、开启 `contextIsolation`，并通过 `contextBridge` 暴露最小 API。
- Electron 的难点不只是“会写页面”，而是要清楚进程边界、能力边界和安全边界。

## 一句话总结

Electron 本质上是“桌面应用外壳里的 Web 页面 + Node.js 能力桥接”。前端做 Electron，真正要掌握的不只是页面开发，而是主进程、渲染进程、preload、IPC 和安全隔离这一整套架构思维。

# reference
