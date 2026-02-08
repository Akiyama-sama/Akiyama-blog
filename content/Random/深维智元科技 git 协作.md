---
date: 2026-01-26
tags:
---
# Git 快速开始指南

> 分支策略主要采用 gitlab flow 降低心智负担
> 
> 主要分支：
> 
> - main - 主分支，始终保持稳定可发布状态
>     
> - release/x.x.x - 生产环境分支，当前部署的版本
>     
>       临时分支：
>     
> - dev-个人姓名 - （可选）开发分支，用于集成新功能
>     
> - feature/功能名 ｜fix**Bug名** - 功能开发分支 ｜修复bug
>     
> - hotfix/紧急修复 - 生产环境紧急修复
>     

![](https://scn7nr4axh9v.feishu.cn/space/api/box/stream/download/asynccode/?code=NDM4ZmY0NTg3OWY4YzgwMDIwMzc2YTJhN2FlYjAwMzFfTHpibURWMFFoZnlkWVAxYW1HQzRtbHc3NzUyYldFcWRfVG9rZW46TVcybWJhSWI3b21tcER4Q2hyR2MxcEZlbmdiXzE3NjkzOTU4NzU6MTc2OTM5OTQ3NV9WNA)

## 一：环境配置

### 1. 安装 Git 钩子

如果后续钩子启动失败，请查看 git 获取当前钩子安装路径进行问题排查

```Bash
# Windows 环境
向开发获取钩子，安装即可

# Linux/macOS 环境
# 进入项目目录
cd /path/to/originpointengine系统完整后端/backend

# 方式1: 设置 Git 钩子目录（推荐）
git config core.hooksPath .githooks

# 方式2: 复制钩子到 .git/hooks
cp .githooks/* .git/hooks/

# 给钩子脚本添加执行权限
chmod +x .githooks/*
# 或
chmod +x .git/hooks/*
```

### 2. 配置用户信息

```Bash
# 设置全局用户信息（推荐）
git config --global user.name "你的名字"
git config --global user.email "your.email@example.com"

# 设置项目用户信息（可选，会覆盖全局设置）
git config user.name "你的名字"
git config user.email "your.email@example.com"

# 查看配置
git config --list
```

---

## 二：日常开发流程

1. 开始新功能开发 or 修复bug `main → feat/xxx → main → release/x.x.x → 部署`

```Bash
# 1. 确保 main 分支是最新的
git checkout main
git pull origin main
# 2. 创建功能分支
git checkout -b feat/user-authentication
# 3. 开始开发...
# 编写代码，添加功能
# 4. 查看修改
git status
git diff
# 5. 提交代码
git add .
git commit -m "feat(auth): 添加用户登录功能"
# 6. 推送到远程
git push origin feat/user-authentication
```

2. 创建 Pull Request
    
    1. 在GitLab 上创建 Pull Request
        
    2. 填写 PR 标题和描述（使用模板）
        
    3. 选择审查者
        
    4. 关联相关 Issue
        
    5. 等待代码审查
        
3. 代码审查和合并
    

一般是主程审核，审核失败会拒绝合并

```Bash
# 审查通过后，由审查者或管理员合并到 main
# 本地同步最新代码
git checkout main
git pull origin main
# 删除已合并的本地分支
git branch -d feat/user-authentication
# 删除远程分支（通常在 PR 合并时自动删除）
git push origin --delete feat/user-authentication
```

4. 处理代码审查意见
    

```Bash
# 如果有审查意见需要修改
git checkout feature/user-authentication
# 修改代码...
git add .
git commit -m "fix(auth): 修复登录验证逻辑"
# 推送更新（PR 会自动更新）
git push origin feat/user-authentication
```

---

## 三：常用操作以及常见问题

### 🔧 常用操作

- 分支操作
    

```Bash
# 查看所有分支
git branch -a
# 创建并切换到新分支
git checkout -b feature/new-feature
# 切换分支
git checkout main
# 重命名分支
git branch -m old-name new-name
# 删除本地分支
git branch -d feature/old-feature
# 强制删除本地分支
git branch -D feature/old-feature
# 删除远程分支
git push origin --delete feature/old-feature
# 清理已删除的远程分支引用
git remote prune origin
```

- 提交操作
    

提交操作会通过钩子检查 message 格式，如有问题请咨询主程

```Bash
# 查看状态
git status
# 查看详细修改
git diff
# 查看暂存区修改
git diff --staged
# 添加文件到暂存区
git add .                    # 添加所有文件
git add specific-file.go     # 添加特定文件
git add *.go                 # 添加所有 .go 文件

# 提交代码
git commit -m "feat(module): 描述变更"

# 提交并添加详细说明
git commit -m "feat(module): 简短描述" -m "详细说明..."

# 修改最后一次提交
git commit --amend

# 修改最后一次提交消息
git commit --amend -m "新的提交消息"

# 查看提交历史
git log
git log --oneline
git log --graph --oneline --all
git log -p  # 显示每次提交的差异
git log --author="作者名"
git log --since="2 weeks ago"

# 查看某个文件的提交历史
git log -- path/to/file
```

- 同步操作
    

```Bash
# 拉取远程最新代码
git pull origin main
# 拉取并 rebase
git pull --rebase origin main
# 获取远程更新（不合并）
git fetch origin
# 推送代码
git push origin branch-name
# 推送新分支
git push -u origin branch-name
# 推送标签
git push origin v1.0.0
git push origin --tags  # 推送所有标签
```

- 撤销操作
    

```Bash
# 撤销工作区修改（未暂存）
git checkout -- file-name
git restore file-name  # Git 2.23+
# 撤销暂存区修改（已 add，未 commit）
git reset HEAD file-name
git restore --staged file-name  # Git 2.23+
# 撤销所有暂存
git reset
# 撤销最后一次提交（保留修改）
git reset --soft HEAD~1
# 撤销最后一次提交（不保留修改）
git reset --hard HEAD~1
# 撤销到指定提交
git reset --hard commit-hash
# 撤销某次提交（创建反向提交）
git revert commit-hash
# 清理未跟踪的文件
git clean -n  # 预览
git clean -f  # 删除文件
git clean -fd  # 删除文件和目录
```

- 暂存操作
    

```Bash
# 暂存当前修改
git stash
# 暂存并添加说明
git stash save "工作进行中：添加登录功能"
# 查看暂存列表
git stash list
# 恢复最近的暂存
git stash pop
# 恢复指定的暂存
git stash apply stash@{0}
# 删除暂存
git stash drop stash@{0}
# 清空所有暂存
git stash clear
```

---

### 💡 常见问题

#### 远端已经更新了最新的，我本地还在开发新 feat 怎么办？

- 提示未 Commit 问题
    

还没准备好 commit

使用 `stash` 临时保存，rebase后再恢复：

```Bash
# 1️⃣ 保存工作目录的修改
git stash
# 2️⃣ 执行rebase
git rebase main
# 如果有冲突，解决冲突后：
# git rebase --continue
# 3️⃣ rebase完成后恢复之前的更改
git stash pop
```

准备好了 commit 一下

- Rebase 和 merge
    
    |   |   |   |
    |---|---|---|
    |你是唯一在feat分支开发|Rebase ✅|保持历史干净|
    |多人在feat分支协作|Merge|不改写其他人的历史|
    |feat分支已经推送到远程，其他人在用|Merge|避免强制推送影响他人|
    |个人功能分支，最后会squash合并|Rebase|方便最终处理|
    
    - Rebase
        

提交历史干净、线性，易于查看git log；但是改写历史，如果feat是共享分支需要强制推送，可能影响他人

```Bash
# 1️⃣ 切换到main分支
git checkout main
# 2️⃣ 拉取远程最新的main代码
git pull origin main
# 3️⃣ 切换回feat分支
git checkout feat
# 4️⃣ 使用rebase将feat分支重建到最新的main之上
git rebase main
# 如果有冲突，解决冲突后继续
# git rebase --continue
# 5️⃣ 推送到远程（如果feat是共享分支，需要强制推送）
git push origin feat -f
```

- merge
    

  不改写历史，安全，多人协作友好；但会产生merge commit，历史不够线性

```Go
# 1️⃣ 切换到main分支
git checkout main
# 2️⃣ 拉取远程最新代码
git pull origin main
# 3️⃣ 切换回feat分支
git checkout feat
# 4️⃣ 将main分支合并到feat分支
git merge main
# 如果有冲突，解决冲突后commit
# 5️⃣ 推送到远程
git push origin feat
```

#### 不小心本地提交了不想要的文件怎么办

远端会有审核人，不需要过于担心

```Bash
# 从暂存区移除文件
git reset HEAD file-name
# 从提交中移除文件（保留工作区）
git reset --soft HEAD~1
git reset HEAD file-name
git commit -m "feat(module): 重新提交"
```

#### 不小心把本地分支删了怎么办？

```Bash
# 查看最近删除的分支
git reflog
# 恢复删除的分支
git checkout -b recovered-branch commit-hash
```

#### Windows 用户必看，防止提交乱码

默认采用 lf 为换行符，需进行操作

```Bash
# 自动转换行尾符（Windows）
git config --global core.autocrlf true
```

#### 不小心 pull 远端的时候拉错分支了

有时候你本地在 main，这时候拉取了远端的某个 feat 分支，这是不合规的，但是已经拉下来了，怎么回退呢？

请参考撤回操作

`git reflog // 查看过去的日志`

以这个为例，我们可以看到main分支合并了不希望的 feat/worldInfo，我们查看上一条获取哈希值**5f73389**

![](https://scn7nr4axh9v.feishu.cn/space/api/box/stream/download/asynccode/?code=ZjAxY2Y3YTdjYmFjZDY3ZmQ1NTYwYWE1N2M0NzhiM2JfVzh4dm1PMklpdlVYakpTc1pSVmU5RVlMRUZuNktMeXFfVG9rZW46VTk1U2JzVEFYb1c3YjR4RVpmVmNkak5ObkVlXzE3NjkzOTU4NzU6MTc2OTM5OTQ3NV9WNA)

`git reset --hard 5f73389` 即可回退成功

## 四：解决冲突

### 1. 合并冲突

```Bash
# 拉取最新代码时出现冲突
git pull origin main

# Auto-merging file.go
# CONFLICT (content): Merge conflict in file.go
# Automatic merge failed; fix conflicts and then commit the result.

# 查看冲突文件
git status

# 编辑冲突文件，解决冲突
# 文件中的冲突标记：
# <<<<<<< HEAD
# 你的代码
# =======
# 别人的代码
# >>>>>>> commit-hash

# 解决冲突后，标记为已解决
git add file.go

# 完成合并
git commit -m "resolve: 解决合并冲突"
```

### 2. Rebase 冲突

```Bash
# 开始 rebase
git rebase main

# 遇到冲突后
# 1. 编辑冲突文件
# 2. 标记为已解决
git add file.go

# 3. 继续 rebase
git rebase --continue

# 如果想跳过当前提交
git rebase --skip

# 如果想放弃 rebase
git rebase --abort
```

### 3. 查看冲突

```Bash
# 查看冲突文件
git diff

# 查看冲突的双方版本
git show :1:file.go  # 共同祖先版本
git show :2:file.go  # 当前分支版本
git show :3:file.go  # 合并分支版本

# 使用可视化工具解决冲突
git mergetool
```

---

## 五：版本发布以及打版本规则

### 版本发布

版本发布我们以主版本为依据

main (开发)

↓

release/1.x (当前生产版本)

↓

Git Tags: v1.0.0, v1.0.1, v1.1.0, v1.2.0...

何时创建新分支？

- 发布 1.0.0 时，创建 release/1.x
    
- 发布 2.0.0 时，创建 release/2.x
    
- 平时只有 2-3 个 release 分支同时存在
    

日常工作：

新功能 → main

准备发布 → release/1.x

打标签 → v1.x.x

Hotfix → 基于 tag 创建临时分支 → 合并回 release/1.x

  

注意生产分支合回主分支，主分支合到生产分支都是先看下log，然后有选择的`git cherry-pick <commit-hash>`

```Bash
# 1. 在 main 开发新功能
git checkout main
git merge feature/new-feature
git push origin main

# 2. 准备发布 v1.1.0
git checkout release/1.x
git merge main
git tag -a v1.1.0 -m "Release v1.1.0"
git push origin release/1.x --tags

# 3. CI/CD 自动检测到 release/1.x 更新，自动部署
```

```Bash
# 当前状态：
# 生产环境: v1.2.0
# main 分支已经到 v1.4.0 了（有很多新功能）

# 发现 v1.2.0 有严重 Bug，需要紧急修复

# 1. 基于 v1.2.0 创建 hotfix 分支
git checkout -b hotfix/critical-bug v1.2.0

# 2. 修复 Bug
# ... 修改代码 ...
git commit -m "fix: critical bug in payment"

# 3. 合并到 release/1.x 并打 tag
git checkout release/1.x
git merge hotfix/critical-bug 
git tag -a v1.2.1 -m "Hotfix v1.2.1: 修复支付 Bug"
git push origin release/1.x --tags

# 4. 同步修复到 main（避免 Bug 在新版本里复现）
git checkout main
git merge hotfix/critical-bug
git push origin main

# 5. 删除 hotfix 分支
git branch -d hotfix/critical-bug
git push origin --delete hotfix/critical-bug

# 6. CI/CD 检测到 v1.2.1 tag，自动部署
```

```Bash
# 当前生产: v1.3.0（有问题）
# 需要回滚到: v1.2.0

# 方式 A：直接重新部署旧版本（推荐）
git checkout release/1.x
git reset --hard v1.2.0
git push origin release/1.x --force

# 或者在服务器上直接拉取旧 tag
git fetch --tags
git checkout v1.2.0
docker-compose up -d --build
  
# 方式 B：创建回滚版本（保留历史）
git checkout release/1.x
git revert v1.3.0..HEAD  # 反向提交
git tag -a v1.3.1 -m "Rollback to v1.2.0"
git push origin release/1.x --tags
```

```Bash
# 1. 从 main 创建新的主版本分支
git checkout main
git checkout -b release/2.x
git tag -a v2.0.0 -m "Release v2.0.0: 重大更新"
git push origin release/2.x --tags
  
# 2. 配置 CI/CD 部署到生产
# （可以先灰度发布，再全量）
  
# 3. release/1.x 进入维护模式
# 只接受 hotfix，不再新增功能
```

Main 分支同步策略

```Bash
# 当 main 分支的功能开发完成，准备发布时

  # 方式 A：直接合并（推荐）
  git checkout release/1.x
  git merge main --no-ff -m "Merge main for v1.3.0 release"
  git tag -a v1.3.0 -m "Release v1.3.0"
  git push origin release/1.x --tags

  # 方式 B：Cherry-pick 特定提交（精细控制）
  git checkout release/1.x
  git cherry-pick abc123  # 只挑选某些提交
  git tag -a v1.3.0 -m "Release v1.3.0"
  git push origin release/1.x --tags

  方向：main → release/x.x（单向）
  - ✅ main 的新功能合并到 release 分支
  - ❌ 通常不从 release 反向合并到 main（但有例外，见下面）

  关键点：main 永远领先于 release 分支

  时间线：
  main:        v1.3.0 → v1.4.0 开发中 → v1.5.0 开发中
                  ↓
  release/1.x: v1.2.0 → v1.3.0（刚同步过来）

  # main 总是比 release 超前
```

```Bash
# 场景：生产环境 v1.2.0 有严重 Bug
  # 但 main 已经开发到 v1.4.0 了

  # 步骤 1：基于生产版本创建 hotfix
  git checkout -b hotfix/payment-bug v1.2.0

  # 步骤 2：修复 Bug
  # ... 修改代码 ...
  git commit -m "fix: critical payment bug"

  # 步骤 3：合并到 release/1.x（生产分支）
  git checkout release/1.x
  git merge hotfix/payment-bug
  git tag -a v1.2.1 -m "Hotfix v1.2.1"
  git push origin release/1.x --tags

  # 步骤 4：⚠️ 关键！同步到 main（避免 Bug 在新版本复现）
  git checkout main
  git merge hotfix/payment-bug
  # 或者用 cherry-pick（如果冲突太多,尽量采用精细控制）
  # git cherry-pick <hotfix-commit-hash>
  git push origin main

  # 步骤 5：删除 hotfix 分支
  git branch -d hotfix/payment-bug

  方向：hotfix → release/x.x + main（双向）
  - ✅ Hotfix 必须同时合并到生产分支和 main
  - ⚠️ 这是唯一一种"反向同步"的场景
```

|   |   |   |   |
|---|---|---|---|
|场景|操作|是否同步？|方向|
|开发新功能|feature → main|✅ 是|→|
|准备发布|main → release|✅ 是|→|
|发布完成|release → main|❌ 否|-|
|紧急修复|hotfix → release|✅ 是|→|
|紧急修复|hotfix → main|✅ 必须|→|
|生产回滚|release → main|❌ 否|-|

### 打版本规则

非常简单

第一位大版本重构位，第二位功能开发位，第三位功能修复位

重构开发大版本 V1.0.0 -> V2.0.0

从需求池提出需求 组成一个版本号 V1.1.0 -> V1.2.0 -> V1.3.0

线上已有功能修复版本：V1.1.0 -> V1.1.1 -> V1.1.2

---

## 六：🔥生产环境紧急修复

```Go
release/1.0.0 → hotfix/xxx → release/1.0.0 → 部署
                           ↘ main (同步修复)
```

```Bash
# 从 main 创建热修复分支
git checkout main
git checkout -b hotfix/critical-bug-fix

# 修复问题...
git add .
git commit -m "fix(critical): 修复紧急问题"

# 合并到 main
git checkout main
git merge hotfix/critical-bug-fix
git push origin main

# 同步到版本分支
git checkout 1.1.0
git merge hotfix/critical-bug-fix
git push origin 1.1.0

# 删除热修复分支
git branch -d hotfix/critical-bug-fix
```

---

## 团队协作最佳实践

### 1. 同步频率 ？

新功能群里会通知，请各位通知之后使用

```Bash
# 每天开始工作前
git checkout main
git pull origin main

# 定期同步个人分支
git checkout dev-yourname
git merge main
# 或使用 rebase 保持历史整洁
git rebase main
```

### 2. 保持分支整洁

```Bash
# 定期清理已合并的分支
git branch --merged main | grep -v "main" | xargs -n 1 git branch -d
# Windows PowerShell
git branch --merged main | Select-String -NotMatch "main" | %{git branch -d $_.Line.Trim()}
# 清理远程分支引用
git remote prune origin
# 查看可清理的远程分支
git remote prune origin --dry-run
```

### 3. 提交前检查

Git 钩子会对代码质量进行检查

#### 后端

`go fmt ./...` `go vet ./...` `go test ./...`

失败则会被阻止提交