---
date: 2025-12-20
tags: 
---

# Feature 开发文档 (V4.0 - 切片化与意图驱动模式)

## 一、 Feature 定义
一个 Feature 是一个独立的业务模块（如：`auth`, `discover`, `chat`）。它遵循“高内聚，低耦合”原则，包含该业务所需的所有 UI、逻辑、状态与类型。
## 二、 目录结构

1. **顶层 Feature 组件**：入口组件（如 `discover.tsx`），负责业务布局组装。
2. **components/**：功能拆分的子组件，仅负责 UI 渲染与数据/事件绑定。
3. **hooks/**：**仅存放 TanStack Query 相关 Hook**。负责服务端数据获取、缓存与同步。
4. **stores/**：存放 Zustand Store。包含 **Sliced State** 与 **Global Handlers**。
5. **types/**：存放该 Feature 相关的类型定义（DTO、业务模型、Store 接口）。
6. **index.ts**：统一出口，供外部 Feature 导入。


---

## 三、 Store 架构分层（核心规范）

在 `stores/[name]-store.ts` 中，必须按照以下“切片与编排”逻辑组织：
### 1. 切片化状态 (Sliced State & Atomic Actions)

将**状态**与其对应的**原子操作**聚合在同一个命名切片中。
- **命名规范**：使用名词指代业务块（如 `searchParams`, `engineDetail`）。
- **包含内容**：
    - **State**：基础变量。
    - **Actions**：如果与修改基础变量相关就以 `setXXX` 命名的原子 setter 函数。如果是其他逻辑就自行命名
- **准则**：切片内的 Actions 必须是**纯函数**，严禁包含业务判断或异步请求。


### 2. 业务意图层 (Global Handlers)

- **命名规范**：统一以 `handle[动作]` 命名（如 `handleExecuteSearch`）。
- **职责**：作为指挥官，**编排**各个切片中的原子 Actions。
- **适用场景**：
    - **业务拦截**：校验登录状态（`useAuthStore`）、权限判断。
    - **异步副作用**：调用接口（Mutate）、弹出 `toast`、路由跳转。
    - **多状态联动**：一次交互需要同时更新多个切片状态。

---
## 四、 Feature 开发流程
### 1. 数据规划
- 在 `types/` 补齐类型，在 `hooks/` 封装 `useGetXXX`（TanStack Query）。
### 2. Store 编写模板 (Zustand)
```TypeScript
export const useDiscoverStore = create((set, get) => ({
  // --- 切片 1：搜索参数 (高聚合) ---
  searchParams: {
    query: '',
    page: 1,
    setQuery: (query) => set(s => ({ searchParams: { ...s.searchParams, query } })),
    setPage: (page) => set(s => ({ searchParams: { ...s.searchParams, page } })),
  },

  // --- 切片 2：详情控制 ---
  detail: {
    isOpen: false,
    selectedId: null,
    setOpen: (isOpen) => set(s => ({ detail: { ...s.detail, isOpen } })),
    setSelectedId: (id) => set(s => ({ detail: { ...s.detail, selectedId: id } })),
  },

  // --- 业务编排：Handlers ---
  handlers: {
    handleSearch: (query) => {
      const { user } = useAuthStore.getState().auth;
      if (!user) return showErrorData('请先登录'); // 业务拦截
      
      const { setQuery, setPage } = get().searchParams;
      setQuery(query); // 调用原子 Action
      setPage(1);
    },
    handleOpenDetail: (engine) => {
      get().detail.setSelectedId(engine.id);
      get().detail.setOpen(true); // 多状态联动
    }
  }
}))
```

### 3. 组件装配原则

- **UI 绑定**：组件只关心“展示什么”和“发生了什么”。
- **禁止逻辑渗透**：组件内严禁出现 `if (!user)` 或复杂的 `split/filter` 数据处理逻辑。
- **写法示例**：
    - 简单受控：`<Input value={searchParams.query} onChange={e => searchParams.setQuery(e.target.value)} />`
    - 业务触发：`<Button onClick={() => handlers.handleSearch(query)} />`

---
## 五、 核心开发守卫 (Guardrails)

|**范畴**|**归宿**|**命名规范**|**AI 判定逻辑**|
|---|---|---|---|
|**服务端数据**|**Hooks (Query)**|`useGetXXX`|只要是后端接口返回的数据|
|**聚合参数/状态**|**Store (Slice)**|`nounSlice`|相关的变量及其 set 动作|
|**原子变更**|**Slice Actions**|`setXXX`|仅仅是单值的 `set` 操作|
|**业务逻辑/流程**|**Store Handlers**|`handleXXX`|包含判断、异步、提示、或跨切片操作|
|**极简局部 UI**|**useState**|-|只有当前组件自己用的状态（如 `isHovered`）|

---

## 六、 AI 开发提示语 (Prompt Enhancement)

> “请按照 **V4.0 切片化架构** 开发此 Feature。
> 
> 1. 状态与原子 `set` 函数必须聚合在对应的切片对象中（如 `searchParams`）。
>     
> 2. 所有涉及 `if/else`、`toast`、`mutate` 或跨切片的操作，必须封装在顶层的 `handlers` 对象中，并以 `handle` 开头。
>     
> 3. 确保组件层是‘无脑渲染’的，不包含任何业务校验逻辑。”
>