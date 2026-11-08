---
date: 2026-10-11
tags:
aliases:
---
# 固定模型下评测 agent harness：方法综述 + 可落地方案

> 主题：**在同一个 LLM 的前提下，怎么评测 harness（脚手架/外壳：agent loop、system prompt、工具定义、上下文管理、权限、重试）本身的效果。**
> 调研时间：2026-10-11。所有外部结论均带来源；标注 **✅ 已核对** 的是我直接抓取过一手来源（arXiv 摘要/HTML、官方页面）并按原文核对的数字；标注 **📄 详见报告** 的来自本次两份详细调研（含 URL，未逐条回原文核对）。
> 详细材料见同目录 `harness-eval-academic.md`（学术线，81 篇论文）与 `harness-eval-industry.md`（工业线，benchmark 与实操）。

---

## 0. 一句话结论

这已经是独立课题，而不是"顺便看看"。结论有三条，且互相约束：

1. **固定模型只换 harness，pass rate 可以翻转任务、甚至反转模型名次。** ✅ 2610.00917（66 配置 / 6,204 轨迹）：Claude 在 OpenHands 上领先 GPT +7.94pp，在 PI 上落后 −30.16pp；5 个模型中 4 个"最优 harness"随 benchmark 变化。
2. **但换 harness 造成的翻转幅度，常与"同一配置重跑一遍"的噪声同量级。** ✅ 2610.04433（3 个生产 harness × 5 模型 × SWE-bench Verified）：换 harness 翻转 13% 任务，**重跑也翻转 13%**；最重与最轻 harness 在 5pp 内等价；45 题只有 50% 把握检出 13pp 差距，447 题才能分辨 5pp。
3. **稳定可测的 harness 效应大头是成本/资源，不是分数。** ✅ 2607.22585（3 harness × 2 模型 × Terminal-Bench Pro 50 题）：**每解决一题 token 差最高 40×**，而同模型内 pass rate 差仅 0–8pp（配对 bootstrap CI 多含 0）。✅ 2610.04433：同模型同任务**成本差最多 3×**，差距由"首调用 system prompt + 工具 schema 的 preamble 尺寸 × 步数"决定。

**推论（这就是方法）：** 只比 pass@1 无法区分"harness 变好了"和"这次运气好"。正确流程是
**先量化重跑噪声 → 声明你要回答的 claim → 配对设计 → 有效性/效率/可靠性三类指标并报 → harness 改动配回归门。**

---

## 1. 标准实验设计的四条铁律

| # | 铁律 | 依据 |
|---|---|---|
| 1 | **模型真正冻结**。自托管（vLLM + OpenAI 兼容接口）或 pin 到"版本号 + 日期"，禁止依赖厂商默认别名 | ✅ 2607.03691 明确写 "By self-hosting the model, we ensure that the LLM remains identical across all 35 releases, **eliminating silent model updates as a confound**" |
| 2 | **harness 版本 pin 成自变量**（commit hash 或 npm 版本）。harness 迭代速度是传统项目的 13–28×（>2 release/天） | ✅ 2607.03691（5 个开源 harness 发布节奏分析） |
| 3 | **先测噪声基线，再测效应**：同一配置重跑 2–3 次，先证明 run-to-run 差异可控 | ✅ 2607.03691 用 Wilcoxon 证明两次运行分布相同（resolve p=0.478 / token p=0.432 / tool calls p=0.466），87.7% 任务两次二值结果一致，才继续谈版本差异 |
| 4 | **任务级配对 + 难度分层**，绝不把两个独立样本当配对 | ✅ 2607.22585 用 paired-task bootstrap（B=10,000）；✅ 2607.03691 按 SWE-bench 难度分层抽样（easy 20 / medium 25 / hard 5 = 50 题） |

### 一手案例：最干净的一套设计（✅ 2607.03691，就是"固定模型换 harness"的范式）

