---
date: 2026-07-23
tags:
  - React
  - UI
  - 组件库
  - 架构决策
aliases:
---

# Ant Design 与 Radix UI 组件能力对比

> 对比目标：为“小牛业务组件库 + 设计规范体系”选择合适的底层交互能力。本笔记比较 Ant Design（成品视觉组件库）与 [[Radix UI|Radix UI Primitives]]（无头交互原语），而不是把二者视为同类替代品。

> [!important] 决策结论
> 新建的小牛 Layer 1 原子组件，推荐以 **Radix UI 作为交互与无障碍基础**，由小牛完全拥有视觉、Token 和组件 API。Ant Design 更适合作为“立即可用的企业后台 UI 成品”，不适合作为本次以 AI 受约束生成、设计语言可演进、运行时 Token 覆盖为核心目标的视觉底座。
>
> 这不意味着一次性替换存量 MUI。存量页面保持 MUI；新组件按适配器/封装层渐进接入 Radix。Radix 缺少的表格、日期、上传等数据密集能力，须保留现有 MUI 能力或单独选型，不能假设 Radix 可以覆盖。

## 两者解决的问题不同

| 维度 | Ant Design | Radix UI Primitives |
| --- | --- | --- |
| 本质 | 带完整默认视觉的企业级 React 组件库 | 只提供行为、语义、状态与可访问性的 React 原语 |
| 首要价值 | 快速拼出统一的 Ant 风格后台页面 | 自建设计系统时避免重复实现复杂交互 |
| 默认 DOM / CSS | 内部结构与视觉样式由库主导，可通过主题 token 和覆写定制 | 无默认视觉；业务方定义 DOM 外观、CSS Variables、动效和 token |
| 组件使用方式 | 直接使用 `Button`、`Table`、`Form` 等成品 | 用 `Dialog.Root`、`Trigger`、`Content` 等部件组合并封装为自有组件 |
| 适合谁 | 需要快速交付、接受 Ant 设计语言的项目 | 有设计团队、明确 Token 与自有设计语言的产品/设计系统 |

## 组件能力映射

| 能力分类 | Ant Design 代表组件 | Radix 对应能力 | 小牛工程含义 |
| --- | --- | --- | --- |
| 基础输入 | Button、Input、InputNumber、AutoComplete、Mentions | Checkbox、Radio Group、Select、Slider、Switch、Toggle；文本输入使用原生 `input` 自行封装 | Radix 足以支撑 Button/Input 等 Layer 1，但需自行定义尺寸、校验态、图标和 loading 规范 |
| 选择与复杂录入 | Cascader、DatePicker、TimePicker、TreeSelect、Transfer、ColorPicker | Select、Radio Group、Slider | **Ant 覆盖明显更全**；Radix 没有日期、级联、树选、穿梭、颜色选择等成品，需保留 MUI/另选库或建设业务组件 |
| 浮层与反馈 | Modal、Drawer、Popover、Tooltip、Dropdown、Notification、Message | Dialog / Alert Dialog、Popover、Tooltip、Hover Card、Dropdown Menu、Context Menu、Toast | **Radix 强项**：焦点圈定、Esc、Portal、菜单键盘操作等底层交互已实现，视觉可以完全走小牛 token |
| 导航与组织 | Menu、Tabs、Breadcrumb、Steps、Anchor、Pagination | Navigation Menu、Menubar、Tabs、Accordion、Collapsible、Toolbar、Scroll Area | 核心交互足够；Breadcrumb、Steps、Pagination 这类展示/业务规则应在 Layer 2 自建 |
| 信息展示 | Avatar、Badge、Tag、Card、Descriptions、Empty、Result、Statistic、Timeline | Avatar、Badge、Progress、Separator、Aspect Ratio | Ant 成品更多；但这些多数是纯视觉 Layer 1/2，正是应由小牛 Token 体系自主定义的部分 |
| 数据密集组件 | Table、List、Tree、Calendar、Image、Carousel、QRCode | 无 Table、Tree、Calendar、虚拟列表能力 | **Radix 不覆盖**。后台数据页必须保留 MUI X / 现有方案或独立选择 headless table（如 TanStack Table） |
| 表单体系 | Form、Form.Item、校验与布局整合 | Form primitive 处理语义与校验提示，不提供完整表单状态方案 | 表单状态和业务校验仍应由 React Hook Form 等统一管理；不要把规则锁进基础 UI 库 |
| 无障碍 | 基础能力较完整 | 以 WAI-ARIA、键盘导航、焦点管理为核心设计目标 | 两者都可达标；Radix 更方便将无障碍行为与小牛视觉解耦并在封装层统一回归 |

