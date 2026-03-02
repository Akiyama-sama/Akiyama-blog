## 代码质量
- 除非绝对必要，不使用 `any`
- 外部 API 的类型优先在 node_modules 中查找，不要猜
- 绝不使用内联导入，不使用 `await import("./foo.js")`，不在类型位置使用 `import("pkg").Type`，不使用动态导入类型，只用顶层标准导入
- 不允许通过移除或降级代码来规避旧依赖导致的类型错误，应该升级依赖
- 移除看似有意保留的功能或代码前必须先询问
- 禁止硬编码键位判断，例如 `matchesKey(keyData, "ctrl+x")`，所有键位绑定必须可配置，并在匹配对象中添加默认值（`DEFAULT_EDITOR_KEYBINDINGS` 或 `DEFAULT_APP_KEYBINDINGS`）
