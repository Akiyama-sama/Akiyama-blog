---
date: 2026-10-16
tags:
aliases:
---

# supermemory 调研：架构、部署与多 Harness 对接

> [github.com/supermemoryai/supermemory](https://github.com/supermemoryai/supermemory) · **31.2K stars**（检索时点，GitHub API）· MIT（仓库部分）· TypeScript · 2024-02 创建，push 到检索当天仍活跃。定位"State-of-the-art memory and context engine for AI"，自称 LongMemEval / LoCoMo / ConvoMem 三大记忆 benchmark 均 #1。
> 调研时间：2026-10-16。背景与同类方案对比见 [[Agent 记忆方案]]（本篇原为其第七节，拆出独立成篇）。
> 材料：README（main 全文）、`supermemory.ai/docs` 的 llms.txt 索引 + how-it-works / graph-memory / agents-and-mcp / self-hosting 全套 / supermemory-mcp / integrations（claude-code、codex、opencode、cursor）/ smfs 页、`apps/mcp` 源码结构与 wrangler.jsonc、`claude-supermemory` 插件 README、research 页。

## 1. 它是什么：一句话架构

**不是"文件记忆"，是托管的记忆/上下文引擎（Memory API）**：你把原始内容（对话、文档、URL）`add` 进去，它用一个**自研学习模型 + 时序向量图引擎**在后台抽取事实、建图、维护用户画像，然后你用 `search` / `profile` 把"该进上下文的那点东西"取回来。

```
你的 app / AI 工具
      ↓  add() / search() / profile()   （REST: /ns/{namespace}/document|search|profile）
┌─────────────── supermemory ───────────────┐
│ Memory Engine   抽事实、追踪更新、解矛盾、自动遗忘      │
│ User Profiles   static（长期事实）+ dynamic（近期上下文），~50ms 一次调用 │
│ Hybrid Search   一条查询同时跑 RAG（文档 chunks）+ Memory（图事实） │
│ Connectors      Drive / Gmail / Notion / OneDrive / GitHub / Web Crawler（实时 webhook） │
│ File Processing PDF / 图片 OCR / 视频转录 / 代码 AST-aware chunking │
└────────────────────────────────────────────┘
```

两个核心内部件（✅ how-it-works）：
1. **Learning model**（自研）——决定学什么、什么重要、何时忘、如何建关系。
2. **Temporal vector-graph engine**——事实基时序图，内建三种检索：**Vector**（embedding 语义近邻，抓改写）、**FTS**（Full-Text Search，倒排索引 + BM25 类词法打分，抓精确 token：报错串/标识符/人名）、**Graph**（沿 `updates`/`extends`/`derives` 关系边多跳遍历，召回与 query 无词面/语义重合的关联事实；API 层用 `include: { related: true }` 取边）。业界 hybrid search 通常只指 Vector+FTS，它把图也内建进同一存储。

**Ingest 流水线**：`queued → extracting（文本/OCR/转录/抓页）→ chunking → embedding → indexing → done`；`done` 只代表文档可搜，**记忆进图靠第二阶段的 "dreaming"**（把内容过一遍记忆模型，合并/组织/链接）。dreaming 两模式：`dynamic`（默认，相关文档成组抽，质量高，可能在 done 之后继续跑）/ `instant`（立即单文档入图，多计一次 operation，适合 demo 和"add 完马上 search"）。

**图模型**（✅ graph-memory，与 [[Agent 记忆方案]] 第二节 Zep/Graphiti 同族但更自动）：
- 记忆原子化，三类边：`updates`（新事实**替换**旧的用于检索，旧史保留审计，`isLatest` 标记）、`extends`（补充细节不作废）、`derives`（从多条记忆**推断**出没明说过的事实）。
- 记忆类型：Facts（持续到被更新）/ Preferences（重复即强化）/ Episodes（不显著就衰减）。
- **自动遗忘**：时间过期（"明天考试"）、矛盾（updates 获胜）、噪声过滤。
- 你**不手工维护图**——只管 add，schema 和边都由模型长出来。

**隔离三层**：`namespace`（硬隔离，URL 里带）/ metadata（namespace 内软过滤）/ scoped API keys（不能跨 namespace 的凭证）。插件层叫 container tag / space，同一个东西。

## 2. ⚠️ 开源边界（选型前必须知道）

| 部分 | 开源？ |
|---|---|
| 仓库 `supermemoryai/supermemory`：SDK、文档站、MCP server（`apps/mcp`）、各 harness 插件、memory-graph 可视化组件、MemoryBench | ✅ MIT |
| **自托管 server 二进制（`supermemory-server`）** | ❌ **闭源**——"built from a separate, non-public codebase"（✅ self-hosting/overview 原文）。装它 = 下载官方预编译二进制 |
| 云端生产用的记忆抽取模型 | ❌ 专有（"proprietary long-horizon models"） |

**含义**：本地部署能免费用全 API，但核心引擎是黑盒二进制 + "lite license limit"（免费额度，条款未在文档中量化）；要 connectors、托管 MCP、最好的抽取质量，就得上云/Enterprise。和 [[Agent 记忆方案]] 第六节那批"一切纯文本可 git diff"的方案是**相反的哲学**——supermemory 的记忆在加密快照里（`~/.supermemory/data`，每 10s 全量 dump），不在你能 review 的 markdown 里。

## 3. 部署：三种形态

### A. 本地单二进制（Supermemory local）

```bash
curl -fsSL https://supermemory.ai/install | bash   # 或 npx supermemory local
supermemory-server
```

- 首次启动：内嵌图引擎 + 本地 embeddings（`Xenova/bge-base-en-v1.5`，768d，无需 API key）+ 自动生成 API key，全落在 `~/.supermemory/`；监听 `http://localhost:6767`（v0.0.9 起 bind `127.0.0.1`，localhost 请求也要 key；**v0.0.8 及以前 bind 所有网卡且隐式本地认证，文档明令不要暴露**）。
- LLM 自带：OpenAI / Anthropic / Gemini / Groq / Vertex / Workers AI，或任何 OpenAI-compatible 端点。**全离线**：`OPENAI_BASE_URL=http://localhost:11434/v1` + Ollama（官方推荐 `gpt-oss:20b`）+ `SUPERMEMORY_DISABLE_TELEMETRY=1`；例外：URL 摄取走 Firecrawl 需 key，PDF 抽取需 `GEMINI_API_KEY`。
- 资源治理：searches 永不排队；adds 进队列后台处理，ingest 内存增量默认封顶 1GB（`SUPERMEMORY_EMBEDDING_RAM_LIMIT`），超了新文档等待、不丢。
- 升级 `supermemory-server upgrade`；回滚先备份数据目录（旧版二进制读不懂新 schema）。

### B. Docker（预编译镜像，Linux amd64/arm64）

```bash
curl -fL https://github.com/supermemoryai/supermemory/releases/download/server-v0.0.9/compose.yaml -o compose.yaml
# .env: OPENAI_API_KEY=... + SUPERMEMORY_VERSION=0.0.9
docker compose up -d --wait --wait-timeout 180
```

- 镜像 `docker.io/supermemory/supermemory`；6767 只绑 127.0.0.1；数据卷 `supermemory_supermemory-data` 挂 `/data`（store + api-key + 加密身份 + 模型缓存全在里面）；key 从 `docker compose exec supermemory cat /data/api-key` 读。
- 升级流程 = stop → `cp /data` 全量备份 → 换镜像 → up；**严禁 `docker compose down -v`**。原生 Windows 停在 0.0.8，Windows 走 Docker。

### C. 云端平台（console.supermemory.ai）

- 同一套 API，换 `baseUrl` + 平台 key 即可（**本地数据不会自动迁移过去**）。加：专有抽取模型、Connectors、托管 MCP、org/角色/scoped keys、用量看板。v3/v4 API 将于 **2026-12-31 关停**，新接入直接 v5。
- 云端 MCP server（`apps/mcp`，开源）是个 **Cloudflare Worker**：MCP SDK v2、每请求新建 McpServer（无协议 session）、OAuth 每请求校验、active space 存 Durable Object（按 `organizationId+userId` 键）。想自己仿一个托管 MCP，这就是参考实现。

### 自托管 vs 平台能力对照（✅ self-hosting/overview）

| | 自托管 | 平台 |
|---|---|---|
| 完整 Memory API / 混合搜索 | ✅ | ✅ |
| Embeddings | 本地默认（或 OpenAI/Gemini/Ollama） | 托管 |
| 文件摄取 | ✅（PDF 需 `GEMINI_API_KEY`，图片走 Gemini/Vertex） | ✅ |
| Connectors（Drive/Notion/Gmail/OneDrive） | — | ✅ |
| 托管 MCP（mcp.supermemory.ai） | — | ✅ |
| 记忆抽取模型 | 你带的模型 | 专有 long-horizon 模型（质量更高、规模化更便宜） |
| 团队/治理 | 单机单 key | org、角色、scoped keys、看板、SLA |

## 4. 与各 Harness 对接（重点：怎么写进 coding 工作流）

### 路线 1：官方插件（推荐，覆盖"一个工作区切多客户端"场景）

每家一个开源插件仓库，机制都是 **hook 注入 + 自动捕获**，且 **Claude Code / Codex / OpenCode 对同一 git repo 生成同一个 container tag**（`repo_<project-name>__<remote-hash>`，remote 归一化后哈希 → clone 共享记忆、同名仓库不撞车；无 remote 回退本地路径身份）——**这就是跨 harness 共享项目记忆的键**：

| Harness | 安装 | 机制要点 |
|---|---|---|
| **Claude Code**（[claude-supermemory](https://github.com/supermemoryai/claude-supermemory)） | `/plugin marketplace add supermemoryai/claude-supermemory` → `/plugin install supermemory`；key 走 `SUPERMEMORY_CC_API_KEY` 或浏览器登录 | 4 个 hook：`SessionStart`（装 profile + 6h 未归的 welcome-back）→ `UserPromptSubmit`（**hook 直接搜索并注入**，不等模型决定调工具；`recallDirective` 可切成"建议模型自己搜"模式）→ `PreToolUse`（只读 MCP 工具自动放行，写仍要权限）→ `Stop`（后台存对话增量）。`context-gatherer` 子代理跨多 container 扇出搜索。`/supermemory:index` 把架构/约定/运行方式索引进项目 container。项目级配置 `.claude/.supermemory-claude/config.json`（`baseUrl` 指本地即接自托管） |
| **Codex CLI**（[codex-supermemory](https://github.com/supermemoryai/codex-supermemory)） | `npx codex-supermemory@latest install`（写 `~/.codex/supermemory/`、开 `codex_hooks`、注册 hook + skills） | 两层：implicit hooks（`UserPromptSubmit` recall + **每 N 轮增量 capture**，默认 3，让同 session 后半段能吃到前半段记忆；`Stop` flush）+ explicit skills。scope：user tag = `git config user.email` 哈希，project tag = git common dir 哈希（worktree 默认共享）。`<private>…</private>` 包裹的内容入库前打码。自托管：`SUPERMEMORY_API_URL=http://localhost:6767` 或 `~/.codex/supermemory.json` 的 `baseUrl` |
| **OpenCode**（[opencode-supermemory](https://github.com/supermemoryai/opencode-supermemory)） | `bunx opencode-supermemory@latest install`；`opencode.jsonc` 加 `"plugin": ["opencode-supermemory"]` | session start 注入 profile+项目知识+语义匹配；"remember/save this" 关键词触发存储；**80% 上下文容量时自动摘要会话存为记忆**（smart compaction——记忆层与压缩层的合流点，参见 [[Agent 记忆方案]] 第三节）；`<private>` 同样生效。自托管配置在 `~/.config/opencode/supermemory.jsonc` |
| **Cursor**（[cursor-supermemory](https://github.com/supermemoryai/cursor-supermemory)） | Cursor 内 `/add-plugin cursor-supermemory` 或 Marketplace；`/supermemory-setup` 浏览器登录 | 需要 PATH 上有 Node（Cursor 安装不带） |
| 其他 | Muse Code、OpenClaw、Hermes（NousResearch 官方 memory provider） | 同模式 |

Claude Code 插件的全局/项目配置项（✅ 插件 README + integrations 文档）：

```json
// ~/.supermemory-claude/settings.json（全局）
{ "maxProfileItems": 5, "signalExtraction": true,
  "signalKeywords": ["remember", "architecture", "decision", "bug", "fix"],
  "signalTurnsBefore": 3, "includeTools": ["Edit", "Write"] }

// .claude/.supermemory-claude/config.json（每仓库）
{ "apiKey": "sm_...", "baseUrl": "https://api.supermemory.ai",
  "repoContainerTag": "my-team-project", "signalExtraction": true }
```

### 路线 2：MCP（任何 MCP 客户端通用，含 Claude Desktop / Windsurf / VS Code）

- 云端：`https://mcp.supermemory.ai/mcp`，OAuth 浏览器授权，无 API key。工具面：`search_memory` / `get_profile` / `add_memory` / `forget_memory` / `list_documents` / `get_document` / `list_memories` / `list_spaces` / `who_am_i` + 4 个交互 widget（space 选择器 / guided-save 表单 / 文件上传 / **记忆图可视化**，走 MCP Apps）。资源 `supermemory://profile`、prompt `context`。
- **注意：托管 MCP 是平台功能，自托管表里 MCP 一栏是 "—"**——本地部署只能走插件（`baseUrl` 指本地）或直连 REST/SDK。
- 另有 **docs MCP**（`https://supermemory.ai/docs/mcp`，开源在仓库）：这是给 coding agent **边写集成边查 supermemory 文档**用的，和记忆本身无关，别混淆。

### 路线 3：SMFS —— 把记忆挂成文件系统（对 coding agent 最顺手的形态）

把 supermemory container **挂载成真实目录**，agent 用 `ls`/`cat`/`grep` 读记忆，不用学任何 SDK。开源免费。四个 trick 解决"文件系统不适合当记忆"的问题：
- **语义 grep 默认**：`grep` 一次调用即全 container 按语义排序召回；带任何 flag 则 fall through 到真 grep 做精确匹配。
- **memory path 蒸馏**：标记为记忆路径的文件被抽取索引，不撑爆上下文。
- **虚拟 `profile.md`**：挂载根下一个实时 digest，`cat profile.md` 一次拿到全 container 摘要。
- **双向后台同步**：本地读走缓存，写推回 supermemory。
- 两种用法：**mount**（`smfs` 二进制，macOS NFSv3 / Linux FUSE，适配 Claude Code、Cursor、devcontainer、Docker、Codespaces）和 **bash tool**（`@supermemory/bash` / `supermemory-bash`，给 Cloudflare Workers、Lambda、Vercel、Modal 这类无真实文件系统的 runtime 一个虚拟 bash）。已有 Daytona / E2B / Vercel AI SDK / Cloudflare Workers 的 provider 指南。
- 官方数据（自述，✅ research 页）：xAFS 110 题上 SMFS 比默认文件方案省 **3.0× token（Claude，24M vs 72M）/ 1.75×（Codex）** 且准确率更高。

### 路线 4：SDK / REST（自己写 harness 或 mini_code 时）

```typescript
import { Supermemory } from "supermemory";            // npm i supermemory / pip install supermemory
const client = new Supermemory({ apiKey: "sm_...", baseUrl: "http://localhost:6767" }); // 自托管只改 baseUrl
await client.add("user_123", { content, dreaming: "instant" });
const { profile, searchResults } = await client.profile({ containerTag: "user_123", q: "..." });
// search 三模式：hybrid（默认，RAG+Memory 一条查询）/ memories / documents
```

REST 就三个主端点：`POST /ns/{namespace}/document|search|profile`，`Authorization: Bearer sm_...`；namespace 只在 URL，body 里没有。框架封装：Vercel AI SDK / LangChain / LangGraph / OpenAI Agents SDK / Mastra / Agno / Claude Memory Tool / n8n（`withSupermemory(model, {containerTag})` 一行包模型）。**给 mini_code 抄的话，这一层就是"记忆即服务"的最小接口面：add / search / profile 三个动词。**

### 路线 5：CLI / Skill（给 coding agent 做集成开发时用）

```bash
npx supermemory setup              # 检测项目，启动/打印集成流程
npx supermemory setup --prompt     # 只打印集成 prompt
npx supermemory help --json        # agent 可读的命令目录
npx supermemory add "User prefers TypeScript" --namespace user_123   # 冒烟测试
npx skills add https://github.com/supermemoryai/skills --skill supermemory  # 官方 skill，防 agent 幻觉 API
```

## 5. Benchmark 与评测基建（接 [[Agent Harness 评测]] 的方法论）

- 自报成绩（✅ research 页，2026-05 报告）：LongMemEval-S **97% Recall@20**（500 题 6 类，对比 Zep 71.2%、Full context 60.2%；分类最强项 KU 知识更新 100%、SSA 100%）；README 口径 **95% Recall@15，仅注入 ~720 token（99.4% 上下文缩减）**。Judge 是 gpt-4o + benchmark 自带 prompt。**注意这是 vendor 自测**，且"Recall@20 with aggregation"的口径比常见 Recall@5 宽松——按 [[Agent Harness 评测]] §4 陷阱 6/11 的标准，采信前要看它开源的 MemoryBench 复现。
- **[MemoryBench](https://supermemory.ai/docs/memorybench/overview)**：它顺手开源的记忆 provider 横评框架，可把 supermemory / Mem0 / Zep 拉到同一 runner 下跑（`bun run src/index.ts run -p supermemory -b longmemeval -j gpt-4o`），还提供 `npx skills add supermemoryai/memorybench` 的 agent skill 让 coding agent 自动跑 `/benchmark-context`。这与 [[Agent 记忆方案]] 第六节档 D 的 Agent Memory Leaderboard 互补：AML 是中心化提交制，MemoryBench 是自己机器上可复现的 head-to-head。

## 5.5 "装了对 coding 提升多少"——证据审查（2026-10-17 追加）

**直接回答：没有任何可信公开数字能回答这个问题。** 逐条审查官方 coding 相关证据：

1. **LongMemEval 97% Recall@20**：是**对话记忆召回**基准（"用户上次说过什么"），不是 coding 任务完成率；vendor 自测、gpt-4o judge。证明"取得准"，不证明"活干得好"。
2. **SMFS "xAFS 110 题，Claude 3×/Codex 1.75× token 省且准确率更高"（research 页）**：⚠️ **官方口径不稳定实锤**——smfs.ai 研究页现版本写的是 **20 个检索任务：Claude 643,668→410,797 token（−36%）、16/20→18/20 对；Codex 1,212,380→203,427（−83%）、19/20→19/20**。任务数/倍数/说法两处全对不上，说明官方在替换 benchmark 叙事，旧口径不可当稳定事实引用。另外 "xAFS" 不是公开基准（GitHub 搜不到对应项目，命中全是无关的 DevExpress XAF）。
3. **MemoryBench**：只有 runner + MemScore 方法学，**仓库和 docs 均无已发布结果页**——"能测"≠"测过"。
4. **独立第三方**：Agent Memory Leaderboard 的 Coding Agent Memory 赛道 **Cycle 1（2026-08-12）榜上无 supermemory**，Cycle 2 结果 2026-11 中旬发布；HN 无成规模独立复现。
5. **结构原因**：插件的作用机制（SessionStart/UserPromptSubmit 注入 recall + Stop 捕获）决定收益集中在**跨会话**场景（省 re-explain、少踩重复坑）；单会话内的编码能力不变。CMB 论文侧面佐证天花板：最强基线也只 solve 36.6% 长程 coding 记忆任务（见 [[Agent 记忆方案]] §6.6）。

**合理预期**：常在"同一仓库跨天/跨周继续"→ 省 re-explain 时间和重复探索（SMFS 那组 −36%/−83% 是"按需检索 vs 全量读文件"的方向性对比，幅度存疑）；任务多在一个会话内完成 → 提升接近零。最可靠的验证是**自己 A/B**：同类任务开/关插件各跑几轮，比 token 与一次通过率。

## 6. 怎么选：supermemory vs 纯文件方案

| 维度 | supermemory | [[Agent 记忆方案]] §6 档 A/B（brain.md / OKF / deja-vu…） |
|---|---|---|
| 记忆形态 | 加密快照里的图（黑盒二进制引擎） | 纯文本/Markdown，git 可 diff 可 review |
| 谁抽取 | 自研学习模型（云端专有 / 本地 BYO LLM） | 你自己写 or agent 显式 save，deja/Funes 只索引已有会话 |
| 跨 harness | ✅ 官方插件 6 家 + 统一 repo container tag + 托管 MCP | ✅ 各自实现（AGENTS.md 公约数 / MCP / 共享索引） |
| 离线 | ✅（Ollama + 本地 embedding；URL/PDF 摄取除外） | ✅ 多数天然离线 |
| 遗忘/矛盾 | ✅ 引擎自动（updates/时间过期/噪声过滤） | 手动或半自动（`OUTDATED` 标记、`promote --state`） |
| Vendor lock-in | 中——API 开放、插件开源，但引擎闭源、本地↔云数据不互迁 | 低 |
| 适合 | 想要"装上就聪明"、多端一致、不想自己管记忆生命周期 | 想要记忆完全可审计、可版本化、零信任第三方 |

**落地建议**（一个工作区切 Claude Code / Codex / OpenCode）：
1. 先本地跑 `npx supermemory local` + Ollama（或任一已有 key），零成本验证抽取质量是否对你的项目有效——`/supermemory:index` 索引一次 codebase，切到 Codex 看 recall 是否命中同一 container。
2. 三家插件都装上，靠统一 repo tag 天然共享；`SUPERMEMORY_ISOLATE_WORKTREES=true` 只在你想按 worktree 隔离时开。
3. 隐私敏感内容用 `<private>` 包裹（Codex/OpenCode 插件会打码）；密钥过滤是 Kilo 式默认，但仍建议 capture 前自查。
4. 若验证后不想依赖闭源引擎：退回 [[Agent 记忆方案]] §6 组合（AGENTS.md + brain.md/OKF + deja-vu），supermemory 的插件 hook 结构（SessionStart/UserPromptSubmit/PreToolUse/Stop 四件套）本身仍是给 mini_code 做 L2 自动记忆时最好的抄写对象。

## 7. 本地部署实录（2026-10-16，本机 macOS arm64）

实际装出来的可用组合与文档没写的坑：

| 组件 | 最终选择 | 原因 |
|---|---|---|
| server | **v0.0.8** 二进制（`~/.supermemory/bin/supermemory-server`）+ `WORKFLOW_ENGINE=direct` | v0.0.9 darwin-arm64 摄取流水线**永远卡在 queued**（rivet workflow 不派发，`WORKFLOW_ENGINE=direct` 又已移除），是上游 bug；v0.0.8 direct 引擎 ~10s 出 4 条原子记忆 |
| 数据目录 | `SUPERMEMORY_DATA_DIR=$HOME/.supermemory` 显式设置 | v0.0.8 默认落在 **cwd**，不设会把 vault 污染出 `.supermemory/` |
| embeddings | `Xenova/bge-m3`（1024d）替默认 `bge-base-en-v1.5`（768d，纯英文） | 默认模型中文查不出英文记忆（issue #1740）；换模型必须**清空重灌**（维度不同） |
| LLM | 本地 magpie 网关 `http://127.0.0.1:3425/v1`（OpenAI-compatible，占位 key） | BYO-LLM 走 `OPENAI_BASE_URL/OPENAI_API_KEY/OPENAI_MODEL` |
| Claude Code | 官方插件 `supermemory@supermemory-plugins` v0.1.12 + `~/.claude/settings.json` 注入 `SUPERMEMORY_API_URL=http://127.0.0.1:6767` | 插件只调 `POST /v3/documents`（capture）和 `POST /v4/profile`（recall），**全是 v0.0.8 支持的 legacy 端点** → 完整可用 |
| Codex | 官方 `codex-supermemory`，`~/.codex/supermemory.json` 写 `apiKey`+`baseUrl`+`apiVersion:"legacy"` | 同上：自定义 baseUrl 默认走 legacy 兼容路径；install 需本人跑 `npx codex-supermemory@latest install` |

**版本陷阱**：v0.0.9 才有 v5 `/ns/` API，但它的摄取是坏的；官方 `apps/mcp`（Cloudflare Worker）只说 v5 ⇒ **自托管 MCP 在"能用的本地后端"上不存在**。凡对接本地 server，认准 v3/v4 legacy 端点的插件路线。另注意 v4/search 相似度阈值默认 ~0.55，中文↔英文跨语检索常落在 0.3–0.55，插件配置里要把 `similarityThreshold` 压低（本机取 0.35/0.2）。

**验证方法**：新开会话看 SessionStart 是否注入 `<supermemory-context>`；`curl localhost:6767` 浏览器 UI 看 Memory 标签；日志 `/tmp/sm-m3.log`；服务开关 `smctl start|stop|status|restart|logs`（`~/.supermemory/smctl`，已链到 PATH）。

**内存治理**（本机 16GB，实测）：v0.0.8 空闲时常驻 ~550MB，大头是预热的 bge-m3 ONNX 模型。`smctl` 已内置两个开关：`SUPERMEMORY_SKIP_EMBEDDING_PREWARM=1`（开机不预热）+ `SUPERMEMORY_LOCAL_EMBEDDING_IDLE_TIMEOUT_MS=60000`（空闲 60s 卸载模型）——实测 45s 内 539MB→51MB，冷搜索约 1s 恢复（首次 ~15s 加载）。**坑**：embedding 维度必须和已灌数据一致，配错报 `different vector dimensions 1024 and 768`；且 v0.0.8 首启会把明文 `env` 文件消费加密进 `env.enc` 并删除原件——所有配置要写死在启动脚本 export 里，别依赖 env 文件存活。harness 插件的 hook 在服务 stop 后静默跳过不报错，所以随时可以关掉省内存，用时 `smctl start`。

---

**验证说明**：✅ 逐字抓取过全文——supermemory 主 README（main）、`supermemory.ai/docs` 的 how-it-works / graph-memory / agents-and-mcp / self-hosting overview+quickstart+configuration+docker+local-vs-enterprise / supermemory-mcp/mcp / integrations（claude-code、codex、opencode、cursor）/ smfs/overview（均走 llms.txt 暴露的 `.md` 端点）、`claude-supermemory` 插件 README、`apps/mcp` README + wrangler.jsonc + 目录树、research 页、GitHub API 仓库元数据与目录结构（stars 31,242 / MIT / TS / pushed 2026-10-16）。**未验证**：97% Recall@20、95% Recall@15、99.4% 上下文缩减、SMFS 3.0×/1.75× token、~50ms profile 等全部为 vendor 自报口径，未跑 MemoryBench 复现；"lite license limit" 的具体额度文档未量化；`apps/web`（历史 Cloudflare 版 app）与 `packages/memory-graph` 仅看了目录/README，未读引擎代码（server 引擎本身闭源，无从读起）。
