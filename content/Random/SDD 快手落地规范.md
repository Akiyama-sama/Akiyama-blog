---
date: 2026-06-18
tags:
aliases:
private: true
---

# ESP-SDD：磁力金牛前端团队级多仓SDD研发模式

> 来源：<https://docs.corp.kuaishou.com/d/home/fcAC57PsBUdVrciRBjfge_tLf>
> 同步时间：2026-06-18

磁力金牛前端研发团队 2026-Q2

磁力金牛前端团队 2026-Q2 推出的本地化规格驱动（SDD）研发模式实践。文章在 OpenSpec + Superpowers 初步试用基础上，系统构建"需求理解、技术规约、执行出码、验证归档"四阶段标准化Workflow，打通全码与低码（大运河）多仓协作链路，并配套统一工作区、Skill 体系、知识工程与自动化质量保障，为团队提供可复用的 AI工程化范式。
## 一、前言
规范驱动的AI研发模式升级
随着AI编程工具能力的持续迭代与增强，一些共性问题在实践中逐渐浮现：如需求常常散落在需求群、PRD、评论或口头沟通中，开发者将零散的描述抛给AI助手开始编码，就是是所谓的Vibe Coding。短期内，Vibe Coding 确实能带来研发效率的提升，但部分共性问题可能也因此被掩盖或延迟暴露，例如：
- 需求理解偏差导致返工：开发者基于个人理解向助手下达指令，缺少输入信息的充分对齐（PRD、设计稿、后端接口等）。
例如：在推广列表中新增消耗列，AI在table中增加了列，直接读取record.cost展示；但联调/提测时发现：PRD中单位要求保留两位数字、支持排序功能、增加权限控制、列宽、对齐方式等情况，都需要继续对齐/返工。
- 上下文容易流失：技术选型、对话决策过程以及代码中兜底分支、特殊处理的背景，往往只存在于当时与助手的多轮对话里，会话结束即丢失。
    例如：后续回溯"为何采用前端分页"、"这段 if (xxx) 为什么要兜底"时缺乏可回溯的记录。团队中无法形成可复用的资产，新同学接手时也无法判断历史逻辑的合理性，只能保守保留，技术债持续累积。
- 需求拆解依赖个人经验：交付的质量高度依赖个人经验&需求理解&拆解粒度，团队整体水位难以稳定，Code Review 阶段反复补漏，形成隐性返工。
例如：部分开发者会将需求进行细粒度拆解为接口契约、状态流转、异常处理、埋点、权限等等维度后再交付AI助手执行；部分同学可能倾向于直接描述功能，导致产出覆盖度不足，整体质量难以稳定。     
总结：生成的代码偏离预期、遗漏边界场景、无法与存量代码库兼容——我们把时间从「写代码」转移到了「改 AI 写的代码」上。

### 第一阶段：代码补全时代
核心特征是局部优化——AI 仅聚焦于当前光标位置，提供单行或单词级别的补全建议。它主要缓解“手动输入繁琐”的问题，本质上仍属于高级自动补全工具。
### 第二阶段：辅助编程时代
AI 能够基于注释生成完整函数，理解上下文并主动推断开发意图，同时提供多个结构合理、语义清晰的候选方案供开发者选择与调整。
### 第三阶段：VibeCoding 时代
开发者以自然语言描述目标意图，通过运行结果而非逐行审查代码来验证实现效果；借助多轮对话持续迭代，直至达成预期目标。
### 第四阶段：规范式驱动 时代
在日常开发中，我们很快发现纯VibeCoding无法满足工程化要求，于是开始在Prompt中主动加入编码规范、命名风格、架构约束、异常处理模式等具体规则。通过持续扩充Prompt中的约束条件，让AI生成更符合团队标准的代码。但在企业级场景下，如何确保AI生成代码的可靠性、可维护性和合规性，仍是重大挑战。此时，规范驱动编程被提了出来。

### 1.1 什么是SDD？
规范驱动开发（Spec-Driven Development，SDD）是一种软件开发方法论，其核心理念是：在编写任何代码之前，先定义完整、清晰的规范文档，将其作为 AI Agent 进行代码生成、测试与验证的"可执行契约"。文档不是“写完就扔”的摆设，而是整个开发过程的唯一事实来源。

传统 AI 开发模式：
用户描述需求 → AI 直接写代码 → 用户检查 → 不对 → 重来
SDD 模式：
用户描述需求 → 生成规范文档 → AI 按规范实现 → 按规范验证
用户描述需求 → 生成规范文档 → AI 按规范实现 → 按规范验证

### 1.2 SDD的价值？
规范驱动开发的核心，是为开发者与 AI 之间的协作建立明确的「契约」——不绑定特定 AI 工具，可无缝融入现有开发流程。它通过结构化的 Markdown 文件作为单一真相源，将模糊的聊天式需求转化为可审查、可追溯的工程计划。

| 痛点 | Vibe Coding | SDD |
| --- | --- | --- |
| 需求易漂移 | 边聊边写，半小时后已偏离原始诉求 | proposal/spec 落盘，每一步对齐文件 |
| 上下文易丢失 | 会话超长、/clear 后从零开始 | 文件即状态，任意时刻断点恢复 |
| 结果不可审查 | AI 直接动代码，Review 只能看 diff 猜意图 | spec → tasks → code 三段可追溯 |
| 协作无契约 | 人和 AI、AI 和 AI 之间没有交接物 | Markdown 契约即交接物，跨工具通用 |

SDD 带来的四个核心价值：
- 文件即约定，跨工具通用：所有产物均为普通 Markdown，不依赖特定 AI 工具，可直接阅读评审；
- 需求实现可追溯：代码可追溯至需求，需求可追溯至决策，可定位问题出在需求、设计还是实现环节；
- 断点恢复：进度持久化到本地目录，会话清空后能自动从断点继续，不用担心上下文内存问题；
- 人机/机机协作的统一语言：人与 AI 在关键阶段清晰审阅，AI 之间通过 tasks.md 切分边界，按文件交接，不依赖会话上下文。

