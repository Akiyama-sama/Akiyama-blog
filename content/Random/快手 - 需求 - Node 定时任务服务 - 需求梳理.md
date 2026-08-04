---
date: 2026-07-07
tags:
aliases:
---
写一个 node 定时任务框架，保证能一直周期性的执行这些任务。这个框架不一定要用 web 框架暴露端口这些，要求写出来的框架简单易扩展，能够支持任务易扩展，所以得考虑好设计模式。任务的这些配置的话需要用快手的那些 kconf 的包，可以让用户从 kconf里面进行可视化配置，而不重启服务。这个框架肯定是要将任务的时间数据进行一个持久化的，好让整个框架服务断开的时候，进行一个断线重连，例如一个任务以一个小时为周期执行一次，中间这个服务断开了 30min 中，30min 过后再进行一次执行，如果这个任务要执行 2 个小时，要等 3 个小时再执行，因此一个周期=空闲周期时间+任务执行时间 

## 需求澄清版 v1

### 需求定位

该需求不是为某几个固定业务任务写脚本，而是建设一个面向内部业务方复用的 Node 定时任务基础框架。框架需要提供清晰的任务注册协议、调度语义、状态持久化能力和运行历史记录，让业务方可以用较低成本接入周期性任务，并在服务重启后保持任务执行状态可恢复、可追踪。

### 核心目标

- 支持业务方通过代码注册任务，框架负责任务调度、状态记录、运行历史和异常日志。
- 周期性执行统一使用 Cron 表达式描述
- 任务配置通过 kconf 管理，第一版只支持热更新任务开关和 Cron 表达式，避免运行中修改复杂策略导致状态语义混乱。
- 框架需要持久化任务运行状态和运行历史，便于服务重启恢复、问题排查和执行结果复盘。
- 第一版按单实例部署设计，不考虑多实例竞争、分布式锁和任务分片。

### 任务注册方式

任务由业务方在代码中显式注册，任务逻辑以 handler 函数形式提供。kconf 不负责动态注册任务，只负责控制已注册任务是否启用以及 Cron 表达式。

示例形态：

```ts
scheduler.register({
  name: "syncAdvertiserReport",
  cron: "0 * * * *",
  enabled: true,
  overlapPolicy: "skip",
  misfirePolicy: "once",
  handler: async (ctx) => {
    // business logic
  },
})
```

### 调度语义

Cron 表达式是唯一的周期性触发来源。每当 Cron 命中一个计划时间点，框架尝试触发对应任务。

如果任务没有正在执行的实例，则直接执行本次触发。

如果上一次执行尚未结束，则按照任务声明的 `overlapPolicy` 处理：

- `skip`：跳过当前 Cron 触发点，等待下一次 Cron 时间点。适合缓存刷新、报表刷新、巡检同步等允许少跑一轮的任务。
- `queue`：将当前 Cron 触发点放入等待队列，等当前执行结束后继续执行。适合不希望漏触发的扫描、补偿类任务。

第一版不支持 `parallel`。并行策略会引入并发上限、幂等、锁、下游限流和运行实例追踪等复杂问题，暂不纳入范围。

### Queue 策略约束

当任务使用 `queue` 策略时，需要支持最大队列长度配置，例如 `maxQueueSize`。如果队列已满，超出的触发点应被丢弃并记录日志/运行事件，避免任务执行速度慢于 Cron 触发速度时无限积压。

第一版需要明确：

- 队列长度按任务维度维护。
- 队列只表达“待补跑的触发点”，不扩展成完整任务队列系统。
- 队列溢出时需要记录可排查信息。

### 停机恢复语义

服务停机或框架暂停期间可能错过 Cron 触发点。第一版通过 `misfirePolicy` 控制恢复行为：

- `none`：恢复后不补偿错过的触发点，只等待下一次 Cron 命中。
- `once`：恢复后如果发现存在错过的触发点，最多立即补偿执行一次，然后回到正常 Cron 调度。

第一版暂不支持 `all`，即不按错过次数逐个补偿，避免服务恢复时集中打满下游。

