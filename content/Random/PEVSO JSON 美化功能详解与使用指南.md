---
date: 2026-01-13
tags:
---

## PVESO 帮助文档

## 1\. PVESO JSON 美化叙述

### 1.1 导入角色

PVESO 完全兼容 Sillytavern 角色卡格式，支持携带的完整世界书与正则脚本。

如果导入后遇到显示异常，这通常是由于不同平台的渲染标准差异所致，请参考下面的说明进行调整。

#### PVESO 的渲染标准与安全设计

平台渲染引擎兼容 Markdown 和 HTML 混合解析。严格遵循主流 Web 标准，采用 GitHub Flavored Markdown 规范。

平台将保障用户的流畅体验与数据安全作为首要任务，防止恶意脚本和内容注入带来的风险；我们移除了 iframe 渲染及 JavaScript 脚本执行，使用更安全的渲染方式进行安全隔离。

如果您导入的角色卡有 JavaScript 脚本，并且需要点击交互行为，请查阅目录《标签交互指令》章节修改相关内容。

#### 常见问题及修改建议

- **问题：** 在 Markdown 语法内部使用 HTML 标签
	HTML
	```
	<div>要展示的 html</div>
	```
	- **技术解释：** 在标准的 Markdown 语法中，代码块内的所有内容都应被视为纯文本，而非可解析渲染的内容。
	- **正确使用：** 移除 Markdown 代码块（\`\`\`）语法，这将确保内容被正确解析和渲染。
- **问题：** 在 HTML 标签内部使用 Markdown 语法
	- **技术解释：** 标准的 Markdown 规范在处理 HTML 标签时，通常会跳过标签内部区域，以保留 HTML 的完整性。因此，其中的 Markdown 语法不会生效。
	- **正确使用：** HTML 标签内，不要书写任何 Markdown 语法。
- **建议：** 尽量选择单一标记风格（纯 Markdown，或合理分段的 HTML），避免将它们混杂嵌套。

---

## 2\. 创建角色

### 30 秒创建角色

**创建新角色的步骤：**

1. 菜单-「创意工坊」-「创建角色」
2. 在"角色名称"下，指定一个名称，例如 Amanda
3. 在"角色封面"下，选择随机生成，或上传你喜欢的图片
4. 点击右上角"创建角色"按钮

恭喜你，你现在有一个可以聊天的基本角色。从角色列表中选择角色，新的聊天将开始。

---

## 3\. 角色设置

创建角色后，你可以返回并编辑任何信息，以丰富角色的设定、对话风格等。

你可以调整角色的描述、设定、场景、对话示例、第一条消息、多条开场白等设置。

---

## 4\. 高级定义

**角色卡美化：**

- **Markdown** ：你可以使用 Markdown 语法为角色卡提供基础的格式效果
- **正则表达式** ：你可以使用正则表达式为角色卡提供更复杂的前端样式效果
- **美化建议** ：使用单一标记风格（纯 Markdown，或合理分段的 HTML），避免将它们混杂嵌套
- **注意事项** ：不要在开场白中填写 HTML 标签和 CSS 样式，避免造成模型理解困难，并造成大量 token 消耗

**预设提示词：**

- **系统提示词** ：定义模型需要遵循的一般指令，为对话设定基调和背景
- **后续历史指令** ：在对话历史后添加特殊指令，控制 AI 如何理解和处理历史对话
- **深度提示词设置** ：在对话历史特定位置插入提示词，支持插入类型和插入位置

这些预设功能将以系统级别指令发送给模型，帮助你更加精确控制 AI 的回复行为。

---

## 5\. 提示构建原理

向 AI 发送消息时，文本会与其他内容组合形成"提示"：

- 向 AI 提供的主要说明
- AI 应承担的角色的定义
- 用户角色的定义
- AI 正在交互的"世界"信息
- 数据库的相关文件或信息
- 过去对话摘要
- 网络搜索或其他外部数据源的结果
- 对话中以前的消息
- 用户给 AI 的信息
- AI 关于如何生成响应的最终说明

PVESO 将帮助你构建和修改发送给 AI 的请求。

---

## 6\. 世界书

### 6.1 导入世界书

平台提供独立的世界书管理模块，支持导入 Sillytavern 格式的世界书 JSON 文件。

你可以将任意世界书挂载到多个角色卡，或按需分配给单个角色；使用场景灵活。

在角色卡编辑页内，也提供角色自身的世界书编辑；二者结合满足复杂设定需求。

### 6.2 创建条目

世界书条目可将条目内容动态插入你的聊天中。

**使用方法：**

- 设置常驻，禁用或关键词触发
- 编写条目内容
- 配置插入位置和策略

### 6.3 高级设置

**递归扫描：**

- 允许条目激活其他条目，实现复杂交互
- 可以设置递归延迟和防止进一步递归
- 支持多级递归，按级别分组激活

**包含组：**

- 控制同时触发多个条目时的选择策略
- 支持随机选择或优先级选择
- 可以设置组权重和优先级

**定时效果：**

- 粘性：条目激活后保持 N 条消息的活动状态
- 冷却时间：激活后无法再次激活 N 条消息
- 延迟：需要聊天中有 N 条消息才能激活

---

## 7\. 宏替换

### 7.1 功能概述

世界书条目或本地预设中出现 `{{ macro }}` 结构时，服务端会先展开宏，再将结果发送给 AI。

**使用场景**

- **模块化预设：** 上游集中 setvar，下游通过 getvar 复用；只需开/关前置预设就能快速切换不同设定和行为。
- **可控随机性：** roll 与 random 宏提供 RPG 级别的判定与事件变体，用少量文案就能制造丰富分支与惊喜。

**注意事项**

- 本地预设中的宏与世界书不互通。
- 未支持或无法识别的宏会原样保留输出给 AI。

### 7.2 静态 user / char

**作用：** 快速引用当前会话的用户昵称（ `{{ user }}` ）与角色名称（ `{{ char }}` ）。

**示例**

```
亲爱的 {{user}}，我是 {{char}}；你今天想体验怎样的冒险？
```

### 7.3 时间 time / date / datetime

**作用：** 适合在提示词里描述当前时间线、生成“今日任务”等带日期的提示。

**示例**

```
当前日期：{{date}}，时间：{{time}}
记录最近一次情报更新：{{datetime}}
```

### 7.4 掷骰 roll

**语法：** `{{roll NdM}}` 或 `{{ roll::NdM }}` ，例如 `{{roll 3d6}}` 、 `{{ roll::d100 }}`

**作用：** 生成随机数或返回掷骰总和，可用于跑团事件判定或随机奖励。

**限制：** 单段文本最多 20 个 roll 宏、单宏掷骰不超过 30 次、单骰面数 ≤ 100000、累积掷骰总数 ≤ 150，超限时该宏会被忽略。

**示例**

```
{{roll d10}} 生成1-10的随机数
{{roll 2d6}} 若数值 ≥ 9，请提示玩家谨慎前进
```

### 7.5 随机 random

**语法：** `{{ random::内容1::内容2 }}` 或 `{{random:内容1,内容2}}` ，英文逗号或双冒号分隔。

**作用：** 从候选项里等概率选择一条，适合制造微变体、任务分支或随机事件。

**示例**

```
获得物品：{{random::破旧的航海图,断裂的徽章}}
通关奖励：{{random::屠龙刀::倚天剑::九阴真经}}
```

### 7.6 变量 setvar / getvar

**作用：** 在单段文本内部临时存储变量，实现“先记录，再引用”的链式宏。

**语法：** `{{ setvar::key::value }}` 会写入变量并移除文本； `{{ getvar::key }}` 读取已存值，若不存在则移除文本。

变量生命周期仅限当前世界书条目或预设段落，按顺序执行，不会跨条目共享。

**示例**

```
{{setvar::target::北境要塞}}
侦察目标：{{getvar::target}}
若 {{getvar::target}} 处于戒严状态，请提示玩家走密道
```

---

## 8\. JSON 美化

### 8.1 功能概述

🔥 业界独家，PVESO 率先把结构化 JSON 美化做成可配置产品，真正实现了无脚本的高级 UI 控制。

✨ JSON 美化引擎通过 **结构化配置 + 模板渲染 + 标签交互指令** 直接生成安全、可控的 UI，彻底摆脱正则美化方案的脆弱性。

- ⛔️ 不再受正则贪婪、地狱回溯、流式半截输出、卡顿、电量消耗快的影响。
- 📦 AI 只需输出含有指定「type」的 JSON 协议，掉格式概率极低。
- 🎨 模板内可定义插值、插槽、全局样式，轻松组合复杂界面。
- 🧱 样式可复用、字段可校验，后续维护与扩展都更轻量。
- 🧠 提示词更简洁，数据更可控；可限制 AI 只更新指定 type 或 部分字段，或输出随机数量 JSON。
- 🔒 Shadow DOM + 加密脚本：JSON 模板与正则一样经过加密传输，创作者资产更安全。

### 8.2 基础使用：结构与字段

#### 1️⃣ 定义开场白中 或 AI 回复需返回的 JSON 结构

系统会用 `type` 匹配模板，其他字段将匹配并填充内容：

**NODE**

> 注意：使用 `json ` 进行包裹并换行



```JSON
{
  "type": "status-card",
  "title": "指挥官简报",
  "comment": "保持冷静，优先稳定全排士气。"
}
```

- **type 字段** ： JSON 唯一标识，用于匹配与插槽，建议使用语义化英文（如状态面板： `status-card` ）。
- **其余字段** ： 承载动态内容，字段名使用英文，语义越贴近业务，AI 越易正确更新。

#### 2️⃣ 定义 JSON 模板

由 **type / style / html** 三部分组成：

**NODE**

```JSON
{
  "type": "status-card",
  "style": ".status{padding:14px;border-radius:12px;background:skyblue;}",
  "html": "<div class=\"status\"><h3>{{title}}</h3><p>{{comment}}</p></div>"
}
```

通过 `{{ title }}` 、 `{{ comment }}` 等插值表达式即可从 AI 输出的 JSON 中读取数据，缺失时默认输出空字符串。

### 8.3 特殊标识

#### intro-before / intro-after

当 JSON 标识为 `intro-before` 或 `intro-after` 时，无需匹配任何内容，将在开场白中展示定义的 style 和 html。

- **适用场景：** 表单信息收集、角色卡介绍、引导说明，不依赖正文里的 JSON 块
- **intro-before** ：顶部固定展示
- **intro-after** ：底部固定展示
- **提示** ：支持 LiquidJS 模板语法（如 `{{ user }}` 、 `{{ char }}` 等），但不会匹配正文里的 JSON 块进行注入

#### global-theme

当 JSON 标识（ `type` ）为 `global-theme` 时，无需匹配任何内容，程序自动注入定义的 `style` ，不渲染 HTML。

- **适用场景：** 沉浸式聊天背景、1v1 气泡对话、剧情 HUD、状态面板等需要统一装饰的模块。
	- `.markdown-body` 消息容器 类名
	- `.markdown-dark` 夜间模式 类名

**NODE**

```JSON
# 可为消息容器或对话气泡设置边框圆角，间距，背景颜色，渐变，玻璃拟物背景等

