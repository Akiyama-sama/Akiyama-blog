---
date: 2025-10-21
tags: 
---
● 内存泄漏的根本原因分析

  旧版代码存在的问题

  用户提供的旧版代码中，监听函数 handleLyricsActivity 被定义为一个 useCallback 函数，并作为依赖项传递给了 useEffect：

```tsx
  const handleLyricsActivity = useCallback(...) // 依赖 [isAutoScrolling, syncedLyrics]

  useEffect(() => {
    document.addEventListener('player/positionChange', handleLyricsActivity);

    return () => document.removeEventListener('player/positionChange', handleLyricsActivity);
  }, [handleLyricsActivity]); // 使用 handleLyricsActivity 作为依赖
```

  这种模式会导致内存泄漏，原因如下：
  1. handleLyricsActivity 函数依赖于 [isAutoScrolling, syncedLyrics]，当这些依赖发生变化时，useCallback 会返回一个新的函数引用。
  2. 每次 handleLyricsActivity 变化时，useEffect 都会执行，先移除旧的监听器，再添加新的监听器。
  3. 关键问题：useCallback 返回的是新的函数引用，而移除监听器时需要使用与添加时完全相同的函数引用。当函数引用变化时，removeEventListener       
  无法找到要移除的旧监听器，导致旧监听器永远留在 document 上。

  React 中的函数引用问题

  在 React 中，每次组件渲染时，函数都会被重新创建。useCallback 可以记忆函数，但当依赖变化时仍会返回新的引用。当 useEffect
  的依赖变化时，旧的 useEffect 清理函数会执行，但此时要移除的监听器已经被更新为新的引用，导致清理失败。

● 修复方案：使用 useRef 解决问题

  修复后的代码

  修复后的代码使用了 useRef 来存储最新的事件处理函数，并使用一个稳定的中间函数来调用它：

```tsx
  const activityHandlerRef = useRef<(e: Event) => void>();

  useEffect(() => {
    activityHandlerRef.current = (e: Event) => {
      // 事件处理逻辑
    };
  }, [isAutoScrolling, syncedLyrics]);

  useEffect(() => {
    const listener = (e: Event) => activityHandlerRef.current?.(e);

    document.addEventListener('player/positionChange', listener);

    return () => document.removeEventListener('player/positionChange', listener);
  }, []); // 空依赖数组，仅在组件挂载/卸载时执行
```

  为什么这样能解决内存泄漏？

  1. 稳定的函数引用：listener 是一个稳定的中间函数，它的引用不会改变（因为 useEffect 的依赖数组是空的）。
  2. 更新机制：当 isAutoScrolling 或 syncedLyrics 变化时，第一个 useEffect 会更新 activityHandlerRef.current
  的值，使其指向最新的事件处理函数。
  1. 清理保证：第二个 useEffect 在组件卸载时，始终能够正确移除 listener（因为 listener 的引用始终相同）。

● 未来避免内存泄漏的启示

  1. 理解事件监听的移除机制

  - 向 DOM 或全局对象（如 window、document）添加事件监听器时，必须确保能在组件卸载或不再需要时移除它们。
  - removeEventListener 必须使用与 addEventListener 完全相同的函数引用才能生效。

  2. 正确使用 React 的依赖管理

  - 避免在 useEffect 中直接使用依赖变化的函数，除非这些函数不依赖于组件状态或 props。
  - 对于依赖频繁变化的事件处理函数，推荐使用 useRef + 中间函数的模式。

  1. 优先使用 React 提供的受控事件

  - 尽可能使用 React 组件内部的 onClick、onChange 等事件属性，而非直接操作 DOM。这些事件会被 React 自动管理，无需手动清理。

  2. 组件卸载时的清理

  - 对于任何在组件外部创建的资源（如事件监听、定时器、WebSocket 连接等），都必须在组件卸载时清理。

  3. 代码审查关注的重点

  - 检查所有 useEffect 中是否存在未正确清理的资源。
  - 检查事件监听的移除是否使用了与添加时相同的函数引用。

● 总结

  内存泄漏原因

  旧版代码中的事件监听器没有被正确移除，因为 handleLyricsActivity 函数依赖于 [isAutoScrolling,
  syncedLyrics]，当这些依赖变化时，函数引用也会变化，导致 removeEventListener 无法找到要移除的旧监听器，从而造成内存泄漏。

  修复原理

  修复后的代码使用 useRef 存储最新的事件处理函数，并使用一个稳定的中间函数 listener 来调用它。这样，addEventListener 和 removeEventListener    
   始终使用相同的函数引用 listener，确保了监听器能在组件卸载时被正确移除。

  预防措施

  1. 理解事件监听的移除机制
  2. 正确使用 React 的依赖管理
  3. 优先使用 React 提供的受控事件
  4. 组件卸载时清理所有外部资源
  5. 代码审查关注清理逻辑 