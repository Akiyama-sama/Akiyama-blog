---
date: 2026-06-18
tags:
aliases:
---
在[[SDD 快手落地规范]]这个 SDD 流程当中，几个状态我需要记录一下：

简要流程：
1. 需求约束。无论是需求清晰的，还是不清晰的，都通过对话来生成一份proposal.md，这份文档用于理清需求，定义需求边界。
2. 规格生成。本质上是封装 OpenSpec，但在需求理解这一步，做了一些提供 LLM 核心需求上下文的步骤，在上面做的就是读 Wiki，规格包含的文档有：spec.md 或 design/specs/tasks/plan-ready.md。规格文档是`把需求翻译成可验证、可实现、可拆任务的工程规格说明` 介于需求文档以及技术文档之间，作为其中间层。
	1. 轻量的规格文档只有spec.md
	2. 完整模式下的规格文档design/specs/tasks/plan-ready.md

3. 执行实现。读取规格文档，并加载 Superpowers SKILL 阅读规格说明，先生成 impl-plan.md，然后进行执行变更（TDD 驱动）
4. 验证归档。
	1. 检查prd checkbox功能是否都已经完成
	2. 代码规范检查， 例如是否 tsc 编译通过/lint通过
	3. 如果要走 TDD，看测试用例是否都通过
	4. LLM 代码 CR，读取design.md对比暂存区变更的代码，看是否符合预期/要求
	5. 产出业务知识（起草agent + 审查agent配合使用），更新到对应模块的wiki
	6. 归档，将 openspec/changes的变更给放进openspec/archive里面


详细流程：

```txt
[PHASE1: 需求收敛]
  |-- 需求不清晰/修 bug --------> brainstorming
  |-- 需求清晰/PRD ------------> proposal
  |-- 产物: proposal.md
  v
[GATE1: A/B/C]
  |-- A --> [TRACK1: phase_1_complete] --> [PHASE2]
  |-- B --> 回到 PHASE1 补充
  \-- C --> 回到 PHASE1 重做

[PHASE2: 规格生成]
  |-- triage=plan --> 生成 spec.md 单文件 （提案文档的复杂度小，无黑话或者其他需要 Agent 知道的上下文，即可走这一步）
  |-- triage=full --> create/resync/amend （复杂度很高，有大量的黑话以及需要查询 Wiki 知识库）
  |      |-- create  -> 黑话解析 -> 知识库 -> 代码定位 -> 低码预判
  |      |             -> 低码三步(入口/模块/边界) -> 组件识别
  |      |             -> OpenSpec propose -> 自审
  |      |-- resync  -> proposal 变更后重对齐方案
  |      \-- amend   -> 方案增量调整
  |-- 产物: spec.md 或 design/specs/tasks/plan-ready.md
  v
[GATE2: A/B/C]
  |-- A --> [TRACK2: phase_2_complete] --> [BRANCH PREP] --> [PHASE3]
  |-- B --> 回到 PHASE2 调整
  \-- C --> 回到 PHASE2 重做

[PHASE3: 执行实现]
  |-- 依赖检测 -> 断点恢复 -> 生成 impl-plan.md
  |-- 有 [comp-*] -> 先走组件前置链
  |-- [canal] 统一一次下发
  |-- [code] 逐任务 TDD 执行 （仅UI 改动不走 TDD，任务当中设计到类似后端的逻辑改动时才会走）
  |-- 完成后只 git add，不 commit
  v
[GATE3: A/B/C]
  |-- A --> [TRACK3: phase_3_complete] --> [PHASE4]
  |-- B --> 人工介入 / 暂停
  \-- C --> 回到 PHASE3 局部重跑

[PHASE4: 验证归档]
  |-- verify.sh -> LLM 补检 -> 设计一致性 -> 规格完整性
  |-- 不一致:
  |      |-- 阻塞问题 --> 回 PHASE3 或 PHASE2(amend/resync)
  |      \-- 记录级问题 -> 记 close-issues 后继续
  |-- 归档 -> 展示 staged diff -> 人工 review 门控
  v
[HUMAN REVIEW]
  |-- 暂不提交 ----------> [KB UPDATE] -> [TRACK4] -> [DONE]
  |-- 仅 commit ---------> [branch check] -> [commit] -> [KB UPDATE] -> [TRACK4] -> [DONE]
  \-- commit + push -----> [branch check] -> [commit/push] -> [KB UPDATE] -> [TRACK4] -> [DONE]
```

## 开源仓库映射与落地判断

结论：目前没有一个开源仓库能完整覆盖[[SDD 快手落地规范]]里的 ESP-SDD 流程。原因是这套流程不只是“规格驱动开发”，还包含了企业内部 Wiki 读取、业务黑话解析、多仓工作区、低码/大运河链路、MCP 调度、知识库回写、人工 gate 和归档策略。

