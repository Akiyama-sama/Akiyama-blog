---
date: 2026-03-25
tags:
---
# Provider 与 API 的统一、归一化与配置机制

## 这篇文档解决什么问题

这个项目支持很多模型提供商，例如 OpenAI、Anthropic、Google、Mistral、xAI、Groq、Cerebras、OpenRouter、GitHub Copilot、Amazon Bedrock 等。

这些提供商表面上都在做同一件事：接收一段上下文，返回一段模型输出，有时还会返回工具调用、思考内容、图片输入、用量和费用。

但它们实际上有很多差异：

- 鉴权方式不同，有的用 API Key，有的用 OAuth，有的用云平台默认凭证
- 请求协议不同，有的走 OpenAI Chat Completions，有的走 OpenAI Responses，有的走 Anthropic Messages，有的走 Google Generative AI
- 同样叫“支持 OpenAI 兼容”，字段也可能不完全一样
- 思考能力的开关不同，有的叫 `reasoning_effort`，有的叫 `thinking`，有的叫 `enable_thinking`
- 工具调用格式不同，工具结果回传格式也不同
- 流式输出格式不同，有的按文本分块，有的按 item 分块，有的按 reasoning / text / tool call 分开流出
- tool call ID 的格式约束不同，有的能接受很长很复杂的 ID，有的只能接受短且受限字符集的 ID
- 有的支持图片输入，有的不支持
- 有的支持 prompt cache，有的支持但字段不一样，有的完全不支持

这个项目的核心价值，不是简单地“支持很多 provider”，而是把这些差异收敛成一套统一的内部模型，让上层只用面对一致的概念。

换句话说，这个项目解决的是：

1. 如何让多个 provider 共用一套调用入口
2. 如何把各家输入格式统一成同一种上下文模型
3. 如何把各家输出格式统一成同一种事件流和消息结构
4. 如何让配置尽量声明式，而不是到处写特判
5. 如何让“新增 provider”变成一种可复制的模式，而不是一次性工程

如果只看一句话，这个项目的设计思想是：

> 先统一内部语义，再为每种 API 写适配器；provider 只是“模型归属与默认配置”，真正的协议差异由 api adapter 和 compat 层吸收。

---

## 一句话总览

这个项目把“模型提供商差异”拆成四层：

1. **模型元数据层**：描述“这个模型是谁、走什么 API、支持什么能力”
2. **统一上下文层**：把所有会话都表示成统一的 `Context / Message / Tool / AssistantMessage`
3. **API 适配层**：按 API 类型把统一上下文转换成各家请求，再把原生响应转换回来
4. **兼容修补层**：对“看起来兼容但其实不完全兼容”的 provider 做小范围修正

这四层叠起来，才能同时做到：

- 上层调用简单
- 配置可扩展
- 差异被控制在局部
- 跨 provider 切换时上下文还能继续使用

---

## 先建立最重要的心智模型：`provider` 不等于 `api`

很多系统会把 provider 和协议绑死，例如“OpenAI 就是 OpenAI API”，“Anthropic 就是 Anthropic API”。这个项目没有这样做。

这里有两个独立概念：

### 1. provider

`provider` 表示“这个模型归属于谁，默认使用哪套认证和配置”。

它更接近业务视角，关心的是：

- 这个模型应该显示在谁的 provider 下面
- 默认应该去哪个 base URL
- 默认用哪种鉴权方式
- 它属于哪组模型
- 在 CLI、TUI、设置面板里怎么被展示和选择

例如：

- `openai`
- `anthropic`
- `google`
- `github-copilot`
- `openrouter`
- `mistral`
- `zai`
- `amazon-bedrock`

### 2. api

`api` 表示“这个模型实际使用哪一种协议适配器”。

它更接近技术视角，关心的是：

- 请求体长什么样
- 响应流怎么解析
- thinking / tool call / image / usage 分别怎么映射
- stop reason 怎么归一化

这个项目内置了若干种 API 适配器，例如：

- `openai-completions`
- `openai-responses`
- `azure-openai-responses`
- `openai-codex-responses`
- `anthropic-messages`
- `google-generative-ai`
- `google-gemini-cli`
- `google-vertex`
- `bedrock-converse-stream`

### 为什么要拆成两层

因为现实世界不是“一家 provider 对应一种协议”。

典型情况有两类：

#### 一类是“多个 provider 共享同一种 API”

例如很多服务都走 OpenAI 兼容接口，但并不是真正的 OpenAI：

- Mistral
- xAI
- Cerebras
- Groq
- OpenRouter 中的一部分模型
- 一些本地推理服务，例如 Ollama、LM Studio、vLLM

