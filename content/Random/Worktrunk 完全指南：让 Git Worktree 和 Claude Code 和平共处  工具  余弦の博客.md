---
tags:
  - "#literature"
URL: "https://blog.cosine.ren/post/git-worktrunk-guide"
author:
  - "[[cos]]"
created: 2026-03-15
---
## Worktrunk 完全指南：让 Git Worktree 和 Claude Code 和平共处

发表于 2025-12-31 20:10 3250 字 17 min read

![cover](https://blog.cosine.ren/img/site_header_1920.webp)

## 写在前面

最近用 Claude Code 写代码的频率越来越高，有时候会同时开三四个任务：一个在修 bug，一个在加新功能，一个在 review 中，还有一个在跑测试验证新点子。问题来了：它们都需要独立的工作目录，不然会互相串代码。

Git 的 `worktree` 功能本来就是为这种场景设计的，但原生命令实在有些啰嗦。传统创建一个新 worktree 要这样：

```bash
git worktree add -b feature-auth ../myproject-feature-auth
cd ../myproject-feature-auth
```

删掉它又得回到主目录：

```bash
cd ../myproject
git worktree remove ../myproject-feature-auth
git branch -d feature-auth
```

分支名要输三次，每次都要手动 `cd` 。干这事儿多了，会觉得有些浪费生命，这也是我之前为什么不喜欢 worktree。

直到发现 [Worktrunk](https://worktrunk.dev/) ，才发现 worktree 管理原来可以这么优雅（当然还有很多别的工具）。

用下来感觉非常好，写一篇博客卖一卖安利。

## Worktrunk 是什么

简单来说，Worktrunk 是一个 **Git Worktree 的 CLI 包装工具** ，专门为 **并行运行多个 AI Agent** 的场景优化。它的核心理念是：

> **每个 worktree 对应一个分支，用分支名管理 worktree，路径自动生成。**

对比一下命令差异就能感受到差异：

| 任务 | Worktrunk | 原生 Git |
| --- | --- | --- |
| 切换到某个 worktree | `wt switch feat` | `cd ../repo.feat` |
| 创建 worktree + 启动 Claude | `wt switch -c -x claude feat` | `git worktree add -b feat ../repo.feat && cd ../repo.feat && claude` |
| 清理当前 worktree | `wt remove` | `cd ../repo && git worktree remove ../repo.feat && git branch -d feat` |
| 列出所有 worktree 状态 | `wt list` | `git worktree list` (只显示路径) |

基本就是把 `git worktree` 的操作复杂度从「记三个参数」降到「说个分支名」。

## 为什么需要 Worktrunk?

如果你只是偶尔用一下 worktree，原生命令当然就行了。但当你需要 **频繁并行开发** （比如同时跑多个 AI Agent）或者 **需要自动化流程** （创建 worktree 后自动装依赖、跑测试）的时候，Worktrunk 能省下不少时间和心智负担。它本质上是把「用 worktree 的正确姿势」固化成了工具。

## 安装与配置

### 安装

**macOS/Linux (推荐 Homebrew)：**

```bash
brew install max-sixty/worktrunk/wt
```

**或者用 Cargo：**

```bash
cargo install worktrunk
```

### Shell 集成

装完之后 **必须跑这一步** ，否则 `wt switch` 无法切换目录：

```bash
wt config shell install
```

它会在你的 `.zshrc` 或 `.bashrc` 里加一段函数，让 `wt` 命令可以改变当前 shell 的工作目录。

装完重启终端，跑 `wt --version` 确认安装成功。

## 核心命令详解

### wt switch - 切换/创建 Worktree

[wt switch | Worktrunk](https://worktrunk.dev/switch/)

这是最常用的命令，用法极简：

```bash
# 切换到已存在的 worktree (分支名 feat)
wt switch feat

# 基于主分支 main 创建新 worktree + 分支 feat
wt switch -c feat

# 创建 worktree + 自动启动 Claude Code
wt switch -c feat -x claude

# 基于 dev 分支创建新 worktree + 分支 feat-new (而不是 main) + 自动启动 claude
wt switch -c feat-new -b dev -x claude
```

**路径规则** ： Worktrunk 会自动在主仓库的 **同级目录** 下创建 worktree，命名格式是 `<repo>.<branch>` 。比如主仓库在 `~/code/myproject` ，分支 `feat` 的 worktree 就在 `~/code/myproject.feat` 。

**参数说明** ：

- `-c` / `--create` ：创建新 worktree + 分支
- `-x <cmd>` ：切换后自动执行命令 (比如 `claude`, `code`, `npm install`)
- `-b <base>` ：指定基础分支 (默认是 `main`)

| Shortcut | 含义 |
| --- | --- |
| `^` | 默认分支（main/master） |
| `@` | 当前分支/工作树 |
| `-` | 之前的工作目录（例如 `cd -` ） |
|  |  |

```bash
wt switch -                      # Back to previous
wt switch ^                      # Default branch worktree
wt switch --create fix --base=@  # Branch from current HEAD
```

#### 实战场景

假设你在跑三个并行任务：

```bash
# Terminal 1: 修复认证 bug
wt switch -c -x claude fix-auth

# Terminal 2: 重构 API
wt switch -c -x claude refactor-api

# Terminal 3: 加新功能
wt switch -c -x claude feat-dashboard
```

每个 Claude 实例跑在独立目录里，互不干扰。

### wt list - 查看所有 Worktree

[wt list | Worktrunk](https://worktrunk.dev/list/)

```bash
wt list
```

输出大概长这样:

```bash
wt list
  Branch       Status        HEAD±    main↕  Remote⇅  Commit    Age   Message
@ feature-api  +   ↕⇡     +54   -5   ↑4  ↓1   ⇡3      ec97decc  30m   Add API tests
^ main             ^⇅                         ⇡1  ⇣1  6088adb3  4d    Merge fix-auth: hardened to…
+ fix-auth         ↕|                ↑2  ↓1     |     127407de  5h    Add secure token storage

○ Showing 3 worktrees, 1 with changes, 2 ahead, 1 column hidden
```

![](https://r2.cosine.ren/i/2025/12/b12f258c2137deadbbc05beada5680de.webp)

比原生 `git worktree list` 强很多，可以看到很多信息

- **Git 状态** ：有多少未提交/未追踪文件
- **CI 状态** ：如果配置了 GitHub Actions,会显示最新的构建状态

对于管理多个 worktree 来说,这个视图非常实用。

### wt remove - 清理 Worktree

[wt remove | Worktrunk](https://worktrunk.dev/remove/)

```bash
# 删除当前 worktree + 分支
wt remove

# 删除指定 worktree
wt remove feature-branch
wt remove old-feature another-branch

# 删除 worktree 但保留分支
wt remove --no-delete-branch feature-branch

# 强制删除未合并的分支
wt remove -D experimental
```

### wt merge - 合并工作流

[wt merge | Worktrunk](https://worktrunk.dev/merge/)

这个命令封装了「合并 → 清理」的完整流程：

```bash
# 把当前 worktree 合并到默认分支 如 main
wt merge
# 把当前 worktree 合并到 dev 分支
wt merge dev
# 合并后保留工作树
wt merge --no-remove
# 保留提交历史（不合并）
wt merge --no-squash
# 跳过提交/合并（除非使用 --no-rebase 参数，否则 rebase 仍会运行）
wt merge --no-commit
```

如果配置了 [**pre-merge hook**](https://worktrunk.dev/hook/) ，会在合并前自动跑测试或 lint。

### wt select - 交互式选择器

[wt select | Worktrunk](https://worktrunk.dev/select/)

如果你记不清 worktree 名字,可以用 `select` 命令:

```bash
wt select
```

会弹出一个 fzf 风格的界面,用方向键选择要切换的 worktree。

![](https://r2.cosine.ren/i/2025/12/362d232f3f5a0d035809dcbe2e14ab46.gif)

## Hooks

[wt hook | Worktrunk](https://worktrunk.dev/hook/)

Worktrunk 支持在 worktree 生命周期的不同阶段执行命令，同时支持全局用户 hook 配置（ `~/.config/worktrunk/config.toml` ）和项目 hook 配置（ `.config/wt.toml` ） 好的,我只给你补充 Hook 系统这一段内容:

### Hook 类型一览

| Hook | 触发时机 | 阻塞模式 | 失败即停 |
| --- | --- | --- | --- |
| `post-create` | worktree 创建后 | 是 | 否 |
| `post-start` | worktree 创建后 | 否(后台) | 否 |
| `post-switch` | 每次切换后 | 否(后台) | 否 |
| `pre-commit` | merge 时提交前 | 是 | 是 |
| `pre-merge` | 合并到目标分支前 | 是 | 是 |
| `post-merge` | 合并成功后 | 是 | 否 |
| `pre-remove` | worktree 删除前 | 是 | 是 |

**阻塞模式**: 命令执行完成前,主流程会等待  
**失败即停**: 第一个失败的命令会中止整个操作

### 核心 Hooks 说明

**post-create** - worktree 创建后立即执行,会阻塞直到完成:

```toml
[post-create]
install = "npm ci"                    # 安装依赖
migrate = "npm run db:migrate"        # 数据库迁移
env = "cp .env.example .env"          # 复制环境配置
```

**post-start** - worktree 创建后在后台执行,不阻塞切换:

```toml
[post-start]
build = "npm run build"               # 构建项目
server = "npm run dev"                # 启动开发服务器
```

日志输出到 `.git/wt-logs/{branch}-{source}-post-start-{name}.log`

**post-switch** - 每次 `wt switch` 后在后台执行(无论是新建、切换还是切到当前):

```toml
post-switch = "echo 'Switched to {{ branch }}'"
```

**pre-commit** - merge 时提交前执行,失败即停:

```toml
[pre-commit]
format = "cargo fmt -- --check"       # 代码格式检查
lint = "cargo clippy -- -D warnings"  # Lint 检查
```

**pre-merge** - 合并到目标分支前执行,失败即停:

```toml
[pre-merge]
test = "cargo test"                   # 运行测试
build = "cargo build --release"       # 生产构建
```

**post-merge** - 合并成功后在目标分支的 worktree 执行(如果存在),否则在主 worktree 执行:

```toml
post-merge = "cargo install --path ."
```

**pre-remove** - worktree 删除前执行,失败即停:

```toml
[pre-remove]
cleanup = "rm -rf /tmp/cache/{{ branch }}"
```

### 模板变量

Hook 命令支持模板变量,运行时自动展开:

| 变量 | 示例 | 说明 |
| --- | --- | --- |
| `{{ repo }}` | my-project | 仓库名 |
| `{{ branch }}` | feature-foo | 分支名 |
| `{{ worktree }}` | /path/to/worktree | worktree 绝对路径 |
| `{{ worktree_name }}` | my-project.feature-foo | worktree 目录名 |
| `{{ repo_root }}` | /path/to/main | 主仓库根路径 |
| `{{ default_branch }}` | main | 默认分支名 |
| `{{ commit }}` | a1b2c3d4e5f6… | HEAD 完整 SHA |
| `{{ short_commit }}` | a1b2c3d | HEAD 短 SHA |
| `{{ remote }}` | origin | 主远程名称 |
| `{{ remote_url }}` | [git@github.com](mailto:git@github.com) /repo.git | 远程 URL |
| `{{ upstream }}` | origin/feature | 上游跟踪分支 |
| `{{ target }}` | main | 目标分支(仅 merge hooks) |

### 安全机制

项目 hook(`.config/wt.toml`)首次运行需要用户批准:

```plain
▲ repo needs approval to execute 3 commands:
○ post-create install:
  echo 'Installing dependencies...'
❯ Allow and remember? [y/N]
```

- 批准记录保存在用户配置中
- 命令变更需要重新批准
- `--yes` 跳过提示(适用于 CI)
- `--no-verify` 完全跳过 hooks

管理批准记录:

```bash
wt hook approvals add      # 预批准当前项目所有命令
wt hook approvals clear    # 清除当前项目批准
wt hook approvals clear --global  # 清除全局批准
```

### 用户级 Hooks

在 `~/.config/worktrunk/config.toml` 中配置的 hook 会对所有仓库生效,且不需要批准:

| 维度 | 项目 hook | 用户 hook |
| --- | --- | --- |
| 配置位置 | `.config/wt.toml` | `~/.config/worktrunk/config.toml` |
| 作用范围 | 单个仓库 | 所有仓库 |
| 需要批准 | 是 | 否 |
| 执行顺序 | 后执行 | 先执行 |

我觉得看下来，这个 hook 非常重要，可以 **复用主 worktree 的缓存**:

```toml
[post-create]
# 软链接 node_modules 避免重复安装
cache = "ln -sf {{ repo_root }}/node_modules node_modules"
env = "cp {{ repo_root }}/.env.local .env"
```

### 独立运行 Hooks

除了自动触发,也可以手动运行 hook 进行测试或重试:

```bash
wt hook pre-merge           # 运行 pre-merge hooks
wt hook pre-merge --yes     # 跳过批准提示(适用于 CI)
wt hook show                # 查看所有已配置的 hooks
```

**适用场景**: Hook 开发测试、CI 流水线、失败后重试等。

### Claude Code 插件监测状态

```bash
claude plugin marketplace add max-sixty/worktrunk
claude plugin install worktrunk@worktrunk
```

#### 手动设置状态标记

除了自动追踪 Claude 状态,你也可以手动给 worktree 设置任何标记，用于其他工作流：

```bash
# 给当前分支设置标记
wt config state marker set "🚧"

# 给指定分支设置标记
wt config state marker set "✅" --branch feature

# 直接操作 Git Config (高级用法)
git config worktrunk.state.feature.marker '{"marker":"💬","set_at":0}'
```

#### Statusline 状态栏

`wt list statusline --claude-code` 可以输出一行紧凑的状态信息,用于 Claude Code 的状态栏显示:

```plain
~/w/myproject.feature-auth !🤖 @+42 -8 ↑3 ⇡1 ● | Opus
```

## LLM Commit Messages 自动生成提交信息

[LLM Commit Messages | Worktrunk](https://worktrunk.dev/llm-commits/)

Worktrunk 可以调用 LLM 自动生成 commit message，集成在 `wt merge` 、 `wt step commit` 、 `wt step squash` 等命令中。

不配置也能用，默认会基于文件名生成简单的 message，但配置 LLM 后能生成更有意义的提交信息。

### 安装与配置

**1\. 安装 llm 工具**

使用的是 [llm](https://llm.datasette.io/) ：

```bash
uv tool install -U llm
# 或者直接 brew
brew install llm
```

**2\. 配置 API Key**

选择你喜欢的 LLM 提供商：

```bash
# 使用 Claude (推荐)
llm install llm-anthropic
llm keys set anthropic
# 输入你的 Anthropic API Key

# 或者使用 OpenAI
llm keys set openai
# 输入你的 OpenAI API Key
```

**3\. 配置 Worktrunk**

创建配置文件（如果还没有）：

```bash
wt config create
```

编辑 `~/.config/worktrunk/config.toml` ，添加：

```toml
[commit-generation]
command = "llm"
args = ["-m", "claude-3-5-haiku-latest"]  # 或 gpt-4o-mini
```

### 使用场景

配置完成后，以下命令会自动生成 commit message：

**场景 1: 合并分支时生成 squash commit**

```bash
$ wt merge
◎ Squashing 3 commits into a single commit (5 files, +48)...
◎ Generating squash commit message...
   feat(auth): Implement JWT authentication system

   - Add JWT token generation and validation
   - Implement refresh token mechanism
   - Add middleware for protected routes
```

**场景 2: 提交当前变更**

```bash
$ wt step commit
◎ Generating commit message...
   fix(api): Handle null response in user endpoint
```

**场景 3: 把多个 commit 压缩成一个**

```bash
$ wt step squash
◎ Squashing 5 commits...
◎ Generating squash commit message...
   refactor(ui): Modernize component architecture
```

### 使用其他 AI 工具

除了 `llm` ，任何能从 stdin 读取提示词并输出文本的工具都行：

```toml
# 使用 aichat
[commit-generation]
command = "aichat"
args = ["-m", "claude:claude-3-5-haiku-latest"]

# 使用自定义脚本
[commit-generation]
command = "./scripts/generate-commit.sh"
```

### Fallback 行为

如果没配置 LLM，Worktrunk 会生成基于文件名的简单 message：

```plain
Changes to auth.rs & config.rs
```

## CI 状态集成

如果你用 GitHub Actions,Worktrunk 可以在 `wt list` 里显示构建状态:

```bash
# 配置 GitHub Token
wt config github.token "ghp_xxxxxxxxxxxx"

# 之后 wt list 就会显示 CI 状态
wt list
```

## 实战工作流

### 并行跑多个 Claude Code

假设你在用 [Zellij](https://zellij.dev/) 或 Tmux 管理多个终端窗口:

```bash
# Pane 1: 修 bug
wt switch -c -x claude fix-login-bug

# Pane 2: 重构
wt switch -c -x claude refactor-utils

# Pane 3: 新功能
wt switch -c -x claude feat-export
```

每个 Claude 在独立目录里工作,你可以随时切回主目录看全局状态:

```bash
wt switch main
wt list
```

### 临时验证想法

有时候你想快速验证一个想法,但不想污染当前分支:

```bash
# 创建临时 worktree
wt switch -c -x code experiment

# 验证完毕,直接删掉
wt remove
```

因为 worktree 是独立目录,删掉不会影响其他分支。

### Review PR 时跑代码

有 PR 来了,你想在本地跑一下代码:

```bash
# 基于 PR 分支创建 worktree
wt switch -c review-pr-123 -b origin/pr-123

# 装依赖、跑测试
npm install
npm run test

# Review 完毕,清理
wt remove
```

## 参考资料

- [Worktrunk 官网](https://worktrunk.dev/)
- [Anthropic - Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices) (官方推荐的 worktree 工作流)
- [incident.io - Shipping faster with Claude Code and Git Worktrees](https://incident.io/blog/shipping-faster-with-claude-code-and-git-worktrees)
- [Git Worktree 官方文档](https://git-scm.com/docs/git-worktree)