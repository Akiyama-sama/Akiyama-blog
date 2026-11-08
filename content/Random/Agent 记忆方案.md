---
date: 2026-10-12
tags:
aliases:
---

> 三次调研：2026-10-12（§1–5：各家 harness **内建**记忆的四层综述）＋ 2026-10-16（§6：**第三方**跨 harness 文件持久化方案，应对"一个工作区切多个客户端"的场景；supermemory 单点深挖拆至 [[supermemory 调研]]）。

我直接抓了各家官方文档 + 几个仓库源码（curl → r.jina.ai 转 markdown，代码文件走 raw.github），市面上 harness 的"记忆"其实不是一层，而是四层，且 2025→2026 的重心明显从**人写规则**转向**agent 自己写 + 索引注入 + 按需召回 + 失效校验**：

| 层 | 干什么 | 代表 |
|---|---|---|
| L1 指令/规则文件 | 人写的持久指令，每 session 全量注入 | AGENTS.md / CLAUDE.md / GEMINI.md / `.cursor/rules` |
| L2 自动记忆 | agent 自己记、跨 session 召回 | Claude Code auto memory、Codex memory、Gemini Auto Memory、Copilot Memory、Kilo/Trae/Windsurf |
| L3 上下文压缩 | 同一问题的另一半：把窗口里的东西丢掉 | context editing、`/compact`、microcompaction |
| L4 外部记忆框架 | 可插拔的记忆服务/SDK | Letta、Mem0、Zep、LangGraph+LangMem、Anthropic memory tool |

---

## 一、CLI/IDE harness 速查

| 产品 | 指令/规则文件 | 自动记忆 | 存储位置 |
|---|---|---|---|
| **Claude Code** | CLAUDE.md（含 `@import`、嵌套目录、`.claude/rules/` 路径作用域、AGENTS.md 兼容） | ✅ auto memory，4 类 type | `~/.claude/projects/<repo>/memory/` |
| **Codex CLI** | AGENTS.md | ✅ 内建记忆库（SQLite + 后台 consolidation + 引用溯源） | 本地 state 库（memories 表） |
| **Gemini CLI** | GEMINI.md 分层（repo → 私有 → `~/.gemini/GEMINI.md`） | ✅ 实验性 Auto Memory，产出 patch/SKILL.md 候审 | 项目内 inbox + markdown 记忆文件 |
| **GitHub Copilot** | `.github/copilot-instructions.md` | ✅ Copilot Memory（repo facts + user prefs） | 云端，按 billing entity 归属 |
| **Cursor** | `.cursor/rules/*.mdc`（4 种生效模式）+ User/Team Rules + AGENTS.md | ⚠️ beta "Generate Memories" | 云端/本地（文档已并入 Rules 页） |
| **Windsurf (Devin Desktop)** | `.devin/rules/*.md`（回退 `.windsurf/rules`）+ AGENTS.md | ✅ Cascade Memories 自动生成 | `~/.codeium/windsurf/memories/`（本地、按 workspace） |
| **Cline** | `.clinerules/` | ⚠️ Memory Bank（自定义指令模式，非内建） | 仓库内 6 个 md |
| **Roo Code** | 全局/workspace 自定义指令 | ⚠️ 社区方案（官方页已 404） | `memory-bank/` 目录 |
| **Kilo Code** | `.kilo/rules/` → **已废弃，转 AGENTS.md** | ✅ Kilo Memory（opt-in，产品化最完整） | `~/.local/share/kilo/memory/<slug>-<sha1>` |
| **Trae** | Rules | ✅ global/project memory | `~/.trae/memory/...`（本地，不跨设备） |
| **Devin** | — | ✅ Knowledge（人工维护 + 自动召回） | 云端，repo/org/enterprise scope |
| **Augment** | — | ✅ Expert memory | 共享 VFS 里的 markdown |
| **Qwen Code** | QWEN.md | ✅ 异步 memory recall | 项目/用户/团队三级 managed-memory |
| **Zed** | Instructions（`.rules` 等 **8 种文件名**兼容） | ❌ | 文件 |
| **OpenCode / Amp** | AGENTS.md（OpenCode `/init` 就地改进） | ❌ | 文件 |
| **Aider** | repo map（AST 符号图，每次请求注入） | ❌ | 无状态 |