这些服务如果都重写一遍完整 provider 逻辑，代码会非常重复。更好的做法是：

- 复用 `openai-completions` 适配器
- 只在必要处补一个 `compat` 配置

#### 另一类是“同一个 provider 可能同时提供多种协议或多种模型来源”

例如：

- `github-copilot` 下面既可能代理 OpenAI 风格的模型，也可能代理 Anthropic 风格的模型
- `openrouter` 从业务上看是一个 provider，但上游真正跑模型的可能是 OpenAI、Anthropic、Bedrock 等

因此：

- `provider` 决定“是谁”
- `api` 决定“怎么说话”

这就是这个项目能同时支持很多 provider、又不把逻辑写炸的关键。

---

## 整体架构：从调用到输出的一条完整链路

可以把整条链路理解为下面这张图：

```text
调用方
  |
  | 传入 Model + Context + Options
  v
统一入口
  |
  | 根据 model.api 找到对应 API 适配器
  v
API 适配器
  |
  | 1. 把统一上下文转换成 provider 请求
  | 2. 发起真实请求
  | 3. 解析原生流式响应
  v
统一事件流 / 统一 AssistantMessage
  |
  | 输出 text / thinking / toolCall / usage / stopReason
  v
上层应用（CLI / TUI / Agent / Web UI）
```

这条链路里最重要的是“统一入口”和“统一输出”。

因为只要这两端稳定：

- 中间想新增多少 provider 都可以
- 上层应用不用跟着新增条件分支
- 会话可以在 provider 之间迁移

---

## 第一层：模型元数据层

模型元数据层负责回答一个问题：

> 对于一个具体模型，系统最少需要知道哪些信息，才能正确调用它？

这个项目把一个模型抽象成一份标准化元数据。你可以把它理解成“模型注册表中的一行记录”。

### 一个模型最核心的字段

每个模型至少要有这些信息：

- `id`：模型在远端 API 中使用的真实标识
- `name`：展示给用户看的友好名称
- `provider`：这个模型属于哪个 provider
- `api`：这个模型走哪种 API 适配器
- `baseUrl`：请求默认发到哪里
- `reasoning`：是否支持思考/推理能力
- `input`：支持哪些输入类型，例如文本、图片
- `contextWindow`：上下文窗口大小
- `maxTokens`：最大输出 token 数
- `cost`：输入、输出、缓存读写的费用信息
- `headers`：provider 级别的默认请求头
- `compat`：对“半兼容协议”的差异修补配置

### 为什么模型元数据要这么全

因为它既是“配置”，也是“能力声明”。

例如：

- 如果 `reasoning = false`，上层就知道不要给这个模型强行传 thinking 配置
- 如果 `input` 不含 `image`，消息转换时就知道要丢掉图片输入
- 如果 `api = openai-completions`，就知道应该走 OpenAI Chat Completions 适配器
- 如果 `compat.maxTokensField = max_tokens`，就知道请求里不能发 `max_completion_tokens`

也就是说，很多差异并不是靠 `if provider === ...` 写死，而是先沉淀为模型元数据和兼容配置。

### 模型元数据从哪里来

这个项目同时支持两类模型来源：

#### 1. 内置模型

项目自带一份模型清单。用户安装后，不需要手动录入每个模型的能力参数。

这让系统具备两个优势：

- 用户体验好，开箱即用
- 上层可以做更强的能力推断，比如默认模型选择、thinking 能力判断、成本统计

#### 2. 自定义模型

用户也可以通过配置文件增加或覆盖模型，例如：

- 接一个公司内部代理
- 接本地 Ollama / vLLM / LM Studio
- 用 OpenRouter 或其他统一网关
- 覆盖内置 provider 的默认地址和兼容设置

因此模型层本质上是一个“注册表”，而不是写死在代码里的枚举。

---

## 第二层：统一上下文层

如果模型元数据回答的是“这个模型是什么”，那么统一上下文层回答的是：

> 不同 provider 之间，怎样用同一种内部表示来描述一段会话？

这个项目的做法是：不直接把上游 API 的消息结构暴露给上层，而是定义一套内部统一消息模型。

### 统一上下文结构

一段会话被表示成：

- `systemPrompt`
- `messages`
- `tools`

其中 `messages` 只允许三种角色：

1. `user`
2. `assistant`
3. `toolResult`

这很重要，因为有些上游协议角色很多，有些角色很少，但内部只保留“真正影响代理推理链”的最小集合。

### assistant 消息不是一整段文本，而是内容块数组

assistant 的内容不会被压成一整段字符串，而是拆成内容块列表。块的类型包括：

- `text`
- `thinking`
- `toolCall`

这是一项非常关键的设计。