- 模型：Qwen3-Next-80B-A3B-Instruct，vLLM v0.18.0 自托管，OpenAI 兼容端点，35 个 release 全程同一份权重。
- harness：Qwen Code CLI 的 35 个连续 npm release（每个都装出来跑）。
- 任务：SWE-bench Verified 500 题中分层抽 10%（50 题），并先剔除 8 个"gold patch 都跑不过"的环境坏题。
- 运行时：每题 timeout 600s；每题跑 2 次；判分用官方 SWE-bench Docker harness（patch 应用 + 全量测试通过才算 resolved）。
- 指标：resolve rate（有效性）/ token consumption / tool call frequency（效率）。
- 它测出来的东西，正是"harness 会变坏"的机制：
  - resolve rate 在 30.5% 均值上下波动（23%–39%），与版本序号**无显著单调趋势**（Spearman ρ=0.208, p=0.231）；新版**并不更好**。
  - token 消耗**显著上升**：ρ=0.743 (p<0.0001)，前 9 个版本均值 ~391K/题 → 最新版本 ~668K/题（**+70%**），而 resolve rate 没有对应提升。
  - 失败任务比成功任务贵得多：未解决 697.7K tokens / 12.95 次工具调用 vs 解决 258.7K / 7.2 次（**2.7× tokens、1.8× 工具调用**）。
  - 归因到具体组件：初始 prompt 载荷（system prompt + 工具 schema）涨 ~8%，LLM 轮数涨 18%（token 与轮数 ρ=0.941），二者相乘放大成本。
  - 反向证据：一次 PR 删掉 5 个 CLI 模块、817 行未使用 harness 代码后，token 从 517K → 450K（−12.9%）、工具调用 10.2 → 9.1。

---

## 2. 该报告的指标：三层，别只报第一层

### A. 有效性（Effectiveness）
| 指标 | 口径 | 出处 |
|---|---|---|
| resolve rate / pass@1 | 判分用可执行 verifier（跑测试/gold 对比），**不解析 agent 的最终消息**；patch 从 git 状态导出 | ✅ 2607.03691；📄 2606.12344 §3.1（Claw-SWE-Bench adapter 协议） |
| 分层结果 | 按难度分层报，聚合会掩盖局部回归 | ✅ 2607.03691 分层抽样；📄 2606.11686（聚合 −1.7~−5.9pp vs 层切片 −25~−91pp） |
| pass^k（可靠性） | k 次**全部**成功才算；指数级惩罚不一致 | ✅ 2406.12045 τ-bench 提出；gpt-4o retail 域 pass^8 < 25% |
| 最小可分辨差异 + 功效 | 别在小样本上排名次 | ✅ 2610.04433（45 题检出 13pp 只有 50% 把握；447 题分辨 5pp） |

### B. 效率（Efficiency）— harness 效应最稳的地方
| 指标                                                       | 口径                                                                      | 出处                                                                                        |
| -------------------------------------------------------- | ----------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| tokens per **solved** task（摊销）                           | Σ tokens_total ÷ solved 数，**失败与 infra error 的 token 也计入分子**（这才是部署方真实成本） | ✅ 2607.22585；✅ 2607.03691                                                                 |
| USD 成本，拆分 input / cached input / output + cache hit rate | cache 单价与命中率会实质性改变账单排名                                                  | ✅ 2610.04433（3× 成本差）；✅ 2607.03691；📄 hal.cs.princeton.edu（每行带 $）；📄 artificialanalysis.ai |
| wall-clock / 每任务等待 / no-action turns                     | "既没改文件也没发新命令"的轮次是**监督税**，不只是 token 税                                    | ✅ 2607.22585                                                                              |
| 工具调用次数 / LLM 轮数                                          | 成本膨胀的直接驱动量（token 与轮数 ρ=0.941）                                           | ✅ 2607.03691                                                                              |

