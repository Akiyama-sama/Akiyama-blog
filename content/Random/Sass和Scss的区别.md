---
tags:
  - '#pernamant'
---
Sass全称为：css预处理器，意在规定一种写法，让开发者更好写css，写好后会转换为css

[[Scss]]
支持css原生写法，在css基础之上添加了嵌套写法，由: {}组成
```scss
.container {
  width: 80%;
  margin: 0 auto;
  padding: 20px;

  .header {
    background-color: $primary-color;
    color: white;
    padding: 10px;
  }

  .content {
    margin-top: 20px;
  }
}
```

[[Sass]]
不支持css原生写法，由缩进组成
```sas
.container
  width: 80%
  margin: 0 auto
  padding: 20px

  .header
    background-color: $primary-color
    color: white
    padding: 10px

  .content
    margin-top: 20px

```



# reference