### kconf 热更新范围

第一版只允许通过 kconf 热更新以下字段：

- `enabled`：任务是否启用。
- `cron`：任务的 Cron 表达式。

暂不支持运行中热更新 `overlapPolicy`、`misfirePolicy`、`maxQueueSize` 或业务参数。原因是这些字段会影响任务状态解释和恢复语义，随意热更新容易导致运行状态不可预期。

### 持久化与观测

框架需要使用数据库进行状态持久化，不使用本地文件、Redis 或抽象 Storage Adapter 作为第一版主方案。

至少需要两类数据：

- 任务状态表：记录任务当前状态、最近一次开始/结束时间、最近一次成功/失败信息、下次计划执行时间、队列数量等。
- 任务运行历史表：记录每一次任务执行的触发来源、开始时间、结束时间、耗时、执行结果、错误信息等。

同时框架需要输出关键日志：

- 任务注册成功/失败。
- kconf 配置加载与更新。
- Cron 触发。
- 任务开始、成功、失败、跳过、入队、队列溢出。
- 服务启动恢复时的 misfire 判断结果。

### 非目标

第一版暂不做以下能力：

- 多实例部署与分布式锁。
- 任务分片执行。
- 并行执行同一个任务。
- 完整任务队列系统。
- Web 管理后台。
- 通过配置动态注册任意任务。
- 复杂告警平台集成。

## 待确认问题

- 数据库类型是否有指定，例如 MySQL、PostgreSQL 或公司内部统一存储。
- Cron 表达式第一版仅需支持到分钟级。
- 任务失败是否需要内置重试机制，还是只记录失败并等待下一次 Cron。
- `queue` 队列溢出后是静默丢弃、记录历史，还是需要触发告警钩子。
- 任务执行超时是否由框架统一控制。
- kconf 配置异常时是沿用上一版有效配置，还是停用对应任务。

## 需求澄清版 v2：基于 Agenda 的内部封装方案

### 方案调整背景

v1 的思路偏向自研一个 Node 定时任务调度内核，需要自己处理 Cron 解析、任务持久化、服务重启恢复、任务锁、运行历史、队列积压和并发控制。进一步调研后发现，开源框架 Agenda 已经封装了大量底层调度能力，包括任务持久化、重复任务、Cron 调度、任务锁、并发控制、任务事件和优雅停机。

因此该需求不再优先定义为“从零自研 Node 定时任务框架”，而是调整为：

> 基于 Agenda 封装一层适配快手内部使用习惯的定时任务基础框架。底层复用 Agenda 的持久化调度、锁、并发控制和运行事件能力；上层提供统一的任务注册 API，并接入 kconf 实现任务启停和 Cron 表达式热更新。

### 核心设计理念

Agenda 的设计中，数据库是调度引擎的运行态事实来源。Agenda 会把任务定义、下次执行时间、锁状态、执行状态等信息持久化到数据库中，并基于数据库中的记录驱动任务执行。

但本需求希望业务方通过 kconf 可视化配置任务开关和 Cron 表达式，因此在业务配置层面，kconf 才是期望状态的事实来源。

所以整体设计应区分两类事实来源：

- **kconf：业务期望态的 Single Source of Truth**，负责描述某个任务是否启用、应该按照什么 Cron 表达式执行。
- **Agenda 数据库：调度运行态的 Single Source of Truth**，负责记录 Agenda 实际执行所需的 job、nextRunAt、lockedAt、lastRunAt、lastFinishedAt 等运行状态。

两者之间需要通过一个配置协调器进行同步：

```txt
kconf 配置变更
  -> KconfWatcher / ConfigReconciler 感知变化
  -> 校验任务是否已在代码中注册
  -> 校验 Cron 表达式是否合法
  -> 对比 kconf 期望态与 Agenda 数据库运行态
  -> 调用 Agenda public API 同步 job
  -> Agenda 基于数据库中的最新 job 状态执行任务
```

### 主要模块

#### TaskRegistry

任务注册表，负责收集业务方通过代码注册的任务。

