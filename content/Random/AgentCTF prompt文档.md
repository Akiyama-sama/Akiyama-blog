---
tags:
  - '#pernamant'
---
# 产品与设计文档

## 核心目标与用户价值

**产品核心目标**：创建一个AI Agent 驱动的攻防场景平台，让用户可以输入不同的靶机环境场景，让用户可以通过Agent来对靶机进行攻击与防御，让用户可以在这个过程当中学习Agent是如何发现靶机漏洞，运用攻击，编写脚本来实施攻击，Agent是如何防御这些攻击，修补漏洞的。

**目标用户：** 比赛参与者、安全研究员、比赛组织者。

**用例描述：** 用户通过平台创建并部署一个 AI Agent 驱动的攻防场景，然后利用 AI Agent 对靶机进行攻击和防御，并监控整个过程和结果。

## 场景列表页面用例
**场景状态 (Status)**: 场景的生命周期由状态机管理，主要包含以下状态：
    * `pending`: 场景已创建，等待编排 
    * `building`: 场景编排构建中 
    * `starting`: 场景各容器启动中 
    * `running`: 场景内所有服务成功启动并运行中 
    * `stopped`: 场景被关闭或成功构建后等待启动 
    * `error`: 场景在构建或启动过程中发生错误 
    * `removing`: 场景正在被删除 

具体用例如下：

**进入场景（Create Scenario）**

- **前置条件：** 用户已登录系统。
- **操作步骤：**
    * 用户点击导航栏，进入“AI Agent 攻防场景模式”。
- **预期结果：**
    - 如果至少有一个场景：Agent攻防场景模式页面渲染出各个已经创建好的场景
    - 如果没有场景：提示没有场景被创建，引导用户创建场景


**场景创建（Create Scenario）**

- **前置条件：** 用户已登录系统，并进入“AI Agent 攻防场景模式”页面。
- **操作步骤：**
    1. 用户点击页面顶部或左侧的“添加场景”按钮。
    2. 系统弹出“创建场景”表单页面。
    3. 用户在表单中填写：
        - **场景名称：** （文本输入框，例如：“WebLogic CVE-2017-10271 渗透测试”）
        - **场景说明：** （Markdown 编辑器，用于详细描述场景背景、漏洞类型、技术细节、网络拓扑等信息）
    4. 用户上传以下三类压缩包文件：
        - **攻击容器包：** （`hacker.zip` 或 `hacker.tar.gz`，包含 Dockerfile、脚本和工具）
        - **防御容器包：** （`defender.zip` 或 `defender.tar.gz`，包含 Dockerfile、脚本和工具）
        - **靶机环境包：** （`target.zip` 或 `target.tar.gz`，包含 `docker-compose.yml` 及相关构建上下文）
    5. 用户点击“创建场景”按钮。
- **预期结果：**
    - 系统提示“场景创建成功（pending），正在构建中（building）”。
    - 页面自动跳转到AI Agent 攻防场景模式主页，主页显示用户创建的场景卡片。
    - 场景卡片状态栏显示为“构建中（building）”。
	    - 如果创建成功，场景状态栏显示构建成功（stopped）
	    - 如果构建失败，状态变为“错误（error）”，弹出创建失败提示框，引导用户可以点击“详细信息"来进行修改场景配置，重新构建。

**场景删除**

- **前置条件：** 用户已登录系统，进入“AI Agent 攻防场景模式”页面，且页面至少有一个场景创建。
- **操作步骤：**
    1. 用户点击要删除的场景的”删除”按钮。
    2. 系统弹出“是否删除场景”的提示表单页面。
    3. 用户点击确认/取消
- **预期结果：**
	* 如果用户点击确认，该场景被删除，主页面的该场景卡片消失
	* 如果用户点击取消，该场景不会被删除，主页面的该场景卡片不消失

**场景启动（Start Scenario）**

- **前置条件：** 用户已登录系统，在“AI Agent 攻防场景模式”页面，场景已成功构建完成，状态为“已停止/已构建（stopped）且未启动。
- **操作步骤：**
    1. 在“AI Agent 攻防场景模式”列表页，用户找到目标场景卡片。
    2. 用户点击场景卡片上的“启动”按钮。
- **预期结果：**
    - 系统提示“场景启动中”。
    - 场景状态更新为“启动中（starting）” 。
    - 如果启动成功，场景状态更新为“运行中（running）” 。
    - 如果启动失败，场景状态更新为“错误（error），引导用户修改场景所需附件和配置” 。

**场景配置修改** 

- **前置条件：** 用户已登录系统，在“AI Agent 攻防场景模式”列表页， 场景已成功构建完成，状态为“已停止/已构建（stopped）。
- **操作步骤：**
    1. 如果场景状态为”stopped“ ，用户点击”详细信息“，可弹出场景修改表单。
    2. 用户修改场景配置，点击确认，提交修改信息
