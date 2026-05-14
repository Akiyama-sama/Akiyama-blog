---
tags:
  - #pernamant
  - 前端实习挑战
  - 前端
  - HTML
---
## 主要作用

srcset 属性可为同一图像提供多个文件源和各自的分辨率描述符。浏览器会根据当前设备的屏幕尺寸（如宽度）和像素密度（如 DPI ）来选择最合适的图像源进行加载。这样，就能 **获得与其设备相匹配的最佳图像体验，而不必加载比所需更大或更高分辨率的图像**，从而节省带宽并加快页面加载速度。用法如下：

```html
<img 
  src="small.jpg" 
  srcset="small.jpg 500w, 
  medium.jpg 1000w, 
  large.jpg 1500w" 
  alt="示例图片"
/>
```





# reference
[[HTML 中，img 标签 srcset 属性的作用是什么？ - 前端 HTML 面试题 - 面试鸭 - 程序员求职面试刷题神器]]