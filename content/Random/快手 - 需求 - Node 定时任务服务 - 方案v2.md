---
date: 2026-07-08
tags:
aliases:
---

## 一、背景

v1 方案中选择 Agenda 作为底层调度引擎，原因是 Agenda 能提供 Cron 调度、任务持久化、任务锁、并发控制和生命周期事件，适合用来替代自研调度内核。

但后续约束发生变化：当前落地环境需要支持 **MySQL**。Agenda 的主流使用路径更偏 MongoDB/PostgreSQL，不适合作为 MySQL 约束下的第一选择。如果继续使用 Agenda，就需要额外验证或改造数据库 backend，方案复杂度和落地风险都会上升。

因此 v2 方案切换到 [Sidequest.js](https://github.com/sidequestjs/sidequest)。Sidequest.js 是一个 Node.js 后台任务处理框架，原生支持 PostgreSQL、MySQL、SQLite、MongoDB 等 backend，并提供持久化任务、Cron/定时任务、任务唯一性、重试、并发控制、worker threads、dashboard 和 stale job recovery 等能力。

本需求的核心不是实现一个完整任务队列平台，而是先建设一个能跑周期性任务的内部基础服务。因此 v2 的重点是：**基于 Sidequest.js + MySQL 实现持久化任务状态和分钟级 Cron 定时执行**。

## 二、目标

### 业务目标

- 替代 autocode 中不稳定或受配置对象大小限制的定时任务场景。
- 使用 MySQL 作为任务状态持久化存储，符合当前内部基础设施约束。
- 支持业务方通过代码注册任务，并由框架负责定时调度和执行。
- 服务重启后能够基于 MySQL 中的任务状态继续调度。

### 技术目标

- 使用 Sidequest.js 作为底层 job engine，不从零自研调度器。
- 使用 `@sidequest/mysql-backend` 作为 MySQL backend。
- 支持分钟级 Cron 表达式，不需要支持秒级调度。
- 任务逻辑通过代码注册，避免通过配置动态执行未审核任务。
- 任务状态持久化到 MySQL。
- 支持基础执行日志，能够排查任务开始、成功、失败等关键事件。

### 非目标

第一版 v2 不实现以下能力：

- 不接入 kconf。
- 不实现配置热更新。
- 不实现 watcher。
- 不实现手动刷新接口。
- 不实现轮询配置。
- 不自研任务锁和状态表。
- 不做 Web 管理后台定制。
- 不做复杂告警。
- 不承诺 exactly-once。

## 三、为什么选择 Sidequest.js

### 3.1 对比 Agenda

Agenda 更适合 MongoDB/PostgreSQL 路线。虽然它的调度模型成熟，但在当前必须支持 MySQL 的前提下，继续使用 Agenda 会带来额外 backend 适配和验证成本。

Sidequest.js 则原生提供 MySQL backend，更符合当前数据库约束。它不仅能表达定时任务，还能把任务状态、执行状态、重试、锁和恢复逻辑交给框架处理，避免在业务服务中重复实现这些基础能力。

### 3.2 对比轻量 Cron 库

`node-cron`、`node-schedule` 这类库适合在单进程内表达“到点执行函数”，但它们不负责：

- 任务状态持久化。
- 服务重启恢复。
- 多实例任务领取。
- 失败重试。
- 执行历史/状态追踪。

如果基于轻量 Cron 库实现，需要自研 MySQL 状态表、锁、恢复逻辑和日志链路。对这个需求来说，轻量库太薄。

### 3.3 对比 Redis 队列方案

BullMQ 这类方案能力很强，但核心依赖 Redis。当前诉求是使用 MySQL 做任务状态持久化，因此 Redis 队列不是最优解。

Sidequest.js 的优势在于：在不引入 Redis 的前提下，直接使用 MySQL 承担任务持久化和调度状态管理。

## 四、总体方案

v2 方案中，框架只保留最核心的一层封装：`SidequestEngine`。

```txt
业务任务代码
  -> SidequestEngine 注册任务
  -> Sidequest.js 创建/调度 job
  -> MySQL 持久化任务状态
  -> Sidequest worker 执行任务
```

第一版不引入 kconf，因此代码中的任务定义就是唯一配置来源。

### 4.1 事实来源

v2 第一版只有一个事实来源：

- **代码任务定义**：描述任务名、Cron 表达式、任务 handler。

Sidequest.js + MySQL 负责运行态：

- job 状态。
- 调度状态。
- 执行状态。
- 失败/重试状态。

由于不接入 kconf，暂时不存在“kconf 期望态”和“数据库运行态”之间的同步问题。

## 五、模块设计

### 5.1 目录组织

```txt
src/
  app.ts
  config/
    sidequest.ts
  scheduler/
    sidequestEngine.ts
    types.ts
  tasks/
    index.ts
    demoTask.ts
```

各文件职责：

- `app.ts`：服务启动入口，初始化 SidequestEngine，注册任务，启动 worker。
- `config/sidequest.ts`：Sidequest/MySQL 连接配置和默认参数。
- `scheduler/sidequestEngine.ts`：封装 Sidequest 初始化、任务注册、定时任务创建和生命周期管理。
- `scheduler/types.ts`：定义任务注册协议。
- `tasks/index.ts`：集中导出业务任务列表。
- `tasks/demoTask.ts`：MVP 示例任务，用于验证 Cron 执行和持久化。

### 5.2 SidequestEngine

`SidequestEngine` 是 v2 MVP 的唯一核心模块，负责：

- 初始化 Sidequest.js。
- 配置 MySQL backend。
- 注册业务任务 handler。
- 创建或更新定时任务。
- 启动 worker。
- 输出基础执行日志。
- 服务退出时做优雅关闭。

对业务侧暴露最小 API：

```ts
type TaskDefinition = {
  name: string
  cron: string
  handler: () => Promise<void>
}

class SidequestEngine {
  defineTask(task: TaskDefinition): void
  start(): Promise<void>
  stop(): Promise<void>
}
```

### 5.3 任务定义

业务任务通过代码定义：

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

集中注册：

```ts
// tasks/index.ts
import { demoTask } from "./demoTask"

export const tasks = [demoTask]
```

启动时注册到 SidequestEngine：

```ts
const engine = new SidequestEngine(sidequestConfig)

for (const task of tasks) {
  engine.defineTask(task)
}

await engine.start()
```

## 六、启动流程

```txt
1. 读取 Sidequest/MySQL 配置
2. 初始化 SidequestEngine
3. 加载 tasks/index.ts
4. 注册所有业务任务
5. SidequestEngine 创建或确认对应 Cron job
6. 启动 Sidequest worker
7. 监听任务执行状态并输出日志
8. 服务退出时执行 stop()
```

## 七、运行语义

第一版 v2 需要明确以下语义：

- 不承诺 exactly-once。
- 任务 handler 需要具备幂等性。
- Cron 仅支持分钟级表达式。
- 任务配置来自代码，不支持运行时热更新。
- 服务重启后依赖 MySQL 中的持久化状态恢复调度。
- 任务失败、重试、stale recovery 等行为优先使用 Sidequest.js 默认能力。

## 八、验证项

v2 落地前需要完成 PoC 验证：

### 8.1 MySQL backend

- Sidequest.js 是否能稳定连接内部 MySQL。
- MySQL backend 是否会自动创建所需表结构。
- 表结构和索引是否符合内部数据库规范。

### 8.2 Cron 调度

- 分钟级 Cron 是否能按预期执行。
- 服务重启后任务是否继续调度。
- 同一任务多次启动服务是否会产生重复 job。

### 8.3 执行状态

- 任务开始、成功、失败是否能被记录。
- 失败任务是否能按 Sidequest 默认策略处理。
- stale job recovery 是否符合预期。

### 8.4 运行环境

- Sidequest.js 对 Node.js 版本有要求，需要确认内部运行时是否满足。
- Sidequest.js license 为 LGPL-3.0-or-later，需要确认公司内部使用合规性。

## 九、风险与边界

### 9.1 Sidequest.js 项目成熟度

Sidequest.js 相比 Agenda、BullMQ 等方案更年轻，需要通过 PoC 验证稳定性、维护活跃度和内部运行兼容性。

### 9.2 MySQL 压力

任务调度状态、执行状态和 worker 协调都会依赖 MySQL。虽然第一版任务量预计不大，但仍需关注：

- 调度查询频率。
- job 表索引。
- 锁竞争。
- 失败任务堆积。

### 9.3 业务幂等

框架不承诺 exactly-once。即使 Sidequest.js 提供任务锁和恢复能力，进程崩溃、MySQL 异常或 worker 重启仍可能导致重复执行。业务任务需要通过幂等逻辑兜底。

### 9.4 暂不支持配置热更新

由于 kconf 当前没有稳定 watcher 能力，v2 第一版不接入 kconf。任务周期和开关需要通过代码变更发布。

## 十、后续演进

MVP 跑通后，再考虑以下能力：

```txt
v2 MVP：SidequestEngine + MySQL + 代码注册任务
  -> v2.1：结构化日志和基础指标
  -> v2.2：任务失败告警
  -> v2.3：手动刷新配置接口
  -> v2.4：kconf 轮询或配置中心事件能力
  -> v2.5：任务开关和 Cron 热更新
```

当前阶段优先验证最核心链路：**Sidequest.js 能否基于 MySQL 稳定持久化任务状态，并按分钟级 Cron 执行业务任务**。
