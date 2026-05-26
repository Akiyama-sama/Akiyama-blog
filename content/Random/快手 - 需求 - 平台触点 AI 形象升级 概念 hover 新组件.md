---
date: 2026-05-25
tags:
aliases:
---
---
title: ConceptExplainPopover
group:
  title: 数据展示
displayName: 概念解释 Popover
description: 用于概念型文案的统一解释入口，支持虚线触发、hover 展示页面内简介、固定高度加载态以及“查看完整回答”回调。组件只负责交互与样式，不内置磁力小牛唤起、内容请求或业务跳转逻辑。
device: pc
business: ESP
---

# ConceptExplainPopover

概念解释 Popover，用于“虚线概念文案 + hover 页面内简介 + 查看完整回答”的统一交互。典型场景包括“快速冷启”“智能优惠券”“冷启 ROI”“人群倾向”“预算智投”等功能名词说明。

组件本质是一个增强版 Popover：除 `content` 和 `title` 由组件内部接管外，其它 Popover 配置可直接透传。业务侧可通过 `onViewFullAnswer` 接收点击事件并完成打开磁力小牛、请求完整答案或跳转等后续动作。

## 何时使用

- 功能名词或概念文案需要 hover 展示简短解释时
- 解释内容超过 30 字，需要引导用户查看完整回答时
- 解释内容包含图文、分段说明或运营要求推广功能介绍时
- 需要把“页面内简介”和“完整回答跳转/小牛唤起”解耦时

## 代码演示

### 基础用法

<code src="./demos/basic.tsx"></code>

## API

### ConceptExplainPopover

| 参数             | 说明                                                                                                                | 类型                                             | 默认值         |
| ---------------- | ------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------ | -------------- |
| keyword          | 概念关键词，用于默认触发文案和默认问题标题                                                                          | `string`                                         | -              |
| children         | 自定义触发内容，不传时展示 `keyword`                                                                                | `ReactNode`                                      | -              |
| explanation      | 解释内容，由调用方传入最终可渲染内容；Markdown、分段、图文等内容需先在业务侧渲染成 ReactNode                        | `ReactNode`                                      | -              |
| title            | 自定义问题标题，不传时展示 `问问小牛：什么是${keyword}？`                                                           | `ReactNode`                                      | -              |
| icon             | 标题前的小牛图标或图片占位，不传时展示组件内置占位图标                                                              | `ReactNode`                                      | -              |
| actionText       | 底部按钮文案                                                                                                        | `string`                                         | `查看完整回答` |
| loading          | 是否展示加载态                                                                                                      | `boolean`                                        | `false`        |
| loadingHeight    | 加载态骨架固定高度                                                                                                  | `50 \| 100 \| number`                            | `100`          |
| disabled         | 是否禁用解释能力。禁用后只渲染触发内容，不展示虚线和 Popover                                                        | `boolean`                                        | `false`        |
| showUnderline    | 是否展示文字虚线                                                                                                    | `boolean`                                        | `true`         |
| triggerClassName | 触发文字外层类名                                                                                                    | `string`                                         | -              |
| triggerStyle     | 触发文字外层样式                                                                                                    | `React.CSSProperties`                            | -              |
| source           | 触点来源标识，用于业务回调和埋点                                                                                    | `string`                                         | -              |
| loggerParams     | 扩展埋点参数，组件仅透传，不做上报                                                                                  | `Record<string, unknown>`                        | -              |
| onViewFullAnswer | 点击“查看完整回答”时触发，业务侧可在这里打开磁力小牛或执行跳转                                                      | `(payload: ConceptExplainActionPayload) => void` | -              |
| ...PopoverProps  | 其它 Popover 配置，例如 `placement`、`trigger`、`align`、`overlayClassName`、`overlayInnerStyle`、`onVisibleChange` | `Omit<PopoverProps, 'content' \| 'title'>`       | -              |

### ConceptExplainActionPayload

| 参数         | 说明           | 类型                      |
| ------------ | -------------- | ------------------------- |
| keyword      | 当前概念关键词 | `string`                  |
| source       | 当前触点来源   | `string`                  |
| explanation  | 当前解释内容   | `ReactNode`               |
| loggerParams | 扩展埋点参数   | `Record<string, unknown>` |

## 功能说明

### 触发内容

默认使用 `keyword` 作为触发文字，也可以通过 `children` 自定义触发内容。组件默认给触发文字添加虚线，适配概念解释类入口。

### 解释内容

`explanation` 直接接收 `ReactNode`。组件不解析 Markdown，也不内置分段结构；如果业务需要 Markdown、图文或多段说明，请先在业务侧渲染成 ReactNode 后传入。组件会按可提取的文本长度自动处理内容高度：50 字以内自然展示，50-100 字按 50 字介绍高度展示并在底部渐隐，超过 100 字按 100 字介绍高度展示并在底部渐隐，引导用户点击“查看完整回答”。

### 完整回答

点击按钮只触发 `onViewFullAnswer`，不会内置打开页面、调用接口或唤起磁力小牛逻辑。这样业务侧可以按不同页面、不同触点自由决定后续行为。

### 加载态

`loading` 状态下会展示固定高度骨架，不遮挡页面其它内容。可通过 `loadingHeight` 控制骨架高度，该字段只影响加载态，不参与正常解释内容的 50/100 字折叠规则。

## 注意事项

1. 组件只负责“页面内简介”的展示，不负责完整答案内容生成。
2. 除 `content` 和 `title` 外，其它 Popover 配置会透传到底层 Popover，业务侧可覆盖 `placement`、`trigger`、`overlayInnerStyle` 等配置。
3. 如果传入 Markdown、图文或分段内容，请先在业务侧渲染成 ReactNode 后放入 `explanation`；需要调整弹层宽度时，通过 `overlayInnerStyle` 透传到底层 Popover。
4. 正常内容折叠依赖组件从 `explanation` 中提取文本长度；普通字符串、数组、ReactElement children 可被识别，完全封装在自定义组件内部的文本无法保证被统计。
5. `disabled` 为 `true` 时，不展示虚线、不绑定 Popover，仅保留原触发内容。
6. 小牛真实图片资源可通过 `icon` 传入；不传时组件展示默认占位图标。