### C. 可靠性与过程（Reliability & Process）
| 指标 | 口径 | 出处 |
|---|---|---|
| 重跑一致性 / 可复现率 | 同配置重跑的二值一致率（案例：87.7%） | ✅ 2607.03691 |
| 失败模式指纹 | 固定 taxonomy（REASON / VERIFY / TIME / MAX_TURNS / HANG / ERROR）；**失败指纹跨模型复现 ⇒ 属于 harness 属性而非模型属性** | ✅ 2607.22585（Goose→REASON、OpenHands-SDK→VERIFY/MAX_TURNS、OpenCode→idle-loop/TIME） |
| 回归率 | 改 harness 有没有把原来做对的任务做坏 | 📄 2607.14004（只有内置回归控制的方法能正迁移）、2606.11686、2608.27311 |
| 过程质量 / Lucky Pass | 通过但过程脏（回归循环、盲目重试、缺验证）要单列 | 📄 2605.12925（10.7% 通过轨迹是 Lucky Pass）、2610.01833（92.6% 通过终态检查的 run 仍有过程偏差） |
| harness 自身质量 | 覆盖/变异分数/真实 bug 数 | 📄 2610.04921（LLM 依赖的 harness 代码覆盖不到一半） |
| 安全（若要报） | ASR 与 Utility **并列** | 📄 2608.17597（ASR 12.6–80.9%，Utility 仍 75–97.6%） |

### 一个可直接抄的多维可靠性指标集
✅ **HAL Reliability Dashboard**（15 agents × 2 benchmark × 12 指标，4 个维度）：
- **Consistency**：Aggregate / Outcome / Trajectory-Distribution / Trajectory-Sequence / Resource
- **Predictability**：Aggregate / Calibration / AUROC / Brier
- **Robustness**：Aggregate / Fault / Structure / Prompt-perturbation
- **Safety**：Aggregate / Harm / Compliance
- 该页原文的关键结论："the gap between capability (pass@k) and reliability (pass^k) is substantial across all models"，且"**recent capability gains have yielded only small improvements in reliability**"。

---

## 3. 统计：最小够用的一套

| 做法 | 具体参数 | 出处 |
|---|---|---|
| 每题重复 | **≥3 次**，报 mean ± 1 SEM | 📄 MLE-bench 官方要求；Claw-SWE-Bench repeats=3 |
| 配对比较 | **paired-task bootstrap，B=10,000**（同题配对，而非两独立样本） | ✅ 2607.22585 |
| 名次差异 | 精确 **McNemar** + 多重比较校正（Holm） | 📄 2609.17394（Verified top30 相邻对 0/29 显著） |
| 小样本 | 用 Dirichlet **后验可信区间**替代 pass@k（非重叠 CI 作显著性判据） | 📄 2510.04265 |
| 全失败题 | 先过有效性筛查（oracle / 基础设施 / verifier 绕过）再当"难题" | 📄 2609.26826（125 个全失败题只有 78 个合格） |
| 方差分解 | 报"agent 主效应 / agent×task 交互 / 任务 / 重复"分量 | ✅ 2610.00651（固定 model-scaffold 系统排名可靠性 0.935–0.994，但**底层模型**排名可靠性仅 0.148–0.841；任务数无限增加最多只提升 0.097，瓶颈是 scaffold 覆盖度）；📄 2608.11323（agent 主效应 <3%、agent×task 交互 7–23%） |

> ⚠️ claim 决定设计：✅ 2610.00651 的核心提醒是"reliability is **claim-dependent**"——你要排的是"部署系统"（固定 harness 比模型）还是"底层模型"（固定模型比 harness），两者的样本预算与统计口径完全不同。**先写 claim，再决定怎么固定。**

---

## 4. 常见陷阱（按危害排序）

