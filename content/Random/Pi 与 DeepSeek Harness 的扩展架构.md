---
date: 2026-10-16
tags:
aliases:
---
# Pi 与 DeepSeek Harness（dsh）的扩展架构对比

> 调研时间：2026-10-16。两个项目都以本机 checkout 的源码 + 官方文档为准（非二手博客转述）：
> - **pi** = [`badlogic/pi-mono`](https://github.com/badlogic/pi-mono)（现 `earendil-works/pi`，Mario Zechner 的 "shitty coding agent"），本机 `~/Develop/github/pi-mono`，HEAD `4954d76`（2026-10-15）。MIT · TypeScript · 约 11.6 万 stars。
> - **dsh** = [`deepseek-ai/deepseek-harness`](https://github.com/deepseek-ai/deepseek-harness)（"DeepSeek Harness: Everything is a Plugin."），本机 `/tmp` 一次性 checkout，HEAD `86a40220`（v0.2.1-alpha.4，2026-10-15）。MIT · TypeScript · 约 25 万 stars。底层框架是 [Cordis](https://github.com/cordiverse/cordis)。
> 本文只谈**扩展架构**（怎么在不改核心的前提下加东西），provider/协议归一化那套见 [[Pi-mono 是如何处理 provider 或者 api 的各个接口的差异并进行归一化处理的]]；harness 概念本身见 [[构建自己的 Agent]]、[[Agent Harness 评测]]。

---

## 这篇文档解决什么问题

同样是 agent harness，pi 和 dsh 都对外喊"我 Everything-is-a-plugin"，但两者"什么算核心、什么算扩展"的切法完全不同。写扩展、移植工作流、或者自己造 harness 时，最先要回答的三个问题它们给的答案都不一样：

1. **扩展附着在哪一层？**——是挂在一条固定循环的几个 hook 上，还是循环本身就是个可替换的插件。
2. **用配置还是用代码来扩展？**——是写一个 TS 文件导出工厂函数，还是往一棵 YAML 组合树里加一层 patch。
3. **扩展会不会互相踩？**——扩展之间怎么通信、副作用怎么在卸载时干净回收。

这篇把两家的扩展面拆开对齐，最后给一张概念对照表和一段"只记一句话"的总结。

---

## 一句话总览

> **pi 是「一个不可变的小内核 + 一圈事件 hook 与注册表」**：agent loop 是硬编码的 `while(true)`，扩展通过工厂函数拿到 `ExtensionAPI`，用 `pi.on()` 订阅生命周期事件、用 `pi.registerTool/Command/Provider/McpServer()` 往注册表里塞东西。核心永远在那儿，扩展只是环绕它。
>
> **dsh 是「一整棵可组装的插件树，内核本身也是插件」**：没有一个叫"核心"的固定对象。运行中的 dsh 是 profile → bundle → patch 逐层叠加出来的配置树，连 agent loop（`ctx.agentLoop`）、工具注册表（`ctx.tools`）、会话日志（`ctx.sessions`）、模型适配器都是同一个 Cordis 框架上的插件，每一个都能被上层 patch 整条替换掉。

一张图先建立心智：

```text
pi:                              dsh:

  ┌───────────────────┐            你的 patch (最高层)
  │  extensions (TS)  │ 环绕       ┌───────────────────┐
  │  on() / register* │──注册──▶   │ profile.patch.yml │
  └───────┬───────────┘            ├───────────────────┤
          │ 订阅/注入               │  bundle A / B / C │  ← 每个都是插件
  ┌───────▼───────────┐            ├───────────────────┤
  │  AgentSession     │            │  dsh-base         │  ← 共享第一层
  │  (固定 agent loop)│            ├───────────────────┤
  ├───────────────────┤            │  agentLoop 插件    │  ← "内核"也是插件
  │  pi-agent-core    │            │  tools   插件      │     可被整条替换
  ├───────────────────┤            │  session 插件      │
  │  pi-ai (LLM API)  │            │  llm     插件      │
  └───────────────────┘            └───────────────────┘
   固定分层，扩展只在最外圈          同构：任何东西都是同一层的插件
```

关键差别一句话：**pi 的扩展是"往一个既定形状上贴东西"，dsh 的扩展是"重新组装这棵树本身"**。下面分别展开。

---

## 一、pi 的扩展架构

### 1.1 分层：三层包，扩展只发生在最外层

pi 是 monorepo，扩展架构建立在三个各司其职的包之上：

| 包                                | 职责                                                                                        | 与扩展的关系             |
| -------------------------------- | ----------------------------------------------------------------------------------------- | ------------------ |
| `pi-ai`（`@earendil-works/pi-ai`） | 统一多 provider LLM API：`createModels()` + provider 工厂 + `streamSimple/completeSimple` 归一化入口 | 自定义 provider 在这里落地 |
| `pi-agent-core`                  | 有状态 `Agent` 类：agent loop、工具执行、事件流、`convertToLlm`/`transformContext` 等钩子                   | 想造自己的 harness 直接用它 |
| `pi-coding-agent`                | CLI/产品：session、TUI、**extensions 运行时**、skills、templates、themes、packages                    | 用户扩展的主战场           |

和 dsh 的根本区别从这里开始：**agent loop 是硬编码的**。`packages/agent` 的 README 展示的 `Agent` 类就是那个固定内核——订阅事件、`prompt()`、循环执行工具。pi 官方文档的定位（`coding-agent/README.md:15-19`）：

> Pi is a minimal, extensible agent harness that you can make your own. … Pi ships with powerful defaults but **skips features like sub-agents and plan mode**. Ask Pi to build what you want, or install a package that does it your way.

内置连 subagent 和 plan mode 都不给，但仓库 `examples/extensions/` 里就摆着 `subagent/`、`plan-mode/`、`sandbox/`、`gondolin/`（VM）这些例子——**官方用"不内置、给你自己写"来表达极简立场**，扩展面就是产品面。

### 1.2 一个扩展是什么：工厂函数 + `ExtensionAPI`

最小扩展（`docs/extensions.md:19-29`）：

```typescript
import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";

export default function (pi: ExtensionAPI) {
  pi.registerCommand("hello", {
    description: "Show a greeting",
    handler: async (name, ctx) => {
      ctx.ui.notify(`Hello, ${name || "world"}!`, "info");
    },
  });
}
```

- **默认导出一个工厂**，接收 `ExtensionAPI`，在工厂里注册能力。工厂可异步——pi 会等它完成才继续启动（以便注册 startup 阶段需要的 provider）。
- **`jiti` 运行时加载 TS**，零编译步骤；小扩展一个 `.ts` 文件即可，多文件放目录（`index.ts` 入口），npm 依赖放旁边的 `package.json`。
- **加载位置**：用户级 `~/.pi/agent/extensions/` 或项目级 `.pi/extensions/`，外加 `--extension ./hello.ts` 显式加载。
- **信任模型**：扩展在 Pi 进程内运行、拥有全部 OS 权限，"只加载你信任的来源"；**project trust 先于项目扩展解决**，且只有个人扩展和命令行显式扩展能参与 `project_trust` 事件。
- **生命周期纪律**：工厂里不许起进程/socket/watcher/timer（有的调用只加载扩展不开会话）；长寿命资源从 `session_start` 起，在幂等的 `session_shutdown` 里释放。reload 会**替换整个扩展运行时**——没有"卸载单个插件撤销其副作用"的机制，这点和 dsh 的 `ctx.effect` disposer 文化正好相反。

### 1.3 `ExtensionAPI` 方法总表（源码 `types.ts:1592+`）

官方文档给的"选择哪个集成点"表（`docs/extensions.md:74-87`）+ types.ts 核对后补全：

| 能力 | API |
|---|---|
| 观察/改写生命周期 | `pi.on(event, handler)`（返回 unsubscribe 函数） |
| 加模型可调用工具 | `pi.registerTool()` |
| 加 `/命令` | `pi.registerCommand()` |
| 加快捷键 / CLI flag | `pi.registerShortcut()` / `pi.registerFlag()` |
| 注入用户/自定义消息 | `pi.sendUserMessage()` / `pi.sendMessage()` |
| 持久化非上下文会话数据 | `pi.appendEntry()` |
| 换活跃工具集/模型/思考等级 | `pi.getActiveTools()` / `setActiveTools()` / session 控制方法 |
| 加模型 provider | `pi.registerProvider()`（`ProviderConfig` 配置式或原生 `Provider` 对象；`unregisterProvider`） |
| 加虚拟模型（按请求路由） | `pi.registerVirtualModel()` / `unregisterVirtualModel()` |
| 接 MCP server | `pi.registerMcpServer()` / `unregisterMcpServer()` / `getMcpServers()`（`mcp.json` 同名优先） |
| 改渲染 | `registerToolRenderer()` / `registerMessageRenderer()` / `registerEntryRenderer()` |
| 扩展间通信 | `pi.events`（进程内 EventBus） |
| 终端 UI | `ctx.ui`（notify/confirm/select/dialog/custom 组件、状态栏、标题、编辑器） |

### 1.4 生命周期事件：三十多个，observe / transform / cancel 三种语义

事件名直接从 `types.ts` 的 `on()` 重载枚举（以文档声明的返回类型区分效果——**有的只通知，有的能改写数据、替换结果或取消操作**）：

```text
发现与信任    project_trust | resources_discover
会话         session_start | session_info_changed | session_tree | session_shutdown
             session_compact | session_compact_failed | mcp_servers_change
             session_before_switch/_fork/_tree/_compact（可取消的会话操作前闸）
上下文改写    context | context_with_system            （transform：返回新消息列表）
provider     before_provider_request | before_provider_headers | after_provider_response
             provider_stream_event                     （通知：归一化前逐帧观察）
运行         before_agent_start（可注入 message / 换 systemPrompt）
             agent_start | agent_end
             agent_before_settle（最后可行动边界：追加条目、要求续跑一次）
             agent_settled（终局，仅通知）
轮次/消息    turn_start | turn_end | message_start | message_update | message_end
工具         tool_call（改 input / block: true 拦截）→ tool_execution_start/update/end
             → tool_result（可组合改写，每个 handler 看到前面的改动）
输入         input | user_bash（handler 返回 operations/result 即接管本地执行）
选择         model_select | thinking_level_select
缓存         cache_warming_decision（最后一个返回 action 的胜出：warm / stop）
UI           ui_prompt_start | ui_prompt_end
```

几个值得注意的设计：

- **`agent_before_settle` / `agent_settled`** 显式定义了"agent 还会不会自己继续"的边界——续跑只能由 actionable boundary 提议一次，防循环由作者负责（`turn_end` / `agent_before_settle` 可返回 `continue: true`）。
- **`provider_stream_event`** 暴露归一化*之前*的原始流事件，只读、不持久化——这是给调试和旁路分析留的缝。
- **`tool_call` handler 抛异常 = 阻断工具**（fail-safe），而工具本身执行失败只是给模型一个 error result——两种失败的处理路径是分开的。

### 1.5 工具模型：exposure 是 pi 最有特色的一块

`registerTool`：名字 + 面向模型的 description + **TypeBox** 参数 schema + `execute()`；结果要求模型可见 `content` 加 `details`（渲染/状态重建用），可选 `outputSchema` + `structuredContent`（给 codemode 脚本等程序化调用方，模型仍只拿文本）。

**`exposure` 五种曝光档**（`docs/extensions.md:153-165`）——控制模型怎么"够到"一个工具：

| 档 | 声明给模型? | 可被代码调? | 用途 |
|---|---|---|---|
| `direct`（默认） | 活跃时 | 是 | 普通工具 |
| `model-only` | 活跃时 | 否 | 编排类/问用户类工具 |
| `codemode` | 默认不声明 | 注册即可被脚本调 | 给 codemode 工作流当 API |
| `deferred` | 不声明 | 脚本可调但不列出 | 靠 `tool_search` 发现再激活 |
| `hidden` | 否 | 否 | 撤回工具的手段（工具不可注销，只能隐藏） |

配套三件套：**`namespace`**（像 MCP server 那样分组工具）、**`annotations`**（MCP 式 `readOnlyHint`/`destructiveHint`/`openWorldHint` 提示，权限扩展靠它决定要不要弹确认）、**`reachesTools(input)`**（声明一次调用可能够到哪些工具，让"晚注册"的 MCP 扩展能在调用前补注册）。编排型工具还能用 **`prepareLoadout`** 在活跃期间改写模型看到的工具声明（codemode 自身就只靠这个 hook 实现——**内置功能和扩展功能用的是同一套 API**，这是"核心无特权"在 pi 里的弱化版体现）。

嵌套调用 `ctx.executeTool()` 完整重走 `tool_call`/`tool_result` 拦截链，产生 `<parent>/<n>` 形式的内部 id、不进 transcript、usage 逐层上卷——这套约束的细致程度说明 pi 把"工具即 API"当成第一公民在维护。

### 1.6 状态与持久化：按"参与对话的方式"选存储

官方四档（`docs/extensions.md:228-240`）：

| 状态 | 存法 |
|---|---|
| 跟随活跃分支的工具状态 | 工具结果里的 `details` |
| 持久但不进模型上下文 | `pi.appendEntry()` |
| 要存、也要发给模型 | `pi.sendMessage()`（自定义消息类型） |
| 跨会话 | 外部存储 |

session 是 JSONL 文件里的**树**（每条 entry 指向 parent，活跃分支供给模型历史），所以分支敏感状态要在 `session_start` 从 `ctx.sessionManager.getBranch()` 重建——**不许**扫全部条目，因为废弃分支是替代历史。

### 1.7 扩展的四种资源形态 + 分发

"往 pi 里加东西"按需求分四类，官方文档边界划得很清：

| 形态 | 是什么 | 什么时候用 |
|---|---|---|
| **Extension** | TS 模块，进程内可执行代码 | 需要工具/命令/handler/provider/UI 等**可执行行为** |
| **Skill** | 目录 + `SKILL.md`（Agent Skills 规范）：名字+描述进系统提示，全文**按需加载** | 只需要**指令和附属文件**，不需要新执行点 |
| **Prompt template** | 可复用消息文本，编辑输入时展开 | 复用提示词 |
| **Theme** | 终端配色 | 外观 |
| **Pi package** | npm/git/本地目录，`pi install npm:@example/pi-tools`，把上面四类捆成一件分发 | 共享与安装 |

MCP 则处在特殊位置：注册入口是 `pi.registerMcpServer`（`mcp.json` 是配置入口），实现拆在兄弟包 `@earendil-works/pi-mcp` 里；文档还允许"别的 MCP 扩展"接管连接（读 `pi.getMcpServers()` + 处理 `mcp_servers_change`）——注册 API 与具体实现解耦，内置实现并不占特权位，这一点倒是有几分 dsh 的味道。同理 `codemode` 也是独立包（`pi-codemode`，依赖 `quickjs-wasi` 跑沙箱脚本）。

### 1.8 宿主形态即扩展面

同一个 agent/session 机制暴露成五种界面：interactive TUI、print、JSON（事件流 JSONL）、**RPC**（stdin/stdout JSONL 命令，扩展 UI 可经 RPC Extension UI 协议转发到前端）、**TypeScript SDK**（进程内创建控制 session）。扩展在所有模式加载，`ctx.mode === "tui"` 守卫终端专属行为、`ctx.hasUI` 判断交互能力——**写一次扩展，五种宿主都能跑**，前提是别把渲染逻辑混进工具逻辑。

---

## 二、dsh（DeepSeek Harness）的扩展架构

### 2.0 底层框架 Cordis：五个概念

dsh 的一切扩展语义都来自 Cordis（以 `@deepseek-ai/cordis` 的 alias vendored 进仓库，论文 *A Programming Paradigm for Spatiotemporal Composability*，arXiv:2608.25512）。作者必须先懂这五个原语（`docs/cordis-primer.zh.md:7-23`）：

- **插件 = 实现 Service 的对象**：一个带可选 `inject` 和 `apply(ctx)` 字段的函数，或一个 `Service` 子类（生命周期由框架接管），或 `{id, base, config?}`。`apply(ctx)` 必须同步，异步工作放 `ctx.effect`。
- **上下文 = 服务容器**：每个服务占一个稳定 `ctx.<key>`（`ctx.tools`、`ctx.llm`、`ctx.sessions`…）。插件按 key 找服务，不 import 具体实现。
- **`inject` 声明依赖**：插件声明所需服务后才启动——加载顺序由依赖图表达，不靠手写启动序列。
- **类型化事件 = 通信**：通过 TS 声明合并（`declare module`）注册事件名，按 `emit`/`waterfall`/`parallel`/`serial`/`bail` 五种模式分发。
- **注册 = 可逆副作用**：提示词片段、工具 schema、适配器、监听器都经 `ctx.effect()` / `ctx.on()` 安装，**reload 和 teardown 时自动撤销**。这是"没有特权内核"的机制基础——dsh 明说"注册是临时性的、卸载时被丢弃"。

五种分发模式（`cordis-primer.zh.md:27-35`），是理解 dsh 事件语义的关键：

| 模式 | await? | 顺序 | 返回值 | 语义 |
|---|---|---|---|---|
| `emit` | 否 | 注册序观察 | 否 | 纯通知 |
| `waterfall` | 否 | 注册序，须调 `next()` | 是 | 环绕中间件（改请求/决策对象） |
| `parallel` | 是 | 全部并行 | 否 | 扇出观察 |
| `serial` | 是 | 注册序 | 是 | 按序执行 |
| `bail` | 否 | 注册序，遇首个 bail 停 | 是 | 短路（首个决策胜出） |

实践规则（`cordis-primer.zh.md:50-51`）：**拦截与策略优先用事件，直接能力调用优先用服务方法**。工具流水线事件属于 `ctx.tools`、模型流式属于 `ctx.llm`、实时 agent 协调属于 `ctx.agents`。

### 2.1 "Everything is a plugin" —— 没有特权内核

`docs/architecture.zh.md:9-11` 的原话：

> 产品的每一部分都是插件，包括模型适配器、工具注册表、会话日志，以及 agent loop 本身，因此每个都可以从配置替换。
> **不存在需要打补丁的特权内核**：扩展 dsh 的方式是把插件挂载到其他插件旁边，而各项注册都是副作用，会在其插件卸载时撤销。

对照 pi：pi 的 agent loop（`Agent` / `AgentLoop` 类）是**不可替换的核心**，扩展只能 hook 它；dsh 的 `ctx.agentLoop` 是**一个插件**，默认实现叫 `dsh-agent-loop`，换掉它等于换掉整个产品的"思考方式"，而且不需要 fork 仓库。这是两家最根本的分野。

### 2.2 装配树：profile → bundle → patch

运行中的 dsh 是一棵插件树，由启动时**按序叠加**的几层组成（`architecture.zh.md:14-39`）：

- **profile**：Harness home 里的具名组装。列出它叠放的 bundle、存放树外插件、保存用户自己的 `cordis.patch.yml`。发行版随附模板：`web` / `headless` / `sdk` / `sdk-minimal` / `acp`（`plugin` 是管理命令，不是运行 profile）。
- **bundle（组合包）**：Cordis 配置项 + 挂载代码的**分发格式**。`dsh-base`（`packages/bundle/base`）是 web/headless/sdk/acp 的共享第一层——模型适配器、工具、持久化、沙箱、审批策略、设置、凭据、遥测。`dsh-web-app` 加浏览器应用，`dsh-headless` 加一次性 runner，`dsh-sdk-app` 加 JSON-RPC server，`dsh-acp-app` 加 ACP server。`dsh-sdk-minimal` 是刻意例外（自带完整显式树，不叠 `dsh-base`）。
- 两者都在各自 `package.json` 的 `dsh` 字段声明：`dsh.profile` 列出组合包，`dsh.bundle` 指向 patch 文件。

**叠加顺序**（每层应用在空条目列表之上，`architecture.zh.md:25`）：

```text
profile 的有序 bundle 列表 → bundle 自带 patch → profile 自己的 cordis.patch.yml
   → home patch → --patch overlay（单次启动，最高）
```

一条 patch 按 `id` 定位条目并**替换其整个 config**，或插入新条目。`--patch` 是只对本次启动生效的最高优先级 overlay，值可以是文件路径或 YAML 字符串。想看自己机器实际启动的树，`dsh --profile web --dump-config`——**它打印的任何条目都能被你的一条 patch 替换**，这是 dsh 扩展性的核心承诺。

> 这跟 pi 的扩展加载模型形成强对比：pi 没有"多层可覆盖的配置树"这回事，扩展是文件/目录被直接 import 进进程；dsh 的一切都由可寻址、可覆盖的声明式条目构成。

### 2.3 能力 seam：Definition / Provider / Consumer 三件套

dsh 最核心的抽象是 **seam（能力接缝）**——一个可替换能力，恰好三个角色（`docs/capability-seams.zh.md`）：

- **Service Definition**：只描述契约的命名 kind——`Service.define(id, impl, config?, events?, [symbol])`，第 3/4/5 参可选（schema / 事件声明 / realm symbol）。
- **Service Provider**：往 `ctx[key]` 上贡献一个实现——可以是整个服务子类、`ctx.provide(definition, value)`，或仅贡献一段方法切片。
- **Consumer**：用它的通常是面向模型的 tool 或其它服务。

> **seam 正是"替换一个提供方就能改变整个产品"的原因**（`architecture.zh.md:136-138`）。文件系统与进程提供方共享同一个执行世界：把它们指向远程沙箱，Bash、PTY、LSP 就一起搬过去了，**不需要 per-provider 的 fork**。subagent 提供方同理——同一个接口背后，从"新建一个子 agent"到"把轮次委派给另一个产品"。

`fs` 和 `process` 是**两个共享的根 seam**（`capability-seams.zh.md:72-77`），几乎所有 model-facing tool 都经由它们，因此换一个根提供方就重定向整条执行链。加一项能力 = 三件套一起设计，只给一个角色不算 seam。

核心 seam 一览（`architecture.zh.md:55-66` + 附录 A）：

| `ctx` 键 | 角色 |
|---|---|
| `ctx.llm` | 消息/流式词汇表 + provider 适配器注册表（`registerProvider`/`stream`） |
| `ctx.tools` | 作用域化工具注册表 + 带把关的执行流水线（`pre-execute`/`execute`/`post-execute` 三个 waterfall） |
| `ctx.sessions` | 仅追加 `SessionEvent` 日志 + 内存存储 |
| `ctx.systemPrompt` | 提示词片段与工具 schema 组装 |
| `ctx.agents` | `Agent` 接口 + 活跃 agent 注册表 + `agent/*` 事件 |
| `ctx.agentLoop` | 实现 `Agent` 接口的默认驱动器（**本身是插件**） |
| `ctx.fs` / `ctx.process` | 两个共享根能力（沙箱/SSH 靠替换它们） |
| `ctx.sandbox` / `ctx.credentials` / `ctx.mcp` / `ctx.skills` / `ctx.commands` / `ctx.jobs` … | 各自的策略/适配 seam |

### 2.4 三个事件域 + 轮次流程

`architecture.zh.md:70-79`：**事件就是扩展点，选对事件域是大多数改动的第一个决定**。

- **会话事件**（`turn/*` `step/*` `system/message` `user/message` `assistant/message` `tool/*`）：追加进日志、经 `session/event` 广播的**持久事实**。需要"reload 后仍存在"就用它。
- **Agent 事件**（`agent/*`）：带活跃 `Agent` 的**实时**协调——inbox、步骤、状态、请求、验证、续跑。要观察/拦截进行中的工作用它。
- **能力事件**（`fs/*` `tools/*` `telemetry/*`）：无需 import 循环就能往某个 seam 附策略/适配器。

轮次（turn）= 零个或多个步骤（step，一次模型请求 + 它调的工具）。`turn/start` 在领取首条输入前打开，在不再欠工作时关闭。核心瀑布链（`architecture.zh.md:87-108`）：

```text
agent/pre-step → agent/request (prepareCall) → llm/stream → tools/pre-execute → tools/execute → tools/post-execute
```

`agent/pre-step`（决定接纳哪些输入、可改写或拒绝领取的消息）、`agent/request`、`llm/stream`、三个 `tools/*` 都是 **waterfall**（监听器必须调 `next()` 才委托下去），`agent/turn-stopping` 是 **serial**。

### 2.5 "新行为放哪"的官方路由表

`architecture.zh.md:142-167`——dsh 直接给了一张"你想干什么 → 用什么机制"的表，这是它扩展架构最好用的入口（节选）：

| 目标 | 机制 |
|---|---|
| 添加模型提供方 | 在 `ctx.llm` 上注册适配器 |
| 添加面向模型的能力 | 在 `ctx.tools` 上注册（schema 自动进提示词组装） |
| 让某会话有不同能力集合 | 组装一个 agent preset（服务行需 `isolate` realm） |
| 添加 shell / 持久终端执行 | 注册 `ctx.shell` / `ctx.terminals` 后端 |
| 添加用户命令 | 在 `ctx.commands` 注册（无需模型轮次即可分派） |
| 管理后台任务 | 在 `ctx.jobs` 注册，`job_*` 工具读写 |
| 添加文件系统访问/策略 | 注册 `ctx.fs` 提供方，或监听 `fs/*` |
| 限制启动的进程 | 用 `ctx.sandbox` 后端，消费方启动前包 argv |
| 拦截请求/工具/轮次 | 用对应 `agent/*` 或 `tools/*` 事件 |
| 添加模型可见上下文 | `agent.inject()`（落到下一次获准请求） |
| 添加 Web Client Chat 节点 | 注册 `ConversationNodeDefinition` + keyed renderer |
| 在新后端存会话 | 实现 `SessionPersistence`（`create`/`open`/`stat`/`list`/`export`） |

### 2.6 会话日志 = 单一事实源："模型可见即已记录"

`architecture.zh.md:122-130`：会话日志是"模型所见上下文"的来源，`deriveMessages()` 从中投影模型历史。**每个模型请求都必须能从日志重建；新增模型可见输入需要一条会话事件**。改现有消息内容不能直接改，要注册**纯消息投影**（plugin-owned message projection，`dsh-session-projection` 提供 `ctx.sessionProjections`）。这条不变式让"插件往上下文里注入东西"变得可审计、可回放、可 fork——和 pi 用 `appendEntry` / `context` 事件直接改上下文的做法在约束强度上是两个量级。

### 2.7 怎么真写一个 dsh 插件

一个真实插件的形状（`packages/goal/tool-goal/src/index.ts`，dsh 官方 `tool-goal` 包）——**模块顶层直接导出这几个字段**，Cordis 按约定挂载，没有 `definePlugin()` 包装：

```ts
export const name = "tool-goal"
export const inject = ["agents", "goals", "tools", "systemPrompt", "sessionProjections"]

export const Config = z.object({ /* schemastery schema，可被 profile/home/--patch 覆盖 */ })

export function apply(ctx: Context, config: Config): void {
  // 注册即副作用；需要撤销的用 ctx.effect()/ctx.on()
  ctx.systemPrompt.section({ name: "tool:goal", order: ..., text: guidance(...) })

  ctx.tools.register(defineTool({
    name: "get_goal",
    description: GET_DESCRIPTION,
    parameters: {},                 // 参数 schema
    output: GOAL_OUTPUT,
    execute(_args, exec) { ... },   // 三阶段流水线的执行段
  }))
}
```

要点：
1. 插件顶层导出 `name`、`inject`（按 key 声明所需服务，不 import 提供方实现）、可选 `Config`（schemastery schema，可被 profile/home/`--patch` 覆盖）、`apply(ctx, config)`。`apply` 同步，异步资源放 `ctx.effect`。
2. 加一个面向模型的工具用 `defineTool`（`@deepseek-ai/dsh-tools`，即 `packages/core/tools` 里 `Service.define` 的封装：`prepare / checkPermission / execute` 三段），注册进 `ctx.tools`；schema 由 `ctx.systemPrompt` 自动组装进提示词。
3. 加一个 provider override 用 `ctx.effect` generator，**yield 一个 disposer**，teardown/reload 自动撤销：

```ts
ctx.effect(function* () {
  const prev = this.tools.get("read")
  this.tools.update({ ...prev, tool: myTool })
  yield () => { this.tools.update(prev) }   // 卸载时自动恢复
})
```

4. 外部插件不用改源码：`dsh plugin install <registry|github:owner/repo|git URL|file:|link:>` 装进 profile，`dsh plugin search` 走 GitHub `dsh-plugin` topic。

### 2.8 一切按 agent 作用域：realm 与 preset

dsh 一个容易忽略但架构含义很重的点：**它几乎没有全局单例，ctx 就是 per-agent realm**（`architecture.zh.md:148-151`、`capability-seams.zh.md:59-67`）。同一个 `ctx.tools` key，在两个 agent 上解析到各自 realm 里各自的提供方：

- **realm 三档**：`world`（默认，落到宿主共享服务）/ `shared` / `isolate`（本 agent 私有实例）。
- **agent preset**：一个具名插件束，用 `ctx.presets.create({ preset: "dsh:plan" })` 创建 agent 即得到一套不同的能力集合——"让某个会话拥有不同的能力"不靠改全局配置，靠组装 preset。
- **scope 原语**（`dsh-scope`）：`ctx.scoped("tools")` 之类给服务加一个作用域层（每 scope 独立 provider 解析与事件）。

效果是：同一进程里可以同时跑"带全套工具的 Creator"和"只有只读工具的 Plan 会话"，互不污染。pi 对应机制弱一档：工具激活是 session 级（`setActiveTools`），但 `ctx.fs` 之类 OS 权限是进程级共享的。

### 2.9 skills / MCP / subagent 在 dsh 里的位置

- **Skill**：`ctx.skills`（`skills` 服务）扫三层根（用户级 / workspace / bundle 自带），SKILL.md frontmatter + `context: fork|inline`；模型面两个工具 `use_skill`/`skill`。**只给指令，不授予能力**（`subsystems/skills.zh.md:32`）。
- **MCP**：`ctx.mcp` seam 三段（provider/transport/auth），`dsh-mcp` 工具经 `ctx.tools.register` 注册，同样吃 `pre-execute` 权限闸；`claude_code_mods` 子系统能直接读 Claude Code 的 `.claude` 目录。
- **Subagent**：`ctx.subagents` provider + `agent/*` 事件 + 会话树 + `task` 工具，外加实验性 `ctx.agentTeams`（durable roster + 直接 inbox 消息）。dsh 把 subagent 当一等 seam——pi 则把它留作"你自己写"的扩展示例。

### 2.10 加行为有三条路，都不改源码

dsh 官方总结（`subsystems/extensions.zh.md:59-64`）：

1. **Patch（替换连线）**：`dsh --dump-config` 看真实树 → 按 `id` 换模块 ref 或覆盖 config。适合改变核心组装。
2. **Event（附策略）**：订阅能力事件（`tools/pre-execute`、`fs/*`、`llm/*`），不替换实现只包装行为。
3. **Provider（重定向能力）**：把整个能力（文件系统、持久化、LLM 路由、审批）指向新后端；沙箱和 SSH 就是两个完整的 provider-swap 例子。

外加 discovery 自动扫描（`@deepseek-ai/dsh-module-graph`，构建期生成包图与 id 注册表）和 `dsh plugin` 外部安装。

---

## 三、两者异同

### 3.1 相同点

- **都不把扩展当二等公民**：两家的第一性卖点都是"你可以不 fork 源码就把产品改造成你要的样子"，而且都真的做到了"agent loop 之外的一切都能换"。
- **都区分"指令"和"可执行行为"**：两家都同时有 *skills*（按需加载的指令文本 + 附属文件，不进模型上下文的常驻部分）和 *工具/插件*（真正可执行代码），都不把 skill 当安全边界。
- **都用"注册表 + 生命周期事件"作为核心扩展动词**：pi 的 `pi.on(...)` / `pi.registerTool(...)` 与 dsh 的 `ctx.on(...)` / `ctx.tools.register(...)` 是同一个母题——观察者/改写者订阅一条流水线，注册表承接能力。
- **都把工具执行建成一条可拦截的流水线**：pi 的 `tool_call`(可改 input / 可 block) → `tool_result`(可改/遮蔽) 与 dsh 的 `tools/pre-execute → execute → post-execute` 三段瀑布，都要求嵌套调用重新过一遍拦截，都是 fail-safe（处理器抛异常默认阻断）。
- **都把 provider 当扩展点**：两家都能在不改核心的前提下注册自定义模型 provider（pi 的 `pi.registerProvider`/`registerNativeProvider`，dsh 的 `ctx.llm.registerProvider` + 一个 40 行的 `dsh-llm-adapter`）。

### 3.2 不同点

| 维度 | **pi** | **dsh** |
|---|---|---|
| 内核 | **有固定小内核**：`Agent`/`AgentLoop` 硬编码 `while(true)`，扩展环绕它 | **无特权内核**：agent loop 本身是 `ctx.agentLoop` 插件，可整条替换 |
| 扩展附着方式 | 工厂函数拿 `ExtensionAPI`，命令式 `.on()/.register*()` | 插件树声明式叠加（profile/bundle/patch），服务按 `ctx.<key>` 寻址 |
| 主要表达载体 | TypeScript 文件（`jiti` 运行时加载，免编译） | YAML 配置树 + TypeScript 插件（顶层导出 `apply` / `defineTool`） |
| 装配/覆盖模型 | 单层：按目录/flag 加载，无覆盖层 | 多层可覆盖：patch 按 id 替换整条 config，`--patch` 最高，`--dump-config` 可检视 |
| 事件语义 | `pi.on(event)`，按声明顺序；observe / transform / cancel 靠返回类型区分 | 五种显式分发模式（emit/waterfall/parallel/serial/bail），waterfall 需 `next()` |
| 上下文一致性约束 | `context` 事件可临时改上下文，较松散 | **强不变式**："模型可见即已记录"，改消息必须注册纯投影 |
| 可逆性 | 需自己在 `session_shutdown` 里清理（reload 会替换整个运行时） | **可逆副作用是一等公民**：`ctx.effect`/`ctx.on` 注册自动在 teardown 撤销 |
| 能力替换粒度 | 加/换 hook、工具、provider | 换一个**根 seam 提供方**（`fs`/`process`）就把整条执行链搬进沙箱 |
| 复杂度/上手 | 心智负担小：一个文件一个工厂函数即可 | 心智负担大：要先理解 Cordis + 服务/提供方/消费者 + profile 树 |
| 成熟度 | 稳定主线（clone 为 v1.3.0，2026-10-15，作者长期高频维护） | developer preview（v0.2.1-alpha.4，**明确宣告会破坏兼容**） |

**一句话概括这个差异**：pi 的抽象是 **"core + hooks"**（一个聪明的小内核，外面挂一圈可拆卸的插件），dsh 的抽象是 **"composable substrate"**（没有内核，只有一棵按声明组装、任何零件都可替换的服务依赖树）。pi 优化的是**作者上手速度**——想加个功能，写个 `.ts` 导出工厂就完事；dsh 优化的是**架构可替换性**——想换沙箱、换持久化后端、甚至换整个 agent 循环，都在配置层表达，不碰代码。

### 3.3 三组"同题不同解"，最能看出取舍

**① 卸载/热重载后的世界。** dsh 把"注册 = 可逆副作用"写进框架宪法：每个注册带 disposer，teardown/reload 自动撤销，HMR 监视下改 YAML 即生效。pi 走的是另一个方向：reload **替换整个扩展运行时**，文档明令"reload 之后的代码不得复用旧运行时状态"，资源清理靠作者自己在 `session_shutdown` 写幂等 handler。同样是"扩展会起进程/watcher"这个问题，dsh 用机制兜底，pi 用纪律约束。

**② 多形态能力共存。** dsh 的答案是 **realm/preset**：ctx 天生 per-agent，同一进程里 Creator 和 Plan 会话各拿各的工具集与私有服务实例。pi 的答案是 **exposure**：`direct/model-only/codemode/deferred/hidden` 五档控制模型和脚本分别"够不够得到"一个工具，配合 `setActiveTools` 做 session 级激活、`prepareLoadout` 做编排工具的声明改写。dsh 切的是"**实例边界**"（谁的 ctx），pi 切的是"**可见性边界**"（谁能调用、怎么列出）——前者更适合产品内并存多种 agent 人格，后者更适合"工具太多塞不进上下文"的 codemode/tool_search 式渐进发现。

**③ 上下文完整性的承诺强度。** pi 的 `context` 事件允许扩展在请求前任意改写消息列表（用完即恢复），约束全靠扩展作者自觉。dsh 用一条日志不变式封顶：**模型可见即已记录**——任何模型可见输入必须是持久 `SessionEvent`，改写既有消息必须注册可重放的纯投影，`--dump-log`/`deriveMessages()` 保证任何请求都能从日志重建。dsh 把"可审计/可回放"做成了架构保证，这直接反映在两家的定位上：dsh 要做团队/服务器/多端同步的产品，pi 做的是个人 hackable 的 CLI。

### 3.4 什么场景选谁（或借鉴谁）

- **想快速给 agent 加私有工作流**（自定义工具、审批闸、状态栏、接某家 API）：pi 的工厂函数 + `pi.on/registerTool` 十分钟能跑通，`examples/extensions/` 里 sandbox、subagent、plan-mode 全是现成蓝本。
- **想把 harness 当基建**（同一产品里跑多种 agent 人格、换执行世界、服务端持久化、跨端同步）：dsh 的 profile/bundle/patch + seam 三件套 + per-agent realm 是为此而生的，代价是必须先学会 Cordis 的语言（五种分发模式、effect 生命周期、声明合并）。
- **自己造 harness 时的直接启示**：pi 证明"内核可以小到只有 loop + JSONL 树，其余全是 hook 与注册表"；dsh 证明"连 loop 都可以是插件，只要事件域分得足够清楚（持久事实 / 实时协调 / 能力策略三层分离）"。前者是 Claude Code 式扩展路线的极致简化版，后者是 VS Code 式"一切皆扩展"在 agent 上的重演。

---

## 附：概念对照表

| 你想做的事 | pi 的叫法 | dsh 的叫法 |
|---|---|---|
| 加一个模型可调用工具 | `pi.registerTool()`（TypeBox schema） | `defineTool()` 注册进 `ctx.tools`（z/schemastery schema） |
| 加一个 `/命令` | `pi.registerCommand()` | 注册进 `ctx.commands` |
| 加一个快捷键/CLI flag | `pi.registerShortcut()`/`registerFlag()` | （走 client/命令注册，非独立 API） |
| 加一个模型 provider | `pi.registerProvider()`/`registerNativeProvider()` | `ctx.llm.registerProvider()` + adapter 的 `stream()` |
| 拦截工具调用 | `pi.on("tool_call")` | `ctx.tools.pre-execute`（waterfall，bail=block） |
| 改工具结果 | `pi.on("tool_result")` | `ctx.tools.post-execute` |
| 在每轮前改写上下文 | `pi.on("context")` / `context_with_system` | `agent/pre-step` / `system/message` 投影 |
| 加按需指令（非可执行） | **Skill**（`ctx.skills`） | **Skill**（`ctx.skills`，SKILL.md） |
| 接入 MCP server | `pi.registerMcpServer()` | `ctx.mcp` seam（provider/transport/auth 三段） |
| 运行别的 agent | （靠 extension 自建 subagent） | `ctx.subagents` provider + `ctx.agents` 注册表 |
| 打包分发扩展 | **Pi package**（npm/git） | **bundle（组合包）** / profile（`dsh.profile`/`dsh.bundle`） |
| 持久化自定义数据 | `pi.appendEntry()`（非上下文） | 扩展 `SessionEventMap`（持久会话事件） |

---

## 最后给一个最简化的理解模型

> 如果你只记住一件事：**pi 让你"在一个既定形状上贴插件"，dsh 让你"重新组装这棵树本身"**。
> pi 的价值在于：一个足够聪明的小内核 + 一圈干净的 hook，加功能极快、心智极低。
> dsh 的价值在于：把"什么都能换"贯彻到底——连 agent loop 都是插件——代价是你要先学会它那套 Cordis 服务/事件/patch 的语言。
> 选 harness 或自己造时，本质是在问：**我要的是"扩展点环绕核心"（pi），还是"核心本身就是可扩展的装配结果"（dsh）？**

---

## 验证状态（供复现）

- ✅ pi：本机 `~/Develop/github/pi-mono` checkout 至 `4954d76`（2026-10-15）。`packages/coding-agent/docs/extensions.md` 全文精读；`how-pi-works.md`、`skills.md`、`packages.md`、`README` 首屏、`examples/extensions/` 目录、`src/core/extensions/`（`types.ts`/`loader.ts`/`runner.ts`）已核对。**`ExtensionAPI` 方法表与三十多个生命周期事件名直接枚举自 `types.ts` 的 `on()` 重载**（内置工具事件 read/write/edit/find/grep/ls、`agent_tool_start`/`method_call`/`compaction_end` 等文档提及名不在重载表内，本文以源码为准）。
- ✅ dsh：本机 `/tmp/dsh-research/dsh` 一次性 checkout（HEAD 86a40220，v0.2.1-alpha.4，2026-10-15），精读 `docs/architecture.zh.md`、`cordis-primer.zh.md`、`capability-seams.zh.md`、`subsystems/extensions.zh.md`、`tool-execution-pipeline.zh.md`、`agent-lifecycle.zh.md`、`event-producer-consumer.zh.md`、`glossary.zh.md`、`cookbook/extension-cookbook.zh.md`、`user/develop/**` 共约 16k 行；真实插件源码核对 `packages/goal/tool-goal/src/index.ts`、`packages/core/tools/src/index.ts`。Cordis 以 `vendor/cordis/` alias 到 `@deepseek-ai/cordis`。
- ✅ 仓库元数据来自 GitHub API（stars 为检索时点，dsh 25.07 万 / pi 11.56 万 / cordis 0.92 万）。
- ⚠️ 未逐一验证：两家的 SDK/RPC 编程面只核对了文档，未逐行读实现；dsh 处于 alpha，接口后续会变；dsh 轮次瀑布中 `agent/request`、`prepareCall` 的精确时序以 `agent-lifecycle.zh.md` 时序图为准。
- 检索踩坑：通用 WebSearch 对这两个项目返回的是模型综合的泛化摘要（把 dsh 说成 "LangChain 类框架"、把 pi 描述含糊），不可信；一切以 GitHub API + 本机 checkout 为准。

## 相关

- [[Pi-mono 是如何处理 provider 或者 api 的各个接口的差异并进行归一化处理的]] —— pi 的 provider/api 归一化层（本文只讲扩展面，不讲协议归一化）
- [[构建自己的 Agent]] —— agent loop 的最小实现，本文两家的"内核/循环"都建立在这个概念上
- [[Agent Harness 评测]] —— 固定模型下评测 harness 本身；pi 与 dsh 是两类可对比的 harness
- [[Agent 记忆方案]] · [[supermemory 调研]] —— 跨 harness 的记忆/对接，含各 harness 的扩展对接缝
