---
tags:
  - #pernamant
  - 前端实习挑战
  - 前端
  - HTML
---
defer和async都能让浏览器在解析HTML的过程中，异步加载js文件，不会**阻塞HTML解析**，主要不同在于：
js执行时机不同：
	defer是所有的HTML解析完毕后再执行js文件
	async是哪一个js文件先加载完毕后就开始执行那个js文件
	
![NhkvosHR_1603547262709-5029c4e4-42f5-4fd4-bcbb-c0e0e3a40f5a_mianshiya.png](https://pic.code-nav.cn/mianshiya/question_picture/markdown/NhkvosHR_1603547262709-5029c4e4-42f5-4fd4-bcbb-c0e0e3a40f5a_mianshiya.png)
## 适用场景

async：适用于不依赖或者不被依赖的模块（这样小的单独的模块执行时间少，加载快），例如第三方工具，广告脚本
defer：适用于需要HTML解析完毕后再执行js的脚本，如依赖DOM的脚本，有依赖的脚本

## 影响
1）性能优化：用async和defer可以让HTML的解析和js的加载异步进行，特别是碰到js文件很大的时候可以显著提升网页加载速度
2）减少首屏加载时间，这两个标签不会阻塞HTML的解析，可以帮助减少[[首次内容绘制（FCP）]]和[[首次有意义绘制（FMP）]]的时间







# reference
[[HTML 的 script 标签中 defer 和 async 有什么区别？ - 前端 HTML 面试题 - 面试鸭 - 程序员求职面试刷题神器]]