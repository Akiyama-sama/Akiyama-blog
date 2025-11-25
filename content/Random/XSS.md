---
date: 2025-11-22
tags: 
---
全名为Cross-Sites-Script跨站脚本攻击

**核心原理：** 攻击者在你的网页里**插入了恶意的 JavaScript 代码**。当其他用户访问时，这段代码在用户的浏览器里执行，窃取 Cookie、Session ID 或重定向页面。

**防御错措施**：
- 将输出转义：`<script>`转为`&script`之类的，`"` 转换为 `&quot;`
- 使用CSP（Content Security Policy）：在Ngnix中配置好不在白名单中的js代码不会被执行
- 将Cookie设置为HttpOnly，JavaScript（包括黑客注入的脚本）就无法通过 `document.cookie` 读取到该 Cookie。
