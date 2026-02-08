---
date: 2025-12-20
tags: 
---

---

# Feature 开发文档（V6.0 - 切片化 Store + Actions Hook 意图层）

## 一、Feature 定义

一个 Feature 是一个独立的业务模块（如：`auth`, `discover`, `chat`）。遵循“高内聚、低耦合”，包含该业务所需的 UI、逻辑、状态与类型。

---

## 二、目录结构（V6.0）

1. **顶层 Feature 组件**：入口组件（如 `discover.tsx`），负责业务布局组装。
2. **components/**：子组件，仅负责 UI 渲染与事件绑定（调用 actions）。
3. **hooks/**：只存放与 TanStack Query 相关内容，以及 **业务意图 Actions Hook**

   * `useGetXXX` / `useXXXMutation`（Orval 或手写 Query/Mutation）
   * `use[Feature]Actions.ts`：**唯一的业务意图层（所有 handle/流程都在此）**
4. **stores/**：Zustand Store：**仅存放切片化 state + 原子 set 函数**（无 handlers）
5. **types/**：DTO、业务模型、store 接口、UI 相关类型。
6. **index.ts**：统一出口。

---

## 三、分层职责（核心规范）

### 1）Store：Sliced State & Atomic Setters（仅此而已）

* **命名规范**：名词切片（如 `searchParams`, `detail`）
* **包含内容**

  * State：基础变量
  * Actions：只允许原子 `setXXX`（或纯更新函数）
* **严禁内容**

  * `if/else` 业务判断
  * `toast`
  * 路由跳转
  * 异步请求 / `mutateAsync`
  * 跨切片编排（除了简单合并更新）

> Store 的定位：**“Feature 内的本地 UI 状态容器”**，而不是业务流程层。

---

### 2）Actions Hook：唯一意图层（业务流程/副作用/跨切片编排）

* 文件：`hooks/use[Feature]Actions.ts`
* **命名规范**：对外暴露的动作用动词：`login`, `logout`, `sendCode`, `openDetail`
* **职责**

  * 调用 Orval 的 Query/Mutation hooks（`mutateAsync`）
  * 做业务校验 / 权限拦截
  * 统一 toast、路由跳转
  * 调用 store 的原子 set 完成多状态联动
  * 处理异步串联（verify -> change password 等）
* **强约束**

  * **组件层禁止写业务流程**
  * **Store 禁止写业务流程**
  * 所有业务流程必须集中在 `use[Feature]Actions()`，确保可读性与可追踪性

---

### 3）组件层：无脑渲染 + 调用 actions

* 组件只做：

  * 读取 store slice 状态
  * 调用 actions hook 暴露的方法
* 组件严禁：

  * 登录校验、权限判断
  * 复杂数据处理（filter/split/merge 等）
  * 直接调用 `useMutation().mutateAsync`（必须由 actions hook 封装）

---

## 四、Feature 开发流程（V6.0）

### Step 1：types/ 与 hooks/（Orval）准备

* DTO/Response 类型由 Orval 生成优先
* Query/Mutation hooks 放在 `hooks/`，例如 `hooks/orval.ts` 或按域拆分

### Step 2：stores/ 按切片写 UI State

```ts
export const useDiscoverStore = create((set) => ({
  searchParams: {
    query: '',
    page: 1,
    setQuery: (query: string) =>
      set((s) => ({ searchParams: { ...s.searchParams, query } })),
    setPage: (page: number) =>
      set((s) => ({ searchParams: { ...s.searchParams, page } })),
  },

  detail: {
    isOpen: false,
    selectedId: null as string | null,
    setOpen: (isOpen: boolean) =>
      set((s) => ({ detail: { ...s.detail, isOpen } })),
    setSelectedId: (id: string | null) =>
      set((s) => ({ detail: { ...s.detail, selectedId: id } })),
  },
}))
```

### Step 3：hooks/use[Feature]Actions.ts 写所有业务意图

> 你不再需要 handlers 的签名与 deps 注入样板代码。类型直接来自 Orval 的 hook。

```ts
import { useDiscoverStore } from '../stores/discover-store'
import { useSearchEnginesMutation } from './orval'
import { useNavigate } from '@tanstack/react-router'
import { toast } from 'sonner'
import { useAuthStore } from '@/features/auth/stores/auth-store'

export function useDiscoverActions() {
  const navigate = useNavigate()

  // 只拿 store 的原子 set（避免整 store 订阅导致重渲染）
  const setQuery = useDiscoverStore((s) => s.searchParams.setQuery)
  const setPage = useDiscoverStore((s) => s.searchParams.setPage)
  const setSelectedId = useDiscoverStore((s) => s.detail.setSelectedId)
  const setOpen = useDiscoverStore((s) => s.detail.setOpen)

  const { user } = useAuthStore((s) => s.auth) // 示例：跨 feature 读取

  const searchMutation = useSearchEnginesMutation()

  return {
    executeSearch: async (query: string) => {
      if (!user) {
        toast.error('请先登录')
        navigate({ to: '/login' })
        return
      }

      setQuery(query)
      setPage(1)

      await searchMutation.mutateAsync({ data: { query, page: 1 } })
    },

    openDetail: (engineId: string) => {
      setSelectedId(engineId)
      setOpen(true)
    },

    closeDetail: () => {
      setOpen(false)
      setSelectedId(null)
    },
  }
}
```

---

## 五、组件装配写法（V6.0）

```tsx
const searchParams = useDiscoverStore((s) => s.searchParams)
const detail = useDiscoverStore((s) => s.detail)
const actions = useDiscoverActions()

<Input
  value={searchParams.query}
  onChange={(e) => searchParams.setQuery(e.target.value)}
/>

<Button onClick={() => actions.executeSearch(searchParams.query)}>
  搜索
</Button>

<Dialog open={detail.isOpen} onOpenChange={detail.setOpen} />
```

---

## 六、核心开发守卫（Guardrails - V6.0）

| 范畴                    | 归宿                        | 命名规范                           | 判定逻辑                 |
| --------------------- | ------------------------- | ------------------------------ | -------------------- |
| 服务端数据（Query/Mutation） | hooks/                    | `useGetXXX` / `useXXXMutation` | 后端数据获取与提交            |
| 业务意图/流程/副作用           | hooks/use[Feature]Actions | 动词：`login/sendCode/openDetail` | 判断、异步、toast、跳转、跨切片联动 |
| 聚合参数/状态               | stores/（slice）            | 名词切片                           | 变量 + 原子 set          |
| 原子变更                  | slice actions             | `setXXX`                       | 单值 set / 纯更新         |
| 极简局部 UI               | 组件 useState               | -                              | 仅当前组件使用              |

---

## 七、API 调用原则（V6.0）

1. **Store 内禁止**引入 TanStack Query hooks（`useQuery/useMutation`）
2. **组件内禁止**直接 `mutateAsync`（必须走 actions）
3. Actions Hook 可以：

   * 调用 Orval hooks（mutation/query）
   * 调用 store setters
   * 做校验/跳转/toast
4. Query invalidation / toast 允许放在 Actions Hook（集中可读）

---

## 八、（强烈建议）Actions Hook 书写规范（避免变成巨型文件）

为避免你担心的“actions hook 变大”，给出硬规范：

1. **按用例分组**：一个文件内按 `AuthFlow / PasswordFlow / ProfileFlow` 分段
2. **每个 action 不超过 ~30 行**：超出就提取成同文件内的 `async function` 私有函数（仍在 actions 文件内，保持集中）
3. **Actions 返回对象必须稳定**（性能/可读性）

   * 使用 `useMemo` 包装返回对象
   * 大型 action 用 `useCallback`

> 你也可以先不做 memo，等性能有问题再加；但 “只订阅 setters” 建议立即执行。

---

## 九、AI 开发提示语（V6.0）

> “请按照 **V6.0 切片化 Store + Actions Hook 意图层** 开发此 Feature。
>
> 1. Store 只允许 state + 原子 set（纯更新），禁止 handlers、业务判断、异步、toast、跳转。
> 2. 所有业务流程（if/else、mutateAsync、toast、跳转、跨切片联动）必须集中写在 `hooks/use[Feature]Actions.ts` 中。
> 3. 组件层只渲染与绑定，禁止业务校验与直接 mutateAsync。”

---

## 十、（可选）统一出口 index.ts

```ts
export * from './stores/discover-store'
export * from './hooks/useDiscoverActions'
export * from './types'
```

---
