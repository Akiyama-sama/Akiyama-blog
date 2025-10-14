---
tags:
  - '#pernamant'
---

## 一、基础选择器（Basic Selectors）
#### 1. 通配选择器（Universal Selector）
- **语法**：`*`
- **作用**：匹配文档中所有元素
- **优先级**：0
- **典型应用**：全局样式重置
```css
*{
  box-sizing: border-box; /* 推荐全局设置 */
  margin: 0;             /* 常用于清除默认边距 */
}
```

#### 2. 元素选择器（Type Selector）
- **语法**：`element`
- **作用**：选择特定 HTML 标签
- **优先级**：1
```css
h2 {
  font-size: 1.5em;
}
table {
  border-collapse: collapse;
}
```

#### 3. 类选择器（Class Selector）
- **语法**：`.class-name`
- **作用**：选择具有相同类名的元素
- **优先级**：10
```html
<!-- HTML -->
<div class="alert warning"></div>
```
```css
.alert { padding: 15px; }      /* 通用警告样式 */
.warning { color: #ff0000; }   /* 特定警告类型 */
```

#### 4. ID 选择器（ID Selector）
- **语法**：`#id`
- **作用**：选择唯一元素
- **优先级**：100
```css
#main-content {
  width: 80%;
  margin: 0 auto;
}
```

## 二、属性选择器（Attribute Selectors）
#### 1. 基本属性选择
- **存在判断**：`[attr]`
```css
[disabled] {  /* 所有禁用元素 */
  opacity: 0.6;
}
<div disabled="true"/>/* 选择这个元素 */
<div disabled="false"/>/* 选择这个元素 */
```

#### 2. 精确匹配
- **语法**：`[attr="value"]`
```css
[type="email"] {  /* 精确匹配 email 输入框 */
  border-color: blue;
}

<div type="email"/> 选择这个
<div type="phone"/> 不会选择这个
```

#### 3. 部分匹配（CSS3 增强）
| 选择器             | 说明           | 示例                  |         |     |
| --------------- | ------------ | ------------------- | ------- | --- |
| `[attr^="val"]` | 以指定值开头       | `[href^="https"]`   |         |     |
| `[attr$="val"]` | 以指定值结尾       | `[src$=".png"]`     |         |     |
| `[attr*="val"]` | 包含指定值        | `[class*="btn"]`    |         |     |
| `[attr~="val"]` | 包含完整单词（空格分隔） | `[class~="active"]` |         |     |
| `[attr="val"]`  | 以指定值开头或紧接连字符 | `[lang="en"]`       | （en-US） |     |

---
## 三、[[伪类选择器]]（Pseudo-classes）

这类选择器用于选择特定的状态：例如悬浮、被访问、
格式为：
```css
其他选择器:伪类 {}
```
#### 1. 状态伪类
- **交互状态**：
  ```css
  a:link {}     /* 未访问链接 */
  a:visited {}  /* 已访问链接 */
  a:hover {}  /*悬停*/
  a:active {}  /* 指点击开始但尚未释放时的状态 */
  button:hover { transform: scale(1.05); }
  input:focus { box-shadow: 0 0 3px blue; }/*获得焦点*/

  ```

#### 2. 结构伪类
- **位置选择**：
  ```css
  li:first-child {}    /* 第一个子元素 */
  tr:nth-child(2n) {} /* 偶数行 */
  p:last-of-type {}   /* 同类型最后一个 */
  ```

- **公式应用**：
  ```css
  :nth-child(3n+1)       /* 1,4,7... */
  :nth-last-child(-n+3)  /* 最后三个 */
  ```

#### 3. 表单伪类
```css
input:checked + label { color: green; }
input:disabled { background: #eee; }
input:required { border-left: 3px solid red; }
```

---

## 四、[[伪元素选择器]]（Pseudo-elements）

伪元素器并不是选择HTML结构当中的某个或者某些元素，而是在某个元素的基础之上，去创建一个抽象的元素，而这个元素不在HTML文件内，但浏览器会像普通元素那样对待他，伪元素器就是创建并选择这种元素的选择器