| # | 陷阱 | 证据 |
|---|---|---|
| 1 | **只报 pass@1，不报成本/资源** | ✅ 2407.01502《AI Agents That Matter》：只盯准确率 → SOTA 又贵又复杂，社区对"增益来自哪里"得出错误结论；✅ 2607.22585（40× token 差被分数掩盖） |
| 2 | **把换 harness 的效应与重跑噪声混为一谈** | ✅ 2610.04433（两边都是 13% 翻转）；✅ 2607.03691（先做重跑一致性验证） |
| 3 | **模型悄悄变了**（厂商默认别名/静默更新） | ✅ 2607.03691 专门自托管来消除该混淆 |
| 4 | **harness 版本/配置未 pin，或基线与被测不在同一层** | ✅ 2606.10106（"harness" 一词混用：产品 / eval harness / framework / orchestrator，比较前必须先界定边界） |
| 5 | **只看终态、忽略轨迹** | ✅ 2610.01833（92.6% 仍违反轨迹检查）；📄 2605.12925、2606.11686 |
| 6 | **reward / verifier 设计错误** | ✅ 2608.14711：pass@k 被**误用**（n 用单元测试数而非独立 rollout），在合成多 rollout 基准上把分数虚高 **0.85–0.97**（报 0.96–0.98 vs 校正后 0.00–0.12）；单次 rollout 代理不能替代重复跑（Spearman ρ=0.417）；其 SWE-bench 小规模试点里 **macro hidden-test pass 0.80 而严格任务解决率仅 0.20** |
| 7 | **污染 / 泄漏（含 scaffold 泄漏）** | ✅ 2610.05830：把污染拆成训练期暴露 / 评测期检索 / **pipeline-scaffold 泄漏** 三通道，9 个 HAL 配置 × 3 通道 = 27 项评估**无一可判为 closed**、4 个配置确认有事件；缺少 provenance、对照与**已验证 scorer** 时更强主张不成立 |
| 8 | **聚合指标掩盖局部回归** | ✅ 2607.03691 用分层抽样而非单一总分；📄 2606.11686 |
| 9 | **harness 与模型耦合**（harness 只对某模型调过 prompt） | ✅ 2610.00917（名次反转）；📄 2509.09853（有效性取决于 scaffold 与 base model 的**契合度**）、2608.10178（演化出的 harness 本质是"补偿特定模型的执行缺陷"，缺陷趋零则增益趋零） |
| 10 | **基础设施噪声被当成模型能力** | 📄 Anthropic infrastructure-noise：资源配额 1x → 无上限 = **+6pp（p<0.01）**，infra error 5.8% → 0.5%；建议"leaderboard 差距 <3pp 应持怀疑，直到配置被记录并对齐" |
| 11 | **judge/scorer 未标定就下结论** | ✅ 2610.05830（复现 scorer 未通过验证门）；📄 2609.34198（所有 judge 都拒绝"任务条件化误差不变"假设；假接受率随 agent 能力上升）、2504.08942（规则式评估会**低报**） |
| 12 | **改 harness 没有回归门** | 📄 2607.14004（无回归控制的方法迁移后**低于**未优化 baseline）、2606.09498（编辑须 held-in + held-out 双通过才接受） |

---

## 5. 现成基建：别自己写 runner

| 用途 | 工具 | 为什么 |
|---|---|---|
| 跑 Terminal-Bench / 任意 agent × 任意模型 × 任意沙箱 | **Harbor**（Terminal-Bench 官方 harness） | 命令行就是 `-a <agent> -m <model> -d <dataset>`，内置 40+ agent（claude-code、codex、openhands、mini-swe-agent、swe-agent、aider、goose、opencode…）；`harbor view/upload` 看轨迹 📄 |
| 跑 SWE 类 harness 横向对比 | **Claw-SWE-Bench** | 原生为"固定模型比 harness"设计：7 harness × 3 model × 350 题 × 3 runs；adapter 协议 5 个方法（`create_agent`/`send_task`/`backup_session`/`delete_agent`/`get_docker_args`）；**统一 task prompt，但刻意不统一 hidden system prompt / tool schema / memory policy / stopping rule——它们就是实验变量**；patch 由 runner 从 git 导出 📄 |
| 极简对照基线 | **mini-swe-agent**（~100 行 agent class） | 用来防"复杂一定更好"（📄 2407.01489 Agentless、2605.05716 单工具 > All-In） |
| 通用 eval / scorer / 日志 | **Inspect AI**（UK AISI） | Solvers / Scorers / Agents / Eval Sets / Log Viewer 📄 |
| 多维可靠性指标 | **HAL Reliability Dashboard** | 12 指标 × 4 维度，直接抄指标定义 ✅ |

