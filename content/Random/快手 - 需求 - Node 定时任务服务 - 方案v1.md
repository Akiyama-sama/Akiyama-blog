---
date: 2026-07-07
tags:
aliases:
---

## 一、背景

当前公司内部已有 autocode 能力，可以通过 kconf 做配置，并可视化编写定时任务。但在实际使用中存在两个比较明显的问题：

- autocode 对单个配置对象有大小限制，例如 128kb，复杂任务很容易触及上限。
- 平台任务存在稳定性风险，偶尔会出现任务停止但原因不明确的情况，排查和兜底成本较高。

因此需要建设一个 Node 定时任务服务，用来承接更稳定、可控、可扩展的周期性任务执行能力。

这个需求一开始可以理解成“写一个 Node 定时任务框架”，但进一步澄清后，它更适合定义为一个**内部基础框架**，而不是为某几个固定任务写脚本。它需要让业务方通过统一 API 注册任务，同时由框架负责调度、持久化、配置热更新、日志和恢复能力。

最开始调研时，我优先考虑的是 `node-cron` 这类轻量 Cron 库。它的优势是接入简单，适合在单个 Node 进程里快速表达“到点执行某个函数”。但这个需求不只是定时触发，还涉及任务状态持久化、服务重启恢复、长任务锁续约、配置热更新和运行日志。如果直接基于 `node-cron` 做，就需要自己补一整套调度状态管理和异常恢复逻辑，后续维护成本会比较高。

也对比了偏队列或 worker 模型的方案，例如 BullMQ、Bree 等。它们分别擅长 Redis 队列、任务消费、worker 隔离等场景，但会把问题引向完整队列系统或 worker 编排。本需求第一版更关注“可持久化的 Cron 调度 + 数据库运行态 + kconf 期望态同步”，不希望引入过重的队列语义。