## 与本次目标的匹配度

| 本次约束 | Ant Design 的影响 | Radix UI 的影响 | 判断 |
| --- | --- | --- | --- |
| 所有视觉必须来自 Layer 0 Token | Ant 虽有 Design Token 与 CSS Variables 配置，但成品组件带大量既定视觉和内部结构；深度贴合小牛风格常需覆盖组件级规则 | 原语不带视觉，组件 CSS 可从第一行就只引用 `var(--xxx)` | **Radix 更符合** |
| Chrome 插件运行时注入 CSS Variables | 可修改主题变量，但无法天然保证每个局部视觉与自定义覆写都由小牛变量控制 | 小牛封装层拥有所有 CSS 声明，可保证每个视觉值都有可覆盖变量 | **Radix 更符合** |
| AI 不得自编样式，只能检索组件与 spec.json | AI 容易直接使用 Ant 的大量 props，或以覆写 CSS 将 Ant 组件“改像”小牛组件，产生隐性依赖 | AI 只允许引用 `@niu/ui` 封装组件；交互由 Radix 托底，视觉/API 只暴露小牛规范 | **Radix 更符合** |
| 设计语言持续演进 | 改动常表现为 Ant token 映射、主题配置和局部覆盖并存，排查来源困难 | Token 是唯一视觉来源；变更路径清晰：Token -> 小牛组件 -> 页面 | **Radix 更符合** |
| 设计侧以完整页面验收 | 交付快，适合原型和后台通用页 | 需要先建设 Layer 1/2 与页面模板，初期投入更高 | **Ant 更快，Radix 需投入** |
| 业务卡片与页面快速生成 | 成品多，第一版更快，但视觉容易趋近 Ant | 组件资产不足时 AI 仍会“自编”；必须先完成种子组件、模板和门禁 | 取决于资产建设，不是 Radix 自动获胜 |
| 存量 MUI 复用 | 引入第二套成品视觉体系，MUI 与 Ant 的主题/DOM/交互差异会加大 | 仅引入行为原语，较容易与既有 MUI 页面并存 | **Radix 风险更低** |

## 为什么 Radix 更符合这次变更

本次核心不是“找一套组件最快搭页面”，而是建立一个让 AI **只能沿着设计规则产出代码** 的系统。Radix 的价值正是把“交互正确性”和“视觉决策权”分离：

1. **视觉唯一真相可以落到 Token。** 小牛组件的颜色、间距、圆角、阴影和动效都可直接写为 `var(--xxx)`。这使 Token 编辑器和 Chrome 插件可以精确预览，不必赌第三方组件的内部样式是否可覆写。
2. **`spec.json` 可以定义唯一业务 API。** 例如 `NiuButton` 只暴露 `variant`、`size`、`loading`，而把 Radix 当内部实现细节。AI 检索到的是稳定的小牛规格，不会在页面中随意拼 Ant 的 `type`、`danger`、`ghost` 与私有 CSS 覆写。
3. **层级划分更干净。** Radix 负责 Layer 1 所需的弹层、菜单、选择、焦点与键盘交互；小牛负责 Layer 0/1 的视觉和 Layer 2/3 的领域组合。Ant 同时占据视觉、组件 API 和部分业务模式，容易模糊这些边界。
4. **对存量技术栈更克制。** 规划已明确底层继续复用 MUI。引入另一套“完整视觉组件库”会形成 MUI + Ant + 小牛三套设计语言；Radix 只补足 MUI 不方便直接暴露的无头交互基础，冲突面更小。
5. **可访问性不需要从零实现。** Dialog、Menu、Select、Tooltip 等最容易被忽略的键盘、焦点、ARIA 行为由 Radix 提供；团队把精力投向 Token、业务组件和 AI 门禁。

