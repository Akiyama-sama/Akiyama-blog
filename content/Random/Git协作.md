---
date: 2025-12-09
tags: 
---
在公司里面要与其他人协作的话，先开一个分支进行开发

```bash
git checkout -b feat/分支名
```

开发完毕，add，commit过后，先进行拉取远程最新分支

```bash
git pull
```

如果没有最新提交，就可以先在本地切换到本地main，再进行合并

```bash
git switch main
git merge feat/分支名

#有冲突解决冲突过后再进行合并
```

如果有最新提交，就先
```bash
git fetch
git rebase origin/main
```

查看冲突的文件有哪些，解决冲突并进行提交，确认无冲突过后，再提交这个新开发的分支

```bash
git push origin 本地分支名
```

然后在GitLab上为这个分支创建一个PR，写好信息再进行远程rebase