{
  "type": "global-theme",
  "style": "
    # 消息容器背景
    .markdown-body {
      color: #000;
      background: #ecf7ff;
    }

    # 夜间模式附加类名
    .markdown-dark {
      color: #fff;
      background: #1f2933;
    }

    # 1V1 微信式气泡（仅对话）
    # 需设定AI返回提示词
    # 设置p标签 气泡样式
    .markdown-body p {}
    .markdown-dark p {}

    # 剧情对话气泡（旁白+对话）
    # 设置q标签 气泡样式
    .markdown-body q {}
    .markdown-dark q {}
}
```

**提示** ：多个 JSON 条目请确保不重复定义样式，global-theme 中的样式可被其他 JSON 条目相同样式覆盖。

### 8.4 插槽与嵌套

当你配置了多个 JSON 脚本，且它们的 HTML 模板存在父子嵌套关系时，只需在父模板里写上 `{{slot:type}}` ，系统就能自动建立父子关系。

渲染器会收集 AI 返回的 JSON 数据，即使先后顺序不固定，也能可靠地拼装成定义好的结构，解决了以往正则方案难以处理的顺序与嵌套问题。

**父级 HTML**

```JSON
# type = status-card

<div>
  <h3>{{title}}</h3>
  # slot 插槽：在此处插入 type 为： status-detail 的 JSON 模版
  <div>{{slot:status-detail}}</div>