业务方只能在代码中注册任务 handler，不能只靠 kconf 动态创建任意任务。这样可以保证任务逻辑可测试、可审查、可类型约束，也避免配置错误导致执行不存在或未审核的任务。

示例形态：

```ts
taskScheduler.register({
  name: "syncAdvertiserReport",
  handler: async (ctx) => {
    // business logic
  },
})
```

#### KconfWatcher

监听 kconf 配置变化，并在服务启动时执行一次全量配置加载。

KconfWatcher 不直接执行任务，只负责拿到最新配置快照并交给 ConfigReconciler。需要支持：

- 服务启动时全量读取配置。
- 运行中监听配置热更新。
- 配置异常时保留上一版有效配置，避免错误配置导致所有任务异常停摆。

#### ConfigReconciler

配置协调器，是该封装层的核心模块。

它负责把 kconf 中的期望状态同步到底层 Agenda job：

- 如果 kconf 中配置了一个任务，但代码注册表中不存在该任务，应拒绝同步并记录错误。
- 如果 Cron 表达式非法，应拒绝同步该任务，并保留 Agenda 中上一版有效配置。
- 如果 Agenda 中不存在对应 job，应通过 Agenda 创建重复任务。
- 如果 Cron 表达式发生变化，应通过就地更新修改已有 single job 的 repeat 配置并保存，不能先 `cancel()` 再 `every()` 重建。
- 如果 `enabled` 为 `false`，应 disable 对应 job，而不是直接删除。
- 如果 `enabled` 为 `true`，应 enable 对应 job；如果 job 不存在，则先创建再启用。

推荐优先使用 Agenda public API，而不是依赖内部实现：

- `agenda.define(name, handler)`：注册任务处理函数。
- `agenda.every(cron, name, data, options)`：创建或更新 single 类型的重复任务。
- `agenda.queryJobs(query)`：查询已有 job。
- `job.repeatEvery(cron, options)` + `job.save()`：就地更新已有 job 的 Cron 配置。
- `agenda.enable(query)` / `agenda.disable(query)`：启用或禁用 job。
- `agenda.cancel(query)`：仅用于任务确认下线的场景，不用于 Cron 热更新。

#### AgendaEngine

对 Agenda 实例进行统一初始化和生命周期管理：

- 配置 PostgreSQL 数据库连接。
- 注册所有任务 handler。
- 设置默认并发、锁超时、任务处理间隔等参数。
- 监听 Agenda 的 start/success/fail/complete 等事件。
- 在框架包装层中用 Watchdog/看门狗模式处理长任务续锁逻辑，业务 handler 不需要直接调用 Agenda 的 `touch()`。
- 在服务关闭时执行 `stop()` 或 `drain()`，尽量保证优雅停机。

### kconf 配置范围

第一版 kconf 只管理任务开关和 Cron 表达式：

```ts
type KconfTaskConfig = {
  name: string
  enabled: boolean
  cron: string
  timezone?: string
}
```

暂不允许通过 kconf 修改 handler、并发策略、锁超时、重试策略、任务业务参数等复杂配置。

Cron 表达式第一版仅需支持到分钟级，不需要支持秒级调度，避免高频任务带来额外锁续约、日志和下游压力。

原因：

- handler 必须来自代码注册，避免配置注入任意执行逻辑。
- 并发、锁、重试等策略会影响运行状态解释，第一版不做热更新。
- 业务参数可以由业务任务自己读取对应业务配置，不放进调度框架的通用配置层。

### Agenda 同步策略

服务启动时需要先完成以下步骤：

1. 初始化 Agenda 实例。
2. 注册所有代码中的任务 handler。
3. 读取 kconf 全量任务配置。
4. 执行一次 full reconcile，将 kconf 期望态同步到 Agenda 数据库。
5. 启动 Agenda worker。
6. 开始监听 kconf 后续变更。

运行中当 kconf 发生变化时：

