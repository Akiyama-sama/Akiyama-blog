---
date: 2026-05-11
tags:
aliases:
---
全称为 Largest Content Paint，表示为**最大可见内容/核心内容**完成渲染的时间

[[首次内容绘制（FCP）|FCP]]关心内容是否渲染出来了，LCP 关心核心内容的渲染时间

LCP 差的核心原因：

- 服务器响应时间差 -> 使用 CDN
- CSS/JS阻塞 ->
	-  SSR 或预渲染
	-  减少 hydration 负担
- 资源加载速度过大 ->
	- 图片压缩+webp
	- 使用 CDN
	- [[响应式图片]]
