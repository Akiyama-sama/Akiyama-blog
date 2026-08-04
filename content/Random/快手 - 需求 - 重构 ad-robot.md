---
date: 2026-07-14
tags:
aliases:
---
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

```txt
ad-im-esp-v2/
├── packages/
│   ├── @esp/ui/              # 原子 UI 包（独立发包，设计团队消费）
│   │   └── src/              # Popover / Tooltip / MarkdownRenderer / BaseCard / BubbleCard ...
│   │
│   ├── @esp/core/            # 核心框架包（独立发包）
│   │   └── src/
│   │       ├── components/
│   │       │   ├── shared/   # 跨卡片复用业务组件（AiFooter / GuessAskBubble / TimeStamp ...）
│   │       │   ├── cards/
│   │       │   │   ├── messages/   # 消息卡片 30+（每卡独立目录）
│   │       │   │   └── streaming/ # 流式卡片 15+（每卡独立目录）
│   │       │   └── MessageList / InputInfo / JinGangCard ...  # 页面级业务组件
│   │       ├── store/        # GlobalStore / SessionStore / StreamingStore / RuntimeStore
│   │       ├── eventbus/     # EspEventBus
│   │       ├── streaming/    # 流式引擎核心
│   │       ├── registry.ts   # CardRegistry（lazy import 同包 cards/）
│   │       ├── service/      # 统一请求层
│   │       ├── types / utils / hooks / config / mock
│   │
│   ├── @esp/pc/              # PC 端入口包（独立发包）
│   │   └── src/
│   │       ├── container/    # 侧边栏/展开窗口/拖拽
│   │       ├── history/      # 历史会话面板
│   │       ├── components/   # Avatar / ReachMGT / NPSSurvey / Welcome
│   │       └── entry/        # PcRobotEntry
│   │
│   └── @esp/mobile/          # Mobile 端入口包（独立发包）
│       └── src/
│           ├── container/    # 全屏/抽屉
│           ├── history/      # 历史会话抽屉
│           ├── components/   # Avatar / Welcome
│           └── entry/        # MobileRobotEntry
│
├── pnpm-workspace.yaml       # 四个包，workspace:* 关联
├── turbo.json                # build: ^build 拓扑排序
└── tsconfig.base.json

依赖方向：@esp/ui ← @esp/core ← @esp/pc / @esp/mobile，严格单向。
```

## PC容器设计

[[快手 - 需求 - Pc 容器重构]]
[[无头样式组件库 Ant Design 组件能力对比]]

## 原子组件库设计

[[快手 - 需求 - 原子组件库从零设计]]