</div>
```

**子级 HTML**

```HTML
# type = status-detail

<div>
  <p>{{name}}</p>
  <p>{{age}}</p>
</div>
```

### 8.5 模板引擎

JSON 模板渲染基于 **LiquidJS** ，支持插值，条件判断、循环、过滤器等常用语法；采取沙箱执行，避免任意 JS 代码，适合非技术用户快速上手。

推荐遵循官方语法书写，常用语法参阅：

- [Playground 在线演示](https://liquidjs.com/zh-cn/playground.html)
- [过滤器语法（计算表达式，格式化等）](https://liquidjs.com/zh-cn/filters/overview.html)

**结合 AI 辅助**

1. 先定义好需要展示的 JSON 数据和结构。
2. 将 JSON 发送给 AI，请它按 LiquidJS 语法生成对应的 HTML 模板。
3. 将 HTML 模板发送给 AI，请它生成你想要的 CCS 样式。

### 8.6 提示词技巧

与传统正则方案不同，JSON 美化要求 AI **显式输出需要更新的 JSON 块** ，并在其中填充指定 type/fields。

提示词要明确 AI 更新哪些 JSON/ type 并返回，正常无需附带完整 JSON 内容。

大世界 JSON 字段多时，如果遇到漏字段情况，再附带字段清单或示例 JSON，让模型逐项补齐，防止遗漏。

#### 示例 1 · 通用基础提示词

**PROMPT**

```
# 在其他设定后补充提示词
# 世界书-常驻条目
# 用户发言（插入深度 1）

