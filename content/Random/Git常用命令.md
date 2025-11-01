---
tags:
  - '#pernamant'
---
在一个游戏网站学习的git命令
https://learngitbranching.js.org/?locale=zh_CN

## 给一台新的主机添加ssh权限

首先在自己电脑上生成公钥私钥

```sh
ssh-keygen -t ed25519 -C "lichengyu2005119@gmail.com"
```

查看公钥：

```sh
cat /root/.ssh/id_ed25519.pub
```

登录github，点击ssh安全的一栏，添加ssh密钥，cat输出的就是公钥

给git配置用户

```sh
git config --global user.name "Akiyama-sama"
git config --global user.email "lichengyu2005119@gmail.com"
```

测试看看是否成功

```sh
ssh -T git@github.com
```


## 本地仓库

`git commit` 提交当前记录
`git branch name` 在当前节点创建分支
`git checkout name` 转到name分支
`git merge branchName`将指定分支合并到当前分支
`git rebase main` 将当前分支的记录合并到main分支，作为main分支的儿子
`git checkout hash`可以将HEAD指向具体的某一个提交记录

HEAD是用于方便用户移动提交记录的一个指针而已，没有其他具体的含义

**分支**
`git checkout -b 分支名`创建一个分支并且指向这个分支
`git branch 分支名` 仅仅创建一个分支
`git branch` 列举本地所有分支
`git branch -d 分支名` 删除指定分支

`git merge 分支名` 切换到主分支后，然后在用指定分支名合并到当前分支



**相对引用：**
`git checkout HEAD^`指向HEAD指向的父提交记录，这样就不需要checkout 哈希值了，便于书写
`git checkout HEAD~3` 向前走三步

加上`-f [branchName]`后就有让此分支指向另一个提交
例如`git branch -f main HEAD~3`
上面的命令会将 main 分支强制指向 HEAD 的第 3 级 parent 提交。

**撤销变更**
`git reset HEAD^`是将当前分支撤回一步，像是没有提交过一样
`git reset --mixed HEAD~1` 撤回上一次提交，将上次提交保留在工作区，适用于少提交了一些文件，想重新提交的情况。
`git revert HEAD`是与多人协同工作时的用法，他是新提交一个记录，此记录是用来撤销当前提交的，即revert 之后就可以把你的更改推送到远程仓库与别人分享啦


## 远程仓库
`git clone`将远程仓库的代码克隆到本地，并且多了一个名为 `o/main` 的远程分支（- `<remote name>/<branch name>`）
远程分支有一个特别的属性，在你切换到远程分支时，自动进入分离 HEAD 状态
`git checkout o/main` 就会切换到远程仓库
`git branch -r`查看远程所有分支
`git checkout -b 本地分支名字 origin/远程分支名`在本地创建一个分支，与那个远程分支关联

`git fetch`  - 从远程仓库下载本地仓库中缺失的提交记录
			- 更新远程分支指针(如 `o/main`)

`git fetch` 并不会改变你本地仓库的状态。它不会更新你的 `main` 分支，也不会修改你磁盘上的文件。所以把他理解为单纯的下载操作

`git pull`=`git fetch`+`git merge` 即从远程仓库下载数据到本地的远程分支o/main，然后本地仓库的main分支再合并o/main分支

`git pull --rebase`=`git fetch`+`git rebase`即从远程仓库下载数据到本地的远程分支o/main，然后合并main和o/main到o/mian 的儿子

`git push -u orign main`.` -u`参数用于关联本地与远程分支，后续推送只需`git push`



# reference
https://learngitbranching.js.org/?locale=zh_CN