因为不同 provider 的输出虽然形式不同，但最后都可以投影到这三类语义：

- 普通回答文本
- 模型思考内容
- 工具调用

只要把内部 assistant 消息设计成块数组，就可以保留更多语义，而不是在早期就把信息丢掉。

### tool result 也被统一成标准消息

工具返回不会直接拼进 assistant 文本，而是作为独立的 `toolResult` 消息，包含：

- 对应的 `toolCallId`
- 工具名
- 文本和图片等内容块
- 是否出错

这样做的好处是：

- 续轮对话时可以精确回放工具结果
- 不同 provider 可以按各自协议重新编码
- 图片型工具结果也可以被统一表示

### 为什么统一上下文层是必要的

如果没有这层，上层应用就必须知道：

- Anthropic 的 tool_result 长什么样
- OpenAI Responses 的 function_call_output 长什么样
- Google 的 functionResponse 长什么样

这会导致业务层和协议层耦合。统一上下文层的意义就是把这种耦合切断。

---

## 第三层：API 适配层

统一上下文层解决的是内部表示问题，但真正发请求时，还是必须说各家听得懂的话。

这就是 API 适配层的职责。

### API 适配层做什么

每种 API 适配器都要完成三件事：

1. 把统一 `Context` 转换成目标 API 的请求格式
2. 把统一工具定义转换成目标 API 的工具格式
3. 把目标 API 的流式响应转换回统一事件流和统一 `AssistantMessage`

可以把它理解成“协议翻译器”。

### 为什么是按 API 写适配器，而不是按 provider 写

因为很多 provider 共享一套协议形状。

例如：

- 大量 provider 都能复用 `openai-completions`
- 所有 Anthropic Messages 兼容服务都可以复用 `anthropic-messages`
- 所有 Google Generative AI 兼容服务都可以复用 `google-generative-ai`

这样设计的结果是：

- 代码复用率高
- 新接一个 provider 往往只要补配置，不需要重写请求解析器
- 兼容问题被限制在小范围
 ### 统一入口为什么能成立

因为入口并不关心 provider，而只关心 `model.api`。

调用时流程大致是：

1. 上层拿到一个 `Model`
2. 模型里包含 `api`
3. 系统根据 `api` 找到对应适配器
4. 适配器负责剩下的全部工作

这意味着：

- `openai` 和 `mistral` 虽然是不同 provider，但如果都走 `openai-completions`，上层入口是完全一样的
- `github-copilot` 下面如果某个模型走 Anthropic 风格，入口也不需要特殊处理

---

## 第四层：compat 兼容修补层

到这里还差最后一块拼图。

问题是：现实里很多服务宣称兼容某个协议，但只是“大致兼容”，并不是完全一致。

例如：

- 同样走 OpenAI 兼容接口，但有的 provider 不支持 `developer` role
- 有的不支持 `reasoning_effort`
- 有的要求 `max_tokens`，有的要求 `max_completion_tokens`
- 有的 tool result 必须补 `name`
- 有的对 tool call ID 的字符集和长度有严格要求
- 有的 thinking 不能作为独立块发送，只能降级成普通文本

如果把这些特判都直接写进某个 provider 实现里，代码很快就会失控。

这个项目的做法是：加一个 **compat 配置层**。

### compat 的作用

compat 不是新的协议层，它只做一件事：

> 在复用某个 API 适配器的前提下，对特定 provider 的小差异做声明式修补。

### compat 典型能修什么

以 OpenAI-compatible 体系为例，compat 常见字段包括：

- `supportsStore`
- `supportsDeveloperRole`
- `supportsReasoningEffort`
- `supportsUsageInStreaming`
- `supportsStrictMode`
- `maxTokensField`
- `requiresToolResultName`
- `requiresAssistantAfterToolResult`
- `requiresThinkingAsText`
- `requiresMistralToolIds`
- `thinkingFormat`
- `openRouterRouting`
- `vercelGatewayRouting`

### thinkingFormat 是一个非常典型的例子

表面上很多模型都支持“思考”，但不同服务的参数格式不一样：

- OpenAI 风格：`reasoning_effort`
- z.ai 风格：`thinking: { type: "enabled" }`
- Qwen 风格：`enable_thinking: true`

如果没有 compat，这里就只能写很多 provider if/else。

有了 compat 后，适配器只需要根据 `thinkingFormat` 选择正确的编码方式。这样：

- 业务语义还是统一的“我要开启 reasoning”
- 协议差异被限制在编码层

### compat 的本质

compat 本质上是：

> 用数据描述小差异，而不是用代码扩散小差异。

这是这个项目可维护性的关键之一。

---

## 统一输入：项目如何把不同会话输入归一化

