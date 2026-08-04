---
date: 2026-07-07
tags:
aliases:
---

## 一、MVP 背景

原方案中希望通过 kconf 控制任务开关和 Cron 表达式，并通过 `KconfWatcher + ConfigReconciler` 将 kconf 的期望态同步到 Agenda 的运行态。但进一步确认后，kconf 当前没有稳定的 watcher 能力，无法直接监听配置变更。

如果为了实现热更新而改成接口手动触发或定时轮询，会引入额外复杂度：

- 手动接口需要额外暴露服务入口、权限和调用链路。
- 轮询会带来延迟、无效请求和状态一致性问题。
- 配置热更新不是当前最核心的验证目标。

因此第一版 MVP 先不做 kconf、不做配置热更新、不做任务开关同步，只实现最核心的定时任务能力：**基于 AgendaEngine 持久化任务状态，并能够稳定按 Cron 执行代码中注册的任务**。

## 二、MVP 目标

MVP 只验证一件事：

> 使用 Agenda 作为底层调度引擎，基于 PostgreSQL 持久化任务状态，让 Node 服务能够注册任务、启动调度、按 Cron 执行任务，并在服务重启后继续基于持久化状态运行。

### 核心目标

- 能在代码中注册一个或多个定时任务。
- 能通过 Agenda 创建持久化的 Cron job。
- 能使用 PostgreSQL 保存 job 状态。
- 服务重启后，Agenda 能从数据库恢复 job 并继续调度。
- 能输出任务开始、成功、失败等基础日志。
- Cron 第一版只支持分钟级表达式。

### 非目标

MVP 不实现以下能力：

- 不接入 kconf。
- 不支持配置热更新。
- 不实现 `KconfWatcher`。
- 不实现 `ConfigReconciler`。
- 不实现任务启停开关。
- 不做 Web 管理后台。
- 不做自定义 `skip` / `queue` / `parallel` 策略。
- 不做独立运行历史表。
- 不做复杂告警。
- 暂不封装 Watchdog 自动续锁，长任务续锁作为后续增强。

## 三、MVP 方案

### 3.1 模块范围

MVP 只实现 `AgendaEngine` 一个核心模块，再配一个最小任务注册入口。

```txt
src/
  app.ts
  scheduler/
    agendaEngine.ts
    types.ts
  tasks/
    index.ts
    demoTask.ts
  config/
    agenda.ts
```

各文件职责：

- `app.ts`：服务启动入口，初始化 AgendaEngine，注册任务，启动调度。
- `scheduler/agendaEngine.ts`：封装 Agenda 初始化、任务定义、Cron job 创建、启动和停止。
- `scheduler/types.ts`：定义任务注册类型。
- `tasks/index.ts`：集中注册所有 MVP 任务。
- `tasks/demoTask.ts`：示例定时任务，用来验证 Cron 执行。
- `config/agenda.ts`：Agenda/PostgreSQL 连接配置和默认调度参数。

### 3.2 AgendaEngine 职责

`AgendaEngine` 是 MVP 的唯一核心模块，负责：

- 初始化 Agenda 实例。
- 连接 PostgreSQL backend。
- 注册任务 handler。
- 创建或更新持久化 Cron job。
- 启动 Agenda worker。
- 监听任务生命周期事件并输出日志。
- 服务退出时调用 `stop()` 或 `drain()` 做优雅停机。

MVP 中不暴露复杂框架 API，只保留最小能力：

```ts
type TaskDefinition = {
  name: string
  cron: string
  handler: () => Promise<void>
}

class AgendaEngine {
  defineTask(task: TaskDefinition): void
  start(): Promise<void>
  stop(): Promise<void>
}
```

### 3.3 任务注册方式

MVP 中任务直接在代码里注册，不从外部配置读取。

示例：

```ts
// tasks/demoTask.ts
export const demoTask = {
  name: "demoTask",
  cron: "*/5 * * * *",
  handler: async () => {
    console.log("demo task running")
  },
}
```

```ts
// tasks/index.ts
import { demoTask } from "./demoTask"

export const tasks = [demoTask]
```

```ts
// app.ts
const agendaEngine = new AgendaEngine(agendaConfig)

for (const task of tasks) {
  agendaEngine.defineTask(task)
}

await agendaEngine.start()
```

### 3.4 Cron 与持久化

MVP 中每个任务在代码中声明一个分钟级 Cron 表达式，例如：

```txt
*/5 * * * *
```

AgendaEngine 启动时需要确保对应 job 存在于 PostgreSQL 中：

- 如果 job 不存在，则创建持久化 job。
- 如果 job 已存在，则复用已有 job，避免重复创建。
- 如果代码里的 Cron 和数据库中的 Cron 不一致，MVP 阶段可以选择启动时覆盖为代码中的 Cron。

因为 MVP 不接入 kconf，所以代码中的任务定义是唯一配置来源。

## 四、启动流程

```txt
1. 读取 Agenda/PostgreSQL 配置
2. 初始化 AgendaEngine
3. 加载 tasks/index.ts
4. 对每个任务调用 defineTask()
5. AgendaEngine 内部执行 agenda.define()
6. AgendaEngine 确保每个任务对应的持久化 Cron job 存在
7. 调用 agenda.start()
8. 监听任务生命周期事件并输出日志
9. 服务收到退出信号时调用 agenda.stop() 或 drain()
```

## 五、验证方式

MVP 完成后重点验证以下场景：

### 5.1 定时执行

配置一个每 5 分钟执行一次的 demo task，确认服务启动后任务能按 Cron 执行。

### 5.2 状态持久化

启动服务并创建 job 后，检查 PostgreSQL 中是否存在对应 Agenda job 记录。

### 5.3 服务重启恢复

停止 Node 服务后重新启动，确认 Agenda 能复用数据库中的 job，并继续按 Cron 调度。

### 5.4 避免重复 job

多次重启服务，确认同一个 task name 不会在数据库中创建多条重复 job。

### 5.5 执行日志

确认任务开始、成功、失败时能输出基础日志，至少包含：

- taskName
- startedAt
- finishedAt
- durationMs
- error message

## 六、MVP 边界

MVP 只证明 AgendaEngine 这条链路可行，不解决全部生产问题。

需要明确以下边界：

- 不承诺 exactly-once。
- 不处理 kconf 配置变更。
- 不处理运行中任务启停。
- 不处理配置冲突。
- 不处理复杂长任务续锁。
- 不处理任务失败重试。
- 不处理任务运行历史查询。

这些能力可以在 MVP 验证通过后，再逐步演进到完整版本：

```txt
MVP：AgendaEngine
  -> v1：TaskRegistry
  -> v2：kconf 手动刷新 / ConfigReconciler
  -> v3：Watchdog 自动续锁
  -> v4：结构化日志、指标、告警
```

## 七、MVP 价值

MVP 的价值在于先验证最核心的不确定性：

- Agenda 是否能稳定接入 PostgreSQL。
- Agenda 是否能满足分钟级 Cron 调度。
- Agenda job 是否能正确持久化。
- 服务重启后任务是否能恢复调度。
- 代码注册任务的开发体验是否可接受。

只要这条链路跑通，后续再考虑 kconf、热更新、reconcile、Watchdog 和观测能力，风险会更可控。