**L1 层已基本收敛到 AGENTS.md**：Zed 列表里就有 `.rules/.cursorrules/.windsurfrules/.clinerules/copilot-instructions.md/AGENT.md/AGENTS.md/CLAUDE.md/GEMINI.md` 九种兼容；Cursor、Windsurf、Kilo、Amp、OpenCode、Codex 全部原生读 AGENTS.md。

---

## 二、几个最有参考价值的自动记忆设计

**1) Claude Code —— 索引 + 懒加载的范本**
- `~/.claude/projects/<repo>/memory/`，一个 `MEMORY.md` 索引 + 每个记忆一个 topic 文件；**索引只注入前 200 行或 25KB**，超了会让 Claude 重写索引（超额内容下次就不加载了）
- topic 文件（`user_role.md`、`feedback_testing.md`…）**启动不加载，按需 read**
- 4 类 `type`：`user`（角色/偏好）/`feedback`（纠正）/`project`（代码推不出来的决策）/`reference`（外部信息在哪）
- 写入时打 `modified` ISO 时间戳；`/memory` 可审计；subagent 有独立 memory；repo 级共享（worktree/子目录共用一份）
- 还有一条 **relevant memory prefetch**（相关记忆异步预取）——不是文档，是 Qwen Code 设计文档里明确对齐的 `startRelevantMemoryPrefetch`/`settledAt` 模式

**2) Codex CLI —— 后台"熬"记忆 + 可溯源**（以下来自 `openai/codex` 主线源码，属尚未公开文档的特性）
- SQLite migrations：`0001_memories.sql`、`0002_consolidation_progress.sql` → 记忆是**后台把历史 thread 逐步 consolidation** 出来的，`MemoryStatusParams.min_consolidated_threads` 默认 20 条才 ready
- `MemoryCitation { entries: [{path, line_start, line_end, note}], rollout_ids }` → 每条记忆引用到具体文件和行号
- 还有 `external-agent-migration/src/memory_import.rs`：**从别的 agent 迁移/导入记忆**

**3) Gemini CLI Auto Memory —— 记忆→技能，且必须人工审批**
- 后台扫历史 transcript，找复现的事实/约束/流程，草拟成 **unified diff `.patch`** 和 **`SKILL.md`**，全部丢进项目内 inbox，等你 apply / promote / discard，**绝不自动写入**
- 前提：至少一个空闲 session 且有 ≥10 条用户消息

**4) GitHub Copilot Memory —— 失效与治理做得最实**
- repo 级 facts（带 citation 指向支撑代码）+ user 级 preferences（引用用户原话）
- 用到时**先拿 citation 对当前分支校验**，只使用校验通过的；**28 天未被使用自动删除**，用过则重置计时
- 权限：repo facts 只有写权限用户的操作才会创建；企业下 preferences 归 billing entity 所有；code review 只吃 repo facts 不吃个人偏好

**5) Kilo Memory —— 产品化 UX 最完整**
- 三个来源文件 `project.md`/`environment.md`/`corrections.md` + `sessions/` 下的 session digest
- **注入 index，细节靠 `kilo_memory_recall`**（search/typed/digest/catalog 四模式）；auto-save **只增改、从不删除**；可用 `memory_model` 指定更便宜的小模型跑后台总结；写入前过滤疑似密钥
- 老 memory bank 明确废弃并指向 AGENTS.md