前面讲的是静态设计，下面讲动态过程。

当一段上下文要被发给某个模型时，系统做的不是“直接序列化”，而是一个多步归一化流程。

### 第一步：从统一上下文出发

调用方只需要提供统一的：

- system prompt
- user / assistant / toolResult 消息
- tools

这一步完全不需要关心目标 provider 的协议细节。

### 第二步：做跨 provider 兼容转换

这一步非常关键。因为一段会话可能不是在当前 provider 里产生的，而是从别的 provider 切过来的。

例如：

- 先用 Claude 回答
- 再切到 GPT
- 再切到 Gemini 继续

这时旧消息里会带着原 provider 的 thinking signature、tool call ID 格式、工具调用结构等信息。

系统会先做一次“跨 provider 归一化转换”，主要处理这些问题：

#### 1. thinking block 不能盲目原样回放

只有在“同 provider、同 API、同模型”或者明确兼容的场景下，thinking block 才能安全保留。

否则通常要降级成普通文本，原因包括：

- 目标 provider 不理解原来的 thinking signature
- 原 provider 的 reasoning item 无法被目标 provider 验证
- 强行回放会触发协议校验错误

也就是说，系统优先保证“上下文可继续使用”，而不是强行保留原始底层结构。

#### 2. tool call ID 需要规范化

各 provider 对 tool call ID 的要求不同，例如：

- 有的允许超长、带特殊字符的 ID
- 有的只允许字母、数字、下划线、短横线
- 有的长度上限很短
- Mistral 一类 provider 甚至对格式有更严格要求

因此系统会在必要时对 tool call ID 做规范化，并同步修正对应的 tool result 引用。

#### 3. thought signature 只能在兼容场景下保留

有些 provider 会返回“思考签名”或“加密 reasoning 片段”，它们的意义通常只在原 provider 或原模型下成立。

切 provider 时，这些信息经常必须丢弃或转成普通文本，否则会导致 replay 失败。

#### 4. orphaned tool call 需要被补齐

如果历史里出现 assistant 发起了 tool call，但后续没有匹配的 tool result，某些 provider 会把这视为非法上下文。

系统会插入 synthetic tool result 来保持会话结构完整。

这一步的设计哲学很明确：

> 比起“完全保留底层细节”，更重要的是“让会话可以安全地继续”。

### 第三步：按目标 API 转换消息格式

完成跨 provider 归一化后，系统再把统一消息转换成目标 API 的格式。

这里每种 API 都有自己的一套映射规则。

#### OpenAI Chat Completions 风格

会被映射成：

- `system` / `developer` / `user` / `assistant` / `tool`
- `tool_calls`
- `tool_call_id`
- 可选的 reasoning 相关字段

#### OpenAI Responses 风格

不会直接映射成普通 chat message，而是拆成 item 列表，例如：

- reasoning item
- output message
- function_call
- function_call_output

这套结构比 Chat Completions 更细粒度，因此适配器需要额外维护 item 级语义。

#### Anthropic Messages 风格

assistant 内容会被组织成 block 列表，例如：

- text block
- thinking block
- tool_use block

tool result 则会被封装进 user 角色里的 `tool_result` block。

#### Google Generative AI 风格

消息会被组织成：

- `Content`
- `Part`
- `functionCall`
- `functionResponse`

Google 体系尤其强调 thought signature 和 function response 的结构完整性。

### 第四步：根据模型能力过滤不支持的内容

例如：

- 如果目标模型不支持图片输入，图片块会被过滤掉
- 如果目标模型不支持 reasoning，对应 thinking 配置会被忽略或关闭
- 如果某类 provider 不支持某个工具字段，就在工具转换时去掉

这一步保证“统一输入”不是盲目下发，而是根据模型能力裁剪后的结果。

---

## 统一输出：项目如何把不同 provider 的响应归一化

请求发出后，真正复杂的部分才开始。

因为每家 provider 的流式输出协议都不同，甚至同一家不同 API 也完全不同。

这个项目的策略是：

> 所有 provider 最终都必须产出同一套事件流和同一种 assistant 消息结构。

### 统一事件流

系统定义了一套标准流式事件：

- `start`
- `text_start`
- `text_delta`
- `text_end`
- `thinking_start`
- `thinking_delta`
- `thinking_end`
- `toolcall_start`
- `toolcall_delta`
- `toolcall_end`
- `done`
- `error`

这意味着上层 UI 或 Agent 逻辑完全不需要知道：

- OpenAI 的 chunk 长什么样
- Anthropic 的 content block delta 长什么样
- Google 的 candidates / parts 怎么分布

上层只要消费统一事件流即可。

### 为什么统一事件流很重要