1.请结合上下文，根据最后的 json type=xxx的数据，进行相应的更新并输出 JSON 格式返回。
2.保持type字段，仅更新其余字段的数据。
3.如果某字段信息未知，用 "" 或简短说明代替。

# 扩展（结合剧情任意输出数量）
例：至少包括 1 个 status-card 和 1~3 个 status-detail
```

#### 示例 2 · 1v1 微信聊天（全局样式实现气泡）

**PROMPT**

```
对话风格要求：
1. 以角色身份回复用户，使用对话式的语言。
2. 回答简短口语化，禁止大段叙述。
3. 聚焦当下对话，不预先推理或解释。
4. 永远用真诚直接的语气回应{{user}}，可以黑暗、可以负面、可以冲动。
5. 使用生活化语言，但保持情绪穿透力，偶尔自然地使用表情。

对话环境：
- 发生在即时聊天软件内，双方没有见面，也没有旁白。
- 每次根据上下文，回复 1~5 条消息，多条消息使用换行分隔。
```

### 8.7 注意事项

- JSON 对格式有严格的要求，请始终使用正确的双引号、逗号、英文键名。
- 开场白中的 JSON 数据，必须使用 `json ` 进行包裹，开头结尾换行。
- 字段语义化： `name` 、 `age` 比 `value1` 、 `value2` 更易让 AI 理解字段含义并更新逻辑。
- 可使用在线工具快速校验或格式化 JSON。
- [JSON 在线工具](https://www.sojson.com/)
- [视频教程-持续更新](https://space.bilibili.com/3632287851743583)

---

## 9\. 正则表达式

### 9.1 功能概述

正则表达式功能允许你设置多条正则表达式规则和对应的替换内容。

主要用于将开场白或 AI 回复中的特定内容替换为 HTML 和 CSS，实现更丰富的 UI 效果。

**应用场景：**

- 格式化角色开场白，添加样式和布局
- 美化 AI 回复内容，增强视觉效果
- 统一消息格式，提升用户体验

**注意：** 正则美化方案仅为了兼容导入其他角色卡，新创建角色仅推荐 JSON 美化方案。

**替换内容支持：**

- **内联样式** ：直接在 HTML 标签中使用 style 属性
- **style 标签** ：使用 `<style>` 标签定义 CSS 样式
- **HTML 标签** ：支持常用 HTML 标签

**使用提示：**

- 无需设置完整的 HTML 文档结构（DOCTYPE、html、head 等）
- 可直接书写 style 和 div 等标签，留空将替换为空字符串
- JavaScript 脚本相关内容会被过滤
- 注意亮色/暗色模式，如仅支持单一主题，请在角色卡介绍中说明

### 9.2 注意事项

- 请不要使用相同的正则表达式，后者替换的内容会覆盖前者
- style 标签里的类样式请不要使用相同的类名，类名相同时样式会合并

### 9.3 有用链接

- [视频教程-持续更新](https://space.bilibili.com/3632287851743583)
- https://space.bilibili.com/3632287851743583
- https://regexr.com
- https://regex101.com
- https://extendsclass.com/regex-tester.html

---

## 10\. 标签交互指令

### 10.1 功能概述

平台不支持 JavaScript 脚本，点击交互行为通过指令功能实现。

**应用场景：**

- 元素的展示/隐藏/切换
- 发送消息，提交表单数据
- 类名操作，实现任意自定义 css 效果

### 10.2 发送指令：data-action-send

**🎯 功能说明：**

在需要点击的标签写上 data-action-send 标记为可发送元素，点击该元素就会把文本发送到聊天输入框

**🔧 属性总览**

1. `data-action-send`
	- 作用：获取标签内文本发送至聊天输入框
2. `data-action-send="文本"`
	- 作用：发送指定的文本内容
3. `data-auto`
	- 作用：自动发送消息

**📝 使用方法**

**1️⃣ 发送到对话输入框**

发送标签内部内容

HTML

```
<p data-action-send>搜集线索</p>
```

发送指定内容

HTML

```
<p data-action-send="前往村庄的啤酒馆，听取更多情报">搜集线索</p>
```

发送正则捕获内容

HTML

```
<p data-action-send="$1">$1</p>
```

**2️⃣ 直接发送消息**

HTML

```
<div data-action-send data-auto>搜集线索</div>
```

**💡 实际应用示例**

角色对话中的选择项：

HTML

```
<p>你想要怎么做？</p>
<p data-action-send="我选择战斗">⚔️ 战斗</p>
<p data-action-send="我选择逃跑">🏃 逃跑</p>
<p data-action-send="我选择谈判">💬 谈判</p>
```

快速回复：

HTML

```
<div data-action-send="接受任务" data-auto>
  <p>✅ 接受任务</p>
  <p><small>点击直接接受并发送</small></p>
