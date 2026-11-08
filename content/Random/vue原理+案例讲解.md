---
date: 2026-10-28
tags:
aliases:
---
# Vue 核心机制实战串联笔记

我们通过一个涵盖**响应式数据、计算属性、异步更新、DOM 操作以及静态内容**的典型组件案例，将前面涉及的所有核心机制从头到尾完整串联起来。

---

## 一、完整组件代码案例

```vue
<template>
  <div class="user-panel">
    <!-- 1. 静态节点：完全没有动态绑定 -->
    <header class="title">
      <h2>用户信息看板</h2>
      <p>数据实时同步系统</p>
    </header>

    <!-- 2. 动态内容：涉及响应式数据与计算属性 -->
    <section class="content">
      <p id="level-display">当前用户：{{ user.name }} | 等级称号：{{ levelTitle }}</p>
      <p>积分数值：{{ score }}</p>
      <button @click="upgrade">升级用户并获取DOM</button>
    </section>
  </div>
</template>

<script setup>
import { reactive, ref, computed, watch, nextTick } from 'vue'

// 1. 响应式数据：Proxy 代理对象与 ref
const user = reactive({
  name: '小明'
})
const score = ref(100)

// 2. computed：依赖 score 的派生状态（具缓存与脏检查机制）
const levelTitle = computed(() => {
  console.log('[Computed] 正在重新计算 levelTitle...')
  return score.value >= 200 ? '高级会员' : '初级会员'
})

// 3. watch：处理副作用行为（异步操作/网络请求）
watch(score, (newVal, oldVal) => {
  console.log(`[Watch] 侦听到积分从 ${oldVal} 变动为 ${newVal}，准备上报埋点...`)
})

// 4. 事件方法：修改数据、异步更新与 nextTick
const upgrade = async () => {
  // 4.1 动态新增属性（Vue 3 Proxy 原生支持）
  user.role = 'VIP'

  // 4.2 连续修改响应式数据
  score.value = 150
  score.value = 220

  // 4.3 立即读取 DOM：此时拿不到最新 DOM 内容
  const domBefore = document.getElementById('level-display').innerText
  console.log('【立刻同步读取 DOM】:', domBefore)

  // 4.4 等待微任务队列清空、DOM 渲染完毕
  await nextTick()

  // 4.5 在 nextTick 之后读取 DOM：拿到最新渲染结果
  const domAfter = document.getElementById('level-display').innerText
  console.log('【nextTick 后读取 DOM】:', domAfter)
}
</script>

```

---

## 二、从编译到运行的全流程深度拆解

### 阶段 1：模板编译（Compile）

当打包器或运行时编译这个 `<template>` 时，经历三个步骤：

1. **词法/语法解析生成 AST：**
编译器扫描模板字符串，构建出描述层级关系的抽象语法树（AST 对象）。
2. **优化器标记静态节点（Optimize / 静态提升）：**
* 编译器深度检查 `<header class="title">` 及其子标签 `<h2>`、`<p>`，发现它们**没有任何动态插值或指令绑定**。
* 优化器将其打上 `static: true` 标记（在 Vue 3 中会进行**静态提升 Static Hoisting**，直接提到渲染函数外部只生成一次 VNode）。
* 包含 `{{ user.name }}` 和 `{{ levelTitle }}` 的 `<p>` 被打上动态标记（**Patch Flag**），后续 Diff 仅比对该节点。


3. **代码生成器生成 `render` 函数：**
将优化后的 AST 转换为能够生成虚拟 DOM 的 `render` 函数代码。

---

### 阶段 2：组件初始化与依赖收集（Track）

组件挂载执行时：

1. **响应式代理建立：**
* `user` 通过 `new Proxy(...)` 代理整个对象。此时给它新增 `user.role` 或删除属性，Proxy 的 `set` / `deleteProperty` 均能实时拦截（彻底解决了 Vue 2 `Object.defineProperty` 无法监听动态新增/删除属性的问题）。
* `score` 被包装为一个 `ref` 对象，内部拦截 `.value` 的读写。