如果没有统一事件流，上层会遇到这些问题：

- TUI 要分别支持每家 provider 的增量文本协议
- thinking 面板要分别适配每家 provider 的格式
- tool call UI 要分别处理每家的 partial JSON 格式
- usage 和 stop reason 无法统一显示

统一事件流之后，这些都变成同一个接口问题。

### assistant 最终输出也被统一

流式事件结束后，系统还会得到一个完整的 `AssistantMessage`。它包含：

- 统一的内容块数组
- 统一的 usage
- 统一的 stop reason
- 统一的 provider / api / model 标识

这样无论上层是：

- CLI
- TUI
- Agent Runtime
- Web UI

都可以用同一种方式持久化和回放 assistant 消息。

### stop reason 也被统一

不同 provider 原生返回的停止原因很多种，但内部统一成少数几类：

- `stop`
- `length`
- `toolUse`
- `error`
- `aborted`

统一后的好处是：

- 上层逻辑简单
- 重试逻辑简单
- UI 展示一致
- 统计和测试更容易覆盖

### usage 和 cost 也被统一

不同 provider 返回 token usage 的方式不同：

- 有的会把 cache token 单独给出来
- 有的会把 reasoning token 算在 completion 里
- 有的会把 cached token 包在 input 里
- 有的流式期间不返 usage，只在最终事件给

适配器会把这些差异统一映射成标准 usage：

- `input`
- `output`
- `cacheRead`
- `cacheWrite`
- `totalTokens`
- `cost`

这样上层不需要知道某家 provider 的 usage 统计细节。

---

## reasoning / thinking 是如何被统一的

这是整个项目中最漂亮的一部分之一。

因为“思考能力”几乎是各家差异最大的地方，但这个项目仍然给了一个统一接口。

### 上层看到的接口

上层不需要直接关心 provider 的原生命名，而是用一个统一概念：

- `reasoning: minimal | low | medium | high | xhigh`

这就是所谓的“简单选项接口”。

### 为什么这层统一非常重要

如果没有它，上层调用就会变成：

- OpenAI 要传 `reasoningEffort`
- Anthropic 要传 `thinkingEnabled + thinkingBudgetTokens` 或 adaptive effort
- Google 要传 `thinking.enabled + budgetTokens` 或 `thinking.level`
- z.ai 要传另一种 thinking 结构

这会把业务代码变成一堆 provider 分支。

### 这个项目怎么做

系统先定义统一 reasoning 级别，再在各 API 适配器里做映射。

#### 对 OpenAI 风格模型

通常映射成 `reasoning_effort` 或同义字段。

#### 对 Anthropic

会根据模型能力决定：

- 新模型走 adaptive thinking
- 旧模型走 budget-based thinking

也就是说，对调用方来说只是“我要 high”，但系统会自动决定应该发：

- effort 型参数
- 还是 thinking budget 型参数

#### 对 Google

会根据模型家族决定：

- 有的模型走 `thinkingLevel`
- 有的模型走 `thinkingBudget`

#### 对 z.ai / Qwen 这类 OpenAI 兼容变体

会通过 `thinkingFormat` 兼容配置，把统一 reasoning 语义改写成 provider 需要的字段格式。

### 这件事背后的思想

reasoning 的统一并不是“所有 provider 真有同一个参数”，而是：

> 先统一用户想表达的意图，再由适配器把意图翻译成各家最接近的实现方式。

这才是归一化的正确方式。

---

## tools 是如何被统一的

工具调用是另一个差异很大的领域。

统一工具支持，至少要解决四个问题：

1. 工具定义格式不同
2. 工具调用流式增量格式不同
3. 工具结果回传格式不同
4. tool call ID 兼容性不同

### 统一的工具定义

内部工具定义只保留最核心的三部分：

- 工具名
- 描述
- 参数 schema

然后在发请求时，再由各 API 适配器转换成：

- OpenAI function tool
- Anthropic tool schema
- Google function declaration

### 统一的工具调用输出

无论底层 provider 怎么表达，assistant 最终都统一产出：

- `type: toolCall`
- `id`
- `name`
- `arguments`

这就让工具执行器可以完全脱离 provider 工作。

### 统一的工具结果输入

工具执行完成后，统一塞回一条 `toolResult` 消息。

适配器再根据目标 API 把它翻译成：

- OpenAI 的 `tool` 消息
- OpenAI Responses 的 `function_call_output`
- Anthropic 的 `tool_result`
- Google 的 `functionResponse`

### tool call ID 为什么要特别强调

因为这是跨 provider handoff 最容易炸的地方之一。

原因很简单：

