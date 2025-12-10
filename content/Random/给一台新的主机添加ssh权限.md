---
date: 2025-12-09
tags: 
---
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