</div>
```

### 10.3 表单交互：提交表单

**🎯 功能说明：**

在 `<form>` 标签内部，使用 `data-action-submit` 标记任意元素，点击后会收集表单内含 "name" 属性的表单控件信息。

**🔧 属性总览**

1. `data-action-submit`
	- 作用：标记为表单提交触发器，收集表单字段发送至聊天输入框
2. `data-action-submit="文本"`
	- 作用：添加自定义头部信息，将会作为消息的头部显示
3. `data-auto`
	- 作用：自动发送消息

**📝 表单控件字段设置要求**

- **name** ：字段名称（必填，英文字符，否则不会被采集）
- **data-label** ：采集显示的内容（例：data-label="姓名"）
- **标签显示：** 优先输出 data-label，否则输出 name

**📝 使用方法**

基础表单

HTML

```
<form>
  <input name="name" data-label="姓名" value="" />
  <input name="age" value="" />
  <button data-action-submit="用户信息">提交表单</button>
</form>
```

输出结果

```
用户信息
姓名: 用户输入的姓名
age: 用户输入的年龄
```

**注意事项：**

1. 提交按钮必须在 `<form>` 标签内部
2. 表单字段必须有 name 属性才会被采集
3. 推荐使用 data-label 设置中文显示标签
4. 支持所有表单控件：输入框、单选、复选、下拉等
5. 布尔值会自动转换为中文：true→是，false→否
6. 多选字段会分别显示每个选中的值

### 10.4 类名操作：class

**🎯 功能说明：**

通过 `data-*` 指令为目标元素添加 / 移除 / 切换类名，在不编写 JavaScript 的情况下实现任意 CSS 效果。

**指令功能**

1. `data-add-class` ：为目标添加类名（多个类名空格分隔）
2. `data-remove-class` ：从目标移除类名（多个类名空格分隔）
3. `data-toggle-class` ：逐一切换类名（多个类名空格分隔）

说明：同一元素同时写多条指令时，执行顺序固定为 remove → add → toggle

**属性总览**

指令未定义目标属性时，默认作用于自身；可用 `data-target` 指定统一目标

复杂需求可使用 `data-remove-target` / `data-add-target` 分别指定移除类名，添加类名的目标

1. `data-target` ：指令生效的目标元素（多个元素使用逗号分隔）
2. `data-remove-target` / `data-add-target` ：分别指定 remove / add 的目标元素（多个元素使用逗号分隔）

说明：如果找不到 target 目标元素，指令生效对象将回退至当前触发元素自身

**📝 使用示例**

自身切换背景（原文未提供具体代码，此处保留结构）

控制其它元素

HTML

```
<style>
  button {
    padding: 8px 15px;
    border: 1px solid #dcdfe6;
    background: #f4f4f5;
    cursor: pointer;
    border-radius: 4px;
    margin-right: 4px;
  }

  .panel {
    display: none;
    margin-top: 8px;
    padding: 12px;
    border: 2px solid #4a7b70;
    border-radius: 8px;
  }
  .panel.show {
    display: block;
  }
