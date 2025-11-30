---
date: 2025-11-30
tags:
  - 前端
---
# 第一阶段：网络请求链路 (The Network Journey)

当你在地址栏输入 URL 并按下回车后，浏览器主进程（Browser Process）会接管任务：

## 1. URL 解析与缓存检查

- **解析**：浏览器判断输入的是 URL 还是搜索关键字。如果是 URL，会检查协议（http/https）和合法性。
- **HSTS**：如果网站在 HSTS 列表中，浏览器强制将 http 重定向为 https。
- **缓存检查**：浏览器会先查看**强缓存**（`Cache-Control` / `Expires`）。
    - 如果命中且未过期，直接使用缓存，不发网络请求（状态码 200 form memory/disk cache）。
    - 如果没命中或过期，进入下一步。
 
## 2. DNS 解析 (Domain Name System)

目标是将域名（https://www.google.com/search?q=google.com）转换为 IP 地址（142.250.x.x）。

- **查找链路**：浏览器缓存 -> 操作系统缓存 (hosts) -> 路由器缓存 -> ISP DNS 服务器 -> 根域名/顶级域名服务器（递归或迭代查询）。
## 3. 建立 TCP 连接 (Three-way Handshake)

拿到 IP 后，浏览器通过 TCP 协议与服务器建立可靠连接（三次握手）：
1. **SYN**：客户端发送“我想建立连接”。
2. **SYN + ACK**：服务端回复“好的，我也准备好了”。
3. **ACK**：客户端回复“那我们开始吧”。

## 4. TLS/SSL 握手 (仅 HTTPS)：[[SSL TLS]]

如果是 HTTPS，在 TCP 建立后，还需要进行 TLS 握手以确立加密通信：

- **协商**：双方确定加密套件（如 TLS 1.3）。
- **验证**：客户端验证服务端的数字证书（防止中间人攻击）。
- **密钥生成**：利用非对称加密交换信息，生成**对称加密的 Session Key**（后续数据传输全用这个 Key，速度快）。

#### 5. 发送 HTTP 请求与接收响应

- **发送**：构建 HTTP 请求报文（Request Line, Headers, Body），携带 Cookie 等信息。
- **接收**：服务器处理后返回 HTTP 响应报文。
    - **协商缓存**：如果状态码是 **304**，说明服务器告诉浏览器：“文件没变，你直接用本地旧的吧”。[[浏览器缓存策略]]
    - **重定向**：如果是 301/302，浏览器会重新发起请求到新的 Location。
    - **正常接收**：如果是 200，浏览器网络线程读取响应流（Stream），通过 `Content-Type` 判断是 HTML，准备交给渲染进程。

---

# 第二阶段：浏览器渲染链路 (The Rendering Path)

这是前端最核心的领域，主要由浏览器的**渲染进程（Renderer Process）**完成。

## 1. 解析 (Parsing)

- **构建 DOM 树**：解析 HTML 文本，将标签转换为 DOM 节点。
    - _注意_：遇到 `<script>` 标签会**阻塞** HTML 解析（除非加了 `defer` 或 `async`），因为 JS 可能会修改 DOM。
- **构建 CSSOM 树**：解析 CSS（外链或内联），计算出每个节点的具体样式规则。

#### 2. 构建渲染树 (Render Tree Construction)

- 将 DOM 树和 CSSOM 树合并。
- **过滤**：剔除不可见节点（如 `head`, `script`, `display: none` 的元素）。
- **结果**：生成一棵只包含可见元素的“渲染树”。

## 3. 布局 (Layout / Reflow)

- 计算渲染树中每个节点在屏幕上的**确切坐标**和**大小**。
- _术语_：这个过程也叫[[回流(Reflow)]]。这是性能开销很大的操作。
## 4. 绘制 (Paint / Repaint)

- 遍历布局树，生成绘制记录（Paint Records）。
- 填充像素：处理颜色、背景、边框、阴影、文本等。
- _术语_：这个过程叫[[重绘(Repaint)]]。

## 5. 分层与合成 (Layering & Compositing) —— 现代浏览器优化关键

- **分层**：浏览器会将页面拆分成多个图层（Layer）。例如 `position: fixed`、`z-index`、`transform: translate3d`、`will-change` 会提升为单独的合成层（利用 GPU 加速）。
- **光栅化 (Rasterization)**：将图层拆解为一个个小图块（Tile），并计算出每个像素点的颜色。
- **合成 (Composite)**：合成线程将所有图层按照正确的层级顺序合并，生成最终的一帧图像，发送给 GPU 展示在屏幕上。

---

# 💡 面试加分项 (Summary for Interview)

如果你想让面试官眼前一亮，最后可以总结一下这个流程对**性能优化**的启示：

 “理解这个流程的核心意义在于优化。

 1. **网络层**：我们可以通过 DNS 预解析、HTTP/2 多路复用、CDN、合理的缓存策略来减少 Time To First Byte (TTFB)。   
 2. **渲染层**：我们要尽量避免 **阻塞渲染**（JS 放底部或 defer），并减少 **回流和重绘**。
 3. **合成层**：利用 CSS3 动画（transform/opacity）触发 GPU 加速，跳过 Layout 和 Paint 阶段，直接进入 Composite 阶段，实现高性能动画。”
