---
tags:
  - "#literature"
URL: "https://alibaba-cloud-design.github.io/vibe-designing-playbook/"
author:
created: 2026-07-29
---
PLAYBOOK

01

### 设计工程

把设计判断、执行规范与生成流程放进同一条链路，让 AI 的产出稳定接近明确的质量标准。

Design Engineering02

### 动态交互

界面不再预先画死，而是随用户真实意图在场景中即时生成——先想清任务，再决定此刻该出现什么。

Dynamic Interaction 03

### 自我进化

本章讲飞轮：前两章解决「能做出来」，这一章解决「越做越好，而且不靠人盯」。

Self-Evolution 99

### 结语

把「什么是好的设计」这件原本只存在于直觉里的事，一点点变得明确、可表达、可传递。

Closing A0

### 词典

12 类 188 个审美词条，把「高级」「克制」这类抽象词，翻译成 Agent 能执行的表达规则。

Lexicon

AI 并非不懂设计，而是它的创造力常常被倾向所掩盖。

当需求含糊时，模型倾向于收敛到训练数据中最高频、最稳妥的那一类结果：统一的无衬线字体、浅色背景配紫色渐变、四平八稳的布局。这类结果通用、安全，而这恰恰是它流于平庸的根源。

技术领域将这一现象称为「分布收敛」——模型在采样时偏向多数，而多数往往等同于平均。

真正的问题不在于模型不够强大。它所见过的设计远多于任何一位设计师，本就具备极致的理解力，只是被「向平均靠拢」的惯性所遮蔽。设计师需要做的，不是等待一个更智能的模型，而是把专业的设计能力明确地建立起来、注入给它，让它在具体的业务语境里，知道什么样的设计才称得上好，并沉淀为机制，稳定生产。

作为一支长期服务 Agentic 云产品的设计团队，我们将实践经验拆为三层，构成本书的三章。第一层是设计工程：把设计能力工程化地建立起来，包括判断「什么是好」的设计声明、规定「怎么做对」的执行契约，以及把它们封装成可调度的能力。第二层是动态交互：界面不再是预先画死的页面，而是随用户的真实意图在场景中生成。第三层是自我进化：让产物被持续评估、被打回重做，在 taste 的牵引下自己不断突破模型设计能力上限。

贯穿这三层的，是一个常被略过的事实：能把「什么是好」讲清楚的，始终是人，而不是模型。模型可以学会执行判断、复用判断、规模化地应用判断，但判断本身，得先由一个真正懂设计的人立起来——这正是这套方法由设计团队而非工程团队提出的原因。我们相信，教会 AI 做设计的，从来不是更强的模型，而是更好的设计师。

001 · 03 sections

设计工程解决的是生成阶段的可控性：把设计判断、执行路径和评估机制写进同一条链路，让 Agent 在明确边界内产出符合产品标准的界面。

先看一个具体场景。我们要设计一个 Agent 可视化看板：左边是一列正在跑的任务，中间实时显示每个 agent 的状态——运行中、排队、失败、完成，右边是 token 消耗和耗时趋势。把这段需求交给模型以后，几秒钟内，一个能跑的页面出现了。

这张页面不是完全不可用，但问题很快露出来。运行中、失败、完成各用了一种颜色，饱和度不一，挤在一起难以分辨；任务载入前，中间区是一片空白；某个 agent 失败了，界面只标着「失败」，既点不动，也没有重试入口；再加上蓝紫渐变卡片和每块标题上的大写标签，一眼就能看出是 AI 做的。

这些问题分散在状态语义、边界条件、交互恢复和视觉工艺里。它们不是同一类错误，也不应该靠同一条 prompt 一次性修补。要让生成变得可控，第一步是看清从需求到页面之间究竟发生了什么。

01 <svg viewBox="0 0 700 360" width="100%" role="img" aria-label="Agent 调度看板问题版：四处毛病浮标"><defs><linearGradient id="pb-ai" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#8B7CE6" stop-opacity="0.55"></stop><stop offset="1" stop-color="#6DA0E6" stop-opacity="0.55"></stop></linearGradient></defs><rect x="24" y="24" width="652" height="292" fill="currentColor" stroke="currentColor" stroke-width="1"></rect><line x1="24" y1="60" x2="676" y2="60" stroke="currentColor" stroke-width="1"></line><circle cx="44" cy="42" r="3.5" fill="currentColor"></circle><circle cx="57" cy="42" r="3.5" fill="currentColor"></circle><circle cx="70" cy="42" r="3.5" fill="currentColor"></circle><text x="96" y="46" font-size="11" fill="currentColor" text-anchor="start" font-family="'JetBrains Mono','Chivo Mono',monospace" letter-spacing="1.2" style="text-transform: uppercase;">AGENT SCHEDULER</text> <g><rect x="44" y="84" width="170" height="26" fill="currentColor" stroke="currentColor"></rect><circle cx="58" cy="97" r="3.5" fill="currentColor"></circle><rect x="72" y="94" width="98" height="6" fill="currentColor" opacity="0.55"></rect></g><g><rect x="44" y="122" width="170" height="26" fill="currentColor" stroke="currentColor"></rect><circle cx="58" cy="135" r="3.5" fill="currentColor"></circle><rect x="72" y="132" width="98" height="6" fill="currentColor" opacity="0.55"></rect></g><g><rect x="44" y="160" width="170" height="26" fill="currentColor" stroke="currentColor"></rect><circle cx="58" cy="173" r="3.5" fill="currentColor"></circle><rect x="72" y="170" width="98" height="6" fill="currentColor" opacity="0.55"></rect></g><g><rect x="44" y="198" width="170" height="26" fill="currentColor" stroke="currentColor"></rect><circle cx="58" cy="211" r="3.5" fill="currentColor"></circle><rect x="72" y="208" width="98" height="6" fill="currentColor" opacity="0.55"></rect></g><rect x="236" y="84" width="210" height="146" fill="transparent" stroke="currentColor" stroke-dasharray="3 5"></rect><line x1="316" y1="154" x2="366" y2="154" stroke="currentColor" stroke-width="1.2"></line><rect x="236" y="252" width="210" height="44" fill="currentColor" stroke="currentColor"></rect><circle cx="254" cy="274" r="3.5" fill="currentColor"></circle><rect x="268" y="270" width="84" height="7" fill="currentColor" opacity="0.55"></rect><rect x="470" y="84" width="186" height="146" fill="url(#pb-ai)" stroke="currentColor"></rect><rect x="488" y="102" width="64" height="8" fill="#fff" opacity="0.55"></rect><rect x="488" y="186" width="144" height="6" fill="#fff" opacity="0.4"></rect><rect x="488" y="200" width="112" height="6" fill="#fff" opacity="0.4"></rect><rect x="118" y="96" width="176" height="40" fill="currentColor" stroke="currentColor" stroke-width="1" filter="url(#pb-lift)"></rect><rect x="132" y="113" width="6" height="6" fill="currentColor"></rect><text x="148" y="121" font-size="12" fill="currentColor" text-anchor="start" font-family="'PingFang SC','Noto Sans SC',sans-serif" letter-spacing="0">状态色乱</text> <circle cx="244" cy="116" r="4" fill="#B5514E"></circle><circle cx="260" cy="116" r="4" fill="#C98A2B"></circle><circle cx="276" cy="116" r="4" fill="#5E8C6A"></circle><rect x="280" y="140" width="128" height="40" fill="currentColor" stroke="currentColor" stroke-width="1" filter="url(#pb-lift)"></rect><rect x="294" y="157" width="6" height="6" fill="currentColor"></rect><text x="310" y="165" font-size="12" fill="currentColor" text-anchor="start" font-family="'PingFang SC','Noto Sans SC',sans-serif" letter-spacing="0">空态白屏</text> <rect x="262" y="238" width="208" height="44" fill="currentColor" stroke="currentColor" stroke-width="1" filter="url(#pb-lift)"></rect><rect x="276" y="257" width="6" height="6" fill="currentColor"></rect><text x="292" y="265" font-size="12" fill="currentColor" text-anchor="start" font-family="'PingFang SC','Noto Sans SC',sans-serif" letter-spacing="0">失败无重试</text> <rect x="388" y="248" width="66" height="24" fill="transparent" stroke="currentColor" stroke-dasharray="2 4"></rect><text x="421" y="264" font-size="10" fill="currentColor" text-anchor="middle" font-family="'JetBrains Mono','Chivo Mono',monospace" letter-spacing="1.2" style="text-transform: uppercase;">无重试</text> <rect x="506" y="128" width="152" height="44" fill="currentColor" stroke="currentColor" stroke-width="1" filter="url(#pb-lift)"></rect><rect x="520" y="147" width="6" height="6" fill="currentColor"></rect><text x="536" y="155" font-size="12" fill="currentColor" text-anchor="start" font-family="'PingFang SC','Noto Sans SC',sans-serif" letter-spacing="0">AI 味渐变</text><rect x="614" y="140" width="30" height="20" fill="url(#pb-ai)" stroke="currentColor"></rect></svg>

问题版看板四处毛病 · 各有归属

Design I/O 描述的就是这条链路。Design 是进入系统的设计能力：对功能边界、业务语义、组件使用、视觉工艺和验收标准的判断。Output 是这些判断作用之后产出的界面。中间的 I/O 不是一个抽象说法，而是一组可以被调用、检查和回流的接口。

如果只把生成看成一个黑盒，你能调整的只有送进去的需求。Design I/O 把这个过程拆成几道工序：需求先被理解，再形成结构，填入组件和内容，补齐状态与交互，最后被评估。每一步都可以介入，也都可以承接不同类型的设计能力。