> [!warning] 不应夸大 Radix
> Radix 不是 Ant Design 的“更轻量版本”，也不会自动让 AI 生成更好的页面。没有完善的 `@niu/ui` 封装、`spec.json`、页面模板、token lint 和 visual diff，AI 仍然会写出不符合规范的 CSS。它用初期组件建设成本，换取后续视觉治理与演进的控制权。

## 建议的工程落位

```text
AI / component-composer
          |
          v
  @niu/ui（AI 唯一允许直接导入的组件入口）
          |
          +-- Layer 3：业务组件（BubbleCard、DataMetric 等）
          +-- Layer 2：分子组件（Field、Card、ActionBar 等）
          +-- Layer 1：原子组件（NiuDialog、NiuSelect、NiuButton）
                         |
                         +-- Radix：Dialog / Select / Menu / Popover / Toast 等行为
                         +-- 原生元素：Button / Input / Textarea 等
                         +-- MUI：仅存量或明确保留的数据密集能力
          |
          v
Layer 0：CSS Variables / Design Tokens（唯一视觉来源）
```

落地规则：业务页面不得直接 import `@radix-ui/*`、MUI 或 Ant Design；只能使用 `@niu/ui`。这样未来更换底层实现时，影响被限制在组件库内部。

## 分阶段取舍建议

1. **P0：不引入 Ant Design 作为新的视觉底座。** 完成 Token CSS Variables 双输出、种子原子组件（Button、Input、Dialog、Select、Tag、Card）以及 `spec.json` 和 lint 门禁。
2. **P1：用 Radix 建设高风险交互原语。** 优先 Dialog、Popover、Dropdown Menu、Tooltip、Tabs、Select、Checkbox、Radio、Switch、Toast；这些最能减少可访问性和焦点管理的重复实现。
3. **P1：明确数据组件策略。** Table/Tree/DatePicker/Upload 不纳入 Radix 覆盖承诺。继续复用现有 MUI 能力，或分别评估 TanStack Table、React Aria 日期组件等；对外仍封装为 `@niu/ui`。
4. **P2：渐进迁移。** 新卡片强制使用 `@niu/ui`；存量 MUI 页面只在修改触及组件时迁移。不要做“先全量替换再建设规范”的大迁移。
5. **门禁：检查依赖边界。** 在 `component-spec-check` 之外增加 import lint：页面层禁止直接依赖 `@radix-ui/*`、`@mui/*`、`antd`；组件库内部才允许底层依赖。

## 验收指标

| 指标 | 推荐判定方式 |
| --- | --- |
| Token 可覆盖率 | Layer 1/2 CSS 中视觉值 100% 来自 `var(--xxx)`；禁止颜色、间距、圆角硬编码 |
| AI 规范遵守率 | 自动扫描页面层 import，`@niu/ui` 以外的 UI 依赖为 0；生成组件均有 `spec.json` |
| 预览有效性 | Chrome 插件覆盖一个颜色、间距、圆角 token 后，目标组件即时且可回滚地变化 |
| 交互质量 | Dialog、菜单、Select 通过键盘导航、焦点回归和读屏回归用例 |
| 迁移风险 | 首批 3 个种子组件与 MUI 存量页面并存，无全局样式污染或视觉回归 |

## 官方资料

- [Ant Design Components](https://ant.design/components/overview/)
- [Ant Design Design Token](https://ant.design/docs/react/customize-theme)
- [Radix UI Primitives](https://www.radix-ui.com/primitives/docs/overview/introduction)
- [Radix UI Components](https://www.radix-ui.com/primitives/docs/overview/introduction#primitives)
- [[无头样式组件库调研]]