- 某个 provider 生成的 ID，另一个 provider 可能根本不接受
- 但 tool result 又必须引用这个 ID
- 一旦 ID 规则不兼容，会话就无法继续

所以系统会把“ID 归一化”和“toolResult 引用重写”当成一套联动操作处理。

这也是它能做跨 provider 会话迁移的关键能力之一。

---

## 图片输入与图片型工具结果是如何被统一的

不同 provider 对多模态支持差异很大。

这个项目没有把图片单独搞成另一套会话系统，而是直接纳入统一消息块模型。

### 用户输入中的图片

用户消息内部可以包含：

- 文本块
- 图片块

然后在消息转换时：

- 支持图片的模型按目标协议编码
- 不支持图片的模型过滤图片块

### 工具结果中的图片

工具结果也允许包含图片块。

这样系统就可以支持例如：

- 代码执行后产出图表截图
- OCR 或图像分析工具返回图像
- 浏览器工具返回页面截图

不同 provider 会用不同方式接收这些图像结果：

- 有的把它们作为 tool result 的内嵌部分
- 有的必须拆成额外的用户消息

这种差异依然由适配器吸收，上层只管写统一的 `toolResult`。

---

## prompt cache / session 这类差异是如何被统一的

有些 provider 支持 prompt cache，但实现方式并不一致。

项目没有强行把所有细节都暴露给上层，而是提供一套比较保守的统一选项：

- `cacheRetention`
- `sessionId`

### 统一语义是什么

上层只表达两件事：

- 我希望缓存保留多久
- 我是否希望同一个 session 尽可能复用缓存

### 底层怎么做

不同适配器会根据 provider 能力，映射到各自支持的字段：

- OpenAI 系体系使用它能识别的 prompt cache 机制
- Anthropic 体系使用它自己的 cache control
- 不支持缓存的 provider 直接忽略这些字段

这是一种非常实用的“能力上收”方式：

- 对上层来说，只有统一的缓存意图
- 对底层来说，尽量向 provider 的真实能力对齐

---

## 认证是如何被统一的

认证是 provider 差异最明显的地方之一，但这个项目把它抽成了几类统一来源。

### 上层并不直接关心认证细节

调用适配器时，通常只需要一个 `apiKey` 概念，或者让系统自行解析。

真正的认证来源可以是：

- CLI 显式传入
- 本地 auth 文件
- 环境变量
- OAuth 登录结果
- 云平台默认凭证
- 自定义 provider 配置里的 key

### 为什么要统一成“解析顺序”

因为不同 provider 虽然底层认证方式不同，但对上层来说，本质问题只是：

> 我现在要用这个 provider，请帮我找到当前最合适的凭证。

项目把这个问题变成“统一的 credential resolution”流程，而不是让每个调用方分别实现一遍。

### 特殊认证也被收敛进统一模型

例如：

- GitHub Copilot、OpenAI Codex、Google 系列某些 provider 使用 OAuth
- Google Vertex 依赖 Application Default Credentials
- Amazon Bedrock 依赖 AWS 多来源凭证体系

这些 provider 最终仍然表现为“这个模型可以被成功调用”，而不是把复杂的认证细节暴露到上层会话逻辑里。

---

## 配置是如何做到“方便改、方便扩展、尽量不改代码”的

如果一个系统支持很多 provider，但每加一个 provider 都要改很多代码，那么它仍然不算易配置。

这个项目在配置层做了三件很有价值的事：

1. 让内置 provider 开箱即用
2. 让常见自定义 provider 只靠配置就能接入
3. 让真正不兼容的 provider 才需要写扩展代码

### 配置入口分三档

#### 第一档：直接使用内置 provider

这是最简单的方式。

系统已经知道：

- provider 列表
- 模型列表
- 默认 API
- 默认能力声明
- 默认 URL
- 默认 compat

用户只要提供认证信息即可。

#### 第二档：通过配置文件覆盖或新增 provider

适用于这些场景：

- 把现有 provider 改走自己的代理地址
- 给某个 provider 增加自定义模型
- 接一个 OpenAI-compatible / Anthropic-compatible / Google-compatible 的内部服务
- 覆盖特定模型的 compat、headers、价格、上下文窗口

这时通常只要写配置文件，不需要改源码。

#### 第三档：通过扩展注册自定义 provider

只有当 provider 不属于现有协议家族时，才需要自己实现新的流式适配器。

也就是说，项目把扩展门槛压缩到了：

- 大多数“兼容某现有协议”的 provider，只需配置
- 只有“真正非标的 provider”，才需要写代码

这就是“方便配置”的真正含义。

### 配置为什么能这么灵活

因为系统在设计上明确区分了三类东西：

#### 1. provider 级配置

例如：