**6) 其余值得记一笔的**
- **Windsurf**：官方直接给了 Rules / AGENTS.md / Workflows / Skills / Memories 的选型表，并说"一次性事实交给 Memories，durable 知识请用 Rules 或 AGENTS.md"
- **Trae**：AI 可自动 create/update/delete 记忆文件，单向本地
- **Devin Knowledge**：每条要有 **trigger description**（决定何时召回）+ `!macro` 快捷引用，还支持从对话反馈里**建议**新 Knowledge
- **Qwen Code**：异步 recall（UserQuery 不 await，settled 就用，否则在 ToolResult 回合追加 `system-reminder`）+ **microcompaction 保护** —— 别把 managed-memory 的 `read_file` 结果当普通工具输出清掉
- **Cline Memory Bank**：6 个固定文件（projectbrief/productContext/activeContext/systemPatterns/techContext/progress）+ "initialize/update memory bank" 命令，本质是自定义指令模式
- **Anthropic Skills**：三级渐进披露（name+description 常驻 → SKILL.md 本体按需读 → 目录内附带文件再按需），跟记忆的"索引 + 懒加载"是同一套思路

---

## 三、上下文压缩层（很多产品是二选一或都做）

- **Anthropic 官方 API 策略**：`clear_tool_uses_20250919`（超阈值就按时间顺序清最老的工具结果，可配 `clear_tool_inputs`）+ `clear_thinking_20251015`（思考块保留数，直接影响前缀缓存命中）。官方数据：context editing 单独 +29%，叠加 memory tool **+39%**（内部 agentic search 评测）
- **Codex**：`compact.rs` / `compact_remote_v2` / `auto_compact_token_limit`；**Gemini CLI**：context compression + `/compress-fast`；**Kilo**：context condensing；**Qwen Code**：microcompaction + memory-pressure 压缩；**Cline**：`/newtask`、`/smol` 配合 memory bank 换窗口
- 理论依据：Chroma **Context Rot** —— 控制住任务复杂度只变输入长度，性能仍随长度下降，且 NIAH 这类词面检索把问题掩盖了

---

## 四、外部记忆框架（可直接接进 harness）

| 方案                        | 核心抽象                                                                                              | 关键数据/特点                                                                     |
| ------------------------- | ------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------- |
| **Letta (MemGPT)**        | 分层虚拟上下文 + core memory blocks（`human`/`persona`）+ archival memory；V2 SDK 有 MemFS（git 跟踪记忆）         | 记忆块可 attach/detach 到 agent                                                  |
| **Mem0**                  | 抽取→consolidate→检索；graph 变体                                                                        | LOCOMO 上 LLM-as-Judge 比 OpenAI 方案相对 +26%，graph 再 +2%；p95 延迟 −91%、token −90% |
| **Zep / Graphiti**        | 时序知识图谱：facts + **fact invalidation 记在边上的失效时间** + episode 溯源 + thread/user summary                 | DMR 94.8% vs MemGPT 93.4%；LongMemEval 最高 +18.5% 准确率、延迟 −90%                 |
| **LangGraph + LangMem**   | 短期=thread checkpointer，长期=跨 thread 的 store（namespace）；semantic/episodic/procedural 三类             | LangMem 的写路径统一成"给对话+当前记忆态 → LLM 决定 expand/consolidate → 新记忆态"               |
| **Anthropic memory tool** | client-side 的 `/memories` 目录（view/create/str_replace/insert/delete/rename），just-in-time 检索，路径穿越防护 | 与 context editing 是官方推荐组合                                                   |

**学术脉络**（上面几乎所有设计的出处）：Generative Agents（memory stream + recency/importance/relevance 检索 + reflection）、MemGPT（OS 分层虚拟上下文）、Reflexion（语言化反思进 episodic buffer）、AWM（从历史轨迹归纳可复用 workflow，Mind2Web +24.6%）、A-MEM（Zettelkasten 动态索引/链接/记忆演化，NeurIPS 2025）、CoALA（semantic/episodic/procedural 分类）。

---

## 五、归纳：绕不开的 6 个设计决策

