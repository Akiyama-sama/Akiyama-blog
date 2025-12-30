---
date: 2025-12-13
tags:
  - React
---
### 1. 基础设施：类型与 Query Key 工厂

_最佳实践：不要在 Hook 里手写字符串 key，使用工厂模式统一管理。_


```TypeScript
// src/features/tasks/queries.ts
import { keepPreviousData, queryOptions } from '@tanstack/react-query'

// --- Types (定义清晰的接口) ---
export interface Task {
  id: string
  title: string
  status: 'todo' | 'in-progress' | 'done'
  assignee?: string
  updatedAt: string
}

export interface TaskFilters {
  status?: string
  page?: number
}

// --- Query Key Factory (核心：单一真值来源) ---
// 解决了 "忘记这个 key 是什么" 和 "失效时不确定影响范围" 的问题
export const taskKeys = {
  all: ['tasks'] as const,
  lists: () => [...taskKeys.all, 'list'] as const,
  list: (filters: TaskFilters) => [...taskKeys.lists(), { ...filters }] as const,
  details: () => [...taskKeys.all, 'detail'] as const,
  detail: (id: string) => [...taskKeys.details(), id] as const,
}
```

### 2. 读操作 Hook：关注数据转换与防抖

_最佳实践：利用 `select` 进行数据清洗，利用 `placeholderData` 提升列表体验。_



```TypeScript
// src/features/tasks/useTasks.ts
import { useQuery } from '@tanstack/react-query'
import { taskKeys, Task, TaskFilters } from './queries'
import { fetchTasks } from './api' // 假设这是纯粹的 fetcher

export const useTasks = (filters: TaskFilters) => {
  return useQuery({
    // 1. 使用 Key Factory 生成 Key
    queryKey: taskKeys.list(filters),
    
    // 2. QueryFn 应该只负责请求，不处理业务逻辑
    queryFn: () => fetchTasks(filters),

    // 3. 最佳实践：placeholderData
    // 在切换分页或筛选时，保留上一次的数据直到新数据到来，避免 loading 闪烁
    placeholderData: keepPreviousData,

    // 4. 最佳实践：staleTime
    // 服务端数据多久被认为是“陈旧”的？默认是0。
    // 设置合理的 staleTime 可以减少后台静默请求的频率
    staleTime: 1000 * 60 * 1, // 1分钟

    // 5. 最佳实践：select (数据转换层)
    // 这里的逻辑只会在 data 变化时运行。
    // 它可以把后端生硬的字段转为前端友好的结构，实现逻辑解耦。
    select: (data) => {
      return {
        raw: data,
        // 例如：预计算统计数据，或者处理时间格式
        totalCount: data.length,
        hasCompletedTasks: data.some(t => t.status === 'done'),
        // 甚至可以返回一个 Map 以便 O(1) 查找
        tasksMap: new Map(data.map(t => [t.id, t]))
      }
    }
  })
}
```

### 3. 写操作 Hook：解耦 UI 与乐观更新

_最佳实践：Mutation 不决定义 UI 行为（不弹窗），但处理复杂的缓存一致性逻辑。_



```TypeScript
// src/features/tasks/useUpdateTask.ts
import { useMutation, useQueryClient } from '@tanstack/react-query'
import { taskKeys, Task } from './queries'
import { updateTaskApi } from './api'

// 定义 Mutation 接收的变量
interface UpdateTaskVariables {
  id: string
  data: Partial<Task>
}

export const useUpdateTask = () => {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({ id, data }: UpdateTaskVariables) => updateTaskApi(id, data),

    // --- 核心：乐观更新 (Optimistic Updates) ---
    // 这是高级 Hook 必须掌握的，极大提升用户体验
    onMutate: async ({ id, data: newStats }) => {
      // A. 取消正在进行的查询，防止旧数据覆盖新数据
      await queryClient.cancelQueries({ queryKey: taskKeys.detail(id) })
      await queryClient.cancelQueries({ queryKey: taskKeys.lists() })

      // B. 获取当前的快照（用于回滚）
      const previousTask = queryClient.getQueryData<Task>(taskKeys.detail(id))

      // C. 乐观地更新缓存 (立即修改 UI，不等服务器响应)
      // 1. 更新详情
      if (previousTask) {
        queryClient.setQueryData(taskKeys.detail(id), { ...previousTask, ...newStats })
      }
      
      // 2. (可选) 更新列表中的该项
      queryClient.setQueriesData({ queryKey: taskKeys.lists() }, (old: Task[] | undefined) => {
        if (!old) return []
        return old.map(t => t.id === id ? { ...t, ...newStats } : t)
      })

      // D. 返回 context 供 onError 使用
      return { previousTask }
    },

    // 如果失败，回滚数据
    onError: (err, newTodo, context) => {
      if (context?.previousTask) {
        queryClient.setQueryData(taskKeys.detail(newTodo.id), context.previousTask)
      }
    },

    // --- 核心：解耦 UI ---
    // 这里**不要**写 showSuccessMessage()
    // 这里只处理 "数据一致性"
    onSettled: (data, error, variables) => {
      // 无论成功失败，都让相关查询失效，确保获取服务器最新状态
      queryClient.invalidateQueries({ queryKey: taskKeys.detail(variables.id) })
      queryClient.invalidateQueries({ queryKey: taskKeys.lists() })
    }
  })
}
```

### 4. UI 层调用：策略注入

_最佳实践：在组件中决定如何反馈（Toast/Redirect），而不是在 Hook 中。_



```TypeScript
// src/components/TaskBoard.tsx
import { useTasks } from '@/features/tasks/useTasks'
import { useUpdateTask } from '@/features/tasks/useUpdateTask'
import { toast } from '@/components/ui/toast' // 假设的 UI 库

export const TaskBoard = () => {
  const [filter, setFilter] = useState({ page: 1 })
  
  // 使用 Read Hook
  // data 已经是经过 select 转换过的结构
  const { data, isPending, isPlaceholderData } = useTasks(filter)
  
  // 使用 Write Hook
  const updateMutation = useUpdateTask()

  const handleMarkDone = (taskId: string) => {
    updateMutation.mutate(
      { id: taskId, data: { status: 'done' } },
      {
        // ✨✨ 关键点：UI 逻辑在这里注入 ✨✨
        onSuccess: () => {
          toast.success("任务状态已更新！")
          // 这里甚至可以做路由跳转
        },
        onError: (error) => {
          toast.error(`更新失败: ${error.message}`)
        }
      }
    )
  }

  if (isPending) return <div>Loading...</div>

  return (
    <div style={{ opacity: isPlaceholderData ? 0.5 : 1 }}>
      <h1>任务列表 (总数: {data?.totalCount})</h1>
      {data?.raw.map(task => (
        <TaskCard key={task.id} task={task} onToggle={() => handleMarkDone(task.id)} />
      ))}
    </div>
  )
}
```