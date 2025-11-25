---
date: 2025-11-22
tags: 
---
Cross-Site Request Forgery跨站请求伪造

**核心原理：** **“借刀杀人”**。攻击者诱导用户点击链接，**利用用户浏览器中已保存的 Cookie**，以用户的名义向服务器发送恶意请求（如转账、改密码）。

**防御：** 使用 CSRF Token，或检查 `Referer` 来源。