### 1.3 主流SDD方案
业界主流的 Spec 方案有 OpenSpec、Speckit 以及 Superpowers。协作关系可以这样理解：

| 维度 | OpenSpec | Speckit (Spec-Kit) | Superpowers |
| --- | --- | --- | --- |
| 背景 | Fission AI 团队（社区项目） | GitHub 官方开源，69.1k ⭐ | Prime Radiant 团队，Anthropic 插件市场认证，42k ⭐ |
| 一句话定位 | 聚焦变更管理的规范驱动开发工具，通过结构化文档将每次变更拆解为提案、任务清单和规范差异，重点解决“改了什么”及“改完是否合规”的问题 | GitHub 推出的 0→1 新项目规格驱动开发框架，通过核心原则、需求规格、技术方案、任务拆解四步流程，重点解决新项目“从哪里开始建”及“如何统一规范”的问题 | 为 AI 注入工程纪律的 skills 工作流框架，强制要求 AI 执行先规划、再编码、后测试的完整软件工程闭环，重点解决“AI 该怎么干活”的问题，确保产出质量和可控性 |
| 核心理念 | 将 spec 变成代码库里的长期资产，强调轻量、可持续更新 | 先写规范再编码，强制定义“项目宪法” | 强制执行 TDD 循环，确保每一行代码都有测试验证 |
| 核心工作流 | 3 阶段：propose → apply → archive | 5 阶段：constitution → specify → plan → tasks → implement | 3 阶段：brainstorming → writing-plans → subagent-driven-development |
| 最佳适用场景 | Brownfield 项目：已有代码库，需要增量迭代、持续变更 | Greenfield 项目：从零开始的新项目，需要先定规矩再写代码 | 质量敏感项目：任何需要长期维护、对代码质量有高要求的项目 |
| 推荐团队规模 | 1-5 人小团队或个人 | 10 人以上大型团队 | 不限，但对质量要求高的团队更受益 |
| 上手难度 | 低，开箱即用，一行命令安装 | 较高，需要学习完整的 5 阶段工作流 | 中等，需要适应 TDD 节奏，但有清晰的指引 |
| 许可证/价格 | 免费，MIT 开源 | 免费，MIT 开源 | 免费，MIT 开源 |
| 技术栈 | Node.js / npm | Python / uv 包管理器 | 插件式，原生支持 Claude Code，兼容 Cursor 等 |
| 风格类比 | 灵活敏捷派，边做边调整 | 严谨规范派，未雨绸缪 | 质量把控派，每一步都有检查点 |
| 核心产出 | 变更提案文档（proposal.md / design.md / specs/*.md / tasks.md） | 项目宪法 + 功能规范 + 技术计划 + 任务清单 | 执行计划 + TDD 循环 + 代码审查记录 |
| 核心优势 | 轻量、灵活、适合快速迭代 | 规范一旦定好，AI 执行稳定，团队协作统一 | 强制执行 TDD，杜绝“先写代码后补测试” |
| 核心短板 | 轻量意味着约束力较弱，大团队易出现规范不一致 | 前期投入大，小项目“杀鸡用牛刀”；Python 技术栈对前端不够友好 | 不适合快速原型开发；TDD 节奏需要适应期 |

这些工具虽然都属于“规范驱动开发”的范畴，但关注的是三个不同层级的东西：
- OpenSpec 关注的是规范的增量管理和轻量落地——相当于管理每一次变更。
- Speckit 关注的是规范体系的完整性和治理——相当于给项目定宪法。
- Superpowers 关注的是规范落地的执行纪律——相当于确保施工队按图施工。
这三种工具，可以单独使用，也可以搭配使用：

| 场景 | 推荐方案 | 案例/描述 |
| --- | --- | --- |
| 多人协作需求，需要质量保障 | SDD（OpenSpec + Superpowers） | 适合影响范围较大、需要评审或长期维护的需求，例如新增核心业务流程、改投放策略、跨模块联调；先用 OpenSpec 固化需求和验收标准，再用 Superpowers 拆计划、实现、验证和代码审查。 |
| 提供思路（如 bugfix、检索、方案设计等） | `brainstorming` / `superpowers:brainstorming` | 适合还没确定怎么做的探索阶段，例如定位线上 bug 根因、梳理代码入口、比较技术方案、设计重构路径；重点产出问题拆解、可选方案和风险点，不急着写代码。 |
| 从零开始的新项目，希望建立严谨规范 | Speckit | 适合新仓库、新应用或基础平台从 0 到 1，例如搭建管理后台、组件库、AI 工具链；先生成需求、架构、任务拆解和工程规范，给后续 AI 编码和多人协作提供统一上下文。 |
| 简单需求 | Vibe Coding | 适合低风险、小范围改动，例如改文案、调样式、补一个简单校验、写一次性脚本；直接描述目标，让 AI 修改并做基础验证即可。 |

基于我们的业务特点，应该优先选择 OpenSpec（定义规范）+ Superpowers（TDD 执行）的方案。

## 二、方案设计
### 2.1 核心挑战和应对思路
基于以上技术选型（Openspec+Superpower），在真实业务中进行了试点&试用，在试用过程中，发现了一些困难和不符合预期的情况：
试点记录：<https://docs.corp.kuaishou.com/k/home/VR5VotKJZsfg/fcADCiCgaEiec7It17JegIEN8>

| 挑战                                                                                                                       | 应对                                                            |
| ------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------- |
| 团队内难以形成标准化的统一流程。指令多、试用组合多（20+命令），对于没使用过的同学来说，有一定上手成本；此外还有部分工具中的状态/流程衔接问题（如 OpenSpec 生成的 `tasks.md`，Superpower 不会默认翻转打标）。 | 基于业务场景需要，封装、定制化工作流，为研发同学实际使用提供高阶的一键式指令，无需过多关注内部实现。            |
| 大量配置化场景（低代码、大运河）在 SDD 中的集成难点。金牛业务中存在较多低码联动场景（投放平台配置化渗透率 44.12%，近半数需求涉及低码改造）。                                             | 建设低代码 SDD 子链路，包含 MCP、Skills 工具集、大运河 Agent 联动，并无痛融入主 SDD 工作流中。 |
| 多仓变更的调度问题。ESP 前端常用仓库 6 个（2 个业务仓库、1 个客服仓库、2 个组件库），其中 50%+ 的需求涉及最少 2+ 个仓库改动。                                               | 建立标准化金牛研发工作区，在同一上下文内实现多仓的统一调度与管理。                             |

磁力金牛前端核心仓库列表
- ESP仓库："https://git.corp.kuaishou.com/ks-ad/ad-fe/kuaishou-frontend-esp.git"
- 创编仓库："https://git.corp.kuaishou.com/ks-ad/ad-fe/efe/kuaishou-frontend-esp-create.git"
- 磁力小牛："https://git.corp.kuaishou.com/ks-ad/ad-fe/marketing-profs/dsp/kuaishou-frontend-ad-robot"
- 移动端仓库（旧）："https://git.corp.kuaishou.com/ks-ad/ad-fe/efe/esp-mobile.git"
- 低代码组件库："https://git.corp.kuaishou.com/ks-ad/ad-fe/efe/esp-lowcode-components.git"
- 创编组件库："https://git.corp.kuaishou.com/ks-ad/ad-fe/marketing-profs/dsp/tech/ad-create-comps.git"    解法/思路：建立标准化金牛研发工作区
在同一上下文内实现多仓的统一调度&管理结合现存问题，我们启动了 ESP-SDD 工作流设计，将实现上述提到的三类功能诉求：定制业务工作流、支持低代码调度，同时落地适配研发模式的多仓工作区管理。

### 2.2 整体方案设计
对ESP-SDD的一句话总结：基于一个不断成⻓的规范知识体系，实现符合ESP研发特性的规范驱动研发范式。

设计思路：
- 需求开发流程：使用 OpenSpec 来定义开发规范，并通过 Superpower 完成 TDD（测试驱动开发）执行，实现以变更为核心的规范驱动编码流程。
- Skill 体系沉淀：通过沉淀业务和流程的 Skill 体系，提供“知识性约束”，确保每个环节的输出符合团队规范。同时，传递业务开发经验与最佳实践，减少模型对上下文理解的成本，提升效率。
- 融合低码场景：深度应用大运河，实现与大运河 AI 的联动，推动与全码的融合。大运河通过提供子任务 agent，由 Superpower 主流程根据需要动态调度，确保任务高效执行。
- 领域知识沉淀：基于自更新知识库设计，持续沉淀领域知识，构建更加完善的知识体系。

## 三、方案落地
### 3.1 统一工作区
使用方式：首次使用 `espsdd` 时，执行环境初始化，会自动生成完整的 `espsdd` 工作区，可快速开启开发。

```bash
# 拉取仓库代码
git clone https://git.corp.kuaishou.com/ks-ad/ad-fe/efe/kuaishou-frontend-esp-sdd.git

# 以交互模式运行
myflicker

# 执行初始化&更新指令（SDD 环境依赖检查与安装，首次大约 2 分钟）
```

执行过程与结果

```text
目录结构
kuaishou-frontend-esp-sdd/        ← SDD 主仓（用户克隆的入口）                                                                                                                  
├── .claude/                                                                                                                                                                    
│   ├── commands/espsdd/          # 7 个 SDD 子命令（setup/start/proposal/...）                                                                                                 
│   ├── skills/                   # 12 个内置 Skill（业务黑话/边界认知/低码下发等）                                                                                             
│   ├── mcp/                      # MCP 配置说明                                                                                                                              
│   ├── tools/                    # 环境脚本（check-deps.sh / clone-repos.sh）                                                                                                  
│   └── espsdd-state.json         # 环境就绪标记（.gitignore，本地生成）                                                                                                      
├── core/                         # @ad/espsdd CLI 工具源码（TypeScript）                                                                                                       
├── openspec/changes/             # 变更产物（proposal/spec/tasks/plan-ready）      
├── knowledge/                    # 知识工程
│   ├── rules/                    # 项目规范知识
│   ├── wiki/                     # 业务知识
│    ├── index.md                         # 业务知识（入口映射）
│    └── {module}/                        # 模块（创编/推广/首页/报表等）
│       ├── index.md                      # 业务知识内容
│       └── {submodule}.md                # 子模块（如推广模块下的概览、审核、素材等子模块）
├── repo/                         # 业务仓库聚合目录（.gitignore，setup 时拉取）                                                                                                
│   ├── kuaishou-frontend-esp/            # 投放管理（全码，前端必需）                                                                                                          
│   ├── kuaishou-frontend-esp-create/     # 广告创建（全码，前端必需）                                                                                                          
│   ├── esp-mobile/                       # 移动端（全码，前端必需）                                                                                                            
│   ├── esp-lowcode-components/           # 低码组件库（前端必需）                                                                                                              
│   ├── ad-create-comps/                  # 创建组件库（前端必需）                                                                                                              
│   ├── kuaishou-frontend-ad-robot/       # 智能投放（前端必需）                                                                                                                
│   ├── ad-ecom-esp/                      # 后端服务（可选，接口对照用）                                                                                                        
│   └── ad-esp-promotion-api/             # 后端 API（可选，接口对照用）                                                                                                        
├── CLAUDE.md                     # 项目级上下文（USER_CODE / Canal MCP，.gitignore）                                                                                           
└── README.md
```

设计说明：把"分散在多个仓库 + 多种工具链 + 多份本地配置"的 ESP 研发环境，收敛到一个根目录内：
- 多仓统一调度：业务代码（前端6仓 + 后端2仓）统一拉到 repo/ 子目录，主仓库 .gitignore 屏蔽，各子仓保留独立 git 追踪；AI工具可同时调度多仓改动。
- 工具链内嵌，仓库内共享：Claude Code 命令、Skills、MCP 配置、状态文件全部以文件形式落在 .claude/ 下，跟随主仓版本化。
- 状态/Spec本地化管理：核心状态管理，包含环境标记（espsdd-state.json）、用户标识（CLAUDE.md）、基于OpenSpec的规范（openspec/changes/），会话 /clear 后无缝恢复。

### 3.2 SPEC沉淀
为了保证spec中信息的完整性，并且及时更新，我们需要重新审视AI时代研发的操作对象，从以代码为中心转到以spec为中心，code是spec生成的产物。基于这个原则，我们除了能进一步提升代码生成的比例外，还可以基于spec生成uat（用户验收测试）文档，验证生成code的质量。还可以做到系统描述和实现平台、技术的解耦，比如用AI生成另一种语言实现、在其他平台运行的产品。
本项目中的核心原则如下：
- 从代码为中心→spec为中心：代码从核心关注点变成spec的生成产物；
- spec+uat维护方式：人工主导+AI辅助，人来负责描述清楚产品目标以及交付标准；
- 代码维护方式：AI主导+人工Review，AI生成提效，人工Review保障整体流程和高风险代码的实现质量。
每个变更在 `openspec/changes/<变更名>/` 目录下形成完整的生命周期产物。这个目录设计的核心思路是：文件即状态。所有进度以文件形式落盘，不依赖 AI 的会话记忆，任意时刻 `/clear` 会话后都能通过文件恢复断点。

```text
openspec/changes/<变更名>/
├── proposal.md      需求收敛：背景、功能点、边界拆分
├── design.md        技术设计：关键决策、风险、迁移方案
├── specs/
│   ├── <能力A>/spec.md   全码规格（WHEN/THEN 场景）
│   └── <能力B>/spec.md   低码规格（WHEN/THEN 场景）
├── tasks.md         任务清单（[code]/[canal]/[manual] 标签）
├── plan-ready.md    执行翻译层（供阶段三直接使用）
└── impl-plan.md     执行计划（build 阶段生成，断点恢复依赖此文件）
```

归档后：变更目录移入 `openspec/changes/archive/`，规格合并到 `openspec/specs/`，形成持续积累的规格知识库。

### 3.3 标准化Workflow
分为四个子阶段独立使用，也可以通过 `/espsdd start` 全程驱动：

| 阶段 | 命令 | 产出物 |
| --- | --- | --- |
| 一、需求理解 | `/espsdd proposal` 或 `/espsdd brainstorming` | `proposal.md` |
| 二、技术规约 | `/espsdd spec` | `design.md` + `specs/` + `tasks.md` + `plan-ready.md` |
| 三、执行&出码 | `/espsdd build` | `impl-plan.md` + 代码实现（git staged） |
| 四、归档 | `/espsdd close` | 在 `archive` 目录中归档工作流产物 |

工作流全景：

1. 需求理解
   Quick 模式：`/espsdd-proposal`
   - [通用] 识别输入类型（确认上下文是否完整）
   - [定制] 调用工具 `team_get_task`、`docs_read`
   - [通用] 判断是否需要拆分（控制粒度）
   - [通用] 确认需求，提出关键问题（做什么、为什么、标准、边界、约束）
   - [封装] 创建 OpenSpec 变更（调用 `/openspec new`）
   - [通用] 提示下一步

   Deep 模式：`/espsdd-brainstorming`
   - 用于需求模糊、方案探索、需要深度设计对话的情况。

   产出物：`openspec/changes/<变更名>/proposal.md`

2. 技术规约
   指令：`/espsdd-spec`
   - [通用] 文档存在性检测
   - [通用] 确认活跃变更
   - [定制] 低码 Agent
     - 低码认知：低码入口识别 → 查询大运河模块 → 边界认知
     - 识别组件改造场景
   - [封装] 调用 OpenSpec 生成规格（调用 `/openspec propose`）
   - [定制] Spec 完成度自审
     - PRD 覆盖率检查（基于 `prd-checklist.md`）
     - 3.2 规范一致性检查
     - 3.3 `[canal]` 任务完整性检查（涉及低码时）
   - [通用] 生成 `plan-ready.md`（翻译层）
   - [通用] 与用户确认并提示下一步

   产出物：`proposal.md`、`design.md`、`specs/`、`tasks.md`、`plan-ready.md`

3. 执行&出码
   指令：`/espsdd-build`
   - [通用] 检测执行前置文件
   - [通用] 生成 `impl-plan.md`
   - [通用] 根据 `[code]` / `[canal]` / `[manual]` 分类执行
     - `[code]` 调用 Superpowers 执行全码任务
     - `[canal]` 调用低码 Agent 执行大运河任务
     - `[manual]` 生成人工待办
   - [通用] 回写任务状态
   - [通用] 汇总执行结果

   产出物：`impl-plan.md`、git staged 改动、大运河任务回执

4. 验证归档
   指令：`/espsdd-close`
   - [通用] 运行校验（类型检查、测试、规格一致性）
   - [通用] 更新 OpenSpec 状态
   - [封装] 调用 `openspec archive`
   - [通用] 提示提交/归档完成

#### 3.3.1 需求理解阶段
##### 1) 建立标准化的需求理解
对于不同需求复杂度，分别通过 /proposal 和 /brainstorming 来实现标准化理解。简单需求走快速收敛，复杂需求走深度对话，最终都落盘成 proposal.md。

##### 2) 对需求内容进行准确描述
这个阶段的目标不是“立刻写代码”，而是让 AI 明确知道：需求背景、目标用户、验收标准、边界场景、依赖文档是什么，并将结果以结构化文档沉淀下来。

#### 3.3.2 技术规约阶段
##### 1) 代码关联度建立
AI 会自动扫描本地代码入口，把需求和实际模块建立关联，尤其是需要变更的页面、服务、store、组件。

##### 2) 后端仓库关联
如果需求涉及接口字段、服务端逻辑或联调，工作流允许同时关联后端仓库，在统一工作区内补齐上下文，避免只看前端表象。

##### 3) 低代码（大运河）场景识别
当代码中扫描到低码插槽或低码宿主时，会自动识别这是大运河场景，把低码模块纳入后续规格和任务调度。

##### 4) 多仓场景标记
对于跨仓需求，tasks.md 会显式拆分每个仓库的任务边界，便于后续 AI 并行执行和人工 review。

#### 3.3.3 执行&出码阶段
##### 1）出码约束：使用 Andrej Karpathy Skills（Git Star 153k）作为基础规范
在执行阶段引入 Skills 体系，强制 AI 先做需求理解、计划、验证，再真正开始代码改动，避免“一把梭”式出码。

##### 2) 用例先行（TDD）
通过测试先行和规格驱动，要求每一项变更都能映射到可验证的场景，减少实现偏差。

##### 3) 多轨并行执行&断点恢复机制
可将多个 [code]/[canal]/[manual] 子任务并行推进；一旦中断，也能基于 impl-plan.md 和 tasks.md 从断点恢复，不依赖长会话上下文。

##### 4) 自动化质量保障
类型检查、测试、规格一致性校验会作为阶段收尾动作统一执行，确保产出不是“能跑就行”，而是可交付状态。

#### 3.3.4 归档阶段
归档不仅是把变更收起来，还包括：规格合并、历史沉淀、知识库更新以及为后续需求复用保留检索入口。

### 3.4 低码链路集成
#### 3.4.1 架构全景
ESP-SDD 不把低码视作一个“额外平台”，而是把它纳入主研发链路，在全码、低码、大运河 Agent 之间形成统一调度。

#### 3.4.2 低码集成-Skill体系
在SDD流程中,通过一系列skill，完成低码任务的调度和交付。

| 边界 Skill  | 能力                                                                                                                     |
| --------- | ---------------------------------------------------------------------------------------------------------------------- |
| 全码、低码边界认知 | 结合本地代码（低码入口扫描）+ PRD 需求点 + 规则集，逐条判断归属全码还是低码，产出任务边界拆分清单及全码向低码注入的接口约定。                                                    |
| 低码入口认知    | 在探索本地代码过程中，一旦遇到 `AdCreateReactRuntimeFC` 等低码插槽即识别为低码入口，提取 `moduleId`、`domainCode` 及 `params` 四分组结构，作为后续边界认知和接口约定的基础输入。 |

| 查看 Skill | 能力 | 整体设计 |
| --- | --- | --- |
| 低码模块总结 | 通过探索到代码中的 `moduleId`，使用 MCP 调用低码 Agent 总结模块视图、逻辑、能力等层面信息，为后续需求判别低码、全码等环节提供统一的低码模块认知基础。 | 低码模块调度流程图 |
| 低码组件能力预判 | 针对某个功能、交互需求点，调用 MCP 询问低码 Agent 模块内现有组件是否能满足需求，最终决定直接下发低码任务，还是先开发组件再发布任务。 | 组件和需求的匹配度判断 |

| 执行 Skill | 能力 | 整体设计 |
| --- | --- | --- |
| 升级低码组件 | 所有低码组件 `pnpm sync` 发布完毕后，统一批量调用 MCP 将低码平台中的业务组件同步到最新物料版本。 | `esp-sdd` 调度低码组件的发布和组件物料版本更新。 |

更新过程：
- 组件批量升级时序
- 组件升级详细流程

### 3.5 知识工程
#### 3.5.1 整体架构
知识工程的目标不是把资料“堆起来”，而是构建一个能在需求阶段、规格阶段、执行阶段都被 AI 直接读取和复用的领域知识系统。

#### 3.5.2 知识类型
知识可分为几类：
- 规则类：编码规范、工程约束、命名约定、项目上下文；
- 技术类：组件能力、渲染机制、状态管理、基础设施经验；
- 业务类：模块说明、页面结构、场景规则、业务黑话；
- 变更类：需求决策、规格演化、历史坑点、已知兼容约束。

知识卡片建议包含的维度：

| 模块/场景 | 用途 |
| --- | --- |
| 业务背景 | 这个模块解决什么问题，面向谁 |
| 页面结构 / 交互流程 | 按用户操作时序描述（每步附代码引用） |
| 对外 API / Store / Model / Hook | 供其他模块使用的导出项 |
| 跨模块依赖 | 引用了哪些外部 store / 组件 / service |
| 已知坑点 / TODO | `FIXME` / `HACK` / `WARNING` / 历史决策 |

#### 3.5.3 知识目录&层级体系
直接集成在 `espsdd` 工程下，实现 SDD 工作流复用，并提供 skills，支持三方服务调用。

```text
esp-vertical-knowledge/                ← 独立 Git 目录
├── AGENTS.md                          ← AI 行为规范（ingest / query / lint）
├── index.md                           ← 全景目录（AI 入口，触发词 → 模块路径）
├── log.md                             ← 操作日志（append-only）
├── rules/                             ← 规范层（始终注入）
│   ├── coding-style.md                ← 编码规范
│   ├── domain-rules.md                ← 业务领域约束
│   └── project-context.md             ← 工程结构、技术栈、核心依赖
├── tech-wiki/                         ← 技术知识层（跨业务通用，团队级共享）
│   ├── index.md                       ← 技术主题索引
│   └── {topic}.md                     ← 通用技术经验（如组件库、监控、构建、性能优化等）
└── wiki/                              ← 业务知识层（AI 读写，垂类知识主体）
    ├── index.md                       ← 模块清单（模块名 + 触发词 + 路径）
    └── {module}/                      ← 业务模块（如 manage / capital / home）
        ├── index.md                   ← 子模块清单 + 触发词路由
        └── {submodule}/               ← 子模块（目录，如 store-wide / standard）
            ├── index.md               ← 子模块入口 + 知识条目清单
            └── {topic}.md             ← 具体知识条目（如推广状态列、推广设置列）
```
说明：业务模块下的子模块采用目录形式，目录内可拆分多个知识条目文件。例如「全店推广」子模块（wiki/manage/store-wide/）下可拆分推广状态列、推广设置列、推广调控列等独立知识文件，避免单文件过长。

#### 3.5.4 知识使用和自迭代
在 SDD 归档流程中（执行 /espsdd close 命令），引入需求生命周期管理机制。以需求为基本单位，自动触发拆解动作：
整个自迭代流程为：
1. 将需求拆解为原子化的业务知识单元：拆解后重建对应的业务知识库条目；
2. 遵循原子化更新：每次仅变更受影响的最小知识片段，确保业务知识库始终与最新需求状态保持一致；
3. 原始知识库对比和冲突检测，若在更新过程中检测到冲突（如原子化单元内容不可自动合并，或相同标识的知识单元出现逻辑矛盾），则暂停该条目的自动更新，记录冲突详情，并触发人工判断

产出业务知识（起草agent + 审查agent配合使用），更新到对应模块的wiki中

┌─────────────────────────────────────┐    ┌─────────────────────────────────────┐                                            
│  Step 2-A：起草方 Agent              │    │  Step 2-B：审查方 Agent              │                                          
│  （subagent_type=GeneralPurpose）    │    │  （subagent_type=GeneralPurpose）    │                                          
│                                     │ →  │                                     │                                            
│  独立产出 diff JSON                  │    │  挑错 + 补漏，输出审查结果            │                                         
│                                     │    │                                     │                                            
│  产出规则：                          │    │  产出规则：                          │                                          
│  ✓ 必须读 tasks.md 涉及的代码文件     │    │  ✓ 必须 read 起草方 ref 的代码行     │                                         
│  ✓ 每条 add/update 附 file:line     │    │    验证真实性，附 evidence           │                                           
│  ✓ 每条条目附 linkedTask（关联 tasks）│    │  ✓ 对照变更产物找起草方遗漏          │                                         
│  ✓ 对比现有 wiki，输出新增/修改/废弃   │    │    （additions 同样附 ref+linkedTask）│                                       
│  ✓ 仅返回 JSON，不直接写 wiki         │    │  ✓ 校验 oldSnippet 真在现有 wiki 中  │                                         
│  ✗ 禁止凭 proposal/spec 写结论       │    │  ✓ 术语对齐「磁力金牛业务黑话」       │                                         
│  ✗ 禁止跨模块读源码                  │    │  ✓ rejected 必须给出 evidence        │                                          
│                                     │    │  ✗ 禁止只看 JSON 不读代码           │                                            
│  输出：                              │    │  ✗ 禁止直接修改起草方 diff          │                                           
│  { module, subFile,                 │    │                                     │                                            
│    adds[], updates[],               │    │  输出：                              │                                           
│    deprecates[], openQuestions }    │    │  { approved[],                      │                                            
│  每条含 ref + linkedTask             │    │    rejected[]: {item, reason,       │                                           
│                                     │    │      evidence?},                    │                                            
│                                     │    │    additions[]: {ref, linkedTask}}  │                                            
└─────────────────────────────────────┘    └─────────────────────────────────────┘        

## 四、需求落地 - 以净成交ROI引导需求为例
此章还原了一次真实的 SDD 开发过程。你会看到：开发者输入了什么、AI 回应了什么、每一步的操作逻辑是什么。读完之后，你应该能直接上手用 SDD 做自己的需求。
（原文 @ 杨奇）
<https://docs.corp.kuaishou.com/d/home/fcABmcLML98rPiba-lRV0ZhCz>

- 需求基本信息
  - 需求文档（PRD）：【全站推广】净成交 ROI 平台引导_11月
  - 后端技术方案：净成交 ROI 技术方案
  - Team 任务：商业化技术需求：任务派发
  - 大运河低码任务：<https://canal.corp.kuaishou.com/change/ad.esp.create_mcp_1779259500969>

### 背景：拿到需求，直接开始
今天来了一个全站创编页的需求：在全站直播和全站商品创编时，新增净成交ROI引导卡片，帮助客户了解净成交ROI相对支付ROI的预期提升，并支持默认勾选开启。
以前的做法：自己读 PRD、找低码入口、写代码、手动下发低码任务，来回要两三天。
这次我们用 SDD 试试，全程大约花了 25 分钟。

### 第一步：需求理解
把 PRD 链接、后端方案、Team 链接一起丢给 AI，执行 /espsdd start。
🧑 你输入：

```text
/espsdd start '/Users/yangqi/kuaishou-frontend-esp-sdd/repo/kuaishou-frontend-esp-create'
帮我实现需求，需求文档 https://docs.corp.kuaishou.com/d/home/fcADh25Z7pt2pRYjJD--42eL-，
后端技术方案 https://docs.corp.kuaishou.com/d/home/fcADEYx8NySwo8QrXeJkDrA3q，
team链接：https://team.corp.kuaishou.com/task/T11540870
```

🤖 AI 回复：
已启动 ESP-SDD 规范驱动开发流程。
正在检查环境与项目状态...

╔══════════════════════════════════╗
║     ESP-SDD 四阶段总览           ║
╠══════════════════════════════════╣
║  ○ 阶段一：需求收敛              ║
║  ○ 阶段二：规格生成              ║
║  ○ 阶段三：执行实现              ║
║  ○ 阶段四：验证归档              ║
╚══════════════════════════════════╝

正在并行读取 PRD、后端技术方案、Team 任务...

扫描低码入口：
  StoreWideLive/index.tsx    → moduleId: 14e1d11e-...（全站直播）
  StoreWideProduct/index.tsx → moduleId: a73b6e47-...（全站商品）

边界拆分结果：
  [全码] 白名单类型新增 netTradeRoiGuideSwitch、netTradeRoiDefaultOnSwitch
  [全码] 封装接口 getNetRoiGuide，调用 /rest/esp/promotion/storewide/netRoi/guide
  [全码] 在直播/商品两个低码宿主文件 params.actions 中注入 getNetRoiGuide
  [低码] 全站直播模块：构建净成交ROI引导卡片 UI
  [低码] 全站商品模块：构建净成交ROI引导卡片 UI

proposal.md 已生成。

请确认下一步：
  A. 确认，进入阶段二（规格生成）
  B. 有补充，继续完善需求
  C. 需要修改，重新执行需求收敛
💡 这一步做了什么
你只需要把三个链接丢给 AI，它会自动：
1. 并行读完所有文档，提取功能点
2. 扫描工程源码，找出所有低码模块入口和对应的 moduleId
3. 根据「边界认知」规则，判断哪些任务给全码做、哪些给低码做
4. 生成 proposal.md，等你确认
确认边界拆分没问题，回复：
🧑 你输入：
确认

### 第二步：规格生成
AI 开始生成完整的技术规格文档。
🤖 AI 回复：
正在生成 design.md...
正在生成 specs/net-trade-roi-guide-code/spec.md...（4个需求，6个场景）
正在生成 specs/net-trade-roi-guide-canal/spec.md...（4个需求，11个场景）
正在生成 tasks.md...（12条任务）
正在生成 plan-ready.md...

╔══════════════════════════════════════╗
║  ESP-SDD 进度 [阶段 2/4] 规格生成   ║
╠══════════════════════════════════════╣
║  ✓ 阶段一：需求收敛（已完成）        ║
║  ✓ 阶段二：规格生成（已完成）        ║
║  ○ 阶段三：执行实现                  ║
║  ○ 阶段四：验证归档                  ║
╠══════════════════════════════════════╣
║  任务概览：[code] 6条 / [canal] 6条  ║
╚══════════════════════════════════════╝

请确认下一步：
  A. 确认，进入阶段三（执行实现）
  B. 有补充，调整规格内容
  C. 需要修改，重新执行规格生成
中途发现需求不完整？直接补充
看完规格摘要，我想起 PRD 里有一处细节没有体现：商品场景切换商品或切换投放用户时，引导卡片数据需要重新获取。于是回复 B：
🧑 你输入：
B，低码部分需要加一个描述，商品场景如果切换了商品和投放用户，需要重新获取数据。直播场景如果切换了投放用户需要重新获取数据。
🤖 AI 回复：
已更新 specs/net-trade-roi-guide-canal/spec.md：

+ Scenario: 切换投放账号重新获取数据
    - WHEN 用户切换投放账号
    - THEN 重新调用 getNetRoiGuide 获取新账号数据并更新卡片

全站商品模块 新增：
+ Scenario: 切换商品重新获取数据
    - WHEN 用户切换到不同商品
    - THEN 重新调用 getNetRoiGuide 并更新卡片

+ Scenario: 切换投放账号重新获取数据
    - WHEN 用户切换投放账号
    - THEN 重新调用 getNetRoiGuide 并更新卡片

同步更新 plan-ready.md 中的数据获取机制描述。

请确认下一步：
  A. 确认，进入阶段三（执行实现）
  B. 有补充，调整规格内容
  C. 需要修改，重新执行规格生成
💡 这一步的关键点
- 规格不是一次性的，任何时候回复 B 都可以补充，AI 会精确更新对应场景，不需要从头来过
- AI 不会把字段名写进低码规格（比如 itemId、authorId），只写业务行为（「切换商品」「切换投放账号」），字段映射由低码 agent 自己分析
- 规格文件用 WHEN/THEN 格式，每条场景都是一个潜在的测试用例
确认规格没问题，回复 A：
🧑 你输入：
确认

### 第三步：执行实现
这个阶段基本是 AI 自动跑，你喝杯茶等着就行。
🤖 AI 回复：
[1/6] packages/biz/src/fields/whiteList.ts
      → commonBooleanConfig 新增两个白名单字段 ✅

[2/6] packages/create/src/services/orientedStoreWide.ts
      → 新增 INetRoiGuideParams、INetRoiGuideData 类型
      → 新增 getNetRoiGuide 函数 ✅

[3/6] packages/create/src/services/url.interface.ts
      → 注册 '/rest/esp/promotion/storewide/netRoi/guide' ✅

[4/6] SuperCreate/StoreWideLive/index.tsx
      → import + params.actions 注入 getNetRoiGuide ✅

[5/6] SuperCreate/StoreWideProduct/index.tsx
      → import + params.actions 注入 getNetRoiGuide ✅

[6/6] 低码任务下发（批量）
      → changeId: ad.esp.create_mcp_1779259500969
      → 全站直播模块 sessionId: 529f9a60-...  ✅
      → 全站商品模块 sessionId: 80bc82b7-...  ✅

╔══════════════════════════════════════╗
║  ESP-SDD 进度 [阶段 3/4] 执行实现   ║
╠══════════════════════════════════════╣
║  ✓ 阶段一：需求收敛（已完成）        ║
║  ✓ 阶段二：规格生成（已完成）        ║
║  ✓ 阶段三：执行实现（已完成）        ║
║  ○ 阶段四：验证归档                  ║
╚══════════════════════════════════════╝

请确认下一步：
  A. 确认，进入阶段四（验证归档）
  B. 有问题，需要人工介入处理
  C. 需要修改，重新执行部分任务
💡 这一步做了什么
- 全码 5 个文件的改动全部自动完成，每个文件改了什么都有记录
- 两个低码模块一次批量下发到大运河 agent，不需要手动操作大运河平台
- 返回了 changeId，可在大运河平台追踪低码任务进度：https://canal.corp.kuaishou.com/change/ad.esp.create_mcp_1779259500969
🧑 你输入：
A

### 第四步：验证归档
🤖 AI 回复：
TypeScript 类型检查...
  变更文件零新增错误 ✅（存量错误为老问题，与本次变更无关）

specs 一致性验证...
  netTradeRoiGuideSwitch / netTradeRoiDefaultOnSwitch 已声明 ✅
  getNetRoiGuide 函数已封装 ✅
  url.interface.ts 已注册 ✅
  StoreWideLive actions 已注入 ✅
  StoreWideProduct actions 已注入 ✅

openspec archive net-trade-roi-guide...
  规格合并到 openspec/specs/ ✅
  变更归档到 openspec/changes/archive/2026-05-20-net-trade-roi-guide/ ✅

╔══════════════════════════════════════════╗
║  ESP-SDD 流程完成                        ║
╠══════════════════════════════════════════╣
║  ✓ 阶段一：需求收敛（已完成）            ║
║  ✓ 阶段二：规格生成（已完成）            ║
║  ✓ 阶段三：执行实现（已完成）            ║
║  ✓ 阶段四：验证归档（已完成）            ║
╠══════════════════════════════════════════╣
║  变更已就绪，等待人工 review 后提交      ║
╚══════════════════════════════════════════╝
最后提交代码：
🧑 你输入：
请提交代码
🤖 AI 回复：
git add（5个业务文件）
git commit -m "feat: 净成交ROI引导 - 新增白名单字段、接口封装及低码宿主注入 [T11540870]"
git push origin test-sdd ✅

创建 MR：https://git.corp.kuaishou.com/.../merge_requests/new?source_branch=test-sdd

SDD 规格仓库：
git add openspec/
git commit -m "feat: 净成交ROI引导需求规格归档 [T11540870]"
git push origin master ✅

| 效果数据对比维度 | 常规编程 | Vibe Coding | ESP-SDD |
| --- | --- | --- | --- |
| 总耗时 | ~ 2pd | ~ 2h | ~ 25min |
| 人工对话/交互轮次 | N/A | ~20 轮（人工分步拆解） | 7 轮（workflow 执行，人工核准确认） |
| 代码采纳率 | 100%（手写） | ~65%（不符合预期则重新生成） | ~95% |
| PRD/技术方案理解 | 人工通读 5 - 15min | AI 理解 1 - 5 min | AI 理解 1 - 5 min |
| 全码/低码边界判断 | 人工凭经验判断 | 人工凭经验判断，下发 AI 执行 | 自动扫描 `moduleId`，规则化拆分 |
| 低码任务下发 | 手动登录大运河逐模块创建（10-20 min） | 手动登录大运河逐模块创建（10-20 min） | 自动批量下发，返回 `changeId` |
| 规格/文档沉淀 | 无 | 无 | 自动生成 6 份 specs 并归档 openspec |
| 返工/修复轮次 | 3-5 轮 | 3-5 轮 | 0-3 轮（面向 spec） |

### 产出清单

业务代码（5 个文件，36 行新增）：

| 文件 | 变更 |
| --- | --- |
| `packages/biz/src/fields/whiteList.ts` | 新增 2 个白名单字段类型 |
| `packages/create/src/services/orientedStoreWide.ts` | 新增接口类型 + 函数 |
| `packages/create/src/services/url.interface.ts` | 注册新接口 URL |
| `SuperCreate/StoreWideLive/index.tsx` | 注入 `getNetRoiGuide` |
| `SuperCreate/StoreWideProduct/index.tsx` | 注入 `getNetRoiGuide` |

规格文档（6 份，自动生成）：

```text
openspec/changes/archive/2026-05-20-net-trade-roi-guide/
├── proposal.md       需求收敛 + 边界拆分
├── design.md         技术决策记录
├── tasks.md          12 条任务清单
├── plan-ready.md     执行翻译层
└── specs/
    ├── net-trade-roi-guide-code/spec.md    全码规格（6个场景）
    └── net-trade-roi-guide-canal/spec.md   低码规格（13个场景）
```

低码任务：2 个模块已下发大运河，`changeId: ad.esp.create_mcp_1779259500969`

## 五、未来规划
1. 基建补齐：建设ESP-SDD工作流的生态与工具链，持续提升研发体验；
2. 知识库建设：持续沉淀领域知识与最佳实践，为 Spec 生成和复用提供高质量上下文；
3. 升级 Spec 覆盖范围：把 Spec 驱动从当前场景扩展到更多业务模块与研发环节；
4. 增强Harness建设：完善承载测试执行与agent运行的统一脚手架，让 Spec 契约在自动化框架下被持续验证与回归。

磁力金牛前端研发团队 ｜ 编辑：邓荣耀 杨奇 
