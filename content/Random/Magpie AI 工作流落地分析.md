---
tags:
  - AI
  - Agent
  - 工作流
source: https://x.com/wquguru/status/2109650264601117141
created: 2026-10-15
---

# Magpie AI 工作流落地分析

> 源自 wquguru 对 magpie 仓库 19 天 2862 个 commit 的复盘：AI 代码由 agent 写、审、合、发，人只管方向和闸门。

## 核心机制：一张路由表 + 一本错题本

### 1. CLAUDE.md 只引用两个文件

- **AGENTS.md（路由表）**：不写规则，只指路——改子系统看 docs/subsystems/，写代码看 docs/code-standards.md，审社区 PR 看 docs/contributors.md
- **LESSONS.md（错题本）**：479 行，agent 每晚自己写

### 2. 夜间复盘（错题本）

每天夜里 agent 过一遍当天 commit，只找三类问题：

1. 修完又返工的
2. 压根不该合的
3. 验证做得太糙的

每条教训格式：

```
**<一句话规则>**
- <commit / issue 号，后果>
- <修复 commit>
- Done right: <做对的例子>
- Seen N× (YYYY-MM-DD, ...)
```

### 3. Seen 3× 升级机制（最关键）

同一条教训在 3 个不同日子出现 → 从 LESSONS.md 挪进 code-standards.md，从经验变成硬规则，之后每个 PR 逐条对照。

> 效果实证：LESSONS.md 10-6 引入前日发 168 版，之后 42 → 15，稳定在 15~26。没人开会，靠错题本自己踩刹车。

### 4. PR 验收标准（6 条全过才能合并）

少见的三条：

- **回退测试**：旧代码放回去，新测试必须真的挂，指出具体行为；编译不过/跳过不算
- **真实使用**：改了厂商接入必须拿真账号真接口验；没实测的功能不许接着开发
- **没跑的要写出来**：'A check that wasn't run is listed as not run, never left out.'

### 5. 合并安全

合并命令带 --match-head-commit <审过的 sha>，审的过程中有人 push 则合并失败，保证审过的代码才能进。

### 6. Human in the Loop（人只管三件事）

- 拍过板的产品决定（Don't reverse deliberate decisions）
- 安全闸门：风险检查命中等 maintainer 放行
- 社区报告人建议

人说话方式示例（commit 标题里留着原话）：

> (the owner: 这个太丑了) / (owner: pr-preview 没数据测不了，能否造些假数据)

一句话吐槽，agent 补齐成可验证的改动。

## 普通开发者的最小可行性方案（MVP）

不必学它 19 天 1204 个版本的发版频率，抄这四样就够：

### Step 1：两文件起步（半天）

在仓库根目录建：

1. **AGENTS.md / CLAUDE.md 路由表**：项目结构 + 去哪找规则，控制在 100 行内
2. **LESSONS.md 错题本**：照上面的格式写第一条

### Step 2：每日夜审（自动化）

每天让 agent 跑一次：

> '读一下今天所有 commit / PR，找三类问题：返工的、不该合的、验证不足的。按 LESSONS.md 格式追加，每条挂 commit 号作证据。'

可以是 Claude Code 定时任务或手动每晚一条 prompt。先手动跑一周，稳定后再自动化。

### Step 3：Seen 3× 规则

每周检查 LESSONS.md 的 Seen 计数，出现 3 次的挪进 code-standards.md。这一步是整个系统能自我改进的核心。

### Step 4：PR 验收三件套

给 agent 的 PR 说明里要求：

- 回退测试（故意破坏看测试是否抓到）
- 真实使用验证（能实测就实测，不能就标 Not run）
- 合并前 PR 评论里列出跑了什么、没跑什么

### 落地优先级

| 优先级 | 项 | 成本 | 收益 |
|---|---|---|---|
| P0 | LESSONS.md + 每日复盘 | 低 | 立刻减少返工 |
| P0 | Seen 3× 升级 | 极低 | 规则自动沉淀 |
| P1 | PR 三件套验收 | 中 | 减少'假修复' |
| P2 | AGENTS.md 路由表 | 低 | agent 找上下文更快 |
| P3 | --match-head-commit 类安全合并 | 低 | 防未审代码混入 |

### 一句话总结

> 路由表谁都会写，真正要抄的是错题本：犯过的错写下来，agent 下次一定读到；同一个错犯满三天就升成硬规则。

## 参考

- [原推文](https://x.com/wquguru/status/2109650264601117141)
- magpie: yetone/magpie（本地 LLM 网关）
- 对照项目：OpenClaw（人主导 vs agent 主导的对比）