经过开源方案调研后，[Agenda](https://github.com/agenda/agenda) 比从零自研更适合作为底层调度引擎。Agenda 已经封装了重复任务、Cron 调度、数据库持久化、任务锁、并发控制、生命周期事件和优雅停机等能力。因此本方案不重复造调度内核，而是在 Agenda 之上封装一层适配内部场景的框架能力。

## 二、目标

### 业务目标

- 替代 autocode 中不稳定或受对象大小限制的定时任务场景。
- 让业务方能够用代码注册任务，用 kconf 控制任务启停和 Cron 表达式。
- 支持任务配置热更新，不需要为了调整执行周期而重启服务。
- 提供稳定的任务执行和可追踪的运行日志，降低排查成本。

### 技术目标

- 周期性调度统一使用 Cron 表达式，仅需支持到分钟级。
- kconf 作为业务配置的事实来源，描述任务是否启用、应该按什么 Cron 执行。
- Agenda 数据库作为调度运行态的事实来源，保存 job、nextRunAt、lockedAt、lastRunAt、lastFinishedAt 等运行状态。
- 通过配置协调器将 kconf 的期望态同步到 Agenda 的运行态。
- 任务 handler 必须通过代码注册，避免通过配置动态创建未经审核的任务逻辑。
- 支持 PostgreSQL 作为 Agenda 的数据库后端。
- 长任务超过 `lockLifetime` 时，由框架层自动续锁，业务方不需要感知 Agenda 的 `touch()` 细节。

### 非目标

- 不从零自研 Cron 调度器。
- 不自研任务锁、分布式协调和完整任务队列。
- 不通过 kconf 动态创建未在代码中注册的任务。
- 第一版不做 Web 管理后台。
- 第一版不额外建设独立运行历史表，优先使用 Agenda 自带日志能力。
- 第一版不自定义 `skip`、`queue`、`parallel` 等复杂 overlap 策略，先接受 Agenda 默认行为。

## 三、方案

### 3.1 总体架构

整体方案可以拆成四个核心模块：

```txt
业务代码注册任务
  -> TaskRegistry 收集任务 handler
  -> KconfWatcher 读取/监听 kconf 配置
  -> ConfigReconciler 同步 kconf 期望态到 Agenda
  -> AgendaEngine 基于 PostgreSQL 持久化调度并执行任务
```

其中，最关键的设计是区分两类事实来源：

- **kconf 是业务期望态的 Single Source of Truth**：负责描述任务是否启用、Cron 表达式是什么。
- **Agenda 数据库是调度运行态的 Single Source of Truth**：负责记录 Agenda 实际执行需要的 job 状态、锁状态、运行时间等。

两者之间通过 `ConfigReconciler` 做一致性同步，避免业务配置和底层调度状态脱节。

### 3.2 TaskRegistry：代码注册任务

业务方通过代码注册任务 handler：

```ts
taskScheduler.register({
  name: "syncAdvertiserReport",
  handler: async (ctx) => {
    // business logic
  },
})
```

kconf 只负责配置已经注册过的任务，不负责动态创建任务逻辑。这样可以保证：

- 任务逻辑可审查、可测试。
- 任务名和 handler 有明确映射关系。
- 避免配置错误导致执行不存在或未经审核的任务。

### 3.3 KconfWatcher：监听配置变化

`KconfWatcher` 负责读取和监听 kconf 配置：

- 服务启动时读取全量任务配置。
- 运行中监听配置热更新。
- 配置异常时保留上一版有效配置，避免错误配置导致任务大面积停摆。

第一版 kconf 只管理：

```ts
type KconfTaskConfig = {
  name: string
  enabled: boolean
  cron: string
  timezone?: string
}
```

暂不支持通过 kconf 修改 handler、并发策略、锁超时、重试策略和业务参数。

### 3.4 ConfigReconciler：同步期望态与运行态

`ConfigReconciler` 是封装层的核心。它负责把 kconf 中的期望状态同步到 Agenda job：

- kconf 中配置了未注册任务：拒绝同步并记录错误。
- Cron 表达式非法：拒绝同步，并保留上一版有效配置。
- Agenda 中不存在 job：创建重复任务。
- `enabled=false`：disable 对应 job，不直接删除。
- `enabled=true`：enable 对应 job；如果 job 不存在，则先创建再启用。
- Cron 表达式变化：对已有 single job 做就地更新。

Cron 热更新必须采用 **In-place Update**，不能使用 `cancel() + every()` 重建。原因是如果任务正在执行，`cancel()` 会删除底层 job 记录和锁状态，正在跑的任务会变成无主任务；此时新 job 如果刚好触发，可能导致同一任务并发执行，破坏 `concurrency: 1` 的语义。

正确做法是：

```ts
const job = await findSingleJob(taskName)
job.repeatEvery(newCron, options)
await job.save()
```

### 3.5 AgendaEngine：调度执行与生命周期管理

`AgendaEngine` 负责封装 Agenda 实例：

- 使用 PostgreSQL 作为底层存储。
- 注册所有任务 handler。
- 设置默认并发、锁超时、任务处理间隔。
- 监听 Agenda 的任务生命周期事件。
- 服务关闭时执行 `stop()` 或 `drain()`，尽量保证优雅停机。

并发与恢复策略第一版都接受 Agenda 默认行为：

- 任务执行时间超过 Cron 间隔时，按 Agenda 默认策略处理。
- 服务停机期间错过 Cron 点时，按 Agenda 默认恢复策略处理。
- `disable()` 后重新 `enable()` 时，`nextRunAt` 不由框架手动修正，交给 Agenda 处理。

### 3.6 长任务续锁：Watchdog 模式

如果任务执行时间超过 `lockLifetime`，可能出现锁过期后任务被重复拉起的问题。

因此框架层需要提供自动续锁能力，采用 Watchdog/看门狗模式：

- 任务开始执行后，框架包装层启动一个定时续锁逻辑。
- 在任务运行期间定期调用 Agenda 的 `touch()` 续约锁。
- 任务成功、失败或退出时停止 Watchdog。
- 业务 handler 不需要直接感知 Agenda 的锁和 `touch()`。

这样可以把 Agenda 的运行细节收敛在框架层，业务方只需要关注自己的任务逻辑。

### 3.7 日志与观测

第一版优先使用 Agenda 自带日志能力，记录任务执行过程中的关键信息：

- 任务名。
- 触发时间。
- 开始时间。
- 结束时间。
- 耗时。
- 执行结果。
- 错误信息。

封装层只补充 kconf 同步相关日志，例如配置加载、配置变更、同步成功、同步失败、Cron 校验失败等。不额外建设独立运行历史表，避免重复维护状态。

### 3.8 代码目录组织

推荐将代码拆成“框架层”和“业务任务层”两部分：

```txt
src/
  app.ts
  config/
    agenda.ts
    kconf.ts
  scheduler/
    index.ts
    types.ts
    taskRegistry.ts
    agendaEngine.ts
    kconfWatcher.ts
    configReconciler.ts
    cronValidator.ts
    watchdog.ts
    logger.ts
  tasks/
    index.ts
    syncAdvertiserReport.ts
    refreshMaterialCache.ts
  infra/
    db/
      postgres.ts
    kconf/
      client.ts
  utils/
    time.ts
    errors.ts
```

各目录职责如下：

- `app.ts`：服务启动入口，负责初始化框架、注册任务、启动 Agenda、监听退出信号。
- `config/`：服务级配置，例如 Agenda 数据库连接、默认锁时间、kconf key、日志级别等。
- `scheduler/`：定时任务框架核心，不写具体业务逻辑。
- `tasks/`：业务任务目录，每个文件定义一个具体任务，并通过统一 API 注册。
- `infra/`：基础设施适配层，例如 PostgreSQL 客户端、kconf client。
- `utils/`：通用工具函数，不依赖业务任务和 Agenda 实例。

核心原则是：业务任务只感知 `scheduler.register()` 这种稳定 API，不直接感知 Agenda、PostgreSQL、kconf watcher 和锁续约细节。

### 3.9 scheduler 内部模块划分

#### `types.ts`

定义框架对外暴露的核心类型：

```ts
export type TaskHandler = (ctx: TaskContext) => Promise<void>

export type RegisteredTask = {
  name: string
  handler: TaskHandler
}

export type KconfTaskConfig = {
  name: string
  enabled: boolean
  cron: string
  timezone?: string
}
```

这一层是框架和业务任务之间的契约。后续如果扩展重试、超时、告警等能力，也优先从类型契约开始演进。

#### `taskRegistry.ts`

维护代码注册任务的内存表：

- 提供 `register(task)` 给业务任务使用。
- 校验任务名唯一。
- 提供 `getTask(name)` 给 `ConfigReconciler` 查询。
- 提供 `listTasks()` 给启动流程批量注册到 Agenda。

它的职责是保证“kconf 中只能启停已经在代码里注册过的任务”。

#### `agendaEngine.ts`

封装 Agenda 实例，避免 Agenda API 散落在业务代码里：

- 初始化 Agenda 和 PostgreSQL backend。
- 将 `TaskRegistry` 中的任务 handler 转换成 `agenda.define()`。
- 设置默认 `concurrency`、`lockLifetime`、`processEvery` 等参数。
- 统一监听 Agenda 生命周期事件。
- 暴露少量方法给 `ConfigReconciler` 使用，例如 `findJob()`、`createJob()`、`updateJobCron()`、`enableJob()`、`disableJob()`。

这样后续即使更换 Agenda 版本，影响范围也集中在这一层。

#### `kconfWatcher.ts`

负责从 kconf 获取任务配置：

- 启动时读取全量配置。
- 监听运行时变更。
- 维护上一版合法配置。
- 配置更新后通知 `ConfigReconciler`。

它只负责“拿配置”，不直接操作 Agenda。

#### `configReconciler.ts`

负责把 kconf 期望态同步到底层 Agenda 运行态：

- 校验任务是否已经代码注册。
- 调用 `cronValidator` 校验 Cron。
- 对比当前 Agenda job 与 kconf 配置。
- 决定 create、enable、disable、in-place update。
- 同步失败时记录日志，并尽量保持上一版有效调度状态。

这是整个框架中最关键的状态协调模块。

#### `cronValidator.ts`

集中处理 Cron 校验：

- 校验是否为分钟级 Cron 表达式。
- 校验 kconf 中的 Cron 格式是否能被 Agenda 正确识别。
- 对非法表达式给出清晰错误日志。

这里要保证 kconf 的校验规则和 Agenda 实际执行规则一致，避免“配置层认为合法，执行层无法识别”的问题。

#### `watchdog.ts`

封装长任务续锁逻辑：

- 任务开始后启动 Watchdog。
- 按固定间隔调用 Agenda job 的 `touch()`。
- 任务结束、失败或抛错时停止 Watchdog。
- Watchdog 自身异常时记录日志，必要时让任务失败。

这一层的目标是把锁续约细节完全收敛到框架层，业务 handler 不需要知道 Agenda 锁机制。

#### `logger.ts`

统一框架内部日志口径：

- Agenda 生命周期事件日志。
- kconf 配置读取和变更日志。
- reconcile 成功/失败日志。
- Cron 校验失败日志。
- Watchdog 续锁异常日志。

任务执行日志优先复用 Agenda 自带能力，框架只补充 Agenda 覆盖不到的配置同步和框架异常信息。

### 3.10 启动流程

服务启动时建议按以下顺序执行：

```txt
1. 加载服务配置
2. 初始化 PostgreSQL / Agenda 连接
3. 初始化 TaskRegistry
4. 加载 tasks/index.ts，完成所有业务任务代码注册
5. 将 TaskRegistry 中的 handler 注册到 AgendaEngine
6. KconfWatcher 拉取全量 kconf 配置
7. ConfigReconciler 执行 full reconcile
8. 启动 Agenda worker
9. KconfWatcher 开始监听后续配置变更
10. 注册 SIGTERM / SIGINT，退出时 stop 或 drain
```

关键点是：**先完成代码任务注册，再执行 kconf reconcile**。否则如果先读 kconf，可能出现配置里有任务，但代码注册表还没准备好的误判。

### 3.11 任务接入方式

业务新增一个任务时，只需要新增一个任务文件，并在 `tasks/index.ts` 中注册：

```ts
// tasks/syncAdvertiserReport.ts
export const syncAdvertiserReportTask = {
  name: "syncAdvertiserReport",
  handler: async (ctx) => {
    // 业务逻辑
  },
}
```

```ts
// tasks/index.ts
import { registerTask } from "../scheduler"
import { syncAdvertiserReportTask } from "./syncAdvertiserReport"

export function registerAllTasks() {
  registerTask(syncAdvertiserReportTask)
}
```

然后在 kconf 中配置：

```json
{
  "tasks": [
    {
      "name": "syncAdvertiserReport",
      "enabled": true,
      "cron": "0 */5 * * * *",
      "timezone": "Asia/Shanghai"
    }
  ]
}
```

这样可以做到：

- 任务逻辑走代码评审。
- 执行开关和 Cron 走 kconf 热更新。
- 框架统一处理 Agenda 同步、锁续约、日志和优雅停机。

### 3.12 模块依赖关系

依赖方向应保持单向：

```txt
tasks
  -> scheduler public API

scheduler
  -> infra/db
  -> infra/kconf
  -> Agenda

infra
  -> company runtime / external clients
```

不允许：

- `tasks` 直接调用 Agenda API。
- `tasks` 直接调用 kconf watcher 修改调度配置。
- `tasks` 直接处理 `touch()` 续锁。
- `infra` 反向依赖 `tasks`。

这样可以保证业务任务是“被调度的函数”，而不是和调度框架互相耦合的一团逻辑。后续框架能力升级时，业务任务的改动成本会比较低。