2. **初次渲染触发依赖收集：**
* Vue 创建该组件专属的**渲染副作用（Render Effect）**。
* 执行 `render` 函数生成 VNode，读取 `user.name` 和 `levelTitle`：
* 读取 `user.name` $\rightarrow$ 触发 Proxy 的 `get` 拦截器 $\rightarrow$ `name` 的专属管家 `Dep` 记录下当前渲染 Effect。
* 读取 `levelTitle.value` $\rightarrow$ 计算属性发现自身 `dirty = true`，首次运行 Getter 函数（打印出日志），得到“初级会员”，将结果存入 `value` 缓存并把 `dirty` 设为 `false`。同时，计算属性内部读取了 `score.value`，将计算属性的 Effect 注册到了 `score` 的 `Dep` 管家。
* 模板渲染还要用到 `levelTitle`，于是当前组件的渲染 Effect 也订阅了 `levelTitle`。




3. **`watch` 收集依赖：**
* 执行 `watch(score, ...)` 时，Vue 主动读取了一次 `score.value`，`score` 的专属 `Dep` 也将该 `watch` 的副作用回调收入小本本。


4. **生成真实 DOM：**
* 生成虚拟 DOM（VNode）树，经过 Patch 挂载到浏览器真实 DOM 上。



---

### 阶段 3：用户交互、数据变更与派发更新（Trigger）

当用户点击按钮触发 `upgrade()` 时：

1. **Proxy 拦截属性新增：**
* 执行 `user.role = 'VIP'`：因为 `user` 是 Proxy 代理对象，即使 `role` 是初始不存在的新属性，修改依然会被 Proxy 的 `set` 拦截器精确捕获。


2. **触发派发更新（Trigger）：**
* 执行 `score.value = 150`，紧接着又执行 `score.value = 220`。
* 修改 `.value` 触发 `score` 的 `set` 拦截器，`score` 的 `Dep` 吹响哨子：
* **通知 `watch`：** 将 `watch` 回调推入执行计划。
* **通知 `computed`：** 计算属性 Watcher 收到通知，但**并不立即重算**，而是仅仅将自身标志位修改为 **`dirty = true`**（懒计算）。
* **通知组件渲染 Effect：** 渲染 Effect 准备重新渲染。




3. **异步更新队列缓冲（Async Update Queue）：**
* 虽然 `score.value` 在同步代码中被修改了两次（150 和 220），但 Vue **不会**立刻同步刷新真实 DOM。
* 渲染 Effect 和 Watcher 会被推入一个微任务异步队列中，并依据组件 ID 进行**自动去重**（多次修改只保留一次排队）。


4. **同步读取 DOM 失败的原因：**
* 代码紧接着执行 `document.getElementById('level-display').innerText`。
* **此时当前同步任务还未结束，微任务更新队列尚未执行，真实 DOM 依然是挂载时的旧结构**。
* 控制台输出仍为旧内容：`当前用户：小明 | 等级称号：初级会员`。


5. **事件循环与 `nextTick` 生效：**
* 执行到 `await nextTick()` 时，代码向微任务队列中注册了一个等待点。
* 同步代码执行完毕，浏览器事件循环（Event Loop）开始清空微任务队列：
1. 首先执行 Vue 内部的更新队列：重新执行 `render` 函数。
2. 此时访问 `levelTitle`，发现它的 `dirty === true`，触发重新计算，返回“高级会员”，再次将 `dirty` 置为 `false`。
3. 虚拟 DOM 对比（Diff）：因为静态头部被打上了静态提升标记，Vue **直接跳过对静态头部的比对**，仅针对打上 Patch Flag 的动态 `<p>` 节点进行最小化局部更新。
4. 真实 DOM 完成更新。
5. 紧随渲染微任务之后，`nextTick` 的 Promise 决议（Resolve）。


* 代码恢复执行，再次读取 DOM：成功拿到最新的 `当前用户：小明 | 等级称号：高级会员`。