**题集与规模建议**
- 迭代集 50–80 题（如 SWE-bench Verified Mini 50、Claw Lite-80）；出结论 350–500 题。
- 判分环境先自检：先跑 gold patch，剔除"gold 也跑不过"的坏题（✅ 2607.03691 剔了 8 题）。
- 成本量级心里有数：Claw full-350 × 3 runs ≈ 1,430 小时；HAL 21,730 rollouts ≈ $40,000 ✅。

---

## 6. 给 mini_code 的最小可行评测（MVS）

### 6.1 现状核查（我读了 `src/` 与 `index.ts` 后的结论）

| 评测需要 | 现状 | 缺口 |
|---|---|---|
| token / 成本核算 | `src/agents.ts:120` 用 `client.chat.completions.create({..., stream:true})`，**未开 `stream_options.include_usage`**，且流式循环里没有读取 usage | ❌ 拿不到 token 数 |
| 轮次上限（T 维度） | `while(true)`，**无 max_turns** | ❌ 无法界定交互深度，跑飞会污染成本统计 |
| 批量/非交互运行 | `index.ts` 只有 `runRepl(agent)`（readline REPL） | ❌ 无法脚本化跑任务集 |
| 轨迹落盘 | `.mini_code/sessions/*.json` 存消息（`src/session.ts`），但**不含任何指标** | ⚠️ 有轨迹，缺指标 |
| 每题隔离 | 工具直接在 cwd 执行 shell | ❌ 任务间会互相污染 |
| 模型切换 | 由 `env.conf` 的 `USAGE/LOCAL_MODEL/REMOTE_MODEL` 决定 | ⚠️ 评测需按 run 覆盖并冻结 |

### 6.2 阶段 0：四处小改（前置条件，各半天内）

1. **采集 usage**：`stream:true` 加 `stream_options:{ include_usage:true }`，在流式循环里捕获最后一个含 `usage` 的 chunk，累加 `prompt_tokens / completion_tokens / prompt_tokens_details.cached_tokens`。
2. **加 `max_turns`**：`while(true)` 换成有界循环，超出时记 `failure_category = MAX_TURNS`（这是 ✅ 2607.22585 的失败指纹类别之一，也是 ✅ 2609.20804 里显式变化的 T 维度）。
3. **加 headless 模式**：`bun run index.ts --task "<prompt>" --out run.json`，跑完一轮写一条运行记录后退出。
4. **每题独立沙箱**：任务在 `git worktree`（或容器）里跑，题间重置。

**每题的运行记录（照抄这套字段，一次到位）：**
```json
{
  "task_id": "...", "harness_commit": "<git rev-parse HEAD>",
  "model": "<provider/model@version>", "run_index": 1,
  "resolved": false, "patch_apply_failed": false,
  "turns_used": 0, "hit_turn_budget": false,
  "tokens_input": 0, "tokens_cached": 0, "tokens_output": 0, "tokens_total": 0,
  "tool_calls": 0, "no_action_turns": 0,
  "wall_seconds": 0, "cost_usd": 0,
  "failure_category": "REASON|VERIFY|TIME|MAX_TURNS|HANG|ERROR|null",
  "session_id": "..."   // 指向 .mini_code/sessions 里的完整轨迹
}
```

### 6.3 阶段 1：题集——优先用你自己仓库的已合并 PR（byobench 思路）

比接 SWE-bench 便宜得多，而且**任务分布就是你的真实工作分布**（📄 byobench 作者在 HN 的原话：公开 benchmark "get aggressively optimized against, and their tasks don't necessarily resemble what we consider a unit of work"）。