</style>
<button
  data-target=".panel-1, .panel-2"
  data-add-class="show">
  显示面板
</button>
<button
  data-target=".panel-1, .panel-2"
  data-remove-class="show">
  隐藏面板
</button>
<div class="panel panel-1">面板 1</div>
<div class="panel panel-2">面板 2</div>
```

### 10.5 display

**🎯 功能说明：**

通过 `data-display-*` 指令为任意元素添加或移除隐藏类（ `.is-hidden` ），无需编写 JavaScript 即可完成折叠、面板切换等交互。

**🔧 属性总览**

1. `data-display-hide` ：对选择器匹配的元素添加隐藏类
2. `data-display-show` ：从目标移除隐藏类，恢复展示
3. `data-display-toggle` ：在隐藏/显示之间切换

**💡 使用说明**

- 平台默认提供 `.is-hidden { display: none; }` ，如需其它效果在 `<style>` 中覆写。 例如： `.is-hidden { display: unset; }`
- 每个指令都需要指定目标元素（例如 `.box` 或 `.box1,.box2` ），多个元素使用逗号分隔；未指定目标时不会执行。
- 执行顺序为「hide → show → toggle」，可以在一次点击里完成折叠再激活的组合效果。

**📝 使用示例**

**基础显示/隐藏**

HTML

```
<style>
  /* 可省略，可覆盖成你想要的效果 */
  .is-hidden {
    display: none;
  }

  button {
    padding: 8px 15px;
    border: 1px solid #dcdfe6;
    background: #f4f4f5;
    cursor: pointer;
    border-radius: 4px;
    margin-right: 4px;
  }

  .box {
    padding: 10px;
    border: 1px solid #409eff;
    color: black;
    background: #ecf5ff;
    border-radius: 8px;
    margin-top: 8px;
  }
</style>

<button data-display-toggle=".box">面板显示/隐藏</button>
<div class="box">
  ### 🎯 目标面板
  <br />
  这个面板的显示状态由上面的按钮控制
</div>
```

**Tab 面板切换**

**综合示例：TAB 切换 + 选中高亮**

- **显示/隐藏：** 用 display 指令即可： `data-display-hide=".tab-panel" + data-display-show=".tab-panel-X"` ，一键完成面板切换
- **选中态效果：** 需要选中高亮时才加 class 指令，先对所有按钮移除选择类名，再给当前按钮加选中类名。两组指令互不影响，按钮高亮更直观

📝 **示例：Tab 高亮 + 切换**

HTML

```
<style>
/* 基础布局 */
.tab-header {
  display: flex;
  gap: 8px;
  margin-bottom: 12px;
}

.tab-btn {
  padding: 8px 12px;
  border: 1px solid #d7dbe7;
  border-radius: 6px;
  background: #f7f8fb;
  color: #4a4f62;
  cursor: pointer;
  transition: all 0.2s ease;
}

.tab-btn:hover {
  background: #eef2ff;
  border-color: #b4c4ff;
}

/* 高亮 */
.tab-btn.active {
  background: #5b7bff;
  border-color: #4c6aff;
  color: #fff;
}

/* 面板 */
.tab-body {
  padding: 12px;
  border: 2px solid #4a7b70;
  border-radius: 8px;
}

/* 默认隐藏类 */
.is-hidden {
  display: none;
}
</style>

<div class="tab-header">
  <button
    class="tab-btn tab-btn-1 active"
    data-remove-class="active"
    data-remove-target=".tab-btn"
    data-add-class="active"
    data-add-target=".tab-btn-1"
    data-display-hide=".tab-panel"
    data-display-show=".tab-panel-1"
  >概览</button>

  <button
    class="tab-btn tab-btn-2"
    data-remove-class="active"
    data-remove-target=".tab-btn"
    data-add-class="active"
    data-add-target=".tab-btn-2"
    data-display-hide=".tab-panel"
    data-display-show=".tab-panel-2"
  >配置</button>

  <button
    class="tab-btn tab-btn-3"
    data-remove-class="active"
    data-remove-target=".tab-btn"
    data-add-class="active"
    data-add-target=".tab-btn-3"
    data-display-hide=".tab-panel"
    data-display-show=".tab-panel-3"
  >日志</button>
</div>

<div class="tab-body">
  <div class="tab-panel tab-panel-1">面板1</div>
  <div class="tab-panel tab-panel-2 is-hidden">面板2</div>
  <div class="tab-panel tab-panel-3 is-hidden">面板3</div>
</div>
```