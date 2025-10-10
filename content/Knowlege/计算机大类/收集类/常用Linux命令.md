---
tags:
  - '#literature'
---

## 关于文件

创建文件夹：
```
mkdir 创建文件夹
```

make directory

创建文件
```
touch 文件名
```


如果用vim编辑器：
```
vim 文件名
```
会创建这个文件并且打开这个文件进行编辑

给一个文件设置权限
```
chmod u=rw,g=rw,o=r hello.c
```
chmod 全称为change mode，u即此用户，g即此用户所属组 o即other

创建这个文件的[[硬链接]]
```
ln [目标文件] [硬链接名]
```
创建这个文件的[[软链接]]
```
ln -s [目标文件或目录] [软链接名]
```
ln全称是link，-s的全称是symbolic符号的

搜索文件内容
```
grep [options] [文件名] [搜索起始目录]
```
grep(global regular expression) 

搜索文件名
```
find [路径] [匹配条件] [动作]
```

重命名文件
```
mv [旧文件名] [新文件名]
```

查看文件的所属数据内容
```
ls -l
```


## 关于目录

- ls（英文全拼：list files）: 列出目录及文件名
- cd（英文全拼：change directory）：切换目录
- pwd（英文全拼：print work directory）：显示目前的目录
- mkdir（英文全拼：make directory）：创建一个新的目录
	- -p是parent的缩写，如果创建的文件夹的父目录不存在，会帮你自动创建
	- -m是mode 顾名思义就是创建的时候设置权限
- rmdir（英文全拼：remove directory）：删除一个空的目录
- cp（英文全拼：copy file）: 复制文件或目录
- rm（英文全拼：remove）: 删除文件或目录
- mv（英文全拼：move file）: 移动文件与目录，或修改文件与目录的名称

## 关于用户
switch user切换用户
```
su - 用户名
```
-的意思是模拟完整的登录过程

添加用户组
```
groupadd 组名
```

添加用户
```
useradd -g 组名 -m 用户名
```
-g用来指定创建用户的组，-m是创建这个用户时自动创建这个用户所属的主目录


给此用户设置密码
```
passwd 密码
```