1. **谁来写**：人写（CLAUDE.md）→ agent 写（auto memory）→ agent 提议 + 人审（Gemini Auto Memory、Devin 建议）。越往后越要 UI，Gemini 的 patch+审批是保守而正确的做法。
2. **怎么读**：全量注入 → **索引常驻 + 正文按需 read**（Claude MEMORY.md、Kilo index、Skills 渐进披露）→ 异步相关记忆预取（Claude `startRelevantMemoryPrefetch` / Qwen）。索引要设硬上限并强制瘦身。
3. **存哪**：仓库内文件（可 git 共享、团队可见）vs 用户目录（机器本地、不跨设备）vs DB（可云端共享、企业治理）。Claude 选了"用户目录但按 git repo 聚合"，Copilot 选了"云端 + 引用校验 + 归属治理"。
4. **怎么失效**：这是多数自研 harness 最缺的一环。可参考：citation 用前对当前分支校验（Copilot）、28 天未用即删（Copilot）、fact invalidation 时间戳（Zep）、`corrections.md` 纠正文件（Kilo）、`modified` 时间戳（Claude）。
5. **记忆 vs 压缩的分工**：压缩保"还能接着干"，记忆保"下次不用再说"。压缩是硬上限（会丢），记忆要有**保护名单**（Qwen 专门保护内存文件的 read 结果不被 microcompaction 清掉）。
6. **记忆 vs 技能**：可复用的流程应该沉淀成 skill 而不是记忆条目（Gemini 直接把候选转 SKILL.md；Windsurf/Anthropic 也这么区分）。

对你这个 `mini_code` 来说，L3（`src/context.ts` 四层压缩）已经比大多数 IDE 做得细，L1（skill）也有；**明显的缺口是 L2**：目前只有 session 持久化（`.mini_code/sessions`），没有跨 session 的自动记忆。按上面共识，最小可用方案就是：`.mini_code/memory/MEMORY.md` 索引（限 N 行注入）+ `user/feedback/project/reference` topic 文件按需 `read_file` + 一个 `save_memory` 工具 + 在 Tier 4 全量摘要时给记忆文件开白名单。

---

## 六、第三方跨 Harness 文件记忆方案（2026-10-16 补充调研）

> 场景：**同一个工作区里来回切多个 Harness 客户端**（Claude Code / Codex / Cursor / opencode…），要一套**文件持久化**的项目记忆，不被任何一家厂商锁死。本节材料全部来自 HN Algolia 检索 + 各项目 README / 官方博客一手抓取，标注同全文。

### 6.1 先记住两个失败模式（OKF 的诊断，业界已成共识）

| 失败模式 | 症状 | 出处 |
|---|---|---|
| **Prompt Monolith** | 把全部领域知识塞进 AGENTS.md/CLAUDE.md → 上下文膨胀 + **attention drift**（agent 开始无视关键指令） | ✅ OKF README |
| **RAG Blindspot** | 行为规则丢进向量库 → agent 做普通任务时**根本不会**去语义搜索"格式/安全规则" | ✅ OKF README |

正确分工延续第五节的结论：**规范性内容（构建命令、硬约束、约定）留在 L1 指令文件；事实性/可检索知识（决策、踩坑、环境）放 pull 层按需取。**

### 6.2 L1 约定层：AGENTS.md 已是公约数