![Design I/O —— 设计能力从每一道工序进入链路](https://alibaba-cloud-design.github.io/vibe-designing-playbook/figures/arch-1-light.svg)

FLOW Design I/O —— 设计能力从每一道工序进入链路

上图呈现了 Vibe Design 从输入到输出的基本结构，可以从三个层次来读。

第一层是主链路。prompt 输入后，依次经过理解规划、搭骨架、填充、细化四道工序，产出一版原型，再交由末端评估。这是产物前进的方向，也是设计能力进入系统的位置。

第二层是 token 注入。颜色、间距、字号这类约束不归属于单一工序，而是自搭骨架起，持续作用于链路全局。它被画成一条贯穿线，是因为视觉一致性不取决于某一步做对，而取决于每一步都不破坏既有约束。

第三层是 critique 回流。当评估判定不达标，流程不需要从头重来，而是带着具体问题退回规划或相关环节。回流让生成过程不只是一次性输出，而是一段可以修正的链路。

主链路、token 注入和 critique 回流，构成本节讨论的全部对象。下文先展开主链路。

## 从规划到评估

在这条主链路里，页面不是一次性被生成出来的。需求会先被理解为任务目标和限制条件，再被整理成信息结构、组件选择、状态反馈和验收判断。

规划决定功能为谁服务、覆盖哪些场景、哪些状态必须存在。搭骨架决定信息以什么空间结构铺开。填充把内容映射到具体组件和业务语义里。细化补齐交互状态、边界反馈和视觉工艺。评估则把结果拿回标准里检查，判断它是否需要回流。

所以这里的设计对象，首先不是一张静态页面，而是信息如何被组织、暴露和验证。界面只是这个过程最后可见的结果。

> 「设计，是为达成某个特定目的、对各要素所做的编排方案。」 Design is a plan for arranging elements in such a way as best to accomplish a particular purpose. —— Charles Eames

这条链路看似简单，但环节顺序并不是随意的。每一步大体都以上一步的产出为前提，逐层推进。上游偏差会沿链路放大，所以约束最好尽早进入，并在每个环节持续被检查，而不是只在末端补救。

把这五步连起来看，它和设计师处理复杂页面时的判断过程很接近。区别在于，人可以把很多判断留在经验里，Agent 需要这些判断被显式写出来。拆出链路的价值正在这里：每一步都变成了可以观察、约束和评估的节点。

## 环节即接口

链路拆开之后，每一个环节都不只是一道工序，也是一个可以接收设计能力的接口。

这些接口不是抽象概念。规划需要知道功能该如何定义、该覆盖哪些状态；搭骨架需要知道页面应该采用什么布局和密度；填充需要知道哪些组件可以用、哪些业务语义不能混；细化需要知道动效、层级、空态和错误态应当如何处理。

这些约束并不属于同一类。前四步主要接收设计声明：spec、domain、craft、design.md、components、template，它们定义什么算对、什么不该发生。推动这些声明进入流程的是 skill。到了末端评估，还需要一份把标准执行成检查项的契约，也就是 evaluator。

同一条通用骨架，落到 CloudAI，每个环节都由一份具体的能力来接管：

| 环节 | 进入这一步的能力 | 它在这一步约束什么 |
| --- | --- | --- |
| 规划 | spec.md | 功能为谁做、覆盖哪些状态、什么算验收 |
| 搭骨架 | template / design.md | 页面骨架、密度、颜色、间距怎么取值 |
| 填充 | components / domain.md | 能用哪些组件、领域状态和数据怎么表达 |
| 细化 | craft.md / design.md | 动效、工艺细节、视觉状态，不显套路 |
| 评估 | evaluator | 按维度对照标准打分，决定达标还是回流 |

这里要看清的是分工关系。不同环节接收不同类型的能力，前四步主要接收判断标准，末端接收验收机制。Design I/O 的含义也在这里：设计能力是 Input，符合规范的界面产物是 Output，中间的链路负责把判断带到生成过程里。

如果不知道能力从哪里进、问题从哪里回流，设计师就只能在最外层改 prompt，然后等待下一次结果。把链路拆开以后，问题就可以被定位到具体环节，设计能力也有了进入系统的位置。

回到那个 Agent 可视化看板。状态色语义混乱，要回到 domain 和 design.md；任务载入前空白、失败后没有重试入口，是 spec 应该覆盖的边界条件，也应该被 evaluator 揪出来；页面结构如果偏成卡片墙，要回到 template；蓝紫渐变和大写标签带来的 AI 味，则属于 craft 要挡住的套路。

这些问题不再是一团模糊的「不太对」，而是分别落到链路上的不同接口里。

![](https://alibaba-cloud-design.github.io/vibe-designing-playbook/figures/arch-2-light.svg)

设计声明定义什么是好，执行契约规定怎么做出来。

上一节把 Design I/O 的链路拆开以后，问题随之变得具体：哪些设计能力应该进入链路，它们分别在什么位置发挥作用。

这些分类不是先验设计出来的，而是从一次次生成失败里整理出来的。

更接近实际的过程是：我们先不断撞见问题。一个 Agent 调度看板生成出来了，但失败任务没有重试入口；一个 CloudAI 页面看起来完整，却到处是蓝紫渐变和等大白卡；一个列表页能跑，但把 Badge 和 Tag 混着用；一次视觉改稿里，模型顺手写了 `#636AF1` ，绕过了 token。

当这些问题反复出现，它们就不再是单个页面的瑕疵，而是一组系统性缺口。

一类缺口在判断标准上：Agent 不知道什么样的状态、颜色、组件、动效才算对。另一类缺口在执行路径上：标准写在文档里，但 Agent 不知道什么时候该读、读完怎么用、做完怎么检查。

前者是 **设计声明** 。后者是 **执行契约** 。

声明管方向，契约管路径。

01 <svg viewBox="0 0 700 356" width="100%" role="img" aria-label="生成失败现场沉淀成声明与契约"><g><rect x="20" y="16" width="660" height="92" pathLength="1" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="0.012 0.012"></rect></g><text x="40" y="40" font-size="11" fill="currentColor" text-anchor="start" font-family="'JetBrains Mono','Chivo Mono',monospace" letter-spacing="1.1">生成失败现场</text> <g><rect pathLength="1" x="40" y="54" width="112" height="26" fill="none" stroke="currentColor" stroke-width="1"></rect><text x="96" y="71.5" font-size="12" fill="currentColor" text-anchor="middle" font-family="'PingFang SC','Noto Sans SC',sans-serif" letter-spacing="0">空态白屏</text></g> <g><rect pathLength="1" x="166" y="54" width="112" height="26" fill="none" stroke="currentColor" stroke-width="1"></rect><text x="222" y="71.5" font-size="12" fill="currentColor" text-anchor="middle" font-family="'PingFang SC','Noto Sans SC',sans-serif" letter-spacing="0">状态色乱</text></g> <g><rect pathLength="1" x="292" y="54" width="112" height="26" fill="none" stroke="currentColor" stroke-width="1"></rect><text x="348" y="71.5" font-size="12" fill="currentColor" text-anchor="middle" font-family="'PingFang SC','Noto Sans SC',sans-serif" letter-spacing="0">Badge×Tag</text></g> <g><rect pathLength="1" x="418" y="54" width="112" height="26" fill="none" stroke="currentColor" stroke-width="1"></rect><text x="474" y="71.5" font-size="12" fill="currentColor" text-anchor="middle" font-family="'PingFang SC','Noto Sans SC',sans-serif" letter-spacing="0">hardcode 色值</text></g> <g><rect pathLength="1" x="544" y="54" width="112" height="26" fill="none" stroke="currentColor" stroke-width="1"></rect><text x="600" y="71.5" font-size="12" fill="currentColor" text-anchor="middle" font-family="'PingFang SC','Noto Sans SC',sans-serif" letter-spacing="0">骨架选错</text></g> <g stroke="currentColor" stroke-width="1" fill="none" stroke-linecap="round" stroke-linejoin="round"><line pathLength="1" x1="350" y1="112" x2="350" y2="150" stroke="currentColor" stroke-opacity="0.2"></line><path pathLength="1" d="M345.5 145.5L350 150L354.5 145.5" fill="none" stroke="currentColor"></path></g><circle cx="350" cy="131" r="4" fill="currentColor"></circle><text x="366" y="136" font-size="11" fill="currentColor" text-anchor="start" font-family="'PingFang SC','Noto Sans SC',sans-serif" letter-spacing="0">沉淀成能力</text> <g><rect x="20" y="158" width="468" height="182" pathLength="1" fill="none" stroke="currentColor" stroke-width="1"></rect></g><text x="40" y="182" font-size="11" fill="currentColor" text-anchor="start" font-family="'JetBrains Mono','Chivo Mono',monospace" letter-spacing="1.1">设计声明 · 6</text> <g><rect pathLength="1" x="40" y="200" width="130" height="26" fill="none" stroke="currentColor" stroke-width="1"></rect><text x="105" y="217.5" font-size="12" fill="currentColor" text-anchor="middle" font-family="'PingFang SC','Noto Sans SC',sans-serif" letter-spacing="0">spec</text></g> <g><rect pathLength="1" x="184" y="200" width="130" height="26" fill="none" stroke="currentColor" stroke-width="1"></rect><text x="249" y="217.5" font-size="12" fill="currentColor" text-anchor="middle" font-family="'PingFang SC','Noto Sans SC',sans-serif" letter-spacing="0">domain</text></g> <g><rect pathLength="1" x="328" y="200" width="130" height="26" fill="none" stroke="currentColor" stroke-width="1"></rect><text x="393" y="217.5" font-size="12" fill="currentColor" text-anchor="middle" font-family="'PingFang SC','Noto Sans SC',sans-serif" letter-spacing="0">craft</text></g> <g><rect pathLength="1" x="40" y="254" width="130" height="26" fill="none" stroke="currentColor" stroke-width="1"></rect><text x="105" y="271.5" font-size="12" fill="currentColor" text-anchor="middle" font-family="'PingFang SC','Noto Sans SC',sans-serif" letter-spacing="0">design.md</text></g> <g><rect pathLength="1" x="184" y="254" width="130" height="26" fill="none" stroke="currentColor" stroke-width="1"></rect><text x="249" y="271.5" font-size="12" fill="currentColor" text-anchor="middle" font-family="'PingFang SC','Noto Sans SC',sans-serif" letter-spacing="0">components</text></g> <g><rect pathLength="1" x="328" y="254" width="130" height="26" fill="none" stroke="currentColor" stroke-width="1"></rect><text x="393" y="271.5" font-size="12" fill="currentColor" text-anchor="middle" font-family="'PingFang SC','Noto Sans SC',sans-serif" letter-spacing="0">template</text></g> <g><rect x="504" y="158" width="176" height="182" fill="currentColor"></rect><rect x="504" y="158" width="176" height="182" pathLength="1" fill="none" stroke="currentColor" stroke-width="1"></rect></g><text x="524" y="182" font-size="11" fill="currentColor" text-anchor="start" font-family="'JetBrains Mono','Chivo Mono',monospace" letter-spacing="1.1">执行契约 · 2</text> <g><rect x="524" y="200" width="136" height="26" fill="currentColor"></rect><rect pathLength="1" x="524" y="200" width="136" height="26" fill="none" stroke="currentColor" stroke-width="1"></rect><text x="592" y="217.5" font-size="12" fill="currentColor" text-anchor="middle" font-family="'PingFang SC','Noto Sans SC',sans-serif" letter-spacing="0">skill</text></g> <g><rect x="524" y="254" width="136" height="26" fill="currentColor"></rect><rect pathLength="1" x="524" y="254" width="136" height="26" fill="none" stroke="currentColor" stroke-width="1"></rect><text x="592" y="271.5" font-size="12" fill="currentColor" text-anchor="middle" font-family="'PingFang SC','Noto Sans SC',sans-serif" letter-spacing="0">evaluator</text></g><circle cx="660" cy="200" r="4.5" fill="currentColor"></circle><g stroke="currentColor" stroke-width="1" fill="none" stroke-linecap="round" stroke-linejoin="round"><line pathLength="1" x1="488" y1="249" x2="504" y2="249" stroke-dasharray="0.03 0.03" stroke="currentColor" stroke-opacity="0.2"></line><path pathLength="1" d="M499.5 244.5L504 249L499.5 253.5" fill="none" stroke="currentColor"></path></g><circle cx="496" cy="238" r="3.5" fill="currentColor"></circle></svg>

问题沉淀六份声明 · 两份契约

本节讨论的就是这件事：把实践里反复出现的设计判断，整理成 Agent 能读取、能执行、也能被评估的材料。

## 一、设计声明：把判断标准写下来

设计声明回答判断问题：一个体验是否成立，是否符合产品语言，是否覆盖了真实使用里的边界。它本身不生产界面，而是定义衡量界面的标准。

过去，设计产物大多交给人看：一份 Figma、一份文档、一次 handoff。开发理解它、转译它，再写成代码。到了以 Agent 为中心的协同里，这个关系变了。声明不再只是给人看的说明，它会被模型读取、引用，并影响生成结果。

这意味着，设计不再只是上游交付物。它可以和代码一起进入同一条链路，被调用、执行和验收。质量问题也随之改变：不再只是下游有没有理解到位，而是声明本身有没有把判断说清楚。

在我们的实践里，六类问题反复出现，最后对应成六份声明：

| 生成里暴露的问题 | 沉淀成的声明 | 它约束什么 |
| --- | --- | --- |
| 主流程能跑，空态、错误态、权限态消失 | `spec.md` | 功能定义、状态流、边界条件、验收标准 |
| 页面像通用 SaaS，不像云安全、数据库或控制台 | `domain.md` | 领域语义、风险编码、业务操作边界 |
| 功能完整，但一眼是 AI 模板 | `craft.md` | 排版、层级、动效、材质等通用工艺 |
| 色值、字号、圆角、动效散落在代码里 | `design.md` | token、视觉语义、状态派生、系统缺口 |
| 组件看起来像，但语义用错 | `components` | 组件可用范围和语义边界 |
| 页面骨架从零猜，场景结构走偏 | `template` | 页面骨架、app shell、场景结构起点 |

这六份声明分工不同，但都在回答同一个问题：什么算对。

### spec.md

`spec.md` 是功能定义声明，回答「这个功能在交互层面怎样才算成立」。

它的边界很清楚：只定义功能成立条件，不决定页面视觉风格、组件选型或执行路径。视觉风格交给 `craft.md` 和 `design.md` ，组件选型交给 `components` ，执行路径交给 `skill` 。

先回到上一节的 Agent 调度看板。

第一次生成时，它已经有任务列表、状态标签和趋势卡片，看起来像一个页面。但真正使用时，问题马上出现：中间区加载前是一片空白；任务失败以后只显示「失败」，没有重试入口；排队、运行中、完成、失败这些状态只是被画出来了，没有形成完整的状态流。

这类问题属于 spec 缺口。

spec 定义功能在交互层面的成立条件：为谁做，解决什么，信息怎么组织，流程怎么走，每个状态怎么表现，什么才算验收通过。

这种先写规格、再让模型实现的做法，通常被称为规格驱动开发（Spec-Driven Development，SDD）。

在 Design I/O 链路里， `spec.md` 是一个功能的事实源。规划、搭骨架、细化、评估，都应该回到同一份 spec，避免各自重新理解一遍需求。

人可以补言外之意，模型不行。没有写的状态，很可能不存在；没有写的边界，会被省略；没有写的验收标准，最后就只能凭感觉说「差不多」。

所以 spec 需要覆盖一个功能的完整定义。我们把它拆成六层：

02 <svg viewBox="0 0 700 340" width="100%" role="img" aria-label="spec 六层框架"><g stroke="currentColor" stroke-width="1" fill="none" stroke-linecap="round" stroke-linejoin="round"><line pathLength="1" x1="54" y1="44" x2="54" y2="296" stroke="currentColor" stroke-opacity="0.2"></line><path pathLength="1" d="M49.5 291.5L54 296L58.5 291.5" fill="none" stroke="currentColor"></path></g><text x="54" y="30" font-size="11" fill="currentColor" text-anchor="middle" font-family="'JetBrains Mono','Chivo Mono',monospace" letter-spacing="1.1">抽象</text> <text x="54" y="318" font-size="11" fill="currentColor" text-anchor="middle" font-family="'JetBrains Mono','Chivo Mono',monospace" letter-spacing="1.1">具体</text> <g><rect pathLength="1" x="96" y="20" width="512" height="44" fill="none" stroke="currentColor" stroke-width="1"></rect><text x="114" y="48" font-size="12" fill="currentColor" text-anchor="start" font-family="'JetBrains Mono','Chivo Mono',monospace" letter-spacing="1.1">L1</text> <text x="154" y="48" font-size="13.5" fill="currentColor" text-anchor="start" font-family="'PingFang SC','Noto Sans SC',sans-serif" letter-spacing="0">定位与意图</text> <text x="592" y="48" font-size="11.5" fill="currentColor" text-anchor="end" font-family="'PingFang SC','Noto Sans SC',sans-serif" letter-spacing="0">功能是什么、为谁做、到哪为止</text></g> <g><rect pathLength="1" x="96" y="72" width="512" height="44" fill="none" stroke="currentColor" stroke-width="1"></rect><text x="114" y="100" font-size="12" fill="currentColor" text-anchor="start" font-family="'JetBrains Mono','Chivo Mono',monospace" letter-spacing="1.1">L2</text> <text x="154" y="100" font-size="13.5" fill="currentColor" text-anchor="start" font-family="'PingFang SC','Noto Sans SC',sans-serif" letter-spacing="0">信息架构</text> <text x="592" y="100" font-size="11.5" fill="currentColor" text-anchor="end" font-family="'PingFang SC','Noto Sans SC',sans-serif" letter-spacing="0">屏幕分区，各区承载什么</text></g> <g><rect pathLength="1" x="96" y="124" width="512" height="44" fill="none" stroke="currentColor" stroke-width="1"></rect><text x="114" y="152" font-size="12" fill="currentColor" text-anchor="start" font-family="'JetBrains Mono','Chivo Mono',monospace" letter-spacing="1.1">L3</text> <text x="154" y="152" font-size="13.5" fill="currentColor" text-anchor="start" font-family="'PingFang SC','Noto Sans SC',sans-serif" letter-spacing="0">核心链路</text> <text x="592" y="152" font-size="11.5" fill="currentColor" text-anchor="end" font-family="'PingFang SC','Noto Sans SC',sans-serif" letter-spacing="0">经过哪些状态，怎么流转</text></g> <g><rect pathLength="1" x="96" y="176" width="512" height="44" fill="none" stroke="currentColor" stroke-width="1"></rect><text x="114" y="204" font-size="12" fill="currentColor" text-anchor="start" font-family="'JetBrains Mono','Chivo Mono',monospace" letter-spacing="1.1">L4</text> <text x="154" y="204" font-size="13.5" fill="currentColor" text-anchor="start" font-family="'PingFang SC','Noto Sans SC',sans-serif" letter-spacing="0">组件功能细节</text> <text x="592" y="204" font-size="11.5" fill="currentColor" text-anchor="end" font-family="'PingFang SC','Noto Sans SC',sans-serif" letter-spacing="0">每个组件各状态如何表现</text></g> <g><rect pathLength="1" x="96" y="228" width="512" height="44" fill="none" stroke="currentColor" stroke-width="1"></rect><text x="114" y="256" font-size="12" fill="currentColor" text-anchor="start" font-family="'JetBrains Mono','Chivo Mono',monospace" letter-spacing="1.1">L5</text> <text x="154" y="256" font-size="13.5" fill="currentColor" text-anchor="start" font-family="'PingFang SC','Noto Sans SC',sans-serif" letter-spacing="0">边界条件</text> <text x="592" y="256" font-size="11.5" fill="currentColor" text-anchor="end" font-family="'PingFang SC','Noto Sans SC',sans-serif" letter-spacing="0">空 / 加载 / 错误 / 权限</text></g> <g><rect x="96" y="280" width="512" height="44" fill="currentColor"></rect><rect pathLength="1" x="96" y="280" width="512" height="44" fill="none" stroke="currentColor" stroke-width="1"></rect><text x="114" y="308" font-size="12" fill="currentColor" text-anchor="start" font-family="'JetBrains Mono','Chivo Mono',monospace" letter-spacing="1.1">L6</text> <text x="154" y="308" font-size="13.5" fill="currentColor" text-anchor="start" font-family="'PingFang SC','Noto Sans SC',sans-serif" letter-spacing="0">验收标准</text> <text x="592" y="308" font-size="11.5" fill="currentColor" text-anchor="end" font-family="'PingFang SC','Noto Sans SC',sans-serif" letter-spacing="0">满足哪些条件才算做对</text></g><circle cx="608" cy="302" r="4.5" fill="currentColor"></circle><circle cx="96" cy="42" r="3.5" fill="currentColor"></circle></svg>

spec 六层自抽象 · 到具体

一份 spec 不需要写成文学化的说明，它更像一张可填写的设计表：

```markdown
# [功能名] 交互设计 Spec

## L1 定位与意图
- 一句话定义
- 目标用户
- 场景清单
- 非目标
- 行为边界：始终 / 询问后 / 永不

## L2 信息架构
- 空间区域定义
- 区域边界规则
- 内容生长规则

## L3 核心链路
- 状态清单
- 主链路
- 分支链路

## L4 组件功能细节
- 组件定位
- 功能清单
- 默认 / 悬停 / 加载 / 禁用 / 错误等状态

## L5 边界条件
- 空态
- 加载态
- 错误态
- 权限降级

## L6 验收标准
- Given / When / Then 场景验收
- 设计完成定义
```

最容易被忽略的是 L5 和 L6。模型生成界面时，往往会优先完成主流程和成功态，因为这最像一张完整截图。但真实产品里，用户更常遇到的是加载中、无数据、无权限、失败后重试这些非理想状态。

这里的加载态，spec 只负责把它纳入功能边界：什么时候进入加载、用户此时能不能操作、加载失败后如何恢复。至于用骨架屏还是 Loader、等待多久才展示反馈，是 craft 要处理的表现精度。

验收标准是后续 evaluator 的接口。评估器之所以能判断「这一版是否达标」，是因为 spec 先定义了什么叫达标。

`spec.md` 把需求从一段提示词，变成一份可以被引用、执行和核对的功能定义。

### domain.md

`domain.md` 是领域语义声明，回答「在这个业务领域里，什么数据、状态和操作才算表达正确」。

它只处理业务语义和责任判断，不替代 `craft.md` 的通用工艺，也不替代 `design.md` 的视觉事实源。同一个红色，在 domain 里回答「它代表什么风险」，在 design.md 里回答「它引用哪个 token」，在 craft.md 里回答「它出现得是否克制」。

它和 `craft.md` 正好相对：craft 处理跨业务都成立的设计功底，domain 处理只有在这个业务里才成立的判断。

这个判断来自阿里云控制台和 CloudAI 规则整理过程中的一个问题：通用模型懂「图表」「列表」「状态色」，但它不知道这些东西在云产品里承担什么责任。

以数据可视化为例，通用图表库会说「你可以设置字体」。但在阿里云控制台语境里，字体承担的是生态一致性。o-insight 这类图表规则会要求显式声明 `SF Pro Display / PingFang SC` ，避免回退到不稳定的字体。用户在不同产品间跳转时，需要感知到同一个控制台生态。

状态色也是同理。通用图表里，颜色常常只是区分系列；在云安全语境里，颜色是在编码风险。CloudAI 的规则里已经把风险等级映射到语义 token：

| 业务等级 | token |
| --- | --- |
| Urgent / High Risk | `var(--warning-high)` |
| Suspicious | `var(--warning-medium)` |
| Low Risk | `var(--warning-low)` 或 `var(--info)` |
| 未知 / 中性 | `var(--unknown)` |

这张表看起来像视觉规范，实际上是领域责任。用户在大量告警之间扫读时，颜色承担的是识别风险的责任。页面是否丰富，在这里是次要问题。

领域规则也会落到交互和数据呈现里。

关闭防护策略、批量删除资产、解除高危告警屏蔽，这类操作不可逆，且会改变安全态势。我们在 domain 里会对这一类操作进行限制：先经过二次确认，并在确认文案里写清后果。比如「关闭后，该资产将不再受 XX 防护」，就比「确定吗？」承担了更多产品责任。

AccessKey、主机 IP、账号等字段，在安全语境下是敏感信息。我们在 domain 里也会把这类字段写成数据呈现规则：默认脱敏，用户显式点击后才展示明文，并且明文查看行为需要被记录。通用设计规范不会替你做这个判断，因为它不知道这些字段在你的领域里意味着什么。

缺少 domain，Agent 很容易做出一张「换个产品也成立」的页面。它能用，但不像这个领域。更严重的是，它可能把危险操作做轻，把敏感信息做明，把本该稳定的业务语义做成一次性的视觉选择。

领域规则处理的是业务判断。

### craft.md

`craft.md` 是通用工艺声明，回答「跨业务的界面质量如何被拆成可检查的设计规则」。

它的边界是：不定义具体业务语义，也不维护视觉 token；它把跨业务复用的设计经验写成可检查的工艺规则。

它写的是不绑定具体业务的设计工艺：排版如何形成阅读节奏，层级如何分配注意力，间距和密度如何支撑信息效率，材质和动效如何承担反馈，可访问性如何守住使用底线。

这些规则不能停留在形容词层面。CloudAI skill 更像一个设计知识索引库：它把大量原本散在设计师经验里的判断，按问题层面组织起来。Agent 处理颜色时读色彩与材质规则，处理中文界面时读排版规则，处理数据图表时读图表规则，处理状态反馈时再进入加载、动效和可访问性规则。

因此，craft 更适合按层组织，避免堆成一组零散建议。

| craft 覆盖层面 | CloudAI skill 里沉淀的判断 | 解决的生成问题 |
| --- | --- | --- |
| 基调身份 | 专业、人文、独特；浅色优先；CloudAI 与 dark-minimal / warm / data-agent 的让位边界 | 不知道当前页面应该走哪种视觉气质 |
| 色彩与材质 | brand 色克制、中性灰阶层级、surface 层级、状态色、暗色模式 | 满屏强调色、玻璃态滥用、状态色没有语义 |
| 几何与空间 | 嵌套圆角、组件内距和布局间距分层、阴影档位、视觉静音 | 卡片同质、间距靠猜、层级只靠涂色 |
| 字体与排版 | 中文优先字体栈、字号档位、字重、行高、中英混排 | 默认西文字体导致中文行高、标点、字重失真 |
| 图表与数据可视化 | 官方调色板、fill 规则、图表容器、云安全图表色映射 | 图表能画但不像控制台生态，颜色不可被信任 |
| 状态与反馈 | 加载态分档、操作反馈、可恢复状态 | 等待、失败、重试这些真实使用状态处理粗糙 |
| 动效与可访问性 | 时长、缓动、只动画 transform / opacity、减少动态偏好、键盘触发动作约束 | 动效为了热闹而存在，或破坏性能和可访问性 |

这张索引表先回答「craft 管哪些地方」。下面看一个最容易被感知的切面：AI Slop。

「AI 味」不是抽象感受，它有非常具体的形状。

CloudAI 默认主题 skill 把这些痕迹列成了一张反模式表。为了避免「AI 味」停留在感受层，可以把它拆成四列：它出现在哪一层、长什么样、问题本质是什么、craft 如何挡住它。

| 层面 | AI Slop 的常见表现 | 问题本质 | craft 里的处理 |
| --- | --- | --- | --- |
| 色彩 | `from-purple-* to-blue-*` 作为起手式 | 强调色没有语义，只是在套默认高级感 | 禁用这套默认渐变，强调色只服务关键名词和主 CTA |
| 材质 | `backdrop-blur` 满地铺，普通卡片也做成玻璃 | 材质没有层级职责，只是在堆效果 | 玻璃态只留给极少数语义浮层 |
| 字体 | Inter / Roboto 起手，中文行高和标点发飘 | 默认西文体系没有照顾中文阅读 | 中文 UI 显式走 `var(--font-cn)` |
| 版式 | 一屏等大白卡、全圆角、轻阴影、emoji 图标 | 所有模块同权重，信息没有主次 | 用信息层级、留白和密度区分模块权重 |
| 动效 | bounce / elastic 弹跳、回弹、过冲 | 动效没有信息作用，只是在显得活泼 | 默认禁用，动效必须说明目的 |

这张表来自 CloudAI skill 中真实列出的反模式。把它写进 craft，是为了让 Agent 不再凭「看起来高级」这类模糊词做判断。

03 <svg viewBox="0 0 700 312" width="100%" role="img" aria-label="AI 默认套路对比 CloudAI 规则"><g><g><rect x="20" y="24" width="300" height="268" pathLength="1" fill="none" stroke="currentColor" stroke-width="1"></rect></g><rect pathLength="1" x="21" y="25" width="298" height="46" fill="none" stroke="#F8B62D" stroke-width="1" stroke-dasharray="0.014 0.014"></rect><rect x="40" y="42" width="120" height="9" fill="#F8B62D" opacity="0.5"></rect><g><rect x="40" y="92" width="44" height="7" fill="currentColor" opacity="0.4"></rect><rect pathLength="1" x="40" y="106" width="76" height="96" fill="none" stroke="currentColor" stroke-width="1"></rect></g><g><rect x="130" y="92" width="44" height="7" fill="currentColor" opacity="0.4"></rect><rect pathLength="1" x="130" y="106" width="76" height="96" fill="none" stroke="currentColor" stroke-width="1"></rect></g><g><rect x="220" y="92" width="44" height="7" fill="currentColor" opacity="0.4"></rect><rect pathLength="1" x="220" y="106" width="76" height="96" fill="none" stroke="currentColor" stroke-width="1"></rect></g><rect pathLength="1" x="40" y="232" width="96" height="28" rx="14" fill="none" stroke="#F8B62D" stroke-width="1" stroke-dasharray="0.02 0.02"></rect><text x="170" y="284" font-size="11" fill="currentColor" text-anchor="middle" font-family="'JetBrains Mono','Chivo Mono',monospace" letter-spacing="1.1">AI 默认套路</text></g> <g stroke="currentColor" stroke-width="1" fill="none" stroke-linecap="round" stroke-linejoin="round"><line pathLength="1" x1="334" y1="158" x2="366" y2="158" stroke="currentColor" stroke-opacity="0.2"></line><path pathLength="1" d="M361.5 153.5L366 158L361.5 162.5" fill="none" stroke="currentColor"></path></g><circle cx="350" cy="146" r="3.5" fill="currentColor"></circle><g><g><rect x="380" y="24" width="300" height="268" pathLength="1" fill="none" stroke="currentColor" stroke-width="1"></rect></g><rect x="381" y="25" width="298" height="46" fill="currentColor"></rect><rect x="400" y="42" width="84" height="9" fill="currentColor" opacity="0.75"></rect><g><rect pathLength="1" x="400" y="92" width="76" height="82" fill="none" stroke="currentColor" stroke-width="1"></rect><rect x="412" y="104" width="30" height="7" fill="currentColor"></rect><rect x="412" y="120" width="52" height="6" fill="currentColor" opacity="0.4"></rect></g><g><rect pathLength="1" x="490" y="92" width="76" height="82" fill="none" stroke="currentColor" stroke-width="1"></rect><rect x="502" y="108" width="52" height="6" fill="currentColor" opacity="0.4"></rect></g><g><rect pathLength="1" x="580" y="92" width="76" height="82" fill="none" stroke="currentColor" stroke-width="1"></rect><rect x="592" y="108" width="52" height="6" fill="currentColor" opacity="0.4"></rect></g><g><rect x="400" y="232" width="88" height="28" fill="currentColor"></rect><rect pathLength="1" x="400" y="232" width="88" height="28" fill="none" stroke="currentColor" stroke-width="1"></rect></g><text x="530" y="284" font-size="11" fill="currentColor" text-anchor="middle" font-family="'JetBrains Mono','Chivo Mono',monospace" letter-spacing="1.1">CLOUDAI 规则</text><circle cx="680" cy="24" r="4.5" fill="currentColor"></circle><circle cx="488" cy="246" r="3.5" fill="currentColor"></circle></g></svg>

同一张首页AI 默认套路 · CloudAI 规则

为了让 Agent 避开这些套路，craft 的规则至少要满足三点：现象可观察，执行动作明确，结果可验收。下面几条分别来自上面索引里的不同层面。

比如字体。CloudAI 明确禁止默认 `font-sans` 起手，因为 Tailwind 的默认栈容易把中文交给西文字体系统。规则要求中文界面显式走 `var(--font-cn)` ，也就是 `PingFang SC → Noto Sans SC → Microsoft YaHei` 。这条规则关心的是中文字重、标点、行高是否稳定。

比如品牌色。CloudAI 有一条很明确的规则：一屏内 brand 实色 + brand-gradient 总和不超过 3 处，其余全部走中性灰阶。这个数字用来防止每个模块都抢注意力。品牌色出现太多，重点就等于没有重点。

再比如加载态。spec 会说明这个功能有加载态，以及加载失败后该如何恢复；craft 决定的是加载在感知上怎么成立。我们后来把加载态写成分档，替代笼统的「展示 loading」：

```text
<300ms    不展示，避免闪烁
300ms–2s  骨架屏，稳定布局
>2s       Loader + 进度说明
>10s      超时提示 + 重试入口
```

这样写，是为了把等待这件事做准。等待 200ms 和等待 12s，是两种完全不同的用户心理。

最后才是动效。 `cloudai-animation` 这份 skill 是 craft 在动效层面的展开，规则被拆成 7 类、43 条，其中高优先级规则包括：UI 动画不超过 300ms、只动画 transform 和 opacity、每个动画必须有目的、抽屉使用 iOS 风格缓动、键盘触发动作不做多余动画。

`craft.md` 的价值，是把原本依赖设计师经验的判断，改写成 Agent 能读取、执行和检查的规则。

缺了 craft，页面可能功能完整、视觉也不难看，但排版、颜色、动效和状态处理会退回模型最常见的默认答案。

### design.md

`design.md` 是视觉系统声明，回答「视觉语言如何从意图、语义、取值到执行约束逐层成立」。

它的边界是：定义视觉系统怎么表达、怎么取值、怎么派生、怎么暴露缺口；不判断某个业务状态意味着什么，业务语义归 `domain.md` ；也不评判一个页面是否用得克制，使用质量归 `craft.md` 。

`design.md` 的结构可以分成三类：视觉意图、视觉值、执行约束。

视觉意图定义品牌气质、页面密度、中性色温。视觉值定义颜色、字体、圆角、间距、动效时长应该引用哪个变量。执行约束定义找不到变量时如何处理、焦点态是否可以省略、状态变体是否允许临时新造。

一份可执行的 `design.md` 通常要同时容纳两类内容：Agent 可以直接引用的取值，以及解释这些取值如何使用的文字。前者保证生成精确，后者让 Agent 知道这些值承担什么角色、在哪些场景里成立。

这三类需要分层写清。只给意图，Agent 会自由发挥；只给 token，它不知道每个值承担什么角色；只给禁止项，它能避错，但做不出稳定的视觉语言。

展开到 `design.md` 里，视觉定义可以拆成七层。

这张表里，token 只覆盖 V3 和一部分 V4。真正让视觉系统成立的，是从 V1 到 V7 的连续关系。

这七层对应三类内容：上层写意图和角色，中层写值和派生，下层写执行与缺口。这样拆，是为了避免 `design.md` 同时承担太多没有层级的责任。

V1 是视觉意图。它不能停在「高级一点」这类形容词上，至少要回答三个问题：品牌色带来的情绪是什么，页面密度应该偏紧还是偏松，中性色温该偏暖、偏冷还是保持中性。

`design.md` 可以把视觉意图写得很具体：品牌色会被转成 OKLCH，再结合色相、明度和饱和度描述视觉倾向。高饱和红色更接近热情、活力、紧迫；中高明度蓝色更接近冷静、专业；低明度、低饱和的蓝、绿、灰更接近稳重、可靠。密度也有判断依据，紧凑适合数据密集型工具，宽松更适合营销页或触摸友好场景。中性色温则决定页面底色是微暖、纯灰，还是偏冷。

语言优先级也属于这一层。CloudAI 是中文优先的产品，视觉意图需要承认中文排版的事实：默认字体、标点节奏、行高和数字混排，都不能按西文界面推导。

V2 是视觉角色。它决定一个值应该承担什么工作。 `--brand` 对应主品牌和主 CTA 的实色； `--brand-surface` 对应选中行、软徽章、引用块这类低强度强调； `--foreground-link` 专门给正文链接； `--chart-1` 到 `--chart-12` 给多系列图表； `--success` 、 `--warning-high` 、 `--info` 这些状态色用于表达结果和风险。

角色写清楚以后，Agent 就不会把所有蓝色都当成同一件事。主按钮、链接、选中背景、图表系列、信息提示都可能是蓝，但它们不能随便互换。

V3 是视觉值系统。这里包括颜色、字体、版式栅格、间距、形状、阴影、动效、层级和明暗模式。放进 `design.md` 时，这些值可以分成三类：必须按品牌填写的、可以按调性调整的、除非有强证据否则不要改的。

```text
⚠️ 必填：brand、background、foreground、primary、chart-1..12
🟡 可调：radius、font-cn / font-en、状态色
🔒 勿改：duration、ease、z-index、leading
```

这个分类很有用。它告诉 Agent 哪些值是品牌身份，哪些值是调性选择，哪些值是人因学底线。比如 `duration` 和 `ease` ，不能因为某个页面想「活泼一点」就被改成 bounce；中文行高也不能为了压缩页面而被压到难读。

V4 是派生机制。视觉系统不能只靠一堆静态值，它还要说明值之间怎么生长。

在 `design.md` 里，brand 不能只停在一个品牌色。它需要派生出 50 到 950 的色阶，再挑出 hover、active、surface、border、foreground 等角色。density 会联动 radius、space、control height。中性色温会影响 background、foreground、card、border 等一整组中性色。状态变体沿用基础 token 派生：

```text
brand hex → 50-950 色阶 → brand / hover / active / surface / border
density → radius / space / control-h
neutral temp → background / foreground / card / border
base token → hover / active / disabled / selected
```

这层是很多视觉系统容易漏掉的地方。没有派生机制，Agent 会在每个状态里重新发明一个值。今天按钮 hover 深一点，明天卡片 selected 浅一点，后天 dark mode 又换一套。短期看都能跑，长期看没有系统。

V5 是组件视觉属性、状态与响应式。组件能不能用对，后面 `components` 会讲；每个组件在视觉上如何呈现，仍然要回到 `design.md` 。背景、文字、内边距、圆角、默认态、悬停态、按下态、禁用态、选中态、加载态、错误态、焦点态，这些状态都要有视觉定义。

焦点态尤其不能省。 `design.md` 里可以明确写下 `outline: 2px solid var(--ring); outline-offset: 2px;`，并且不可降级到 `outline: none` 。这条规则服务键盘用户的位置指示。模型很容易为了“干净”删掉它，设计声明要把这条底线写死。

响应式也在这一层，但它在这里指视觉规则，不指页面骨架。断点下字号如何缩放、按钮触达面积如何保持、图片是裁切还是等比缩放、卡片间距如何收缩，都属于 `design.md` 。页面从几栏变几栏，归 `template` 。

V6 是图形、数据视觉与典型表面。图标、插画、空态图、图表，看起来像“素材”，实际也需要声明。图标线宽、圆角、填充方式，插画的材质和透视，图表的分类色、正负色、未知色，都在影响一个产品是否像同一个系统。

这层和 `domain.md` 会相遇。比如图表里的 `--chart-positive` 可以是视觉系统的一部分，但“正向”在某个业务里到底代表健康、增长、完成，还是收益，需要领域语义补上。 `design.md` 提供可用的视觉编码， `domain.md` 决定这些编码在业务里指向什么。

典型表面也应该写进这一层。modal、toast、empty state、data table cell 这类常见组合，往往会反复出现。 `design.md` 记录它们在视觉上如何取 surface、border、shadow、radius、padding、typography；至于这些表面什么时候该用，仍然归 `components` 判断。

最后是 V7，执行与缺口。这里才回到那条大家最熟的规则：所有视觉值走 `var(--*)` ，禁止裸写 hex、px、ms、cubic-bezier。

这条规则解决的是责任归属。今天写一个 `#fff` ，明天写一个 `13px` ，后天把 `200ms` 直接塞进 transition，系统就会慢慢失去单一事实源。换一次品牌色、调一次密度、修一次暗色模式，都要逐个搜索和替换。

`design.md` 的执行约束可以收成三件事：唯一范式、变体派生、遇空白报告。

```text
1. 所有视觉值走 var(--*) 引用
2. hover / active / disabled / selected 从基础 token 派生
3. 找不到 token，不硬写字面量，记录到 gaps.log
```

在这套机制里， `gaps.log` 很容易被低估。它记录的不是失败本身，而是真实的系统缺口。

```text
2026-05-06 [low] warm skill 要求的 aurora 背景 hex (#FFE4C4 等) 不在 token -- fallback: 不加 aurora，纯白 bg-background；视觉略平
2026-05-06 [med] transform scale 因子 (active:scale-0.97 / hover:scale-1.02) 无 token -- fallback: Tailwind arbitrary [0.97]，违反 design.md 执行约束 §1 但无替代
```

这两行说明， `design.md` 承认系统不会永远完整。它允许 Agent 合法地暴露缺口。

有合理替代，就采用 fallback 并记录。没有合理替代，就拒绝生成那一部分，等待补 token。比起悄悄写一个 `#FFE4C4` 或 `scale(0.97)` ，明示系统缺口更有价值，因为它会进入下一轮设计系统迭代。

这样写以后， `design.md` 就不只是 token 附录。它说明视觉方向、角色和值，也规定派生方式和缺口处理。

Agent 生成页面时，视觉选择就有了来源。

### components

`components` 是组件语义声明，回答「在这个产品语言里，哪些组件可以用，以及什么场景才算用对」。

它定义组件语义和适用场景，不决定页面骨架，也不负责调用组件。骨架归 `template` ，调用路径归 `skill` 。

它登记 shadcn 组件、自有组件，以及它们各自的使用边界。重点不是「有哪些组件」，而是「在这套产品语言里，这个组件意味着什么」。

一份 `components` 声明至少要写清四层。

| 层面    | components 要声明什么                                   | 防止的问题                                 |
| ----- | -------------------------------------------------- | ------------------------------------- |
| 组件来源  | 来自 shadcn、自有组件库，还是业务定制组件                           | Agent 自造一个看起来相似的组件                    |
| 语义角色  | 表达状态、分类、动作、容器、导航，还是反馈                              | 外观相似的组件被混用                            |
| 变体与状态 | size、variant、loading、disabled、selected、error 等可用范围 | 组件状态靠临场补，交互语法不稳定                      |
| 组合边界  | 哪些组件可以组合，哪些嵌套和替代关系禁止                               | Dialog 套 Drawer、Dropdown 承载复杂命令这类结构误用 |

这条判断也来自实践里的坑。梳理 CloudAI 组件选择时，我们发现模型常会把外观相似的组件当成同一种东西：状态用 Tag，分类用 Badge，复杂设置弹层直接 Modal，命令入口做成普通 Dropdown。页面看起来没问题，但用户会开始重新学习每个组件在这个产品里的含义。

所以 `cloudai-picker` 的 description 里，直接把几组容易选错的组件写进触发条件：Badge vs Tag、Modal vs Dialog、Tabs vs Tabs-Switch、Dropdown vs Menu vs Command。

| 组件对 | 看起来像 | 真正差别 |
| --- | --- | --- |
| Badge / Tag | 都是小标签 | Badge 更偏附着、状态、计数；Tag 更偏分类、可选、可移除 |
| Modal / Dialog / Drawer | 都是弹出层 | 打断程度、信息密度、退出方式不同 |
| Tabs / Tabs-Switch | 都能切换 | Tabs 管同空间视图切换，Tabs-Switch 管模式或口径切换 |
| Dropdown / Menu / Command | 都是浮层列表 | Dropdown 是局部选择，Menu 是动作集合，Command 是搜索式操作入口 |

例如，一个资产列表里同时有「运行中」「高危」「ECS」「生产环境」四类短文本。如果全都做成同一种 Badge，视觉上整齐，但语义被抹平了：运行中是状态，高危是风险，ECS 是资源类型，生产环境是业务分类。 `components` 要把它们拆开：状态和计数用 Badge，分类属性用 Tag，风险等级还要回到 `domain.md` 的风险语义。

这类规则可以写得很具体：

```text
asset_status: Badge
  semantic: runtime status
  allowed_values: running / stopped / pending / failed

risk_level: RiskBadge
  semantic: domain risk
  source: domain.md risk mapping

resource_type: Tag
  semantic: resource category
  removable: false

environment: Tag
  semantic: business classification
  removable: optional
```

这段声明没有规定颜色和圆角，那是 `design.md` 的工作；也没有规定高危代表什么业务后果，那是 `domain.md` 的工作。它只把组件选择的语义边界固定下来。

单个组件误用未必造成大问题。但误用积累起来，整套产品的交互语法就会变得含混。用户每次看到一个组件，都要重新猜它在这里意味着什么。

`components` 要做的，是把这些语义边界写清楚。它定义组件在产品语言里的正确用法，不承担执行契约或物料附件的角色。

### template

`template` 是页面骨架声明，回答「这个场景应该从什么结构起步」。

它提供结构起点，不替代 `spec.md` 的功能定义，不替代 `components` 的组件语义，也不自己决定何时被调用。

它不决定细节样式，也不替代组件选择；它定义的是一个场景最基本的空间关系、信息密度和 app shell。换句话说，template 管「像哪类页面」，不管「这次页面具体写什么」。

这也是实践里反复出现的问题：如果没有 template，Agent 很容易从空白页面开始猜。一个列表页可能被做成卡片墙，一个批量任务页可能没有批量操作区，一个 AI Agent 列表页可能丢掉发布状态 tabs。页面能看，但骨架已经偏了。

`cloudai-picker` 里那条「不要绕过这个 skill 凭直觉选模版」正是从这里来的。CloudAI 和 data-agent 都有同名的 `custom-agent-list.tsx` ，但结构不一样：前者偏通用 grid，后者带发布状态 tabs。文件名相同，不代表场景相同。没有 template 声明，Agent 会把「看起来像」误当成「结构对」。

一份 template 声明至少要写清四件事。

| 层面 | template 要声明什么 | 防止的问题 |
| --- | --- | --- |
| 场景 | 适用于列表、详情、设置、看板、编辑器，还是 AI Agent 管理 | 只按文件名或截图相似度套用 |
| 骨架 | app shell、主区、侧栏、操作区、状态区如何组织 | 页面从局部组件开始拼，主次关系走偏 |
| 密度 | 信息量、行高、卡片密度、操作密度的默认范围 | 列表页被做得像营销页，控制台过度留白 |
| 禁用边界 | 哪些 template 只是 sample / playground，不能用于生产 | 把视觉样本误当成可复用骨架 |

`template` 属于设计声明，因为它回答的是判断问题：这个场景应该从哪种结构开始，哪些区域必须存在，哪些结构不适合。

它是一份会被调用的声明，本身不负责调用。真正负责在链路里选择和使用 template 的，是 `skill` 。这个边界很重要：template 告诉 Agent「什么骨架可用」，skill 才决定「什么时候用哪一个」。

至此，六份设计声明合在一起，覆盖了一张界面成立所需的主要判断：交互逻辑、领域语义、通用工艺、视觉系统、组件语法、页面骨架。

这些分类来自生成失败后的沉淀。它们是把问题一次次收回来以后，留下来的判断标准。

## 二、执行契约：让声明进入链路

声明把「好」写清楚，但写清楚还不够。Agent 不会因为某份文档存在，就自动在正确的时候读取它。

要让声明真正发挥作用，还需要执行契约。

执行契约回答过程问题：在什么时机、调用什么能力、按什么方式推进、最后怎么判断是否达标。

这里真正算执行契约的，只有两份： `skill` 和 `evaluator` 。

### skill：把能力封装成可调度单元

`skill` 是调度契约，回答「声明在什么时候、以什么顺序、被怎样读进生成链路」。

它把一项能力封装成一个可以被 Agent 识别、读取和执行的单元。声明本身只负责定义标准，skill 负责把这些标准带到流程里。换句话说，skill 让声明从「文档」变成「会在正确时机出场的能力」。

它的边界是：不另起一套审美或规则，只负责在正确时机读取、组合和执行前面的声明。

抽象地讲「封装」很容易说空。直接拆一个真实的 skill 会更清楚： `cloudai-picker` 。它负责在写 CloudAI 页面之前，把「要做什么」映射到「用哪个模版、哪些组件」。它不是模版清单，而是一份调度契约。

一个 skill 通常由四层组成。

| `cloudai-picker` 里的契约层 | 解决的问题 | 调用的声明 |
| --- | --- | --- |
| 触发条件 | Agent 怎么知道该读它 | `spec.md` / `template` |
| 能力主体 | 这件事到底按什么步骤做 | `template` / `components` / `design.md` |
| 分层引用 | 细节很多时，哪些内容按需进入上下文 | `template` / `components` |
| 坑位沉淀 | 已经犯过的错怎样避免再次发生 | `craft.md` / `design.md` / `template` |

01 <svg viewBox="0 0 700 392" width="100%" role="img" aria-label="一个 skill 的四个组成部分"><line pathLength="1" x1="302" y1="90" x2="366" y2="90" stroke="currentColor" stroke-width="1" stroke-dasharray="0.05 0.05"></line><line pathLength="1" x1="302" y1="278" x2="366" y2="278" stroke="currentColor" stroke-width="1" stroke-dasharray="0.05 0.05"></line><line pathLength="1" x1="186" y1="164" x2="186" y2="204" stroke="currentColor" stroke-width="1" stroke-dasharray="0.05 0.05"></line><line pathLength="1" x1="482" y1="164" x2="482" y2="204" stroke="currentColor" stroke-width="1" stroke-dasharray="0.05 0.05"></line><g><rect pathLength="1" x="70" y="16" width="232" height="148" fill="none" stroke="currentColor" stroke-width="1"></rect><text x="186" y="42" font-size="11" fill="currentColor" text-anchor="middle" font-family="'JetBrains Mono','Chivo Mono',monospace" letter-spacing="1.2">触发时机</text></g> <g><polyline pathLength="1" points="140,98 164,98 176,78 192,116 204,98 228,98" fill="none" stroke="currentColor" stroke-width="1" stroke-linejoin="round" stroke-linecap="round"></polyline><circle cx="228" cy="98" r="4.5" fill="currentColor"></circle></g><g><rect pathLength="1" x="366" y="16" width="232" height="148" fill="none" stroke="currentColor" stroke-width="1"></rect><text x="482" y="42" font-size="11" fill="currentColor" text-anchor="middle" font-family="'JetBrains Mono','Chivo Mono',monospace" letter-spacing="1.2">判断流程</text></g> <g><line pathLength="1" x1="442" y1="98" x2="522" y2="98" stroke="currentColor" stroke-width="1"></line><circle pathLength="1" cx="442" cy="98" r="6" fill="Canvas" stroke="currentColor" stroke-width="1"></circle><circle pathLength="1" cx="482" cy="98" r="6" fill="Canvas" stroke="currentColor" stroke-width="1"></circle><circle cx="522" cy="98" r="6" fill="currentColor"></circle></g><g><rect pathLength="1" x="70" y="204" width="232" height="148" fill="none" stroke="currentColor" stroke-width="1"></rect><text x="186" y="230" font-size="11" fill="currentColor" text-anchor="middle" font-family="'JetBrains Mono','Chivo Mono',monospace" letter-spacing="1.2">按需细节</text></g> <g stroke="currentColor" stroke-width="1"><rect pathLength="1" x="152" y="268" width="46" height="40" fill="Canvas"></rect><rect pathLength="1" x="164" y="260" width="46" height="40" fill="Canvas"></rect><rect pathLength="1" x="176" y="252" width="46" height="40" fill="currentColor"></rect><line pathLength="1" x1="186" y1="262" x2="212" y2="262" stroke-width="1"></line><line pathLength="1" x1="186" y1="270" x2="212" y2="270" stroke-width="1"></line></g><g><rect pathLength="1" x="366" y="204" width="232" height="148" fill="none" stroke="currentColor" stroke-width="1"></rect><text x="482" y="230" font-size="11" fill="currentColor" text-anchor="middle" font-family="'JetBrains Mono','Chivo Mono',monospace" letter-spacing="1.2">沉淀的坑</text></g><g><g><g><circle cx="452" cy="270" r="6.5" fill="currentColor"></circle><path pathLength="1" d="M448.5 270 l2.5 2.5 l4.5 -5.5" fill="none" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"></path></g><line pathLength="1" x1="466" y1="270" x2="518" y2="270" stroke="currentColor" stroke-width="1" opacity="0.35"></line></g><g><rect pathLength="1" x="446" y="280" width="12" height="12" fill="none" stroke="currentColor" stroke-width="1"></rect><line pathLength="1" x1="466" y1="286" x2="518" y2="286" stroke="currentColor" stroke-width="1" opacity="1"></line></g><g><rect pathLength="1" x="446" y="296" width="12" height="12" fill="none" stroke="currentColor" stroke-width="1"></rect><line pathLength="1" x1="466" y1="302" x2="518" y2="302" stroke="currentColor" stroke-width="1" opacity="1"></line></g></g></svg>

skill 剖面触发 · 流程 · 细节 · 沉淀

第一层是触发条件，解决「Agent 怎么知道该用这个 skill」的问题。 `cloudai-picker` 的 description 开头就写得很直接：

> 写 CloudAI / Data Agent / AI 原生数据服务 / 阿里云相关页面之前必读。把「我要做什么」映射到具体的模版文件和组件，决定 data-skin 主题（cloudai 默认 vs data-agent），并避免易混组件选错（Badge vs Tag、Modal vs Dialog、Tabs vs Tabs-Switch、Dropdown vs Menu vs Command 等）。

这段文字本身就是触发信号。Agent 遇到「写 CloudAI 页面」「选模版」「选组件」这类任务，就知道该读这份 skill。调用时机被封装进 skill，不靠人在旁边提醒。

第二层是能力主体，解决「这件事到底怎么做」的问题。 `cloudai-picker` 把选择过程写成五步：先决定主题，是通用 CloudAI 还是 data-agent；再命中场景，从十几类场景里找到匹配项；接着做布局级决策，因为这一步错了，整个页面骨架都会偏；然后选具体组件；最后报告决策，等确认再动手。

这套流程封装的，是一组原本依赖经验的判断。「做一个工单列表页该用哪个模版」过去靠人的经验回答，现在被固化成可以重复走的步骤。每次都按同样的顺序、同样的判据来选，减少临场发挥。

第三层是分层引用，解决「细节太多怎么办」的问题。 `cloudai-picker` 的主文件不需要塞满所有细节。真正庞大的内容放在 references 里：三十个 CloudAI 模版的决策表、十二个 data-agent 模版的决策表、易混组件的对照表。Agent 走到选模版时读模版表，走到选组件时读组件表。

这已经超出单纯的工程优化。按需加载决定了信息在什么时候、以多大的量进入上下文。如果一开始就把三十多个模版、十几组组件差异全部塞进去，Agent 的注意力会被淹没。skill 在这里做的事，是控制声明进入链路的节奏。

第四层是坑位沉淀，解决「同样的错别再犯第二次」的问题。 `cloudai-picker` 末尾的「重要原则」里，有几条很具体：

> - **不要绕过这个 skill 凭直觉选模版** 。30+12 个模版很容易记错；尤其 cloudai 和 data-agent 都有 `custom-agent-list.tsx` ，但 **结构不一样** （前者偏通用 grid，后者带发布状态 tabs）。
> - **不要把模版当抄板** 。模版是骨架起点，业务字段、配色细节、内容密度都要按用户的实际需求调。
> - **不要污染 skin 体系** 。需要紫色就用 `var(--brand)` ，需要主交互色就用 `var(--primary)`,**不要 hardcode `#636AF1`** 。
> - **样本/playground 模版不要在生产里挑**:`sample-*.tsx` 系列只供视觉参考，不是可复用骨架。

这些原则来自实践里的错误，不来自概念推导。两个同名的 `custom-agent-list.tsx` 结构不一样， `#636AF1` 曾经被模型直接写进代码，sample 模版也确实容易被误当成生产骨架。写进 skill 以后，这些错误就不再只靠人的记忆兜底。

把四层放在一起，skill 就不再是一份说明。它包含触发时机、判断流程、按需引用的细节，以及沉淀下来的经验。封装做的事，是把原本躺在文档里等人去查的知识，变成一个知道何时出场、出场后怎么做、做的时候避开哪些坑的单元。

接下来才是调度。封装解决一个 skill 的内部结构，调度解决多个 skill 在链路上如何各就各位。

| 链路环节 | 典型挂载能力 | 作用 |
| --- | --- | --- |
| 规划 | `spec.md` 相关 skill | 把一句话需求展开成功能定义 |
| 搭骨架 | `variant` / `cloudai-picker` | 选择场景、模版、页面结构 |
| 填充 | 组件库与 `components` | 把骨架填成可用界面 |
| 细化 | `craft` / `cloudai-animation` | 补齐加载、反馈、动效、可访问性 |
| 评估 | `check` / `review` / evaluator | 对照声明检查结果 |

这张表里，「哪个环节用哪个能力」已经被预先安排。Agent 走到规划，spec 相关能力就该到位；走到搭骨架，选结构和选模版的 skill 接手；走到评估，评效果和评代码的能力上场。每个 skill 自己带着触发条件，链路又规定了它在哪个环节出现。两者配合以后，人就不需要在中间逐步指挥。

把这件事跟一句话走一遍，会更清楚。你说：「帮我做一个数据源的批量列表页。」

这句话进入规划环节，「列表页」「批量」触发 spec 相关能力，先定这个页面为谁做、覆盖哪些状态，包括有数据、空数据、加载中、批量选中。接着进入搭骨架， `cloudai-picker` 的触发条件命中，它把「批量列表」映射到对应场景和模版，同时避开同名但结构不同的 `custom-agent-list` 。然后是填充，组件库把真实字段放进骨架；细化阶段，craft 和动效规则补上批量选中的反馈、加载态过渡；最后到评估，evaluator 对照声明逐项核对。

整个过程里，用户只说了一句话。没有一步需要用户喊「现在该用 cloudai-picker 了」。需求内容、skill 的触发条件、链路里的调度位置，共同决定了能力何时出场。

### evaluator：把声明变成验收

`evaluator` 是验收契约，回答「做完之后如何判断产物是否符合声明」。

它把声明里的标准转成可检查的评估维度，对产物逐项打分、列问题，并把 critique 回传给下一轮生成。

它的边界是：不重新发明标准，只把声明转成检查项，并把问题回指到对应声明。

如果说 skill 守住的是入口，evaluator 守住的就是出口。skill 让声明在生成前被调用，evaluator 让声明在生成后被核对。

这个口径要和第三章保持一致。evaluator 的指标不固定。落地页是四维：设计质量、原创性、工艺、功能；控制台是五维：设计质量、可用性、信息密度、工艺、一致性。维度从场景声明里读出来，评估引擎本身不写死。

放在 1.2 里，只需要先说明 evaluator 和设计声明的关系：每一维的判据，都应该能回到一份声明。

| evaluator 检查什么 | 回到哪份声明 |
| --- | --- |
| 是否覆盖空态、加载态、错误态、权限态 | `spec.md` |
| 风险色、敏感字段、危险操作是否符合领域规则 | `domain.md` |
| 是否有蓝紫渐变、等大卡片、无意义动效 | `craft.md` |
| 是否 hardcode 色值、字号、动效时长 | `design.md` |
| Badge / Tag、Modal / Drawer 等是否误用 | `components` |
| 页面骨架是否匹配场景，是否把 template 当抄板 | `template` |

没有 evaluator，声明很容易停留在口头上：知道什么是好的，但每一版到底差在哪里，说不清，也回不去。第三章会继续讨论如何把这些标准做成可循环的评估机制。

## 为什么要分清这两类

把声明和契约分清，是为了避免两种常见误判。

第一种误判，是把所有东西都当成规范。团队写了很多文档，却没有说明这些文档什么时候被 Agent 读取、谁负责执行、怎么判断是否生效。结果是标准很多，链路里却用不上。

第二种误判，是把所有东西都当成工具。团队不断增加 skill、模版和脚本，但没有统一的判断来源。结果是执行很热闹，每一步看起来都有动作，最后产物却没有稳定的产品语言。

声明和契约要配对出现。声明给出判断，契约把判断带进过程；声明定义边界，契约让边界被执行；声明说明什么是好，契约负责让这件事发生。

回到 Design I/O 的框架里，设计声明是 Input 的内容，执行契约是 Input 进入链路的方式。两者同时存在，设计能力才会成为一套可以被调用、生成、评估、回流的系统。

<svg viewBox="0 0 700 392" width="100%" role="img" aria-label="一个 skill 的四个组成部分"><line pathLength="1" x1="302" y1="90" x2="366" y2="90" stroke="currentColor" stroke-width="1" stroke-dasharray="0.05 0.05"></line><line pathLength="1" x1="302" y1="278" x2="366" y2="278" stroke="currentColor" stroke-width="1" stroke-dasharray="0.05 0.05"></line><line pathLength="1" x1="186" y1="164" x2="186" y2="204" stroke="currentColor" stroke-width="1" stroke-dasharray="0.05 0.05"></line><line pathLength="1" x1="482" y1="164" x2="482" y2="204" stroke="currentColor" stroke-width="1" stroke-dasharray="0.05 0.05"></line><g><rect pathLength="1" x="70" y="16" width="232" height="148" fill="none" stroke="currentColor" stroke-width="1"></rect><text x="186" y="42" font-size="11" fill="currentColor" text-anchor="middle" font-family="'JetBrains Mono','Chivo Mono',monospace" letter-spacing="1.2">触发时机</text></g> <g><polyline pathLength="1" points="140,98 164,98 176,78 192,116 204,98 228,98" fill="none" stroke="currentColor" stroke-width="1" stroke-linejoin="round" stroke-linecap="round"></polyline><circle cx="228" cy="98" r="4.5" fill="currentColor"></circle></g><g><rect pathLength="1" x="366" y="16" width="232" height="148" fill="none" stroke="currentColor" stroke-width="1"></rect><text x="482" y="42" font-size="11" fill="currentColor" text-anchor="middle" font-family="'JetBrains Mono','Chivo Mono',monospace" letter-spacing="1.2">判断流程</text></g> <g><line pathLength="1" x1="442" y1="98" x2="522" y2="98" stroke="currentColor" stroke-width="1"></line><circle pathLength="1" cx="442" cy="98" r="6" fill="Canvas" stroke="currentColor" stroke-width="1"></circle><circle pathLength="1" cx="482" cy="98" r="6" fill="Canvas" stroke="currentColor" stroke-width="1"></circle><circle cx="522" cy="98" r="6" fill="currentColor"></circle></g><g><rect pathLength="1" x="70" y="204" width="232" height="148" fill="none" stroke="currentColor" stroke-width="1"></rect><text x="186" y="230" font-size="11" fill="currentColor" text-anchor="middle" font-family="'JetBrains Mono','Chivo Mono',monospace" letter-spacing="1.2">按需细节</text></g> <g stroke="currentColor" stroke-width="1"><rect pathLength="1" x="152" y="268" width="46" height="40" fill="Canvas"></rect><rect pathLength="1" x="164" y="260" width="46" height="40" fill="Canvas"></rect><rect pathLength="1" x="176" y="252" width="46" height="40" fill="currentColor"></rect><line pathLength="1" x1="186" y1="262" x2="212" y2="262" stroke-width="1"></line><line pathLength="1" x1="186" y1="270" x2="212" y2="270" stroke-width="1"></line></g><g><rect pathLength="1" x="366" y="204" width="232" height="148" fill="none" stroke="currentColor" stroke-width="1"></rect><text x="482" y="230" font-size="11" fill="currentColor" text-anchor="middle" font-family="'JetBrains Mono','Chivo Mono',monospace" letter-spacing="1.2">沉淀的坑</text></g><g><g><g><circle cx="452" cy="270" r="6.5" fill="currentColor"></circle><path pathLength="1" d="M448.5 270 l2.5 2.5 l4.5 -5.5" fill="none" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"></path></g><line pathLength="1" x1="466" y1="270" x2="518" y2="270" stroke="currentColor" stroke-width="1" opacity="0.35"></line></g><g><rect pathLength="1" x="446" y="280" width="12" height="12" fill="none" stroke="currentColor" stroke-width="1"></rect><line pathLength="1" x1="466" y1="286" x2="518" y2="286" stroke="currentColor" stroke-width="1" opacity="1"></line></g><g><rect pathLength="1" x="446" y="296" width="12" height="12" fill="none" stroke="currentColor" stroke-width="1"></rect><line pathLength="1" x1="466" y1="302" x2="518" y2="302" stroke="currentColor" stroke-width="1" opacity="1"></line></g></g></svg>

Skill 把触发时机、判断流程和经验细节封装成可调度能力。

前两节分别拆开了 Design I/O 的生成链路，并把设计能力整理成声明和契约。本节把它放回一个真实需求里：一句话如何被拆成规格、结构、组件、交互和验收，最后生成一张可交付页面。

## 理解/规划

任务从一句自然语言开始：

```prompt
帮我做一个 Agent 调度看板，能看到每个任务的实时状态。
```

这一阶段不急着画界面。真正要先做的是把模糊需求变成可执行的功能定义。 `ux-spec` skill 会根据前面定义的六层框架，补齐目标用户、状态流、边界条件和验收标准，最后产出一份 `spec.md` 。

![规划阶段：把需求定义成结构化 spec 与视觉规格](https://alibaba-cloud-design.github.io/vibe-designing-playbook/gifs/01-visual-spec.gif)

DEMO 规划阶段：把需求定义成结构化 spec 与视觉规格

如果页面的视觉方向还没有沉淀，也应该在规划阶段一起定义。否则模型会先用默认视觉补位，再把这些默认选择带进后面的结构和组件里。比较稳的做法是让 Agent 基于产品定位和页面任务，先形成这一页要遵守的视觉规格。

```prompt
基于产品定位和使用场景，探索并确定本页的视觉规格，包括视觉气质、页面密度、状态色和 token 使用规则。
```

## 信息架构设计

spec 确认后，链路进入信息架构设计：

```prompt
基于 spec 梳理这个看板的信息架构，明确页面区域、信息主次和任务流转关系。
```

这里要决定页面如何分区，主视线落在哪里，哪些信息常驻，哪些信息进入侧栏或操作区。对 Agent 调度看板来说，任务列表、状态筛选、运行概览、详情侧栏和操作入口不能随意摆放，它们共同决定用户能否快速判断系统是否正常。

![cloudai-picker 从模版库选出调度看板骨架](https://alibaba-cloud-design.github.io/vibe-designing-playbook/gifs/02-picker.gif)

DEMO cloudai-picker 从模版库选出调度看板骨架

如果页面结构还没有明确方向，可以在这一步调用 `variant` skill。它围绕同一份 spec 生成几种信息架构方案，比如「总览优先」「任务列表优先」「异常处理优先」。差异不在视觉风格，而在页面把用户注意力先交给哪里。

![variant 在画布上展开三种信息架构变体](https://alibaba-cloud-design.github.io/vibe-designing-playbook/gifs/03-variant.gif)

DEMO variant 在画布上展开三种信息架构变体

## 组件设计

结构定下来以后，进入组件设计：

```prompt
在这个页面结构里设计任务状态、任务表格、趋势图和操作入口。注意组件语义、风险状态和敏感字段处理。
```

组件阶段不是把槽位填满，而是把信息映射到正确的组件语义里。「运行中」「高危」「ECS」「生产环境」都是短文本，但它们承担的责任不同：有的是状态，有的是风险，有的是资源类型，有的是环境标记。混成同一种标签，页面看起来整齐，判断会变慢。

![组件语义分槽：状态 Badge、风险 RiskBadge、资源 Tag，敏感字段默认脱敏](https://alibaba-cloud-design.github.io/vibe-designing-playbook/gifs/06-components.gif)

DEMO 组件语义分槽：状态 Badge、风险 RiskBadge、资源 Tag，敏感字段默认脱敏

这一阶段会调用 `components` 、 `domain.md` 和 `design.md` 。 `components` 约束组件用法， `domain.md` 约束业务语义， `design.md` 保证视觉选择回到 token 和系统规则。示例附件： [components.md](https://alibaba-cloud-design.github.io/vibe-designing-playbook/attachments/05-components.md) 、 [domain.md](https://alibaba-cloud-design.github.io/vibe-designing-playbook/attachments/06-domain.md) 、 [design-md.md](https://alibaba-cloud-design.github.io/vibe-designing-playbook/attachments/04-design-md.md) 。

## 交互设计

组件成立以后，再补交互状态：

```prompt
继续补齐空态、加载态、任务失败、无权限、任务超时、批量操作中的反馈。动效只用于解释状态变化。
```

这一阶段处理的是非理想状态。主流程能跑，只说明页面能展示成功结果；真实使用里更常见的是等待、失败、权限不足、任务超时和批量操作中的不确定反馈。这些状态如果缺失，页面会在关键时刻失去可操作性。

![同一看板补齐五个非理想状态，每个都标注回到哪份声明](https://alibaba-cloud-design.github.io/vibe-designing-playbook/gifs/07-states.gif)

DEMO 同一看板补齐五个非理想状态，每个都标注回到哪份声明

这里会调用 `craft.md` 、 `cloudai-animation` 、 `spec.md` 和 `design.md` 。 `spec.md` 负责定义状态边界， `craft.md` 负责反馈质量， `cloudai-animation` 只解释状态变化， `design.md` 约束动效和视觉 token。示例附件： [craft-animation.md](https://alibaba-cloud-design.github.io/vibe-designing-playbook/attachments/07-craft-animation.md) 、 [agent-dashboard-spec.md](https://alibaba-cloud-design.github.io/vibe-designing-playbook/attachments/01-agent-dashboard-spec.md) 、 [design-md.md](https://alibaba-cloud-design.github.io/vibe-designing-playbook/attachments/04-design-md.md) 。

## 评估

页面生成后，进入验收：

```prompt
请按 evaluator 对这一版页面做检查，列出通过项、问题项和需要回流到哪份声明。
```

评估不能只写「页面还可以优化」。它必须说明问题属于哪份声明或契约：是 spec 没写清状态流，domain 没定义业务语义，craft 没挡住 AI 味，design.md 没管住 token，components 用错了语义，还是 template 选错了结构。

![evaluator 逐项检查并回流到对应声明](https://alibaba-cloud-design.github.io/vibe-designing-playbook/gifs/05b-report.gif)

DEMO evaluator 逐项检查并回流到对应声明

这里调用 `evaluator` ，产出达标报告或回流意见。示例附件： [evaluator-rubric.md](https://alibaba-cloud-design.github.io/vibe-designing-playbook/attachments/08-evaluator-rubric.md) 、 [agent-dashboard-spec.md](https://alibaba-cloud-design.github.io/vibe-designing-playbook/attachments/01-agent-dashboard-spec.md) 。

## 回流索引

如果中途不满意，不要在整张页面上反复打补丁。先判断问题属于哪一类，再回到对应声明或契约。

| 看到的问题 | 回到哪里 |
| --- | --- |
| 主流程能跑，但空态、失败、权限态缺失 | `spec.md` |
| 页面不像这个业务 | `domain.md` |
| 页面有 AI 味 | `craft.md` |
| 色值、字号、动效时长写散了 | `design.md` |
| Badge / Tag、Dialog / Drawer 混用 | `components` |
| 页面结构像卡片墙，不像看板 | `template` |
| 评估说不清哪里错 | `evaluator` |

## 走完一遍

从头到尾，用户只输入了一句话。链路实际完成了五件事：

| 步骤 | 产出 |
| --- | --- |
| 理解/规划 | 一份六层 spec |
| 信息架构设计 | 一个匹配场景的页面结构 |
| 组件设计 | 一张有真实组件和业务语义的页面 |
| 交互设计 | 一组完整的状态、反馈和动效 |
| 评估 | 一份可回流的验收结果 |

这就是 Design I/O 的基本工作方式：先把需求拆成可执行的声明和契约，再让链路按这些材料生成、检查、回流，最后变成页面。

## Demo：两条交付路线

为了更直观看到这条链路如何落地，我们准备了两个 demo。

第一个 demo 是主链路演示。它直接基于这一章讲到的声明和契约完成交付：一句需求进入， `ux-spec` 产出 spec，信息架构和 template 定页面结构，components 和 domain 填入组件与业务语义，craft 和 design.md 补齐工艺与视觉约束，最后由 evaluator 做验收。

<video src="https://alibaba-cloud-design.github.io/vibe-designing-playbook/videos/case1-main-chain.mp4" aria-label="主链路演示：一句话逐步生成可交付页面" controls=""></video>

DEMO 主链路演示：一句话逐步生成可交付页面

这条路线适合结构明确、复杂度可控的产品页面。它验证的是一件事：当声明和契约足够清楚，Agent 可以沿链路完成一版可交付原型，而不是只生成一张看起来完整的截图。

第二个 demo 是 Figma 增强链路。它不替代前面的机制，而是在设计复杂度更高的场景里补上一段专业设计工作流：Agent 先按同样的链路完成理解、规划和结构判断；当页面需要更细的视觉探索、版式推敲或细节编排时，调用 Figma MCP 继续在 Figma 里画；设计确认后，再把结果传回 IDE，写入 prototype。

02 <svg viewBox="0 0 700 220" width="100%" role="img" aria-label="Figma 增强链路"><g><g><rect pathLength="1" x="12" y="40" width="116" height="40" fill="none" stroke="currentColor" stroke-width="1"></rect><text x="70" y="64.5" font-size="12" fill="currentColor" text-anchor="middle" font-family="'PingFang SC','Noto Sans SC',sans-serif" letter-spacing="0">理解 / 规划</text></g> <g stroke="currentColor" stroke-width="1" fill="none" stroke-linecap="round" stroke-linejoin="round"><line pathLength="1" x1="130" y1="60" x2="190" y2="60" stroke="currentColor" stroke-opacity="0.2"></line><path pathLength="1" d="M185.5 55.5L190 60L185.5 64.5" fill="none" stroke="currentColor"></path></g></g><g><g><rect pathLength="1" x="192" y="40" width="116" height="40" fill="none" stroke="currentColor" stroke-width="1"></rect><text x="250" y="64.5" font-size="12" fill="currentColor" text-anchor="middle" font-family="'PingFang SC','Noto Sans SC',sans-serif" letter-spacing="0">信息架构</text></g> <g stroke="currentColor" stroke-width="1" fill="none" stroke-linecap="round" stroke-linejoin="round"><line pathLength="1" x1="310" y1="60" x2="370" y2="60" stroke="currentColor" stroke-opacity="0.2"></line><path pathLength="1" d="M365.5 55.5L370 60L365.5 64.5" fill="none" stroke="currentColor"></path></g></g><g><g><rect pathLength="1" x="372" y="40" width="116" height="40" fill="none" stroke="currentColor" stroke-width="1"></rect><text x="430" y="64.5" font-size="12" fill="currentColor" text-anchor="middle" font-family="'PingFang SC','Noto Sans SC',sans-serif" letter-spacing="0">视觉规格</text></g> <g stroke="currentColor" stroke-width="1" fill="none" stroke-linecap="round" stroke-linejoin="round"><line pathLength="1" x1="490" y1="60" x2="550" y2="60" stroke="currentColor" stroke-opacity="0.2"></line><path pathLength="1" d="M545.5 55.5L550 60L545.5 64.5" fill="none" stroke="currentColor"></path></g></g><g><g><rect pathLength="1" x="552" y="40" width="116" height="40" fill="none" stroke="currentColor" stroke-width="1"></rect><text x="610" y="64.5" font-size="12" fill="currentColor" text-anchor="middle" font-family="'PingFang SC','Noto Sans SC',sans-serif" letter-spacing="0">prototype</text></g></g> <g stroke="currentColor" stroke-width="1" fill="none" stroke-linecap="round" stroke-linejoin="round"><line pathLength="1" x1="430" y1="82" x2="430" y2="132" stroke-dasharray="0.03 0.03" stroke="currentColor" stroke-opacity="0.2"></line><path pathLength="1" d="M425.5 127.5L430 132L434.5 127.5" fill="none" stroke="currentColor"></path></g><circle cx="430" cy="82" r="4" fill="currentColor"></circle><g><rect x="360" y="132" width="140" height="44" fill="currentColor"></rect><rect pathLength="1" x="360" y="132" width="140" height="44" fill="none" stroke="currentColor" stroke-width="1"></rect><text x="430" y="158.5" font-size="12" fill="currentColor" text-anchor="middle" font-family="'PingFang SC','Noto Sans SC',sans-serif" letter-spacing="0">Figma MCP</text></g> <path pathLength="1" d="M500 154 H600 V80" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="0.03 0.03" stroke-linecap="round"></path><path pathLength="1" d="M595 90 L600 80 L605 90" fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round"></path><circle cx="600" cy="80" r="4" fill="currentColor"></circle><text x="430" y="200" font-size="10.5" fill="currentColor" text-anchor="middle" font-family="'JetBrains Mono','Chivo Mono',monospace" letter-spacing="1.1">复杂设计场景的补充能力</text></svg>

Figma 支路主链路分支 · 回写 IDE

这条路线适合设计复杂度更高的需求，比如多状态密集页面、视觉探索空间较大的页面、需要设计师在 Figma 里继续微调的页面。Figma MCP 的价值，是把原本只在 IDE 里完成的生成链路，接入一个更适合设计推敲的画布。

<video src="https://alibaba-cloud-design.github.io/vibe-designing-playbook/videos/case2-figma-branch.mp4" aria-label="Figma 增强链路演示：主链路接入 Figma MCP，确认后回写 IDE" controls=""></video>

DEMO Figma 增强链路演示：主链路接入 Figma MCP，确认后回写 IDE

两条 demo 的关系可以这样理解：

| Demo | 适用场景 | 链路特点 |
| --- | --- | --- |
| 直接交付 | 结构明确、组件和视觉规则已有沉淀 | 从声明与契约直接生成 prototype |
| Figma 增强 | 视觉复杂度高、需要继续设计推敲 | 在主链路上接入 Figma MCP，再回写 IDE |

Figma 不是这套能力成立的前提。它是在需求复杂到需要更强设计画布时，对主链路的补充。

## 小结：第一章到这里

回头看整章，第一章走了三步。

1. [1.1](https://alibaba-cloud-design.github.io/vibe-designing-playbook/1.1-%E8%B0%83%E5%BA%A6%E6%9C%BA%E5%88%B6.md) 先打开生成过程的黑盒，看清从需求到原型中间有一条可注入能力的链路。
2. [1.2](https://alibaba-cloud-design.github.io/vibe-designing-playbook/1.2-%E5%A3%B0%E6%98%8E%E4%B8%8E%E5%A5%91%E7%BA%A6.md) 再把要注入的能力拆成六份设计声明和两份执行契约，说明每一份在约束什么、如何进入链路。
3. 这一节用一个真实需求，把这套机制从头到尾跑了一遍。

走完这三步，Agent 具备了一件事的能力：它不只是接收一句 prompt，而是沿着设计师定义的判断标准和执行路径工作。

002 · 04 sections

上一章解决的是「能力如何进入 Agent」。当设计声明、执行契约和 skill 被放进链路之后，Agent 开始具备产出规范界面的能力。

在过去数年间，体验设计很大一部分工作，是在帮用户把目标转成系统操作。设计师理解用户想完成什么，抽象典型场景，再把路径落实为导航、表单、按钮和反馈。

这套工作仍然有效。一个好的导航、一张合理的表单、一次清楚的状态反馈，都在帮助用户把目标翻译成操作。

但大量复杂系统也提醒我们：即使界面已经被认真设计，用户仍然可能停在目标面前，不知道下一步该点哪里、填什么、先看哪组信息。用户不是没有目标，而是不知道如何把目标转成系统动作。这就是执行鸿沟。

随着 Agent 技术逐渐成熟，新的交互形态开始出现。用户不必先理解完整的页面结构，再把目标拆成一串操作；用户可以先表达意图，由 Agent 理解目标、补齐上下文、推进任务，再把过程和结果交给用户判断。

> UX made complex systems usable by improving the journeys people navigate. AX removes the journey altogether, teleporting people directly to their goals.
> 
> —— John Maeda, [Design in Tech Report](https://designintech.report/)

当 Agent 开始代表用户行动，设计重点就不再只是帮助用户完成操作，还要帮助用户判断系统是否做对。基于此，意图驱动成为新的起点，并形成了新的 Agent Experience Loop：用户表达意图，Agent 推进任务，界面承接协作，结果再回到用户的判断和控制中。

![Agent Experience Loop 示意图](https://alibaba-cloud-design.github.io/vibe-designing-playbook/figures/fig-2-1-light.svg)

2-1 Agent Experience Loop 示意图

它不是一次输入和一次输出，也不是把聊天框放在产品入口。它强调的是运行时的持续往返：目标如何被澄清，上下文如何被补齐，关键节点如何被确认，结果如何被评估或修正。

这也带来另一类问题。执行鸿沟被压缩之后，评估鸿沟会变得更突出。用户没有亲手完成每一步，因此更需要知道 Agent 做了什么、为什么这样做、哪里不确定，以及出错时能否撤销或修正。

UX 与 AX 不是替代关系。稳定的仪表盘、固定的设置页、重复发生的审批流，仍然适合被预先设计成页面。Agent Experience Loop 更适合那些带有上下文、下一步依赖数据或推理、用户不一定知道准确操作路径，但仍然需要对结果负责的任务。

在 Agent Experience Loop 里，信息呈现的过程透明度并非越高越好。Agent 在规划、执行和总结中会产生大量中间信息，如果把所有执行细节平铺给用户，透明度本身就会变成新的信息负担。更合适的方式，是根据任务阶段、风险等级和用户决策需要，动态调节界面暴露的信息层级。

![Agent 过程透明度分层。来源：Exploring the Impact of Process Transparency on User Experience in AI Design Agents, ACM CSCW 2025.](https://alibaba-cloud-design.github.io/vibe-designing-playbook/figures/fig-2-2-light-16x9.png)

2-2 Agent 过程透明度分层。来源：Exploring the Impact of Process Transparency on User Experience in AI Design Agents, ACM CSCW 2025.

设计 AX 相关体验前，可以先检查几个问题：

- 用户想完成的目标是什么，而不只是他说了什么？
- 这次表达里哪些信息已经明确，哪些信息还需要澄清？
- Agent 可以自动完成哪些步骤，哪些步骤必须等待用户确认？
- 当前阶段需要展示到哪一层透明度，哪些细节应该按需展开？
- 哪些证据、引用或状态能帮助用户判断结果是否可信？
- 如果结果出错，用户能否撤销、改写或回到上一步？

一个可用的意图入口通常不只接收一句自然语言。它还需要承接对象、时间、文件、历史上下文和权限约束，把模糊表达转成 Agent 可以继续推理的任务上下文。

当意图驱动成为起点，界面就不再只是预先设计好的页面集合。它也会成为一种运行时回应：Agent 用它暴露理解、询问缺失信息、呈现风险、提供证据，并返回与任务匹配的结果。

<svg viewBox="0 0 700 236" width="100%" role="img" aria-label="Agent Experience Loop 流转图"><g><rect x="30" y="28" width="640" height="166" rx="0" fill="transparent" stroke="currentColor"></rect><text x="44" y="48" font-size="10" fill="currentColor" text-anchor="start" font-family="'JetBrains Mono','Chivo Mono',monospace" letter-spacing="1.2" style="text-transform: uppercase;">INTENT FLOW</text></g> <g><circle cx="76" cy="112" r="3.5" fill="currentColor" stroke="currentColor" stroke-width="1.2"></circle><line x1="38" y1="112" x2="68" y2="112" stroke="transparent" stroke-dasharray="2 5"></line><line x1="84" y1="112" x2="114" y2="112" stroke="currentColor" stroke-dasharray="2 5"></line><text x="76" y="86" font-size="11" fill="currentColor" text-anchor="middle" font-family="'PingFang SC','Noto Sans SC',sans-serif">表达目标</text> <text x="76" y="148" font-size="9" fill="currentColor" text-anchor="middle" font-family="'JetBrains Mono','Chivo Mono',monospace" letter-spacing="1.2" style="text-transform: uppercase;">01</text></g> <g><circle cx="184" cy="112" r="3.5" fill="Canvas" stroke="currentColor" stroke-width="1.2"></circle><line x1="146" y1="112" x2="176" y2="112" stroke="currentColor" stroke-dasharray="2 5"></line><line x1="192" y1="112" x2="222" y2="112" stroke="currentColor" stroke-dasharray="2 5"></line><text x="184" y="86" font-size="11" fill="currentColor" text-anchor="middle" font-family="'PingFang SC','Noto Sans SC',sans-serif">补齐上下文</text> <text x="184" y="148" font-size="9" fill="currentColor" text-anchor="middle" font-family="'JetBrains Mono','Chivo Mono',monospace" letter-spacing="1.2" style="text-transform: uppercase;">02</text></g> <g><circle cx="292" cy="112" r="3.5" fill="Canvas" stroke="currentColor" stroke-width="1.2"></circle><line x1="254" y1="112" x2="284" y2="112" stroke="currentColor" stroke-dasharray="2 5"></line><line x1="300" y1="112" x2="330" y2="112" stroke="currentColor" stroke-dasharray="2 5"></line><text x="292" y="86" font-size="11" fill="currentColor" text-anchor="middle" font-family="'PingFang SC','Noto Sans SC',sans-serif">过程协作</text> <text x="292" y="148" font-size="9" fill="currentColor" text-anchor="middle" font-family="'JetBrains Mono','Chivo Mono',monospace" letter-spacing="1.2" style="text-transform: uppercase;">03</text></g> <g><circle cx="400" cy="112" r="3.5" fill="Canvas" stroke="currentColor" stroke-width="1.2"></circle><line x1="362" y1="112" x2="392" y2="112" stroke="currentColor" stroke-dasharray="2 5"></line><line x1="408" y1="112" x2="438" y2="112" stroke="currentColor" stroke-dasharray="2 5"></line><text x="400" y="86" font-size="11" fill="currentColor" text-anchor="middle" font-family="'PingFang SC','Noto Sans SC',sans-serif">证据呈现</text> <text x="400" y="148" font-size="9" fill="currentColor" text-anchor="middle" font-family="'JetBrains Mono','Chivo Mono',monospace" letter-spacing="1.2" style="text-transform: uppercase;">04</text></g> <g><circle cx="508" cy="112" r="3.5" fill="Canvas" stroke="currentColor" stroke-width="1.2"></circle><line x1="470" y1="112" x2="500" y2="112" stroke="currentColor" stroke-dasharray="2 5"></line><line x1="516" y1="112" x2="546" y2="112" stroke="currentColor" stroke-dasharray="2 5"></line><text x="508" y="86" font-size="11" fill="currentColor" text-anchor="middle" font-family="'PingFang SC','Noto Sans SC',sans-serif">结果评估</text> <text x="508" y="148" font-size="9" fill="currentColor" text-anchor="middle" font-family="'JetBrains Mono','Chivo Mono',monospace" letter-spacing="1.2" style="text-transform: uppercase;">05</text></g> <g><circle cx="616" cy="112" r="3.5" fill="currentColor" stroke="currentColor" stroke-width="1.2"></circle><line x1="578" y1="112" x2="608" y2="112" stroke="currentColor" stroke-dasharray="2 5"></line><line x1="624" y1="112" x2="654" y2="112" stroke="transparent" stroke-dasharray="2 5"></line><text x="616" y="86" font-size="11" fill="currentColor" text-anchor="middle" font-family="'PingFang SC','Noto Sans SC',sans-serif">修正方向</text> <text x="616" y="148" font-size="9" fill="currentColor" text-anchor="middle" font-family="'JetBrains Mono','Chivo Mono',monospace" letter-spacing="1.2" style="text-transform: uppercase;">06</text></g> <path d="M614 132 C548 206 154 206 86 132" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="2 6"></path><path d="M92 132 l-9 1 5 8" fill="none" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"></path><text x="350" y="210" font-size="10" fill="currentColor" text-anchor="middle" font-family="'JetBrains Mono','Chivo Mono',monospace" letter-spacing="1.2" style="text-transform: uppercase;">CONTINUOUS FEEDBACK</text></svg>

2-3Agent Experience Loop 流转图

上一节把动态交互的起点放在执行鸿沟和评估鸿沟上。用户先表达意图，Agent 进入体验循环，系统再判断下一步应该如何回应。问题由此转向界面本身：当回应发生在运行时，界面就不再只是预先设计好的页面。

GenUI，也就是 Generative UI，描述的正是这层新的界面形态。它不是让模型随意生成页面，而是让界面参与 Agent 系统的运行：根据用户意图、应用上下文和任务状态，动态组织屏幕上应该出现的内容、结构和判断点。

GenUI 不是生成“页面”，而是定义设计规则，将数据、上下文和组件编排成体验。它不把界面完全交给模型自由发挥，而是在设计系统、组件目录、业务规则和运行时上下文之间建立新的组织方式。

![GenUI 结构图](https://alibaba-cloud-design.github.io/vibe-designing-playbook/figures/fig-2-4-light.gif)

2-4 GenUI 结构图

> GenUI is the New Interface.
> 
> 从固定流程到动态交互，体验随意图被实时组织。

GenUI 可以出现在不同位置：对话流、工作区、原生界面，或一份生成后的结果产物。位置不同，判断标准一致：它能否在运行时把任务状态转成可理解、可操作、可评估的界面。

GenUI 的边界需要被清楚定义。如果只把它理解成“生成一个页面”，它很容易滑向开放式生成：页面每次都不一样，组件和规则难以校验，体验也难以保持一致。更稳妥的边界是：只在任务路径、判断依据或用户决策点会变化的地方引入 GenUI。

稳定页面仍然重要。仪表盘、设置页、固定审批流、长期存在的信息架构，不需要为了“生成”而被重新生成。更适合被动态组织的，是体验循环中的变化部分：用户刚表达完意图时需要补齐什么信息，Agent 推进到中间节点时需要用户做什么判断，结果出来后应该以什么形式让用户评估、纠错和继续行动。

判断 GenUI 是否合适，可以先看两个维度：表达自由度和产品控制权。

表达自由度决定了界面可以承接多复杂的内容。自由度低，Agent 只能选择预设组件，一致性更好，但覆盖范围有限；自由度高，Agent 可以组织更开放的界面，适应性更强，但安全、性能和品牌一致性都会变难。产品控制权关注的是最终界面由谁决定：前端和设计系统预先定义多少，Agent 又能在运行时选择多少。

因此，GenUI 并不是越自由越好。面向真实产品时，更可靠的路径通常是受控生成：Agent 输出结构化意图或界面描述，客户端再用组件目录、渲染规则和交互约束来组织界面。这样既保留了运行时组织体验的能力，也让产品继续控制视觉质量、交互边界和安全风险。

在产品里引入 GenUI 前，团队可以先判断几个问题：

- 任务路径或结果结构是否会随上下文变化？
- 用户是否需要在过程中判断、确认或修正？
- 结构化界面是否比长文本更容易帮助用户理解和行动？
- 这类界面能否被组件目录和规则约束？
![GenUI 决策树](https://alibaba-cloud-design.github.io/vibe-designing-playbook/figures/fig-2-5-light.svg)

2-5 GenUI 决策树

本章后面会先单独展开 A2UI，说明对话 Loop 中即用即消的动态界面如何声明、如何渲染；再回到一条完整案例，看 OmniBox、FlexCard 和 GenReport 如何分别承接意图表达、过程协作和结果评估。

GenUI 追求的不是无限自由，而是有边界的灵活性。好的 GenUI 系统让 Agent 适配意图，也让产品继续控制质量、安全和一致性。

A2UI 是 GenUI 的一种实现机制，即 Agent to UI。它描述的是对话 Loop 中的动态界面机制：Agent 用结构化方式声明界面意图，客户端再用受控组件、设计系统和交互规则完成渲染。它不是让模型自由编写 HTML、CSS 或任意组件代码，而是让界面按任务状态动态出现，并在用户完成判断后回到上下文里。

这套机制可以理解为 Agent 和客户端之间的契约。Agent 描述需要展示什么、涉及哪些数据、用户可以采取什么动作、Agent 是否需要等待；客户端则用自己的组件库、设计 token、无障碍规则和交互模式来渲染这份描述。契约的价值在于把“要表达什么”和“如何渲染”分开，让 Agent 参与界面组织，但不直接接管界面实现。

契约的作用，是定义边界。

在 CloudAI 里，这份契约通常会调动四类资源：

- **业务数据** ：指标、表字段、实例状态、SQL 计划、生成资产或报告内容。
- **工作流** ：任务状态、下一步可执行动作，以及 Agent 是否需要暂停。
- **组件** ：客户端允许渲染的 UI 模板。
- **交互规则** ：决策策略、超时策略、校验、风险确认和动作分发。
<svg viewBox="0 0 700 250" width="100%" role="img" aria-label="A2UI 契约分层"><g><rect x="42" y="36" width="616" height="150" rx="0" fill="transparent" stroke="currentColor"></rect><text x="56" y="56" font-size="10" fill="currentColor" text-anchor="start" font-family="'JetBrains Mono','Chivo Mono',monospace" letter-spacing="1.2" style="text-transform: uppercase;">A2UI CONTRACT</text></g> <g><rect x="82" y="86" width="112" height="54" rx="0" fill="Canvas" stroke="currentColor"></rect><text x="138" y="116" font-size="12" fill="currentColor" text-anchor="middle" font-family="'PingFang SC','Noto Sans SC',sans-serif">Agent 可声明</text> <g stroke="currentColor" stroke-width="1.4" fill="none" stroke-linecap="round" stroke-linejoin="round"><line x1="198" y1="113" x2="228" y2="113"></line><path d="M223 108L228 113L223 118"></path></g></g><g><rect x="234" y="86" width="112" height="54" rx="0" fill="currentColor" stroke="currentColor"></rect><text x="290" y="116" font-size="12" fill="currentColor" text-anchor="middle" font-family="'PingFang SC','Noto Sans SC',sans-serif">结构化 UI 描述</text> <g stroke="currentColor" stroke-width="1.4" fill="none" stroke-linecap="round" stroke-linejoin="round"><line x1="350" y1="113" x2="380" y2="113"></line><path d="M375 108L380 113L375 118"></path></g></g><g><rect x="386" y="86" width="112" height="54" rx="0" fill="Canvas" stroke="currentColor"></rect><text x="442" y="116" font-size="12" fill="currentColor" text-anchor="middle" font-family="'PingFang SC','Noto Sans SC',sans-serif">客户端约束</text> <g stroke="currentColor" stroke-width="1.4" fill="none" stroke-linecap="round" stroke-linejoin="round"><line x1="502" y1="113" x2="532" y2="113"></line><path d="M527 108L532 113L527 118"></path></g></g><g><rect x="538" y="86" width="112" height="54" rx="0" fill="Canvas" stroke="currentColor"></rect><text x="594" y="116" font-size="12" fill="currentColor" text-anchor="middle" font-family="'PingFang SC','Noto Sans SC',sans-serif">用户界面</text></g> <text x="140" y="166" font-size="9" fill="currentColor" text-anchor="middle" font-family="'JetBrains Mono','Chivo Mono',monospace" letter-spacing="1.2" style="text-transform: uppercase;">INTENT / DATA / ACTION</text> <text x="292" y="166" font-size="9" fill="currentColor" text-anchor="middle" font-family="'JetBrains Mono','Chivo Mono',monospace" letter-spacing="1.2" style="text-transform: uppercase;">CONTRACT</text> <text x="444" y="166" font-size="9" fill="currentColor" text-anchor="middle" font-family="'JetBrains Mono','Chivo Mono',monospace" letter-spacing="1.2" style="text-transform: uppercase;">TOKEN / A11Y / FALLBACK</text> <text x="596" y="166" font-size="9" fill="currentColor" text-anchor="middle" font-family="'JetBrains Mono','Chivo Mono',monospace" letter-spacing="1.2" style="text-transform: uppercase;">FLEXCARD</text></svg>

2-6A2UI 契约分层

这种分工决定了 A2UI 的边界。如果 Agent 直接生成开放式 UI，结果可能出现视觉不一致、难以校验、渲染缓慢或安全风险。如果 Agent 只返回文本，用户又很难获得做决策所需的结构。A2UI 位于两者之间：Agent 发送结构化 UI 描述，客户端在可控系统里完成渲染。

<svg viewBox="0 0 700 360" width="100%" role="img" aria-label="A2UI 运行机制"><g><rect x="48" y="70" width="604" height="176" rx="0" fill="transparent" stroke="currentColor"></rect><text x="62" y="90" font-size="10" fill="currentColor" text-anchor="start" font-family="'JetBrains Mono','Chivo Mono',monospace" letter-spacing="1.2" style="text-transform: uppercase;">A2UI RENDERER</text></g> <rect x="252" y="24" width="196" height="42" fill="transparent" stroke="currentColor"></rect><text x="350" y="51" font-size="15" fill="currentColor" text-anchor="middle" font-family="'PingFang SC','Noto Sans SC',sans-serif">用户 / USER</text> <g stroke="currentColor" stroke-width="1.4" fill="none" stroke-linecap="round" stroke-linejoin="round"><line x1="350" y1="66" x2="350" y2="106" stroke-dasharray="2 5"></line><path d="M345 101L350 106L355 101"></path></g><text x="382" y="96" font-size="9" fill="currentColor" text-anchor="middle" font-family="'JetBrains Mono','Chivo Mono',monospace" letter-spacing="1.2" style="text-transform: uppercase;">INTENT</text> <rect x="102" y="132" width="156" height="62" fill="Canvas" stroke="currentColor"></rect><text x="180" y="158" font-size="13" fill="currentColor" text-anchor="middle" font-family="'PingFang SC','Noto Sans SC',sans-serif">Agent</text> <text x="180" y="178" font-size="9" fill="currentColor" text-anchor="middle" font-family="'JetBrains Mono','Chivo Mono',monospace" letter-spacing="1.2" style="text-transform: uppercase;">DECLARE UI</text> <rect x="282" y="132" width="136" height="62" fill="currentColor" stroke="currentColor"></rect><text x="350" y="157" font-size="13" fill="currentColor" text-anchor="middle" font-family="'PingFang SC','Noto Sans SC',sans-serif">A2UI 契约</text> <text x="350" y="178" font-size="9" fill="currentColor" text-anchor="middle" font-family="'JetBrains Mono','Chivo Mono',monospace" letter-spacing="1.2" style="text-transform: uppercase;">DECLARE · ACT</text> <rect x="442" y="132" width="156" height="62" fill="Canvas" stroke="currentColor"></rect><text x="520" y="158" font-size="13" fill="currentColor" text-anchor="middle" font-family="'PingFang SC','Noto Sans SC',sans-serif">客户端 UI</text> <text x="520" y="178" font-size="9" fill="currentColor" text-anchor="middle" font-family="'JetBrains Mono','Chivo Mono',monospace" letter-spacing="1.2" style="text-transform: uppercase;">RENDER CARD</text> <g stroke="currentColor" stroke-width="1.4" fill="none" stroke-linecap="round" stroke-linejoin="round"><line x1="258" y1="163" x2="282" y2="163"></line><path d="M277 158L282 163L277 168"></path></g><g stroke="currentColor" stroke-width="1.4" fill="none" stroke-linecap="round" stroke-linejoin="round"><line x1="418" y1="163" x2="442" y2="163"></line><path d="M437 158L442 163L437 168"></path></g><path d="M520 194 V222 H180 V194" fill="none" stroke="currentColor" stroke-width="1.15" stroke-dasharray="2 6"></path><path d="M185 201 L180 194 L175 201" fill="none" stroke="currentColor" stroke-width="1.15" stroke-linecap="round" stroke-linejoin="round"></path><text x="350" y="222" font-size="9" fill="currentColor" text-anchor="middle" font-family="'JetBrains Mono','Chivo Mono',monospace" letter-spacing="1.2" style="text-transform: uppercase;">RETURN USER ACTION</text> <line x1="350" y1="246" x2="350" y2="272" stroke="currentColor"></line><rect x="100" y="272" width="142" height="44" fill="transparent" stroke="currentColor"></rect><rect x="268" y="272" width="164" height="44" fill="transparent" stroke="currentColor"></rect><rect x="458" y="272" width="142" height="44" fill="transparent" stroke="currentColor"></rect><text x="171" y="299" font-size="12" fill="currentColor" text-anchor="middle" font-family="'PingFang SC','Noto Sans SC',sans-serif">数据 / DATA</text> <text x="350" y="299" font-size="11.2" fill="currentColor" text-anchor="middle" font-family="'PingFang SC','Noto Sans SC',sans-serif">组件 / COMPONENTS</text> <text x="529" y="299" font-size="12" fill="currentColor" text-anchor="middle" font-family="'PingFang SC','Noto Sans SC',sans-serif">规则 / SCHEMA</text> <text x="350" y="344" font-size="10" fill="currentColor" text-anchor="middle" font-family="'JetBrains Mono','Chivo Mono',monospace" letter-spacing="1.2" style="text-transform: uppercase;">STRUCTURED UI DESCRIPTION</text></svg>

2-7A2UI 运行机制

在 CloudAI 里，FlexCard 是这套机制的一个具体落地。它不要求 Agent 描述视觉细节，而是让 Agent 描述意图、内容、动作和行为约束。渲染层再把这些描述映射到组件、token、无障碍规则和降级状态里。这样，Agent 可以表达“需要用户确认什么”，但按钮、卡片、状态提示仍由产品自己的界面系统决定。

下面是一段简化后的 A2UI 消息示意。它不是完整规范，只是用来说明 Agent 发给客户端的内容大致包含什么：

```json
{
  "intent": "confirm",
  "status": "pending",
  "title": "确认是否继续分析",
  "context": {
    "object": "业务对象 / object-id",
    "time_range": "最近 24 小时",
    "finding": "发现 3 个需要用户判断的异常项"
  },
  "content": {
    "type": "options",
    "items": [
      { "id": "item_1", "label": "选项 A", "description": "影响范围最高 / 建议优先分析" },
      { "id": "item_2", "label": "选项 B", "description": "调用次数上升 / 需要继续观察" }
    ]
  },
  "actions": [
    { "id": "analyze_selected", "label": "分析选中项", "primary": true },
    { "id": "view_all", "label": "查看全部" }
  ],
  "behavior": {
    "requires_user_decision": true,
    "blocks_agent_execution": true
  }
}
```

这段结构里的重点不是字段命名，而是分工方式。Agent 不决定按钮长什么样、卡片用什么颜色、图表如何排版；它只说明当前任务状态、需要展示的数据、用户可以采取的动作，以及动作是否会阻塞后续执行。客户端据此选择组件，并把它渲染成符合产品设计系统的界面。字段可以随实现变化，但这条分工需要保持稳定。

![A2UI 消息到 FlexCard 的渲染示意](https://alibaba-cloud-design.github.io/vibe-designing-playbook/figures/fig-2-8-light.png)

2-8 A2UI 消息到 FlexCard 的渲染示意

当用户点击按钮、选择选项或提交表单时，客户端不只是更新界面。它会带着相关上下文把用户动作传回 Agent。下一段 UI 可能是继续执行、二次确认、结果展示，也可能是一份报告。A2UI 的价值正在这里：它让界面不只展示结果，也把用户判断重新写回任务上下文。

前面三节分别讨论了 Agent Experience Loop、GenUI 和 A2UI。放回一条真实任务链路里，它们对应的是同一件事的不同层次：用户表达意图，Agent 推进任务，界面在关键节点承接协作，最后把结果交还给用户判断。

在一个典型的 Agentic 云产品链路中，这套体验可以被压缩成三段：OmniBox 承接意图表达，FlexCard 承接过程协作，GenReport 承接结果评估。OmniBox 让任务进入系统，FlexCard 让用户参与中间判断，GenReport 把一次分析沉淀成可阅读、可分享、可继续操作的产物。

<svg viewBox="0 0 700 220" width="100%" role="img" aria-label="OmniBox FlexCard GenReport 任务链路"><g><rect x="28" y="42" width="644" height="112" rx="0" fill="transparent" stroke="currentColor"></rect><text x="42" y="62" font-size="10" fill="currentColor" text-anchor="start" font-family="'JetBrains Mono','Chivo Mono',monospace" letter-spacing="1.2" style="text-transform: uppercase;">AGENTIC PRODUCT FLOW</text></g> <g><circle cx="110" cy="98" r="3.5" fill="currentColor" stroke="currentColor" stroke-width="1.2"></circle><text x="110" y="78" font-size="13" fill="currentColor" text-anchor="middle" font-family="'JetBrains Mono','Chivo Mono',monospace">OmniBox</text> <text x="110" y="128" font-size="11" fill="currentColor" text-anchor="middle" font-family="'PingFang SC','Noto Sans SC',sans-serif">意图表达</text> <line x1="122" y1="98" x2="258" y2="98" stroke="currentColor" stroke-dasharray="2 6"></line></g><g><circle cx="270" cy="98" r="3.5" fill="Canvas" stroke="currentColor" stroke-width="1.2"></circle><text x="270" y="78" font-size="13" fill="currentColor" text-anchor="middle" font-family="'JetBrains Mono','Chivo Mono',monospace">Agent</text> <text x="270" y="128" font-size="11" fill="currentColor" text-anchor="middle" font-family="'PingFang SC','Noto Sans SC',sans-serif">理解并推进</text> <line x1="282" y1="98" x2="418" y2="98" stroke="currentColor" stroke-dasharray="2 6"></line></g><g><circle cx="430" cy="98" r="3.5" fill="Canvas" stroke="currentColor" stroke-width="1.2"></circle><text x="430" y="78" font-size="13" fill="currentColor" text-anchor="middle" font-family="'JetBrains Mono','Chivo Mono',monospace">FlexCard</text> <text x="430" y="128" font-size="11" fill="currentColor" text-anchor="middle" font-family="'PingFang SC','Noto Sans SC',sans-serif">过程协作</text> <line x1="442" y1="98" x2="578" y2="98" stroke="currentColor" stroke-dasharray="2 6"></line></g><g><circle cx="590" cy="98" r="3.5" fill="currentColor" stroke="currentColor" stroke-width="1.2"></circle><text x="590" y="78" font-size="13" fill="currentColor" text-anchor="middle" font-family="'JetBrains Mono','Chivo Mono',monospace">GenReport</text> <text x="590" y="128" font-size="11" fill="currentColor" text-anchor="middle" font-family="'PingFang SC','Noto Sans SC',sans-serif">结果评估</text></g> <path d="M430 154 C388 190 310 190 270 154" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="2 5"></path><text x="350" y="198" font-size="10" fill="currentColor" text-anchor="middle" font-family="'JetBrains Mono','Chivo Mono',monospace" letter-spacing="1.2" style="text-transform: uppercase;">USER DECISION RETURNS TO AGENT CONTEXT</text></svg>

2-9OmniBox、FlexCard 与 GenReport 的任务链路

下面用一个经营数据分析场景介绍三者具体如何呈现。场景中的用户意图，是基于海外业务月度数据生成一份运营分析报告，指导下一步的行动。

## 用 OmniBox 承接意图

任务通常从一句自然语言目标开始：

> 帮我基于海外业务 3 月数据生成一份运营月报，重点分析产业、品牌、门店和产品的销售表现，并标出需要关注的风险。

这句话里已经有目标、对象、时间范围和分析方向，但还不是一条完整的可执行任务。OmniBox 将自然语言、数据范围、知识库、指标对象和历史上下文放在同一个入口里，让 Agent 拿到足够明确的任务上下文。

在这一层，OmniBox 要处理的是意图结构化：用户用自然语言描述分析目标，同时选择数据范围并关联知识库。数据口径由知识库提供约束，系统需要识别任务对象、分析维度、时间范围、权限边界和可能的业务线索，并把它们转成 Agent 可以继续推理的上下文。

![OmniBox 输入结构图](https://alibaba-cloud-design.github.io/vibe-designing-playbook/figures/fig-2-10-omnibox.gif)

2-10 OmniBox 输入结构图

## 用 FlexCard 承接过程协作

Agent 推进数据分析时，经常会遇到需要用户参与的节点。比如分析方向不明确时，系统需要让用户在“按产业拆解”“按品牌拆解”“按门店拆解”之间选择优先方向；查询数据库时，如果 SQL 可能影响数据库性能，或涉及较高权限的数据访问，也需要先向用户请求授权再继续。

FlexCard 用来承接这类中间判断。它可以把“当前不确定的是什么”“有哪些可选分析路径”“继续执行会访问哪些数据或产生什么风险”放在同一张结构化卡片里。用户确认后，客户端再把选择、授权或修正意见作为结构化上下文传回 Agent。

A2UI 在这里负责界面声明和渲染分工：Agent 不直接决定卡片的视觉样式，而是声明当前任务状态、可展示内容、可选动作和阻塞规则；客户端在设计系统内完成渲染。

![FlexCard 决策卡示意](https://alibaba-cloud-design.github.io/vibe-designing-playbook/figures/fig-2-11-flexcard.gif)

2-11 FlexCard 决策卡示意

## 用 GenReport 承接结果评估

当结果内容较复杂，并且需要被保存、分享或继续追踪时，它更适合作为 Artifacts 产物呈现。一次经营分析通常需要同时呈现指标概览、多维图表、关键洞察、风险判断和策略建议，内容结构比过程中的动态卡片更复杂。GenReport 就是数据分析场景中的一种 Artifacts 形态：它把分析结果组织成一份可以阅读、分享和继续追踪的生成式报告。

GenReport 不是固定报告模板，也不是 A2UI 卡片的放大版。它仍然属于 GenUI：结构、重点和证据组织会随任务目标、数据状态和用户关注点变化。为了让生成结果数据准确、视觉可控，报告需要被声明式规则约束：哪些指标必须出现，图表如何绑定数据，洞察必须引用哪些证据，风险和建议如何落到固定的组件结构里。

一份可用的 GenReport 至少要回答四个问题：

- 关键指标表现如何？
- 哪些结构性问题或风险值得关注？
- 证据来自哪些图表、明细或对比结果？
- 建议动作和后续跟踪方式是什么？
![GenReport 报告页面示意](https://alibaba-cloud-design.github.io/vibe-designing-playbook/figures/fig-2-12-genreport.gif)

2-12 GenReport 报告页面示意

## 回到体验闭环

在这条链路中，OmniBox、FlexCard 和 GenReport 分别承担 Agent Experience Loop 的三个关键职责：承接意图输入，组织过程协作，交付可评估的结果产物。

由此，GenUI 和 A2UI 的分工也落到具体界面上：GenUI 定义运行时如何组织体验，A2UI 负责其中一种动态界面的声明和渲染。一个面向 Agent 的产品，不需要把所有页面都生成出来；它更需要识别哪些时刻会因为意图、上下文、数据和决策变化而需要动态界面。

到这里，Agent 已经具备两件能力：按规则组织界面，在运行时承接任务过程。它解决的是「能做出来」和「能接住真实意图」。但从一版产出到一版更好的产出，仍然需要一套稳定的判断机制。下一章讨论的，就是如何把这种判断从人的反复指正中抽象出来，形成可以持续运转的自我进化循环。

003 · 05 sections

🧭 注释：本章按当前 Evaluator/ v1.5 机制组织，正文主线是 page shape、六维账本、subcheck、浏览器证据、review mode、隔离报告与标准维护。

前两章解决的是「能做出来」。第一章让 Agent 读懂专业声明，第二章让它在运行时接住真实意图。但一个设计系统真正进入 AI 生成以后，还会遇到另一个问题：一版产出之后，谁来判断它该不该进入下一轮。

目前最常见的办法仍然是人看。Agent 生成一版页面，人打开页面或看截图，指出哪里不对、哪里还不够好，Agent 再改一版。这个过程有效，但它的上限很明显：质量取决于那个人愿意看多少遍，也取决于那个人能不能稳定说出为什么不对。

更麻烦的是，很多指正并不新鲜。

「第一屏看不出主任务」「CTA 和页面真实目标不一致」「卡片节奏太平均」「像一个通用模板」「指标有了但来源和时间窗不清楚」「按钮能点但没有状态反馈」——这些话，设计师会在不同项目里反复说。它们不是灵感，也不是某一次偏好。它们是稳定判断。

稳定判断应该被沉淀。

本章所说的自我进化，不是让 AI 自己宣布自己变好了，而是把这些稳定判断变成一套可以运行的评审循环。

这个循环里有两个基本角色：生成器和评估器。

生成器负责把输入变成原型。这里的输入不只是自然语言需求，也包括 Spec、Skills、component.md、design.md 这类设计资产：目标是什么，可以调用哪些能力，组件应该怎么用，视觉和交互有哪些约束。对读者来说，可以先把生成器理解成「提出第一版方案的人」。

评估器负责判断这版原型是否能进入下一步。它并不继续生成方案，也不替设计师做主观打分。它更像一个审稿人：只看当前原型和评审标准，判断产品意图是否清楚、表达是否成立、系统工艺是否稳定、内容语气是否可信、交互是否准备好。

因此，评估器第一次出现时，不必先从工程术语理解。它要解决的是一个很具体的问题：这一版原型是否应当通过；如果不能通过，下一轮到底该改什么。

图 3-1 先把这条关系收束成一个基础闭环：

![Evaluator 自我进化闭环](https://alibaba-cloud-design.github.io/vibe-designing-playbook/figures/fig-3-1-light.svg)

3-1 Evaluator 自我进化闭环

图 3-1 表达的是四个环节：

1. 生成器基于设计输入产出一版原型。
2. 评估器根据评审维度判断原型是否达标。
3. 达标时，原型进入最终设计输出。
4. 不达标时，评估器输出优化指令，回到生成器进入下一轮。

这里的「优化指令」不是一句泛泛的「再优化一下」。它应该说明哪些判断没有成立，证据来自哪里，下一轮应该优先修正什么。比如第一屏看不出主任务，就回到产品意图（Product Intent）；组件状态不稳定，就回到系统工艺（System Craft）；关键动作没有反馈，就回到交互就绪度（Interaction Readiness）。

后文会把这条基础闭环展开成工程机制。原型会被当作可评审的页面产物（Web artifact）；准备阶段（Prepare）会打开页面、采集截图、做浏览器质量检查（DOM/CSS QA）和关键点击检查（click smoke）；评估阶段会按评审标准（rubric）和权重输出结构化判断；收束阶段（Finalize）会重新计算分数、处理阻断问题（blocking findings），并生成报告和回流计划（return plan）。

专业术语会在后面逐层展开。此处先抓住这条主线：生成器提出原型，评估器判断原型，通过就输出，不通过就把优化指令带回下一轮。

这不是取消人。人的位置发生了变化。

过去，人被放在每一轮循环里，反复指出同类问题。现在，人的判断更适合进入上游：修订 framework、prompt、schema 和 harness policy，把稳定判断写成运行时能执行的契约。运行时由 evaluator 执行那些已经显式化的判断。

分数只是外显结果。真正重要的是分数背后的证据链和回流路径。

没有证据链，AI 很容易把完整度误当成质量。没有回流路径，评估只是一份事后报告。两者合在一起，生成循环才有机会从「看起来差不多」走向「这一版为什么还不能交付」。

稳定判断进入 evaluator 以后，不会以一句抽象的 taste 存在。它需要先回答两个问题：这一版原型属于什么页面，以及这类页面应该按什么目标被评估。

这一步很重要。因为云产品里的页面并不承担同一种任务。一个品牌落地页要把注意力转成兴趣和信任，一个控制台要帮用户走通操作路径，一个数据看板要帮助用户判断状态和变化。它们都可以被称为 UI，但失败方式并不相同。

因此，当前 evaluator 的关键变化，不是给每一种页面重新发明一套标准，而是把标准收敛成一套共同语言：先判断页面类型，再用同一组六维度模型评估，只是不同页面类型的权重不同。

这样既保留差异，也保留共同语言。

## 先判断页面类型

同样是 UI，失败方式并不相同。落地页可能输在没有品牌记忆，控制台可能输在任务链路断裂，数据看板可能输在指标没有来源，对话界面可能输在回答缺少依据，文档页可能输在结构难以扫描。

图 3-2 先把常见页面分成三类任务：转化型页面、任务型页面和判断型页面。读者不需要先记住所有英文类型，只要先抓住这个差异：有的页面负责建立信任，有的页面负责完成操作，有的页面负责辅助判断。

![页面类型决定评估目标](https://alibaba-cloud-design.github.io/vibe-designing-playbook/figures/fig-3-2-light.svg)

3-2 页面类型决定评估目标

当前框架会在这三类任务下继续识别更具体的 page shape:

| 页面类型 | 所属任务 | 主任务 | 典型失败方式 |
| --- | --- | --- | --- |
| Brand Landing Page | 转化型页面 | 把注意力转成兴趣与信任 | 通用模板、品牌记忆弱、承诺含混 |
| Product Console | 任务型页面 | 帮用户安全完成操作任务 | 主任务不清、状态断裂、信息密而无用 |
| Conversational Interface | 任务型页面 | 帮用户通过对话提问、判断、恢复 | 轮次状态不清、回答无依据、缺少恢复 |
| Data Dashboard | 判断型页面 | 帮用户判断状态并诊断变化 | 装饰大于含义、指标层级弱 |
| Content / Documentation Page | 判断型页面 | 帮用户找到并应用知识 | 难扫描、结构弱、声明无证据 |

如果用户提供了明确任务，它就是权威输入。如果没有任务，prepare 阶段会从页面产物（Web artifact）的 title、h1、导航、链接、可见文案、图片和页面结构推断临时目标，并把来源标记为 `inferred_from_artifact` 。

这一步解决的是用错尺子的问题。没有 brief 的品牌首页，不应被评成缺少完整下单系统；一个产品控制台，也不应因为不像营销落地页而被误判。

## 从真实业务关注拆出六个维度

页面类型解决的是「该用哪把尺子」。下一步是定义尺子本身。

对云产品页面来说，设计质量并不只是视觉审美。它至少来自三类真实业务关注：

1. 业务语义层：页面是否讲清楚产品价值、业务规则、风险边界和可信依据。
2. 用户任务层：页面是否帮用户找到路径、理解层级、完成动作、处理异常。
3. 界面实现层：页面是否用稳定的组件、间距、字体、状态和视觉表达承载前两层。

六维度模型就是从这三类关注里拆出来的。业务语义层对应 Product Intent 和 Trust & Domain Fit；用户任务层对应 Information Architecture 和 Interaction Readiness；界面实现层对应 System Craft 和 Visual & Brand Expression。

![从真实业务关注拆出六维度模型](https://alibaba-cloud-design.github.io/vibe-designing-playbook/figures/fig-3-3-light.svg)

3-3 从真实业务关注拆出六维度模型

当前评分模型只有六个正式维度：

| 维度 | 中文名 | 评审关注 |
| --- | --- | --- |
| Product Intent | 产品意图 | 价值主张、目标用户、主任务、内容语气、CTA 是否匹配真实目标 |
| Trust & Domain Fit | 业务可信 | 领域术语、数据声明、风险权限、合规、AI 置信和证据是否可信 |
| Information Architecture | 信息架构 | 层级、分组、导航顺序、密度、节奏是否服务扫描和决策 |
| Interaction Readiness | 交互就绪 | 控件是否可理解，动作是否有反馈，关键路径是否可完成和恢复 |
| System Craft | 系统工艺 | 字体、间距、圆角、阴影、组件、状态和桌面布局是否像一套系统 |
| Visual & Brand Expression | 视觉品牌 | 色彩、字体重量、图像、动效是否形成适合品类的品牌表达 |

这六个维度不是为了让评估更复杂，而是为了避免把不同问题混在一个「好不好看」里。产品意图不清，不能只归咎于视觉；领域术语错误，也不能用组件工艺掩盖；主路径断裂，更不能被一个完整的页面布局抵消。

## 权重随页面类型变化

同一组六维度，在不同页面里的重要性不同。

品牌落地页首先要建立记忆和信任，因此 Visual & Brand Expression 的权重更高。产品控制台首先要让任务和状态可用，因此 Product Intent、Information Architecture 和 Interaction Readiness 更重要。数据看板和文档页需要支撑判断，因此 Information Architecture 与 Trust & Domain Fit 会变得更重。对话界面则要让轮次、依据和恢复路径成立，Interaction Readiness 和 Trust & Domain Fit 会被放到更前面。

![页面类型对应的维度权重差异](https://alibaba-cloud-design.github.io/vibe-designing-playbook/figures/fig-3-4-light.svg)

3-4 页面类型对应的维度权重差异

当前权重表如下：

| 维度 | Brand Landing | Product Console | Conversational Interface | Data Dashboard | Content / Documentation |
| --- | --- | --- | --- | --- | --- |
| Visual & Brand Expression | 25% | 8% | 8% | 8% | 8% |
| Product Intent | 20% | 22% | 18% | 18% | 18% |
| Information Architecture | 18% | 22% | 16% | 24% | 28% |
| System Craft | 15% | 14% | 12% | 16% | 14% |
| Trust & Domain Fit | 12% | 18% | 22% | 22% | 22% |
| Interaction Readiness | 10% | 16% | 24% | 12% | 10% |

END · closing note

回头看这三章，它们讲的不是三套分散能力，而是一条连续的工作方式。