更合理的判断是：可以用开源项目组合出 70% 左右的骨架，再补一层业务工作流封装。

| 开源项目                                                                 | 最适合承担的环节            | 和 ESP-SDD 的对应关系                                                                                     | 适配度 |
| -------------------------------------------------------------------- | ------------------- | --------------------------------------------------------------------------------------------------- | --- |
| [OpenSpec](https://github.com/Fission-AI/OpenSpec)                   | 规格资产与变更生命周期         | 对应 `proposal.md`、`design.md`、`specs/`、`tasks.md`、`archive`；适合做 Phase 2 和 Phase 4 的规范底座              | 高   |
| [Superpowers](https://github.com/obra/superpowers)                   | Agent 执行纪律与 TDD 工作流 | 对应 brainstorming、writing-plans、subagent-driven-development、verification；适合做 Phase 1、Phase 3 和验证前置约束 | 高   |
| [GitHub Spec Kit](https://github.com/github/spec-kit)                | 从 0 到 1 的项目规格化      | 强在 constitution、specify、plan、tasks；适合新项目或新模块，不太像 ESP-SDD 这种存量多仓改造流                                  | 中   |
| [BMAD Method](https://github.com/bmad-code-org/BMAD-METHOD)          | 多角色 Agent 协作和敏捷流程   | PM、Architect、Developer 等角色拆分更完整；适合借鉴“多 Agent 协作”和流程编排，但比 ESP-SDD 更重                                 | 中   |
| [Agent OS](https://github.com/buildermethods/agent-os)               | 项目规范、代码库标准和 spec 生成 | 适合沉淀 `standards`、项目约定、规范注入；可补足 ESP-SDD 的 rules/knowledge 层                                          | 中   |
| [Task Master AI](https://github.com/eyaltoledano/claude-task-master) | PRD 到任务拆解与任务状态管理    | 更偏 task management，可替代或增强 `tasks.md` 的拆分、依赖、进度追踪；但不是完整 SDD                                          | 中低  |
| [Kiro](https://github.com/kirodotdev/Kiro)                           | 产品级 SDD IDE 思路参考    | 有 Specs、Hooks、Steering、MCP、Powers 概念，和 ESP-SDD 很像；但更像产品入口/文档仓，不适合作为开源流程底座                           | 参考  |

> [!tip] 推荐组合
> 如果目标是复刻这套 SDD 开发流程，优先用 `OpenSpec + Superpowers + 自定义业务 Skills/Commands`。OpenSpec 管“规格是什么、变更如何归档”，Superpowers 管“Agent 怎么按工程纪律执行”，自定义层负责“读 Wiki、多仓调度、低码预判、MCP 调用、知识库回写”。

### 可以怎么落地

最小可行版本可以先做一个轻量 SDD 工作区：

```txt
sdd-workspace/
├── .claude/
│   ├── commands/sdd/
│   │   ├── proposal.md
│   │   ├── spec.md
│   │   ├── implement.md
│   │   └── archive.md
│   └── skills/
│       ├── domain-glossary/
│       ├── repo-map/
│       └── verification/
├── openspec/
│   ├── changes/
│   └── archive/
├── knowledge/
│   ├── rules/
│   └── wiki/
├── repo/
└── sdd-state.json
```

分阶段看：

1. Phase 1 需求收敛：直接复用 Superpowers 的 brainstorming，输出 `proposal.md`。
2. Phase 2 规格生成：用 OpenSpec 的 propose/change 结构，生成 `design.md`、`specs/`、`tasks.md`，再补业务 Wiki/代码定位/低码预判。
3. Phase 3 执行实现：用 Superpowers 的 writing-plans 和 subagent-driven-development，先产出 `impl-plan.md`，再按任务执行。
4. Phase 4 验证归档：用 OpenSpec archive 管变更归档，用 Superpowers verification 管测试、CR、回归检查，再补知识库回写。

### 判断

如果是个人或小团队，没必要一开始复刻 ESP-SDD 的完整企业形态。最值得先做的是三件事：

- 把 OpenSpec 作为规格资产目录，保证需求、设计、任务、归档可追溯。
- 把 Superpowers 作为执行协议，避免 Agent 直接 vibe coding。
- 写一层薄的 commands/skills，把自己的业务知识、仓库地图、验证命令、常见坑注入进去。

真正难的不是选框架，而是业务上下文工程化：哪些 Wiki 必须读、哪些仓库可能动、哪些低码配置会联动、哪些验证命令必须跑、哪些经验要沉淀回知识库。这部分没有通用开源仓库能直接替你完成，只能基于上述开源底座做本地化封装。
