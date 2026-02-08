

# Quartz 项目指南

本仓库基于 [Quartz](https://quartz.jzhao.xyz/) 静态网站生成器构建。它使用了 TypeScript、Preact 和 Node.js。

## 1. 构建、Lint 和测试命令

* **开发服务器 / 构建：**
```bash
npx quartz build --serve

```


构建到指定目录（例如 `docs`）：
```bash
pnpx quartz build --serve -d docs

```


* **Lint 检查与类型检查：**
```bash
pnpm run check

```


此命令会运行 `tsc --noEmit`（确保类型安全）和 `prettier . --check`（检查格式）。
* **格式化：**
```bash
pnpm run format

```


运行 `prettier . --write` 以修复代码格式问题。
* **测试：**
* **运行所有测试：**
```bash
pnpm test

```


* **运行单个测试：**
```bash
pnpx tsx --test path/to/file.test.ts

```


示例：`npx tsx --test quartz/util/path.test.ts`



## 2. 代码风格与规范

### 通用

* **语言：** TypeScript（启用严格模式）。
* **格式化工具：** Prettier。提交代码前请务必运行 `npm run format`。
* **导入：** 使用显式的相对路径导入。避免使用通配符。

### 组件 (Preact)

* **位置：** `quartz/components/`
* **框架：** Preact（使用 `class` 而非 `className`）。
* **类型定义：** 组件应定义为 `QuartzComponent` 类型。
* **Props：** 组件属性请使用 `QuartzComponentProps`。
* **导出模式：** 使用带有 `satisfies` 关键字的工厂模式：
```typescript
export default (() => MyComponent) satisfies QuartzComponentConstructor

```


* **样式：** 如果需要，直接在组件上附加 CSS：
```typescript
MyComponent.css = `
.my-class {
  color: red;
}
`

```


* **条件渲染：** 使用标准 JavaScript 条件语句（`if`、三元运算符）。

### 插件

* **位置：** `quartz/plugins/`
* **类型：** 实现 `QuartzTransformerPlugin` 或 `QuartzEmitterPlugin`。
* **配置项模式：**
```typescript
interface Options { ... }
const defaultOptions: Options = { ... }
export const MyPlugin: QuartzTransformerPlugin<Partial<Options>> = (userOpts) => {
  const opts = { ...defaultOptions, ...userOpts }
  return {
    name: "MyPlugin",
    // ... 具体实现
  }
}

```



### 测试

* **运行器：** `node:test` (通过 `tsx`)。
* **文件命名：** `*.test.ts`。
* **位置：** 与源代码同级（例如：`quartz/util/path.ts` -> `quartz/util/path.test.ts`）。

## 3. 项目结构

* `quartz/`: 核心应用逻辑。
* `components/`: UI 组件 (Preact)。
* `plugins/`: 构建时插件 (transformers 转换器, emitters 发射器)。
* `util/`: 工具函数。


* `content/`: 网站的 Markdown 内容。
* `quartz.config.ts`: 主配置文件。
* `quartz.layout.ts`: 布局配置文件。

## 4. Cursor/Copilot 规则

* 未发现特定的 `.cursorrules` 或 `.github/copilot-instructions.md`。
* 请严格遵守上述规范，特别是组件导出时必须使用 `satisfies QuartzComponentConstructor` 模式，这对于 Quartz 的依赖注入系统至关重要。

