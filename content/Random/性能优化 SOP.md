---
date: 2026-09-21
tags:
aliases:
---
## 一、 性能诊断与基准设定 (Measurement)

在展开任何优化前，必须先建立可量化的性能指标基线。严禁在没有性能数据的支持下凭感觉“盲目优化”。

### 1. 核心指标与目标值 (Core Web Vitals)

| 指标名称                          | 简称   | 优良阈值 (Good)         | 说明                          |
| ----------------------------- | ---- | ------------------- | --------------------------- |
| **Largest Contentful Paint**  | LCP  | $\le 2.5\text{ s}$  | 最大内容绘制时间，衡量页面主要内容的加载速度      |
| **Interaction to Next Paint** | INP  | $\le 200\text{ ms}$ | 交互到下次绘制延迟，替换 FID，衡量页面的响应灵敏度 |
| **Cumulative Layout Shift**   | CLS  | $\le 0.1$           | 累积布局偏移，衡量页面的视觉稳定性           |
| **First Contentful Paint**    | FCP  | $\le 1.8\text{ s}$  | 首次内容绘制时间，衡量用户首次看到任何内容的时间    |
| **Time to First Byte**        | TTFB | $\le 0.8\text{ s}$  | 首字节到达时间，衡量服务端及网络响应速度        |

### 2. 诊断分析工具链

1. **开发与本地排查**：
* **Chrome DevTools Performance 选区**：定位长任务（Long Tasks $> 50\text{ ms}$）与主线程阻塞。
* **React DevTools Profiler**：勾选 *Record why each component rendered*，查找非必要的反复重渲染（Re-render）。
* **Bundle Visualizer**：使用 `webpack-bundle-analyzer` 或 `vite-plugin-visualizer` 分析打包产物体积构成。


2. **线上真实用户监控 (RUM)**：
* 在项目中集成 `web-vitals` SDK 收集真实的现网 Core Web Vitals 指标，并上报至监控平台（如 Sentry、Datadog 或自研 RUM 系统）。



---

## 二、 加载性能优化 (Loading & Network)

加载性能优化的核心原则是：**减少传输体积、减少请求次数、提升首屏并行度**。

### 1. 代码分割与路由按需加载 (Code Splitting)

* **路由级懒加载**：使用 `React.lazy` 与 `Suspense` 实现按需加载，避免将所有页面逻辑打包进首屏 `main.js` 中。
```tsx
import React, { lazy, Suspense } from 'react';

const Dashboard = lazy(() => import(/* webpackChunkName: "dashboard" */ './pages/Dashboard'));

export const Router = () => (
  <Suspense fallback={<PageSkeleton />}>
    <Routes>
      <Route path="/dashboard" element={<Dashboard />} />
    </Routes>
  </Suspense>
);

```


* **非关键组件延迟加载**：对弹窗、抽屉、复杂图表组件（如 ECharts）执行基于用户交互（如 Hover、Focus）或可见性（`IntersectionObserver`）的延迟加载。

### 2. 构建产物瘦身 (Bundle Optimization)

* **Tree Shaking 检查**：
* 确保项目配置 `sideEffects: false`（在 `package.json` 中配置），剥离未引用的模块。
* 针对工具库使用支持 ES Module 的按需导入方式（如从 `lodash-es` 替换 `lodash`，使用 `date-fns` 或 `dayjs` 替换 `moment.js`）。


* **公共依赖提取与 CDN 托管**：
* 使用分包策略（如 Vite 的 `manualChunks` 或 Webpack 的 `SplitChunksPlugin`）将大型且更新频率低的第三方库（`react`, `react-dom`, `axios` 等）抽离为独立 chunk，利用浏览器强缓存机制。



### 3. 静态资源与网络传输

* **图片优化**：
* **格式转换**：优先选用 WebP 或 AVIF 格式。
* **响应式与懒加载**：大图使用 `loading="lazy"` 属性，配合 `<picture>` 或 `srcset` 适配不同屏幕尺寸。
* **小图标优化**：使用 SVG Inline、SVG Sprite 或 Iconfont，避免过多的小图片 HTTP 请求。