- **预期结果：**
    - 如果用户修改的是附件信息（包含得有例如Dockerfile的附件）：回到场景模式主页面，场景状态提示重新构建中（building）
    - 如果用户修改的是场景配置信息（场景名字、场景介绍）：回到场景模式主页面，场景状态提示（stopped），并修改好场景的文字配置信息。

**场景错误重构** 

- **前置条件：** 用户已登录系统，在“AI Agent 攻防场景模式”列表页， 目标场景状态为错误（error）。
- **操作步骤：**
    * 用户点击该错误场景的“详细信息”按钮，修改好该场景配置，点击确定
- **预期结果：**
    - 系统提示正在重新构建中（building）”。
    - 页面自动跳转到AI Agent 攻防场景模式主页，主页显示用户正在重新构建的场景卡片。
    - 场景卡片状态栏显示为“构建中（building）”。
    	- 如果创建成功，场景状态栏显示构建成功（stopped）
    	- 如果构建失败，状态变为“错误（error）”，弹出创建失败提示框，引导用户可以点击“详细信息"来进行修改场景配置，重新构建。




## 进入场景详情页面用例


**利用 ChatBot 进行攻防操作（Attack & Defense with AI Agent）**

- **前置条件：** 场景状态为“运行中（running）”。
- **操作步骤：**
    1. 用户进入该“运行中”场景的“场景详情页”。
    2. 页面上显示一个 ChatBot 交互界面（或连接到 AI Client 的入口）。
    3. **攻击阶段：** 用户切换到attacker的上下文对话窗口，通过 ChatBot 输入指令，指示 AI Agent 驱动 Attack Agent 对靶机进行攻击。例如，用户可以输入：“请利用 CVE-2017-10271 漏洞对靶机进行渗透测试。”
    4. **防御阶段：** 用户切换到defender的上下文对话窗口，通过 ChatBot 输入指令，指示 AI Agent 驱动 Defender Agent 对靶机进行防御。例如，用户可以输入：“请部署防御策略，阻止攻击。”
- **预期结果：**
    - attacker ChatBot 实时显示 LLM 通过攻击容器的MCP服务器，调用了哪些知识库，发现靶机的哪些问题，写了哪些脚本，调用了哪些工具，如何攻击靶机等等。
    - defender ChatBot 实时显示 LLM 通过防御容器的MCP服务器，访问靶场，发现了哪些漏洞，调用哪些知识库，如何修补这些漏洞等等。
    - 攻防容器的日志区域会实时滚动显示攻击和防御过程中容器内部的日志输出。
    - 靶机容器的服务端口在攻击或防御过程中可能会有状态变化或异常，可以查看靶机容器的日志输出
    - 整个攻防过程会在后续的“战斗日志”中记录。

**查看“战斗日志”

- **前置条件：** 场景已运行，并进行了攻防操作。
- **操作步骤：**
    1. 在“场景详情页”中，用户找到“查看日志”区域。
    2. 用户可以点击“战斗日志”，查看整场攻防推演的高层次日志，这通常是攻防 AI Agent 决策和重要事件的记录。
    3. 用户可以点击“攻击容器日志”，查看攻击容器内部的详细日志。
    4. 用户可以点击“防御容器日志”，查看防御容器内部的详细日志。
    5. 用户可以点击“靶机容器日志”，查看靶机容器内部的详细日志。
- **预期结果：**
    - 各日志区域显示相应的日志信息，支持实时滚动、暂停、清空、复制等操作。
    - 日志可能会有颜色区分或高亮显示，以便用户快速识别关键信息或错误。

**查看容器资源使用情况（View Container Resources）**

- **前置条件：** 场景正在运行中。
- **操作步骤：**
    1. 在“场景详情页”中，用户找到“资源监控”区域。
    2. 用户查看该区域展示的图表或数据。
- **预期结果：**
    - 页面实时或定时更新显示攻击容器、防御容器和靶机 DinD 容器的 CPU 使用率、内存占用、网络 I/O 等资源使用情况。

**进入各个容器（可选用户调试用例）**

- **前置条件：** 场景正在运行中。
- **操作步骤：**
    1. 在“场景详情页”中，用户找到“端口信息”区域，获取攻击容器、防御容器、靶机DinD容器的 SSH 映射端口 。
    2. 用户点击“快速连接指引”提供的 SSH 连接命令模板 。
    3. 用户可以点击攻击容器/防御容器/靶机容器下方的“进入终端”按钮，启动一个新开窗口的网页版终端