- `baseUrl`
- `api`
- `apiKey`
- `headers`
- `authHeader`

它们是“这个 provider 下所有模型默认共享”的配置。

#### 2. model 级配置

例如：

- `id`
- `name`
- `reasoning`
- `input`
- `contextWindow`
- `maxTokens`
- `cost`
- `compat`

它们是“某个具体模型自己的能力声明”。

#### 3. override 级配置

例如：

- provider 的模型覆盖
- 内置模型的局部覆盖
- compat 的局部改写

这样用户可以非常精细地改动，而不需要复制整套 provider 定义。

### 这套配置模型的优势

- 能覆盖 80% 以上的接入需求
- 最小改动原则明显
- 内置 provider 和自定义 provider 共用同一套心智模型
- 用户能理解“我是改 provider 级，还是改 model 级”

---

## 为什么 `streamSimple / completeSimple` 很重要

很多人第一次看这个项目，会以为“统一只是模型清单统一了”。其实不是。

真正让上层舒服的是：项目不只统一了模型注册，还统一了最常用的调用接口。

### 两套接口

项目实际上提供两层调用 API：

#### 1. 简单接口

例如：

- `streamSimple`
- `completeSimple`

特点是：

- 参数最少
- reasoning 用统一语义
- 适合大多数业务调用

#### 2. provider-specific 接口

例如：

- 直接调用某个 provider 适配器
- 使用各家专属选项

特点是：

- 更细粒度
- 能控制特定 provider 的专属行为

### 为什么需要简单接口

因为绝大多数业务并不想知道：

- Anthropic 的 thinking budget 该怎么调
- Google 的 thinking level 该怎么映射
- OpenAI Responses 的 reasoning summary 该怎么开

业务层真正关心的是：

- 我想要普通回答还是更强推理
- 我需不需要工具调用
- 我需不需要流式输出

简单接口的价值，就是把这些“通用意图”从 provider-specific 参数里提出来。

### 为什么还保留 provider-specific 接口

因为完全抽象也会损失能力。

有些高级场景必须直达 provider 选项，例如：

- OpenAI Responses 的 reasoning summary
- Anthropic adaptive thinking 的 effort
- 某些 provider 的特有 headers 或 tool choice

因此这个项目不是“强行只有统一接口”，而是：

- 默认走统一接口
- 需要时允许下钻到 provider-specific 层

这是一个很实际的折中。

---

## 跨 provider handoff 为什么能成立

很多多模型系统都支持“切换模型”，但并不真正支持“把已有会话安全迁移到另一家 provider”。

这个项目专门解决了这个问题。

### 问题本质

如果一段会话原本是由某个 provider 生成的，那么历史消息里可能包含：

- 这个 provider 独有的 thinking signature
- 这个 provider 独有的 tool call ID 格式
- 这个 provider 独有的 message item 结构

直接把这些历史原封不动丢给另一个 provider，很容易失败。

### 系统的解决方法

在真正发送给目标模型之前，先做一次“跨 provider 兼容变换”。

核心策略是：

- 用户消息尽量原样保留
- 工具结果尽量原样保留
- assistant 的 thinking 在不兼容时降级成普通文本
- tool call 的 ID 在必要时规范化
- 无法安全 replay 的内部签名被抹平
- 不完整的工具链条被补齐

### 这意味着什么

这意味着系统优先保证两件事：

1. 会话语义连续
2. 目标 provider 能合法接受

它不追求保留所有底层技术细节，因为那会导致 handoff 不稳定。

### 这是归一化设计成熟的标志

一个系统如果只能“同 provider 内续聊”，那只能算 provider 封装。

一个系统如果能“跨 provider 续聊”，才说明它真的建立了独立于 provider 的内部会话模型。

这也是这个项目最值得学习的地方之一。

---

## 新增 provider 时，为什么不容易失控

支持很多 provider 的系统，最怕“每新增一个 provider，都需要改 10 个地方，而且每个地方都要加 if/else”。

这个项目通过分层设计，把新增 provider 变成了一套固定套路。

### 新增 provider 有三种路径

#### 路径一：复用现有 API 适配器，只加模型配置

适用于：

- OpenAI-compatible
- Anthropic-compatible
- Google-compatible

这是最轻的一种。

只要模型元数据和 compat 写对，就能接入。

#### 路径二：复用现有 API 适配器，再加少量 provider 特殊逻辑

适用于：

- 协议基本兼容，但认证、默认头、thinking 字段或工具字段有点不同

这时通常只需要：

- 配 compat
- 配 headers
- 配 baseUrl
- 必要时在适配器中补一个小分支

#### 路径三：实现一个全新的 API 适配器

适用于：