* **HTTP/Cache 策略**：
* 产物文件使用带有内容 Hash 的文件名（如 `app.a1b2c3.js`），设置 HTTP 响应头 `Cache-Control: max-age=31536000, immutable`。
* 开启服务器传输压缩：优先支持 **Brotli** 压缩，其次为 **Gzip**。
* 使用 `<link rel="preconnect">` 和 `<link rel="dns-prefetch">` 对关键域名提前进行 DNS 解析与 TLS 握手。



---

## 三、 渲染性能与组件优化 (Rendering & State)

渲染性能优化的核心原则是：**控制渲染范围、避免无效重复计算、减少主线程阻塞**。

### 1. 减少非必要重渲染 (Unnecessary Re-renders)

* **状态下沉 (State Colocation)**：将仅在局部使用的状态限制在最靠近它的组件内部，避免引起顶层或父组件的全树渲染。
* **状态拆分与细粒度订阅**：
* 避免在大 Context 中放置高频变更的状态（会导致所有消费该 Context 的组件强制重渲染）。
* 对于复杂全局状态，优先考虑细粒度响应式库或原子化状态库（如 Zustand、Jotai）。


* **记忆化优化 (Memoization)**：
* **`React.memo`**：缓存纯渲染组件，结合自定义对比函数（`arePropsEqual`）避免因父组件更新导致的联动重渲染。
* **`useMemo` / `useCallback**`：对高开销计算结果或传递给子组件的引用类型变量/回调函数进行记忆化。
* *(注：若项目环境升级至 React 19 并引入 React Compiler，可由编译器自动处理记忆化逻辑。)*



### 2. 长列表与大量 DOM 渲染

* **虚拟列表 (Virtualization)**：对于列表数据超 100 项以上的场景，严禁直接全量渲染。必须使用虚拟列表库（如 `tanstack/react-virtual` 或 `react-window`），仅渲染视口内部及边缘缓冲区域的 DOM 节点。
* **分片渲染 (Time Slicing)**：对于不可避免的大量初始 DOM 绘制，通过 `requestAnimationFrame` 将大渲染任务切割为多帧异步分批渲染。

### 3. 响应性与并发更新 (React Concurrent)

* **非紧急更新让步**：使用 `useTransition` 或 `useDeferredValue` 标记低优先级更新（如搜索框输入带来的实时列表过滤），保证高优先级用户输入（如 Typing、Click）不卡顿，优化 INP 指标。
```tsx
const [isPending, startTransition] = useTransition();

const handleInputChange = (e) => {
  setInputValue(e.target.value); // 紧急更新：保持输入框流畅
  startTransition(() => {
    setSearchQuery(e.target.value); // 非紧急更新：延后处理耗时的列表渲染
  });
};

```

---

## 四、 运行期与内存管理 (Runtime & Memory)

* **事件监听与定时器清理**：
* 在 `useEffect` 的清理函数（Cleanup Function）中强制注销全部 `addEventListener`、`setInterval`、`setTimeout` 以及 ResizeObserver 等。


* **防抖与节流 (Debounce & Throttle)**：
* 对 `scroll`、`resize`、`mousemove` 以及 `input` 等高频事件处理函数实施防抖（Debounce）或节流（Throttle）。


* **密集计算任务移出主线程**：
* 对于耗时超过 $50\text{ ms}$ 的纯计算逻辑（如复杂的加密、大数据集解析/转换），使用 **Web Worker** 移至后台线程处理，确保 UI 主线程持续流畅。



---

## 五、 性能卡点与持续集成 (CI/CD)

优化成果需要机制保障，防止代码迭代过程中性能再次滑坡。

1. **Lighthouse CI (LHCI)**：
* 将 `lhci` 集成进 GitHub Actions 或 GitLab CI/CD 流水线。
* 设置性能门槛规则（例如：当 PR 中的 Lighthouse Performance 得分低于 85 分，或 LCP 大于 3.0s 时自动拒绝合并）。


2. **Bundle 体积卡点**：
* 在 CI 阶段使用 `bundlesize` 或 `size-limit` 对产物主 JS 包进行限制，超过预设阈值报错提示。