格式为
```css
其他选择器::伪元素 {}
```
#### 1. 常用伪元素
```css
p::first-letter {  /* 首字母下沉效果 */
  font-size: 2em;
  float: left;
}
::selection {      /* 文本选中样式 */
  background: yellow;
}
```

#### 2. 内容生成
```css
.tooltip::after {
  content: attr(data-tip);  /* 通过 data 属性生成内容 */
  position: absolute;
  /* 其他定位样式 */
}
```

---



## 五、[[层次选择器]]（Combinators）
#### 1. 后代选择器（Descendant）
- **语法**：`A B`
- **作用**：选择 A 元素的所有 B 后代
```css
article p {  /* 选择 article 内的所有段落 */
  line-height: 1.6;
}
<article>
	<p>
		<p></p> 所有的p元素都会被选择
	</p>
</articel>
```

#### 2. 子元素选择器（Child）
- **语法**：`A > B`
- **作用**：仅选择直接子元素
```css
article > p {  /* 仅选择 nav 的直接子 ul */
  padding-left: 0;
}
<article>
	<p>这里的p元素会被选择，因为是直接子元素
		<p></p> 这里的p元素不会被选择
	</p>
</articel>

```

#### 3. 相邻兄弟选择器（Adjacent Sibling）
- **语法**：`A + B`
- **作用**：选择紧接在 A 后的第一个兄弟 B
```css
h2 + p {  /* h2 后的第一个段落 */
  margin-top: 5px;
}
```

#### 4. 通用兄弟选择器（General Sibling）
- **语法**：`A ~ B`
- **作用**：选择 A 之后的所有兄弟 B
```css
input:checked ~ .content {  /* 选中复选框后的所有内容 */
  display: block;
}
```

---



## 六、复合选择器

- 语法：元素选择器.元素选择器

```css
a.my-class {
	color:red
}
```


## 七、优先级计算规则
[[CSS选择器的权重]]
#### 1. 权重等级表
| 选择器类型      | 示例                       | 权重值  |
| ---------- | ------------------------ | ---- |
| !important | `color: red !important;` | ∞    |
| [[内联样式]]   | style="..."              | 1000 |
| ID 选择器     | `#header`                | 100  |
| 类/属性/伪类    | .btn, [type], :hover     | 10   |
| 元素/伪元素     | div, ::before            | 1    |
| 通配符/继承样式   | *                        | 0    |

#### 2. 叠加规则
```css
#nav .list li.active   /* 100 + 10 + 1 + 10 = 121 */
ul#menu li:hover       /* 100 + 1 + 1 + 10 = 112 */
```

#### 3. 特殊场景
- **群组选择器**：`.btn, .icon` 各自独立计算
- **相同权重**：后定义的样式生效
- **!important**：慎用，容易导致样式管理混乱

---

## 七、最佳实践建议
1. **避免过度使用 ID 选择器**：高优先级会导致后续维护困难
2. **合理使用类选择器**：`.card-header` 比 `div > h3` 更灵活
3. **善用属性选择器**：`[class^="col-"]` 实现栅格系统
4. **组合选择器优化性能**：`.nav li` 比 `li.nav-item` 效率更高
5. **伪元素的内容生成**：可通过 `attr()` 函数动态获取数据属性

---

## 八、综合应用示例
```html
<ul class="menu">
  <li><a href="#home">首页</a></li>
  <li class="active"><a href="#news">新闻</a></li>
  <li><a href="#about" data-badge="new">关于</a></li>
</ul>
```

```css
/* 基础样式 */
.menu {
  display: flex;
  gap: 20px;
}

/* 交互效果 */
.menu li:hover {
  background: #f5f5f5;
}

/* 激活状态 */
.menu .active > a {
  color: #2196F3;
  border-bottom: 2px solid;
}

/* 特殊标记 */
a[data-badge]::after {
  content: attr(data-badge);
  background: red;
  color: white;
  /* 更多定位样式 */
}
```

通过系统学习和实践，您将能游刃有余地使用 CSS 选择器实现精准的样式控制。建议在实际项目中多尝试组合使用不同选择器，同时注意保持代码的可维护性。





# reference
[[有哪些 CSS 选择器？请分别介绍 - 前端 CSS 面试题 - 面试鸭 - 程序员求职面试刷题神器]]