- **预期结果：**
    - 如果用户通过 SSH 命令行连接，用户可以通过本地终端成功连接到容器的 SSH 服务。
    - 如果通过网页版终端，新开窗口的终端窗口成功启动，用户可以在新开的浏览器窗口中直接与容器的 Linux 环境进行命令行交互。








# 视觉设计规范
## 配送方案
参考如下自定义css样式：
```css
:root {
  --background: #f5f5f5;
  --foreground: #000000;
  --card: #ffffff;
  --card-foreground: #000000;
  --popover: #ffffff;
  --popover-foreground: #000000;
  --primary: #16a34a;
  --primary-foreground: #ffffff;
  --secondary: #607d8b;
  --secondary-foreground: #ffffff;
  --muted: #e0e0e0;
  --muted-foreground: #757575;
  --accent: #22c55e;
  --accent-foreground: #ffffff;
  --destructive: #ef5350;
  --destructive-foreground: #ffffff;
  --border: #e0e0e0;
  --input: #eeeeee;
  --ring: #22c55e;
  --chart-1: #26a69a;
  --chart-2: #4db6ac;
  --chart-3: #80cbc4;
  --chart-4: #b2dfdb;
  --chart-5: #e0f2f1;
  --sidebar: #f5f5f5;
  --sidebar-foreground: #000000;
  --sidebar-primary: #16a34a;
  --sidebar-primary-foreground: #ffffff;
  --sidebar-accent: #22c55e;
  --sidebar-accent-foreground: #ffffff;
  --sidebar-border: #e0e0e0;
  --sidebar-ring: #22c55e;
  --font-sans: Inter, sans-serif;
  --font-serif: Lora, serif;
  --font-mono: Menlo, monospace;
  --radius: 0.5rem;
  --shadow-2xs: 0.1rem 0.1rem 0.5rem 0.1rem hsl(0 0% 0% / 0.05);
  --shadow-xs: 0.1rem 0.1rem 0.5rem 0.1rem hsl(0 0% 0% / 0.05);
  --shadow-sm: 0.1rem 0.1rem 0.5rem 0.1rem hsl(0 0% 0% / 0.10), 0.1rem 1px 2px -0.9px hsl(0 0% 0% / 0.10);
  --shadow: 0.1rem 0.1rem 0.5rem 0.1rem hsl(0 0% 0% / 0.10), 0.1rem 1px 2px -0.9px hsl(0 0% 0% / 0.10);
  --shadow-md: 0.1rem 0.1rem 0.5rem 0.1rem hsl(0 0% 0% / 0.10), 0.1rem 2px 4px -0.9px hsl(0 0% 0% / 0.10);
  --shadow-lg: 0.1rem 0.1rem 0.5rem 0.1rem hsl(0 0% 0% / 0.10), 0.1rem 4px 6px -0.9px hsl(0 0% 0% / 0.10);
  --shadow-xl: 0.1rem 0.1rem 0.5rem 0.1rem hsl(0 0% 0% / 0.10), 0.1rem 8px 10px -0.9px hsl(0 0% 0% / 0.10);
  --shadow-2xl: 0.1rem 0.1rem 0.5rem 0.1rem hsl(0 0% 0% / 0.25);
  --tracking-normal: -0.025em;
  --spacing: 0.25rem;
}

.dark {
  --background: #121212;
  --foreground: #ffffff;
  --card: #1e1e1e;
  --card-foreground: #ffffff;
  --popover: #1e1e1e;
  --popover-foreground: #ffffff;
  --primary: #a7f3d0;
  --primary-foreground: #000000;
  --secondary: #3d5a80;
  --secondary-foreground: #ffffff;
  --muted: #2e2e2e;
  --muted-foreground: #a3a3a3;
  --accent: #98ff98;
  --accent-foreground: #000000;
  --destructive: #ef5350;
  --destructive-foreground: #ffffff;
  --border: #333333;
  --input: #333333;
  --ring: #98ff98;
  --chart-1: #26a69a;
  --chart-2: #4db6ac;
  --chart-3: #80cbc4;
  --chart-4: #b2dfdb;
  --chart-5: #e0f2f1;
  --sidebar: #121212;
  --sidebar-foreground: #ffffff;
  --sidebar-primary: #a7f3d0;
  --sidebar-primary-foreground: #000000;
  --sidebar-accent: #98ff98;
  --sidebar-accent-foreground: #000000;
  --sidebar-border: #333333;
  --sidebar-ring: #98ff98;
  --font-sans: Inter, sans-serif;
  --font-serif: Lora, serif;
  --font-mono: Menlo, monospace;
  --radius: 0.5rem;
  --shadow-2xs: 0.1rem 0.1rem 0.5rem 0.1rem hsl(0 0% 0% / 0.15);
  --shadow-xs: 0.1rem 0.1rem 0.5rem 0.1rem hsl(0 0% 0% / 0.15);
  --shadow-sm: 0.1rem 0.1rem 0.5rem 0.1rem hsl(0 0% 0% / 0.30), 0.1rem 1px 2px -0.9px hsl(0 0% 0% / 0.30);
  --shadow: 0.1rem 0.1rem 0.5rem 0.1rem hsl(0 0% 0% / 0.30), 0.1rem 1px 2px -0.9px hsl(0 0% 0% / 0.30);
  --shadow-md: 0.1rem 0.1rem 0.5rem 0.1rem hsl(0 0% 0% / 0.30), 0.1rem 2px 4px -0.9px hsl(0 0% 0% / 0.30);
  --shadow-lg: 0.1rem 0.1rem 0.5rem 0.1rem hsl(0 0% 0% / 0.30), 0.1rem 4px 6px -0.9px hsl(0 0% 0% / 0.30);
  --shadow-xl: 0.1rem 0.1rem 0.5rem 0.1rem hsl(0 0% 0% / 0.30), 0.1rem 8px 10px -0.9px hsl(0 0% 0% / 0.30);
  --shadow-2xl: 0.1rem 0.1rem 0.5rem 0.1rem hsl(0 0% 0% / 0.75);
}

@theme inline {
  --color-background: var(--background);
  --color-foreground: var(--foreground);
  --color-card: var(--card);
  --color-card-foreground: var(--card-foreground);
  --color-popover: var(--popover);
  --color-popover-foreground: var(--popover-foreground);
  --color-primary: var(--primary);
  --color-primary-foreground: var(--primary-foreground);
  --color-secondary: var(--secondary);
  --color-secondary-foreground: var(--secondary-foreground);
  --color-muted: var(--muted);
  --color-muted-foreground: var(--muted-foreground);
  --color-accent: var(--accent);
  --color-accent-foreground: var(--accent-foreground);
  --color-destructive: var(--destructive);
  --color-destructive-foreground: var(--destructive-foreground);
  --color-border: var(--border);
  --color-input: var(--input);
  --color-ring: var(--ring);
  --color-chart-1: var(--chart-1);
  --color-chart-2: var(--chart-2);
  --color-chart-3: var(--chart-3);
  --color-chart-4: var(--chart-4);
  --color-chart-5: var(--chart-5);
  --color-sidebar: var(--sidebar);
  --color-sidebar-foreground: var(--sidebar-foreground);
  --color-sidebar-primary: var(--sidebar-primary);
  --color-sidebar-primary-foreground: var(--sidebar-primary-foreground);
  --color-sidebar-accent: var(--sidebar-accent);
  --color-sidebar-accent-foreground: var(--sidebar-accent-foreground);
  --color-sidebar-border: var(--sidebar-border);
  --color-sidebar-ring: var(--sidebar-ring);

  --font-sans: var(--font-sans);
  --font-mono: var(--font-mono);
  --font-serif: var(--font-serif);

  --radius-sm: calc(var(--radius) - 4px);
  --radius-md: calc(var(--radius) - 2px);
  --radius-lg: var(--radius);
  --radius-xl: calc(var(--radius) + 4px);

  --shadow-2xs: var(--shadow-2xs);
  --shadow-xs: var(--shadow-xs);
  --shadow-sm: var(--shadow-sm);
  --shadow: var(--shadow);
  --shadow-md: var(--shadow-md);
  --shadow-lg: var(--shadow-lg);
  --shadow-xl: var(--shadow-xl);
  --shadow-2xl: var(--shadow-2xl);

  --tracking-tighter: calc(var(--tracking-normal) - 0.05em);
  --tracking-tight: calc(var(--tracking-normal) - 0.025em);
  --tracking-normal: var(--tracking-normal);
  --tracking-wide: calc(var(--tracking-normal) + 0.025em);
  --tracking-wider: calc(var(--tracking-normal) + 0.05em);
  --tracking-widest: calc(var(--tracking-normal) + 0.1em);
}

body {
  letter-spacing: var(--tracking-normal);
}
```


## 产品气质描述

科技感、黑客绿、简约、现代、专业、沉浸


# 技术与代码规范文档

## 前端技术栈与环境

* 库：React 
* 语言：Typescript
* 构建工具：vite
* 包管理工具：npm
* 组件库：shadcnUI
* CSS 预处理：TailwindCSS v4
* 状态管理：Redux
* 路由管理：react router

- **命名约定：** 组件、变量、函数、CSS 类名的命名规则（PascalCase 用于组件，camelCase 用于变量，kebab-case 用于 CSS 类名）。
- **代码风格：** ESLint配置，强制执行的代码格式规范。
* **性能优化：** 图片懒加载、代码分割、虚拟列表


# API 接口文档

这个部分你可以自行发挥，我只需要一个原型界面就可以