1. KconfWatcher 获取最新配置快照。
2. ConfigReconciler 对配置做合法性校验。
3. 对每个任务执行增量 reconcile。
4. 通过 Agenda public API 修改对应 job。
5. 记录同步成功或失败日志。

采用 reconcile 思路，而不是只依赖 watch 事件。这样即使服务重启、watcher 漏事件、Agenda 数据库残留旧 job，也可以通过下一次全量 reconcile 重新收敛到 kconf 期望态。

### 调度与并发语义

第一版不在封装层自研 `skip` / `queue` / `parallel` 任务队列语义，而是优先复用 Agenda 的能力：

- 通过 `agenda.define(name, { concurrency: 1 }, handler)` 或等价配置，默认保证同一个任务不并行执行。
- 通过 Agenda 的 lock 机制避免多 worker 抢占同一个 job。
- 通过 `lockLifetime` 控制任务锁有效期。长任务可能超过锁时间时，由框架包装层启动 Watchdog 定时续锁，避免把 Agenda 的 `touch()` 暴露给业务层。
- 任务执行时间超过 Cron 间隔时，第一版接受 Agenda 默认行为，不额外实现自定义 overlap 策略。

如果后续确实需要更强的 `skip` / `queue` 语义，再在 Agenda 之上补充封装，不在第一版实现完整队列系统。

### 停机恢复语义

Agenda 会持久化 job 的运行状态和下次执行时间。服务重启后，Agenda 会基于数据库中的 job 状态继续调度。

第一版不自行实现 `misfirePolicy: none | once | all`，而是直接接受 Agenda 的默认恢复机制。服务停机期间错过 Cron 点、任务执行时间超过 Cron 间隔、disable 后再 enable 的 nextRunAt 计算，都交给 Agenda 的默认策略处理。

### 持久化与观测

Agenda 自身会将 job 状态持久化到数据库。封装层需要在此基础上补充业务可观测能力：

- 监听 Agenda 任务生命周期事件，如 start、success、fail、complete。
- 第一版优先使用 Agenda 自带日志能力记录任务名、触发时间、开始时间、结束时间、耗时、结果、错误信息。
- 封装层只补充必要的 kconf 同步日志和异常日志，不重复建设运行历史表。

第一版优先复用 Agenda 的持久化与日志能力，避免重复维护一套任务状态表或运行历史表。

### 已确认约束

- 数据库后端使用 PostgreSQL，公司内部可以稳定接入，且 Agenda PostgreSQL backend 的接入成本可接受。
- Cron 表达式第一版仅需支持到分钟级。
- 任务执行时间超过 Cron 间隔时，接受 Agenda 默认行为。
- 服务停机期间错过 Cron 点后的恢复行为，接受 Agenda 默认行为。
- 多次调用 `agenda.every()` 同名任务时，Agenda 能稳定避免重复 job。
- Cron 表达式更新时采用就地更新：查询已有 single job，调用 `job.repeatEvery(newCron, options)` 后 `job.save()`。
- `disable()` 后重新 `enable()` 不需要框架手动修正 `nextRunAt`，使用 Agenda 默认策略。
- 长任务超过 `lockLifetime` 时需要续锁，续锁逻辑使用 Watchdog/看门狗模式封装在框架层，不能要求业务 handler 直接处理。
- 任务执行日志优先使用 Agenda 自带日志能力，不额外建设独立运行历史表。

### 非目标

第一版不做以下能力：

- 从零自研 Cron 调度器。
- 自研任务锁和分布式协调。
- 自研完整任务队列。
- 通过 kconf 动态创建未在代码中注册的任务。
- Web 管理后台。
- 复杂告警平台集成。
- 任意任务参数热更新。

### 仍需调研与验证的问题

- Agenda PostgreSQL backend 在当前内部 Node 运行环境中的具体初始化方式和连接配置。
- 分钟级 Cron 表达式在 Agenda 当前版本中的具体格式，以及与 kconf 配置校验规则如何保持一致。
- Watchdog 自动续锁的时间间隔、停止时机和异常处理策略。
- Cron 就地更新时如何处理配置抖动、连续更新和 `job.save()` 失败回滚。