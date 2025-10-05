---
tags:
  - '#pernamant'
---
在一个游戏网站学习的git命令
https://learngitbranching.js.org/?locale=zh_CN
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






<h1 align="center">Hi 👋, I'm Akiyama</h1>  
<h3 align="center">A passionate frontend developer from China</h3>  
  
- 🌱 I’m currently learning **Kotlin**  
  
- 💬 Ask me about **react**  
  
- 📫 How to reach me **lichengyu2005119@gmail.com**  
  
<h3 align="left">Connect with me:</h3>  
<p align="left">  
<a href="https://twitter.com/akiyama" target="blank"><img align="center" src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/twitter.svg" alt="akiyama" height="30" width="40" /></a>  
</p>  
  
<h3 align="left">Languages and Tools:</h3>  
<p align="left"> <a href="https://developer.android.com" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/android/android-original-wordmark.svg" alt="android" width="40" height="40"/> </a> <a href="https://www.gnu.org/software/bash/" target="_blank" rel="noreferrer"> <img src="https://www.vectorlogo.zone/logos/gnu_bash/gnu_bash-icon.svg" alt="bash" width="40" height="40"/> </a> <a href="https://www.w3schools.com/css/" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/css3/css3-original-wordmark.svg" alt="css3" width="40" height="40"/> </a> <a href="https://www.docker.com/" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/docker/docker-original-wordmark.svg" alt="docker" width="40" height="40"/> </a> <a href="https://www.electronjs.org" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/electron/electron-original.svg" alt="electron" width="40" height="40"/> </a> <a href="https://www.figma.com/" target="_blank" rel="noreferrer"> <img src="https://www.vectorlogo.zone/logos/figma/figma-icon.svg" alt="figma" width="40" height="40"/> </a> <a href="https://git-scm.com/" target="_blank" rel="noreferrer"> <img src="https://www.vectorlogo.zone/logos/git-scm/git-scm-icon.svg" alt="git" width="40" height="40"/> </a> <a href="https://www.w3.org/html/" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/html5/html5-original-wordmark.svg" alt="html5" width="40" height="40"/> </a> <a href="https://www.java.com" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/java/java-original.svg" alt="java" width="40" height="40"/> </a> <a href="https://developer.mozilla.org/en-US/docs/Web/JavaScript" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/javascript/javascript-original.svg" alt="javascript" width="40" height="40"/> </a> <a href="https://jestjs.io" target="_blank" rel="noreferrer"> <img src="https://www.vectorlogo.zone/logos/jestjsio/jestjsio-icon.svg" alt="jest" width="40" height="40"/> </a> <a href="https://kotlinlang.org" target="_blank" rel="noreferrer"> <img src="https://www.vectorlogo.zone/logos/kotlinlang/kotlinlang-icon.svg" alt="kotlin" width="40" height="40"/> </a> <a href="https://www.linux.org/" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/linux/linux-original.svg" alt="linux" width="40" height="40"/> </a> <a href="https://www.mysql.com/" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/mysql/mysql-original-wordmark.svg" alt="mysql" width="40" height="40"/> </a> <a href="https://nestjs.com/" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/nestjs/nestjs-plain.svg" alt="nestjs" width="40" height="40"/> </a> <a href="https://nodejs.org" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/nodejs/nodejs-original-wordmark.svg" alt="nodejs" width="40" height="40"/> </a> <a href="https://www.postgresql.org" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/postgresql/postgresql-original-wordmark.svg" alt="postgresql" width="40" height="40"/> </a> <a href="https://www.python.org" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="python" width="40" height="40"/> </a> <a href="https://reactjs.org/" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/react/react-original-wordmark.svg" alt="react" width="40" height="40"/> </a> <a href="https://spring.io/" target="_blank" rel="noreferrer"> <img src="https://www.vectorlogo.zone/logos/springio/springio-icon.svg" alt="spring" width="40" height="40"/> </a> <a href="https://www.sqlite.org/" target="_blank" rel="noreferrer"> <img src="https://www.vectorlogo.zone/logos/sqlite/sqlite-icon.svg" alt="sqlite" width="40" height="40"/> </a> <a href="https://tailwindcss.com/" target="_blank" rel="noreferrer"> <img src="https://www.vectorlogo.zone/logos/tailwindcss/tailwindcss-icon.svg" alt="tailwind" width="40" height="40"/> </a> <a href="https://www.typescriptlang.org/" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/typescript/typescript-original.svg" alt="typescript" width="40" height="40"/> </a> </p>
# reference
https://learngitbranching.js.org/?locale=zh_CN