做法：
1. 挑 **30–50 个已合并 PR**，按改动规模分层（改 1–2 文件 = easy、3–5 = medium、>5 = hard）。
2. 每个任务：checkout 到该 PR 的**父 commit** → 把 PR 描述改写成 issue 文本 → 给 agent → 跑该 PR 对应的测试子集判定 resolved。
3. 留 15 个不参与调参的 PR 作 **held-out**（📄 byobench 也是这么验证 router 的）。
4. 判分**只看仓库终态与测试结果**，不看 agent 自报完成（📄 2608.08654：不信自报后才发现 agent 常忽略被指定的接口）。

### 6.4 阶段 2：三个配置，同一模型

用**同一个模型 + 精确版本**跑三个配置：
1. `mini_code` 当前版（要评测的对象）
2. `mini_code` 的上一版或"关掉某组件"版（组件消融）
3. `mini-swe-agent`（极简对照基线，防止"复杂一定更好"）

每条 3 次重复，先跑"同配置重跑"确认噪声可控（✅ 2607.03691 的做法是报两次运行的二值一致率）。

### 6.5 阶段 3：指标与统计（只做这几样就够）

1. pass@1（题内先平均 3 次、再跨题平均，每题等权）与 **pass^3**（3 次全对）。
2. **tokens per solved task**（Σ tokens ÷ solved 数，失败 token 计入）与 USD per solved task（拆分 cached/uncached/output）。
3. **95% paired-task bootstrap CI（B=10,000）**，题内配对。
4. 失败类别分布（判断是 harness 问题还是模型问题：**指纹跨模型复现 ⇒ harness 属性**）。
5. 明确写出**最小可分辨差异**，别在 30 题上下名次结论。

### 6.6 阶段 4：组件消融顺序（按性价比，从最可能出数的地方开始）

| 顺序 | 改什么 | 参考效果 |
|---|---|---|
| 1 | **输出契约**：让模型改文件、runner 从 git 导 patch，而不是让模型手写 diff | 📄 Claw-SWE-Bench：resolved 19.3% → **71.2%**；patch apply 失败率 <1.5% |
| 2 | **工具输出处理**：截断策略（掐中间保留首尾）、超时返回 partial output、结构化字段（command/status/exit_code/output/error） | 📄 2606.17454（SSA 复现/超过公开 pass@1 的 61/66 个组合） |
| 3 | **上下文管理**：只保留最近 N 个 observation / 压缩策略 | ✅ 2609.20804：收益主要来自**避免 overflow 失败**；"规则式 elision 先行 + LLM 摘要"整体最省；"让被裁内容可恢复"几乎没模型用且不涨分。✅ 2607.03691：不做上下文管理（全历史）会推高 token |
| 4 | **planning**：加/去显式计划 | ✅ 2609.20804：对弱模型是准确率脚手架，对强模型只是省钱 |
| 5 | **action space**：bash-only 还是预定义工具 | ✅ 2609.20804：bash 能力强的模型 bash-only 大幅更便宜 |
| 6 | **skill 机制**（你已有） | 📄 SkillsBench：paired 设计平均 +16.6pp，**≤3 模块的聚焦 skill 优于大 bundle**，配置级 +4.1~+25.7pp |
| 7 | **长任务结构**：initializer + progress file + feature list + 一步步做 | ✅ Anthropic：修掉 4 类失败模式（过早宣布完成、留下 bug/无记录进度、feature 提前标 done、不会启动 app），且强调"其余 system prompt、工具集与 harness **完全相同**，唯一变量是首轮 prompt" |

> ⚠️ 组件别贪多：📄 2605.05716 的全因子实验（2^5=32 子集 × 96 条件 × 10 seeds）显示 "All-In" 一贯次优（单工具比全组件在 HotpotQA 高 32%，p=0.023），且 **183/325 个子模性违规（56.3%）** ⇒ **不要用 greedy 逐个叠加来选组件**。

