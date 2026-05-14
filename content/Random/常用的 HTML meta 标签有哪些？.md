---
tags:
  - #pernamant
  - 前端实习挑战
  - 前端
  - HTML
---
1）viewport 为了响应式设计而设置，主要是为了不同设备显示比例正确

```html
<meta name="viewport" content="width=device-width, initial-scale=1.0">
```
2）description 用于描述网页内容的摘要，提高SEO

```html
<meta name="description" content="这是一个页面描述。">
```
3）keywords 设置网页关键词，尝试优化搜索结果

```html
<meta name="keywords" content="关键词1, 关键词2">
```
4）author 用于指明文档的作者名字。

```html
<meta name="author" content="作者名">
```
5）charset 声明本文档所用的字符集，一般为UTF-8

```html
<meta charset="UTF-8">
```
6）refresh 用于设置页面在一定时间后刷新或重定向到另一个URL。content="30" 表示每30秒刷新页面一次。

```html
<meta http-equiv="refresh" content="30">
```
7）robots 用于告诉搜索引擎蜘蛛不要索引这个页面，或不要跟踪页面上的链接。noindex 防止页面被索引，nofollow 防止搜索引擎跟踪链接。

```html
<meta name="robots" content="noindex, nofollow">
```


# reference
[[常用的 HTML meta 标签有哪些？ - 前端 HTML 面试题 - 面试鸭 - 程序员求职面试刷题神器]]