- Claude Code 文档明确：仓库有 AGENTS.md 时**可原生替代 CLAUDE.md** 加载（✅ docs.claude.com/en/docs/claude-code/memory）；Zed 一家就兼容 9 种文件名（见第一节）。
- 社区最简同步法：只维护一份 AGENTS.md，老的 CLAUDE.md 做软链（[HN 45550965](https://coding-with-ai.dev/posts/sync-claude-code-codex-cursor-memory/)，7 pts）。
- 但 L1 只解决"人写的规则"，解决不了"项目事实的积累"——这正是下面三层要补的。

### 6.3 第三方方案分四档（按形态，非按优劣）

#### 档 A：纯 Markdown 文件记忆系统（最贴合"文件持久化"）

| 项目 | 形态 | 要点 |
|---|---|---|
| [brain.md](https://github.com/mindmuxai/brain.md) | `BRAIN.md` 协议文件 + `brain/` 目录；`brain init` 自动接线各 agent 配置 | 零依赖 CLI、agent 无关；写入必经 CLI 保证不变量；入库判据："半年后还重要且代码推不出来的才进 brain"（✅ README） |
| [OKF Agent Memory](https://github.com/okf-memory/okf-agent-memory)（HN [49581240](https://news.ycombinator.com/item?id=49581240)，81 pts） | Git-native `knowledge/` 包 + **上限 400 token** 的 AGENTS.md codex | **双层架构（DMAA）**：push 层规范常驻 / pull 层语义 0-token baseline、按需 `okf_search`；本地 BM25 <300µs，零 embedding 费；一切纯文本可 `git diff` 审计（✅ README） |
| [IHMT-MEMORY](https://github.com/gonzaroman/IHMT-MEMORY)（HN [50038733](https://news.ycombinator.com/item?id=50038733)） | 一个文件夹的纯文本记忆树，stdio MCP | Claude Code 官方支持，Codex/opencode 实测共用一份记忆；**时间感知**（改动后旧记忆标 `OUTDATED` 保留历史）；50 条和 5 万条检索都只花 200–900 token（✅ README 自述，未复测） |
| [memctl](https://github.com/EltonCherrington/memctl) / [memctl.com](https://memctl.com) | CLAUDE.md/AGENTS.md 的版本管理层 | 只解决记忆文件的 diff/回滚，最轻 |

#### 档 B：会话索引召回（agent 自己"想起来"，不改写作习惯）

思路：各 Harness 本来就把会话落盘了 → 索引它们 → 跨 agent 共享。

| 项目 | 形态 | 要点 |
|---|---|---|
| [deja-vu](https://github.com/vshulcz/deja-vu)（HN [48923111](https://news.ycombinator.com/item?id=48923111)，**131 pts，本档最高**） | Go 单二进制 + MCP + CLI；本地索引、**无 embedding、无 server** | **索引 42 个 agent 的会话**，装上即搜数月历史；召回在会话开始/命令失败时**自动到达**，不用 agent 主动问；`deja handoff --to codex` 跨 agent 接续；抗 compaction（自述 43 次实测压缩后保住 77% 决策）；`deja sync ssh` 跨机；`deja promote --state rejected` 标记已被否决的决策（✅ README） |
| [Funes](https://huggingface.co/blog/funes)（HF 官方，2026-09-03） | 单二进制，本地 embedding，Lance 数据集 | `funes add claude/codex/pi/hermes` 一键接入；**recall 返回原文而非摘要**，带 agent/时间/session/turn 出处 + `get` 看全上下文；可同步到你自己拥有的 HF dataset（✅ 官方博客） |
| [PMB](https://pmbai.dev)（HN [48720682](https://news.ycombinator.com/item?id=48720682)，26 pts） | 本地 MCP | 特色：**能报告记忆到底有没有被用上**（对抗"写了等于没写"） |

#### 档 C：图/数据库后端（重，能力也重）

- [Sibyl](https://github.com/hyperb1iss/sibyl) — 自托管 SurrealDB 知识图谱，"一个图谱所有 agent 共享"；CLI 为主、MCP 为辅；含语义搜索 + epic/task 工作流 + transcript 摄入（✅ README）
- [Beads](https://github.com/steveyegge/beads)（HN [46075616](https://news.ycombinator.com/item?id=46075616)，111 pts） — 严格说是给 agent 的依赖图 issue tracker（Dolt 后端）；`bd remember "insight"` 存持久项目事实；`bd setup claude/codex/cursor/factory` 一键装各 Harness 集成（✅ README）
- [supermemory](https://github.com/supermemoryai/supermemory)（31K stars，本档体量最大）— 托管记忆引擎 + 图 + profile + connectors，官方插件覆盖 6 家 harness → **详见 [[supermemory 调研]]**

#### 档 D：可比评测（选型时盯这个）

**[Agent Memory Leaderboard](https://agentmemoryleaderboard.ai)**（HN [49281370](https://news.ycombinator.com/item?id=49281370)，2026-08-13）：136 队报名、69 个框架完成 Cycle 1；商用 Text Memory 前三 MemoraX 58.02 / MemOS 45.89 / NTES-MEMORY-SMART 44.21；评测边界固定为 **Memory system: Add→Search，Benchmark: Answer→Eval**。Cycle 2 已开，有专门的 **Coding Agent Memory** 赛道。这与本文第一节的结论互证：**memory policy 是 harness 的实验变量**（见 [[Agent Harness 评测]] Claw-SWE-Bench 一节——它刻意不统一 memory policy）。

### 6.4 推荐组合（一个工作区切多 Harness 的最小配置）

1. **打底**：根目录一份小而硬的 AGENTS.md（构建命令、硬约束、目录约定）；旧 CLAUDE.md 软链或删。
2. **结构化项目记忆**：brain.md 与 OKF 二选一（都是 git 内纯 Markdown）。重"决策+原因+过期标记"选 OKF；重极简 CLI 协议选 brain.md。
3. **跨 Harness 会话召回**：deja-vu 优先（唯一明确以"42 agent 共享同一索引"为卖点、且零写作习惯改动）；Funes 备选（胜在出处溯源与 HF 生态）。
4. **token 预算意识**：记忆 preamble 会乘上步数（[[Agent Harness 评测]] §0 Finding 3 的成本机制在这里同样成立）。OKF 的"400 token 封顶 + pull 层 0-token baseline"和 IHMT 的"按需 200–900 token"都是在防 Prompt Monolith；索引常驻 + 正文懒加载与第二节 Claude/Kilo 的内建设计是同一套路。

### 6.5 与第五节 6 个设计决策的对齐

| 决策 | 第三方方案的普遍选择 |
|---|---|
| 谁来写 | 档 A 多为"agent 写 + 人可 git review"（git-native 是卖点）；deja-vu/Funes 干脆**只索引已有会话**，无人工写作 |
| 怎么读 | 全部避开全量注入：OKF pull 层 / IHMT 树检索 / deja 自动短摘要 + TUI 深挖 |
| 存哪 | 档 A/B 几乎全选**仓库内或用户目录的纯文件**（可 git、可 SSH 同步），明确反 vendor lock-in |
| 怎么失效 | deja 的 `promote --state rejected`、IHMT 的 `OUTDATED` 标记、Copilot 的 28 天规则（第二节）是三种可抄的路径 |
| vs 压缩 | deja 显式做 compaction 恢复层；其余靠"记忆在窗口外"天然免疫 |
| vs 技能 | brain.md/OKF 均要求入库内容"不可从代码重建"，流程类留给 skill |

### 6.6 Hy-Memory（腾讯混元，2026-10-15 刚开源）——档 C 新玩家，与 supermemory 正面比较

> 2026-10-17 调研。仓库 [Tencent-Hunyuan/Hy-Memory](https://github.com/Tencent-Hunyuan/Hy-Memory)（465 stars / Apache-2.0 / Python），PyPI `hy-memory==2.0.2`；含 MemHub 本地产品源码。材料：双 README、memhub README、harness-support 全套（含 pi.md/claude-code.md 矩阵）、env_reference、`hy_memory/server.py` 源码、pyproject 依赖、release 制品清单、CHANGELOG、CMB 论文 PDF（pdftotext 摘读）。

**它是什么**："双系统（System 1 快写+调和 / System 2 慢演化）认知记忆"引擎 + Python SDK + **MemHub** 本地优先产品（桌面 App + CLI，统一管理多 AI 应用的会话并跨应用召回）。三场景 `scene`：`chat`（L0–L7 八层记忆：raw→atomic fact→summary→profile→schema→intention 带过期）、`working`（**两层**：每会话恰好 1 条 Fact"干了什么"+0–N 条过价值阈的 Experience"下次可复用的做法"）、`coding`（working 同构 + **版本演化 diff-chain**：同一函数被改了几次、每次真实 diff，零 LLM 调用存储——专为"被 revert 的版本在事实里永远找不到"这个痛点设计）。三档模式：`lite` 纯向量零 LLM / `pro` LLM 抽取+矛盾调和（图可选）/ `ultra` System 2 schema 归纳（图必开）。存储：ChromaDB（默认）/Qdrant/FAISS + Kuzu/Neo4j + SQLite。LLM 和 embedding 都是 OpenAI-compatible BYO 端点。

**与 supermemory 比较**（本机实测背景见 [[supermemory 调研]] §7）：

| 维度 | Hy-Memory | supermemory（本地 v0.0.8 实录态） |
|---|---|---|
| 开源度 | ✅ **全栈开源**（SDK+引擎+MemHub 源码，Apache-2.0）；30B-A3B 记忆写入模型也放 HF | ❌ 引擎闭源二进制 |
| 中文 | ✅ **原生**：jieba（CJK lazy import，缺了退 bigram）+ rank_bm25 词法通道进主依赖；rerank 模型多语言 | ⚠️ 默认英文 embedding，要靠换 bge-m3 补救 |
| 记忆理论 | 重：八层 hierarchy + 双系统演化 + diff-chain，**面向 coding 的抽象明显更深**（CMB 论文指出 87% 决策点引用非最新版本） | 图三类边（updates/extends/derives）+ profile，抽象简单但够用 |
| harness 接入 | ⚠️ 靠 MemHub 产品而非插件：`plugins/hook`、`plugins/mcp` 均"预留"；Claude Code/Codex/**Pi** 的一键插入在 MemHub 里（v1.0.2 release 有 macOS arm64 DMG 305MB + runtime tar.gz，Developer ID 签名公证；x64 未挂），装完 App 由 LaunchAgent 常驻；裸 SDK 只有 REST server（19527）无 MCP | ✅ 官方插件 6 家成熟，hook 四件套开箱即用 |
| 部署重量 | ❌ 重：runtime 包 **194MB**（自带 Python+chromadb+kuzu+sklearn…）；`[rerank]` extra 带 torch（GB 级，可不开）；embedding 无本地选项（`MEMORY_EMBEDDER_PROVIDER` 只有 OpenAI-compatible API）——**本机 magpie 网关没有 /embeddings，全离线跑不起来**，得配 Ollama 或云 key | ✅ 单二进制；bge-m3 本地全离线 |
| 捕获路径 | coding 场景**要求 tool-call trace** 入库（设计使然），lite 模式不区分 scene | 纯文本 add，对话增量自动捕获 |
| 成熟度 | 2 天大：11 open issues、3 watchers、文档中文为主 | 31K stars 生态；但本地 v0.0.9 有 macOS 摄取 bug 实锤 |
| Benchmark | CMB（自办）：双层+chain 43.1%/35.6% vs 最强基线 36.6%/28.2%；基线是 Mem0/MemOS/RAG/OpenViking/RepoMemory——**没测 supermemory**，vendor 自测未复现 | LongMemEval 97% Recall@20（同样 vendor 自测） |

**判断**：理论上最对味（coding diff-chain 和"记忆要能被执行验证"是 supermemory 没有的），且是**能审计的全开源**；但对"现在就要轻量地用"这个目标它比 supermemory 更重——MemHub runtime 194MB + 常驻 Python Core + LaunchAgent 服务（恰好是你上一轮嫌弃的形态），且 embedding 必须外部 API（magpie 网关没有 /embeddings）。它更像 supermemory 的"全开源重引擎版"，不是 Engram 的替代品。若试水：装 MemHub DMG（arm64 已签名发布）→ 配 Ollama embedding + magpie LLM → UI 里一键插入 Claude Code/Codex/Pi 看抽取质量；不想养服务就继续 Engram + supermemory 组合。

---


## 七、supermemory 深挖 → 独立成篇

> 2026-10-16 对 [supermemory](https://github.com/supermemoryai/supermemory)（31.2K stars，本档体量最大、也是唯一"引擎级"方案）做了单点深挖，内容较长，已拆为独立笔记：**[[supermemory 调研]]**。

要点速览（细节、部署命令、插件配置全在独立篇）：

- **定位**：不是文件记忆，是托管记忆引擎——`add` 原始内容，自研 learning model + 时序向量图引擎自动抽事实/建图/维护 profile，`search`/`profile` 取回；REST 三端点 `/ns/{namespace}/document|search|profile`。
- **图模型**：`updates`（替换）/`extends`（补充）/`derives`（推断）三类边 + 自动遗忘（过期/矛盾/噪声），对应本节档 C 但全自动。
- **⚠️ 开源边界**：SDK/插件/MCP server 开源（MIT），**自托管 server 二进制与云端抽取模型闭源**——与档 A/B"纯文本可 git diff"哲学相反，记忆在加密快照里。
- **部署**：本地单二进制（`npx supermemory local`，localhost:6767，可全离线 Ollama）/ Docker 预编译镜像 / 云端平台，同一 API 换 `baseUrl`。
- **跨 Harness**：Claude Code、Codex、OpenCode、Cursor 等 6 家官方插件，hook 四件套（SessionStart/UserPromptSubmit/PreToolUse/Stop）+ **三家 CLI 对同一 git repo 生成统一 container tag**（`repo_<name>__<remote-hash>`）——多客户端共享项目记忆的键。另有 SMFS（把记忆挂成可 grep 的文件系统）和托管 MCP。
- **评测**：自报 LongMemEval-S 97% Recall@20（vendor 自测）；开源了 MemoryBench 横评框架，与档 D 的 AML 互补。

---

**验证说明（全篇）**：以上第一至五节全部抓自官方文档（Claude/Codex/Gemini CLI/Cursor/Windsurf/Cline/Kilo/Trae/Augment/Devin/Copilot/GitHub/LangChain/Anthropic/Zep/Mem0/Letta）或 `openai/codex`、`QwenLM/qwen-code`、`zed-industries/zed` 仓库源码与 arxiv 摘要。两处不确定性已标注：Codex 内建记忆只见于主线源码（无公开文档，可能未 GA）；Cursor 官方 `/context/memories` 现在返回的是 Rules 文档，"Generate Memories" 依据的是社区论坛帖（beta，与 Privacy Mode 互斥）。

**第六节（2026-10-16）新增验证状态**：✅ 逐字抓取过 README/官方博客全文——deja-vu、OKF Agent Memory、Sibyl、Beads、IHMT-MEMORY、brain.md、Funes（HF 博客）、Claude Code memory 文档页；✅ HN 分数与 item id 来自 Algolia API（deja-vu 131 / Beads 111 / OKF 81 / PMB 26 / AML 3 pts 均为检索时点数值）；✅ AML 商用榜前三分数抓自 HN 帖 story_text（榜单页本身为 JS 渲染，未逐项核对全榜）。**未验证**：deja-vu 的 97.2% R@5、抗 compaction 77%、IHMT 的 200–900 token 等自述 benchmark 数字（口径未回溯）；coding-with-ai.dev 软链文未能抓到正文（站点拒抓），仅凭 HN 标题与摘要引用。检索踩坑：`defuddle` 本机未安装；部分站点（coding-with-ai.dev）对 curl 直连无响应。

**第七节**：supermemory 的完整验证状态见 [[supermemory 调研]] 文末（所有 benchmark 数字均为 vendor 自报口径，未复现）。
