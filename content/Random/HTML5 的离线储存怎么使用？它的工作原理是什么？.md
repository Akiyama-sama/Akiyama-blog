---
tags:
  - #pernamant
  - 前端实习挑战
  - 前端
  - HTML
---
HTML5离线缓存是指的是支持开发者允许某些文件（js，html，css等等）缓存，让用户在无网络的情况下使用web服务

## 工作原理
1）缓存清单文件：首先，需要创建一个清单文件（通常以 .appcache 扩展名保存），在这个文件中列出要缓存的资源。这个文件必须声明正确的 MIME 类型，即 text/cache-manifest。
2）引用清单文件：在 HTML 页面的 `<html>` 标签中使用 manifest 属性引用这个清单文件。例如：

```html
<html manifest="example.appcache">
```

3）结构清单文件：清单文件的结构通常如下：

```dts
# 2024-01-01 v1.0.0
CACHE:
/css/style.css
/js/app.js
/images/logo.png

NETWORK:
*

FALLBACK:
/ /offline.html
```

其中：

- CACHE：后面列出的文件在首次下载后会被浏览器缓存，即使用户离线也可以访问。
- NETWORK：指定的资源永远不会被缓存，总是从服务器请求，\*表示默认情况下所有其他资源都需要网络连接。
- FALLBACK：提供备用页面的路径，如果用户请求的资源无法访问，将返回这个备用页面。



# reference
[[HTML5 的离线储存怎么使用？它的工作原理是什么？ - 前端 HTML 面试题 - 面试鸭 - 程序员求职面试刷题神器]]