- 请求协议完全不属于现有家族
- 响应流结构完全不同
- 认证和模型发现也高度定制

这时才需要：

- 新增 API 类型
- 实现新的适配器
- 注册到 API registry
- 加入模型元数据和文档

### 为什么不会失控

因为新增 provider 时，系统会强制你回答几个稳定问题：

1. 它属于哪个 provider
2. 它走哪种 api
3. 它的模型元数据是什么
4. 它有没有 compat 差异
5. 它能否复用现有输入转换和输出归一化逻辑

这些问题一旦稳定，新增 provider 就变成“填空题”而不是“重构题”。

---

## 这个项目的设计优势总结

如果把整个设计压缩成几条原则，可以总结为下面几点。

### 1. 先统一内部语义，再适配外部协议

不是直接围绕 OpenAI、Anthropic、Google 的原生格式做业务，而是先抽出：

- 统一模型
- 统一消息
- 统一工具
- 统一事件流
- 统一 stop reason
- 统一 usage

这样外部协议才能成为“边缘适配层”。

### 2. provider 和 api 解耦

这让系统同时获得：

- provider 维度的业务组织能力
- api 维度的协议复用能力

这是整个架构最核心的抽象之一。

### 3. compat 用数据描述小差异

这让 OpenAI-compatible 这类复杂生态不会把主逻辑污染成大量 provider 分支。

### 4. simple interface 和 provider-specific interface 并存

这避免了两个常见极端：

- 只做统一接口，导致丢失高级能力
- 只暴露 provider 原生接口，导致上层过于复杂

### 5. handoff 设计优先保证可继续，而不是保留所有底层细节

这是一种非常现实而成熟的设计选择。

### 6. 配置优先，代码兜底

能用模型元数据和 compat 表达的差异，尽量不写死进代码。

### 7. 上层永远只消费统一事件流和统一消息结构

这保证了 CLI、TUI、Agent、Web UI 不会因为 provider 增多而指数级复杂化。

---

## 如果你要把这套思路迁移到自己的项目，最值得抄的不是代码，而是方法

你真正应该学的，不是某个具体字段名，而是这套抽象顺序。

### 推荐照抄的顺序

#### 第一步：定义统一会话模型

先定义：

- user / assistant / toolResult
- text / thinking / toolCall / image
- usage / stopReason

如果这一步做不好，后面所有 provider 适配都会变脏。

#### 第二步：把 provider 和 api 分开

不要把“谁提供模型”和“走什么协议”写成一个概念。

#### 第三步：为协议家族写适配器，而不是为每个 provider 重写一遍

例如：

- OpenAI-compatible 一套
- Anthropic-compatible 一套
- Google-compatible 一套

#### 第四步：用 compat 吞掉半兼容差异

不要让小差异扩散成业务层的条件分支。

#### 第五步：统一事件流

如果上层仍然要知道每家 provider 的 chunk 长什么样，那你的统一还没有真正完成。

#### 第六步：把跨 provider handoff 当成一等公民设计

只有当系统能安全地 replay 跨 provider 会话，你的内部抽象才算真正独立于 provider。

---

## 最后给一个最简化的理解模型

如果你想把整套架构压缩成最短的几句话，可以这样记：

- **Model** 负责声明“这个模型是谁、支持什么、走哪个 API”
- **Context** 负责声明“会话内部统一长什么样”
- **API Adapter** 负责把统一上下文翻译成某家协议，再把响应翻译回来
- **Compat** 负责修补“兼容但不完全兼容”的小差异
- **Event Stream** 负责把所有 provider 的流式输出变成同一种消费方式

所以这个项目不是在做“多 provider hardcode”，而是在做：

> 一套稳定的内部语言，加若干个对外翻译器。

这就是它能同时支持很多 provider、又能保持配置简单和会话连续性的根本原因。

---

## 附：用一句话区分几个最容易混淆的概念

### provider

模型属于谁，从业务上如何归类，默认如何鉴权和展示。

### api

这个模型实际使用哪种协议适配器，决定请求和响应的编码方式。

### model metadata

某个具体模型的能力声明和默认配置。

### compat

对某种 API 家族中的小型不兼容差异进行声明式修补。

### normalization

把 provider 特有结构转换成项目内部统一结构，或者把统一结构重新编码成目标 provider 可接受结构。

### handoff

把原来在一个 provider 中产生的会话，安全迁移到另一个 provider 继续使用。

---

## 结语

如果你只记住一件事，请记住这句：

> 这个项目真正统一的不是“模型列表”，而是“会话语义、调用入口、事件流和配置模型”。

也正因为它统一的是这些更本质的层次，所以 provider 越多，系统越能体现这套架构的价值，而不是越多越乱。