### 6.7 阶段 5：回归门（每次改 harness 必过）

1. 改动前写一条**可证伪预测**（"这次改动应该让 easy 层的 token 降 10%，resolve 不变"）。
2. 在**行为相关**的任务子集上验证（省预算且防回归）。
3. **held-in + held-out 双通过**才接受，否则 rollback。
4. 分层看：聚合分数不动，不代表没坏（📄 2606.11686：聚合仅 −1.7~−5.9pp，对应层切片崩 −25~−91pp）。

---

## 7. 一句话交付标准（报告里必须写全）

模型版本 + 日期 · harness commit/版本 · system prompt 与工具 schema（或明确声明未披露）· max_turns · 超时 · 资源配额（floor + ceiling 分开声明）· 并发 · 采样参数（温度/top_p 显式覆盖或声明用默认）· benchmark 版本 · 运行日期与时段 · 每题原始记录与轨迹 · 最小可分辨差异。
> 依据：✅ 2605.23950（Stop Comparing LLM Agents Without Disclosing the Harness）提出 harness-aware evaluation framework，含 **disclosure standard + variance decomposition protocol**，并主张"在 harness 规格被披露前，长程 agent 的榜单比较应视为不完整且可能误导"。

---

## 8. 验证状态（哪些数字我亲自核对过）

**✅ 我抓取并逐条核对过全文：** **2607.03691**（arXiv HTML 全文：35 个 release / 50 题分层 / 600s 超时 / 2 次重复 / 全部 Finding 数字 / Wilcoxon 与 Spearman 检验值 / 失败任务成本对比 / PR 删代码后的 token 变化）。
**✅ 我抓取并逐条核对过摘要：** 2610.04433、2610.00917、2607.22585、2605.23950、2609.20804、2609.32459、2608.08654、2605.27922、2605.05716、2610.04921、2606.12344、2610.00651、2510.11977、2407.01502、2610.08432、2606.10106、2610.05830、2608.14711、2604.14877、2406.12045（均为 arXiv API 返回的官方摘要原文）。
**✅ 我抓取并核对过的非 arXiv 页面：** hal.cs.princeton.edu（榜单含 $ 成本列、"updated scaffold … drastically outperforms the CORE-Agent scaffold"）、hal.cs.princeton.edu/reliability（4 维度 12 指标定义与结论原文）、anthropic.com 两篇工程博客（effective harnesses for long-running agents / building effective agents）。
**✅ 引用真伪抽查：** 对 14 个 arXiv id 逐个 `id_list` 查询，全部存在且标题与两份报告所述一致，未发现子代理引用失真；另有 7 个 id 在核对数字时二次拉取摘要。
**📄 来自两份详细调研报告（均带 URL，我未逐条回原文核对）：** 其余引用，尤其 Claw-SWE-Bench 的具体表格数字（7 harness × 3 model、24.3pp、19.3%→71.2%、Table B.2 参数）、Harbor / Inspect AI 的用法细节、byobench、Anthropic infrastructure-noise（+6pp / 5.8%→0.5% / "<3pp 应怀疑"）、MLE-bench 官方 ≥3 seeds 要求、各 leaderboard 的列定义、HN 讨论内容、SSA / SWE-agent ACI 的逐组件消融数字。
**已知未验证：** Agent Harness Engineering Survey（ETCLOVG，未上 arXiv）；2609.17817（仅有标题）；OpenCastor / neuralnoise harness-bench WIP / agent-memory-leaderboard（仅 HN 标题）。
**检索踩坑（供复现）：** arXiv API 连续 7–10 次请求后返回 HTTP 429，需 sleep 60–90s；组合查询 `all:"a" AND all:"b"` 必须用 `curl -G --data-urlencode`，手工拼 `%22` 会被二次编码而返回 0 结果；arXiv API 必须带 User-Agent（否则空响应）。
