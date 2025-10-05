---
tags:
  - '#pernamant'
---
```yml
name: Deploy flashNotes-ai to aliyun Ubuntu Server

on:
  push:
    branches:
      - main  # 监听 main 分支的 push 事件

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - name: 🔄 检出代码
        uses: actions/checkout@v3

      - name: ⚙️ 设置 Node.js 环境
        uses: actions/setup-node@v3
        with:
          node-version: 23.9.0 

      - name: 📦 安装依赖
        run: npm install

      - name: 🔧 运行构建（本地测试）
        run: npm run build

      - name: 🚀 部署到远程服务器
        uses: appleboy/ssh-action@v0.1.4
        with:
          host: ${{ secrets.SERVER_HOST }}
          username: ${{ secrets.SERVER_USER }}
          key: ${{ secrets.SERVER_SSH_KEY }}
          script: |
            cd /var/www/flashNotes-ai  # 请替换为你的前端项目路径
            git pull origin main
            npm install
            npm run build

```

### **流程拆解**

|步骤|运行在哪？|作用|
|---|---|---|
|`checkout`|GitHub Actions|拉取代码|
|`setup-node`|GitHub Actions|确保 Node.js 版本正确|
|`npm install`|GitHub Actions|安装依赖（在 GitHub 服务器上）|
|`npm run build`|GitHub Actions|本地测试构建|
|`ssh-action`|远程 Ubuntu 服务器|连接服务器并执行命令|
|`git pull origin main`|远程 Ubuntu 服务器|拉取最新代码|
|`npm install`|远程 Ubuntu 服务器|安装依赖|
|`npm run build`|远程 Ubuntu 服务器|重新构建前端项目|



# reference
