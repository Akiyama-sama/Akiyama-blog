---
tags:
  - "#project"
draft: "true"
---
## 项目地址
[前端地址](http://47.109.99.107:80) 
[github地址](https://github.com/Akiyama-sama/flashNotes-ai)
[宝塔面板地址](http://47.109.99.107:8888/home)
面口令登录服务器：
```ssh
ssh -i ~/.ssh/github_actions_key root@47.109.99.107
```
宝塔面板用户名：rljiloxw
```
Cheng15023182754*
```
## 需求来源
当我自己在记闪念笔记的时候，都是在obsidian上记录，我在想能否在网页上，或者手机上有款工具可以很方便的记录我的闪念，并且AI可以帮我调研这个点子的可行性，可以帮我调查世界上是否已经有人实现这个点子或者有类似的点子，或者帮我联想这个点子，或者我想实现这个点子，让AI给我列出具体的计划/清单去实现

## 核心功能
* 记闪念笔记
* 让AI分析这个闪念笔记的可行性
[[闪念笔记+AI 的最佳实践（o1总结）]]

## 页面的具体描述

落地页
![Drawing 2025-02-20 13.20.04.excalidraw](https://obsidian-picgo-mio.oss-cn-hangzhou.aliyuncs.com/Drawing%202025-02-20%2013.20.04.excalidraw.png)


## 实践中的困难

### 到底什么叫做闪念笔记？
最初我给他的定义是我自己脑海中可以商业化、可以赚钱的点子，想法，又或者是一个故事，又或者是从哪里得到的一句金句，想记录下来的短想法等等，后面这些是我后面与人交流的来的定义，估计后面还有其他的定义，这个产品的作用是对用户想法的“扩展”

无论你的想法是什么类型
* 商业化想法
* 金句
* 故事
.....后面在补充

主要是对用户想法的扩展和延伸，让用户打开思维等等

### React-router
```js
import {BrowserRouter} from 'react-router-dom'
createRoot(document.getElementById('root')).render(
  <StrictMode>
   <BrowserRouter>//用BrowerRouter包裹APP
   <App />
  </BrowserRouter>
  </StrictMode>

)
```
并在App.jsx里面定义路由
```js
import { Route, Routes } from 'react-router-dom'
import Home from './pages/Home'  
import NoteDetail from './pages/NoteDetail'
function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/note/:id" element={<NoteDetail/>} />
    </Routes>
  )
}
export default App
```
当点击卡片的时候，调用navigate方法，更新路由
NoteCard.jsx
```js
import '../styles/NoteCard.css'
import { useNavigate } from 'react-router-dom';
function NoteCard({note: { id, createTime, text }}) {
    const navigate = useNavigate();
    const displayText = text?.length > 20 ? text.slice(0,20) : text;
    return (
        <div className="card" onClick={() => navigate(`/note/${id}`)}>
            <div>
                {displayText}
            </div>
            <div>
                {createTime}
            </div>
        </div>
    )
}
export default NoteCard
```

- Router 检测到 URL 变化
- 匹配新的 URL 与已定义的路由模式
- 发现匹配 /note/:id 模式
- 卸载当前组件（Home）
- 挂载目标组件（NoteDetail）
### React-markdown
安装依赖 markdown+高亮
```
npm install react-markdown react-syntax-highlighter
```
对于mvp模型来说，我认为既然是都叫做闪念笔记，我只需要记下来文本就可以了，暂时不需要markdown的格式，mardown的样式弄起来也是头疼。

### 数据存储第一版：localstorage

### 调用AI-API
没有写过，本来想着直接调用，不要太过复杂，毕竟是MVP，想着尽快交付可以使用的版本原型。但实在没写过，看看一些教程，甚至花20买了[[kai  Qwerty Learner]]的一个[小册](https://juejin.cn/book/7347579913702293567/section/7360946625923317798?utm_source=post_pay_page)

但现在看来是冲动了，我学习这个也挺花时间的，感觉后面才有用，后面再看吧。得先快速把原型建好了来

### 状态管理方案

[[状态管理方案]]
### 部署
第一次部署，还不清楚如何部署前端项目和后端项目到服务器上

跨域问题，当用开发者模式的时候前端向后端请求服务的时候正确，这是开发者模式，但用了生产模式的时候，似乎会出现跨域问题？这是什么问题，不太了解，只是用AI让我给Springboot写了一个配置类，然后就可以了

还有一个是

#### 将本地文件dist安装到服务器上
当运行到命令 git push origin main时遇到了问题，需要[[公钥与私钥（SSH）]]才能让用户操作远程仓库

其中，重要的是
- **私钥**：`~/.ssh/id_ed25519`  
  **切勿分享**！文件权限需设为`600`（仅用户可读写）。
- **公钥**：`~/.ssh/id_ed25519.pub`  
  内容以`ssh-ed25519`开头，需复制到GitHub的SSH设置页面。
[[Git命令]]

#### Nginx配置
```nginx
server { 
	listen 80; 
	server_name 47.109.99.107; # 换成你的域名或服务器IP 
	root /project/front-end/flashNotes-ai/flashNotes-ai/; 
	index index.html index.htm; # 默认的首页文件名 
	location / { 
		try_files $uri $uri/ /index.html; 
	} 
}
```

修改宝塔面板的密码
```
 cd /www/server/panel && btpython tools.py panel Cheng150231827554*
```

服务器项目更新、前端存放目录
`/var/www/flashNotes-ai`

#### 用Systemd服务管理Springboot项目
更新后端jar包指令
jar包目录：
`F:\project\flashNote-ai-back\target`
本地更新后打包指令
`mvn clean package -DskipTests`
本地jar包更新到指定目录指令
`scp flashNote-ai-back-0.0.1-SNAPSHOT.jar root@47.109.99.107:/var/www/flashNotes-ai-back`
Systemd服务管理配置
```ini
[Unit]
Description=FlashNotes AI Backend Service
After=network.target
[Service]
User=root
ExecStart=/var/www/flashNotes-ai-back/flashNote-ai-back-0.0.1-SNAPSHOT.jar
SuccessExitStatus=143
Restart=always
RestartSec=10
StandardOutput=append:/var/log/flashnotes-ai.log
StandardError=append:/var/log/flashnotes-ai-error.log
[Install]
WantedBy=multi-user.target
```

#### 一直请求不到后端服务
一直报错说是我的前端一直在请求localhost，但是我已经在本地改了两遍，并进行build然后上传github，然后再服务器上pull，但还是不行，我再根目录下执行：grep -rn "localhost:8000" dist/
这个指令，就是看看这个build好的dist文件夹里面还有没有这个localhost，还真有，想不明白，然后我在服务器上进行build，再查，没了。神奇，然后服务就可以运行了。

### 前后端更新代码

**本地连接服务器**

```ssh
ssh root@47.109.99.107
```

前端
`git push` 更新到github上，再到这个目录下`/var/www/flashNotes-ai` 运行 `git pull` 还有
`npm run build`

后端
jar包目录：
`F:\project\flashNote-ai-back\target`
本地更新后打包指令
`mvn clean package -DskipTests`
本地jar包更新到指定目录指令
`scp flashNote-ai-back-0.0.1-SNAPSHOT.jar root@47.109.99.107:/var/www/flashNotes-ai-back`
启用新的进程
```
sudo systemctl start flashnotes-ai
sudo systemctl status flashnotes-ai  # 检查是否启动成功
```
如果你用的是 **Systemd**，确保它会自动启动：
`sudo systemctl enable flashnotes-ai`

看到AI提示说用`CI/CD`（比如 **GitHub Actions** 或 **GitLab CI**），可以自动化这个流程让每次 `git push` 自动触发 **打包、上传、重启服务器**，这样就不用手动操作了。后面再试试看。

[[GitHub Actions 快速入门 - GitHub 文档]]
[[flashNotes-ai GitHub Actions工作流]]
### READ ME文档
还得写一个文档，记录下这个项目的启动步骤，但还得写作这个项目的具体感受，得把一些深入的思考过程写进去，现在我还想不到怎么弄，后面再写吧
[[flashNotes-ai README文档]]

### 宣传

[[flashNotes-ai宣传文档]]

### 更新
出了一个样式bug，因为我之前对于AI的无脑使用，导致我现在对这个项目的细节把握不了，样式也没有学习到，

