---
tags:
  - index
---

参考文档：[web.dev](https://web.dev/learn/css/welcome?continue=https%3A%2F%2Fweb.dev%2Flearn%2Fcss&hl=zh-cn#article-https://web.dev/learn/css/welcome&hl=zh-cn)


## 重要链接

[[CSS 选择器]]
[[盒模型]]

## 开始

每个元素被视为一个“盒子”，每个盒子都有这几部分组成：
- content：盒子的内容显示区域，子元素就在这里
- padding：border与content之间的区域
- border：盒子的”边界“，盒子的定义在此止步
- margin：盒子与”外界“的区域

![](https://web.dev/static/learn/css/box-model/image/a-diagram-showing-four-m-af72960a9e79a.svg)

## 盒子的大小由什么决定

一个盒子的大小，主要由于对盒子自身的”限制“（extrinsic sizing），或者由content内的子元素大小（intrinsic sizing）与行为决定的

其中”限制“指的是：如果盒子明确限制了宽度，高度，无论子元素尺寸多大，都不会撑开这个盒子，而是会溢出（overflow）。
还有一种“限制”是：看似盒子没有给定限制的尺寸，但是由代理样式表默认赋值给一些属性，让这个盒子有了限制的大小，只不过这个大小由父元素决定。例如div，虽没给任何属性，但会默认display为block的，block会导致宽度由父元素决定，高度由盒子子元素的高度决定


如果没有限制父盒子的尺寸（例如width:min-content），那么其大小就会由子元素的大小决定。

## 溢出行为

在父盒子限制大小，子元素超过父元素的尺寸过后，会溢出父盒子（overflow）如果设置了溢出规则，例如 `overflow: auto` 或 `overflow: scroll`，浏览器自动出现的滚动条是会出现在content和padding之外，border之内的。

## Controll the box model

每种浏览器都有各种的用户代理样式表（use agent style sheet），这个表用于给每个没有设置样式的盒子设置默认值，

例如他会给使用display的元素设置默认值，div元设置为block，li设置为list-item，span设置为inline，而这个元素的display值决定了这个元素在父盒子中，与各个兄弟元素之间的排版关系。display值为block的话，会让这个元素为块级元素，独占一行。

[[display的各个属性值]]

盒子宽度的定义会根据box-sizing的属性不同，而不同

在box-sizing为content-box的时候，盒子定义的width为content的宽度，但实际的宽度为content+padding+border的长度

但在box-siing为border-box的时候，盒子定义的width为content+padding+border，也是实际看到的宽度

==用户代理表所设置的默认box-sizing为content-box，但现在常用的是border-box==
## 选择器

[[CSS 选择器]]

选择器的作用是用于精细化，规模化的选择特定的HTML文档

## 嵌套

嵌套不代表外层元素为嵌套元素的父元素元素，而是通过前面的组合器来决定

例如默认空，为后代选择器，如果为+，是相邻兄弟选择器...
```css
h2 + p {  /* h2 后的第一个段落 */
  margin-top: 5px;
}
h2 {
	+ p{
	 margin-top: 5px;
	}
}

```

可以用&来代表代表父选择器的符号

```css
.feature {
 & button {
    color: blue;
  }
}
```

但嵌套中不能用[[伪元素选择器]]，但能用@嵌套

## [[级联]]

### 为何存在

级联算法就是当样式冲突的时候，通过这个算法，来输出唯一一个优先度高的样式

### 组成部分

- 来源于重要性（Origin and Inportance）：样式的“出身”，优先级从高到低顺序为：
	- **开发者样式 (Author Stylesheets):** 你作为网站开发者写的样式。
    - **用户样式 (User Stylesheets):** 用户为自己浏览器设置的样式。
    - **浏览器默认样式 (User-Agent Stylesheets):** 浏览器自带的默认样式。
    - **`!important` 标记**: 这个标记可以“颠覆”上述天生的优先级。一个带有 `!important` 的规则会比任何不带 `!important` 的规则优先级更高。

- 特殊性（Specificity）：所指的元素越具体，特殊性越高，优先度也越高[[CSS选择器的权重]]
	- **内联样式** (如 `<div style="...">`) - 特殊性最高。
	- **ID 选择器** (如 `#header`)
	- **类选择器、属性选择器、伪类** (如 `.button`, `[type="submit"]`, `:hover`)
	- **元素选择器、伪元素** (如 `div`, `::before`) - 特殊性最低。

-  源顺序（Source Order）：上两个比较都相同的时候利用这个规则，即后来居上，后写的优先度更高

### 运作机制

浏览器严格按照以下三步流程来解决冲突：

1. **第一步：比较“来源与重要性”**。
    - 首先看规则是否带有 `!important`。带有 `!important` 的开发者样式 > 带有 `!important` 的用户样式 > 任何不带 `!important` 的规则。
    - 在不带 `!important` 的规则中，开发者的样式 > 用户的样式 > 浏览器的默认样式。
    - 在这一步，冲突的规则被分到一个“优先级最高的小组”里，进入下一步比较。
        
2. **第二步：比较“特殊性”**。
    - 在同一个来源小组中，浏览器会计算每个规则选择器的特殊性值。
    - 特殊性值越高的规则胜出。例如，`#nav .link` (一个ID和一个类) 的特殊性就高于 `div .link` (一个元素和一个类)。
        
3. **第三步：比较“源顺序”**。
    - 如果在前两步之后，仍然有两条或多条规则打成了平手（来源、重要性和特殊性都完全相同），那么**在样式表中最后出现的那条规则胜出**。后来者居上。


### 级联与继承的关系

级联只是负责处理样式冲突，而[[CSS中的继承]]是一种属性值的传递机制

“级联”是用来解决**多条规则应用在同一个元素上**的冲突，而“继承”是在**没有任何直接规则应用到该元素上**时，提供一个备用值的机制


## 继承

### 为何存在

这是高效率书写样式与保持其一致性的一种解决方案，不必书写每个DOM元素的样式，允许子元素自动地获取其父元素的某些样式属性

### 组成部分

- [[DOM]]树：继承的结构基础
- 可继承属性：这些属性可以被继承，一般为颜色，字体相关
	- _常见例子:_ `color`, `font-family`, `font-size`, `font-weight`, `line-height`, `text-align`, `list-style`。

- 不可继承属性：这些属性不可被继承，一般与长宽，尺寸，位置相关
	- _常见例子:_ `width`, `height`, `padding`, `margin`, `border`, `background-color`。

- 继承控制关键字：几个特殊的CSS属性值，允许我们精确的控制继承行为
	- `inherit`: 强制继承。可以用于一个不可继承的属性，让它强行从父元素那里获取值。
	- `initial`: 重置为初始值。让属性恢复到 CSS 规范定义的默认值，无视任何继承。
	- `unset`: “不设定”。如果该属性默认是可继承的，`unset` 的效果就等同于 `inherit`；如果该属性默认是不可继承的，`unset` 的效果就等同于 `initial`。它是一种智能的“重置”。

### 运作机制

对于一个可继承属性，以下为继承的运作流程

- 首先，检查是否有直接应用到该元素的规则（比如 `p { color: red; }`）。如果有，则使用该规则（这是“级联”胜出）。
- 如果没有直接规则，浏览器就会查看其**直接父元素**上该属性的计算值，并使用那个值。
- 如果父元素也没有，就继续向上查找，直到 `<html>` 根元素。
- 如果到根元素都没有找到，则使用该属性的 `initial` 值。


## 颜色

### Hex

颜色可以直接用green red这种，也可以使用简写的RGB十六进制写法：
```css
h1 {
  color: #b71540;
}
```

这种写法被称为[[hex]]，6位数字，每位数字的范围是 0-9 和 A-F，每两位代表0~255的红、绿、蓝三种元素的数值

还可以在hex后面再加上2位，变成8位，这两位表示的是 alpha 值，即颜色透明度的百分比，例如#00000080这是百分之50的透明度

### RGB

```css
h1 {
  color: rgb(183 21 64); //rgb(0% 0% 0%) 百分比
}
```

rgb里面的元素可以是0~255的数字，也可以是百分比，越深数值越低，越浅数值越高，例如rgb(0% 0% 0%)是黑色

也可以在后面加上 / A
A也就是刚说的alpha 值，即不透明度，可以为百分比，也可以为小数
```css
h1 { 
  color: rgb(0 0 0 / 50%)；0.5也可以
}
```

### HSL

HSL（色相、饱和度、亮度）

```css
h1 {
  color: hsl(344 79% 40%);
}
```

色相指的是在色盘中的对应角度的颜色，单位是deg
饱和度指的是这个颜色的鲜艳程度，用百分比
亮度指的是添加多少黑/白在里面，用百分比

![](https://web.dev/static/learn/css/color/image/the-hsl-color-function-br-02004be01101d.svg)

设置Alpha值与rgb一样，使用hsl的时候只需在后面加上 `/ 百分比` 来表示不透明度就行了

或者直接用hsla：`hsla(0, 0%, 0%, 0.5)`


==RGB 和 HSL 定义的是 sRGB 色域内的颜色==

## 尺寸单位

### 数字

数字定义在各种不同属性上有着不同的含义，具体含义得看上下文

例如`opacity: 0.5`这个数字代表这百分比的意思

### 百分比

颜色中一般表示为不透明度，在rgb中红绿蓝也可以用百分比来表示

宽度可以用百分比来表示，表示占据父元素content的百分比


### 各种类型的长度单位

#### 绝对长度

像是cm，in（英寸）一般在打印这种场景中比较常见
px像素这个单位也是经常用到的（1px = 1/96 英寸）

#### 相对长度

相对长度是根据一个基准值来判断的，以下为常用的相对单位


**相对字体单位**

| 单位名称      | 解释                                                  | 使用场景                                                |
| --------- | --------------------------------------------------- | --------------------------------------------------- |
| **`em`**  | 相对于**父元素**的字体大小。如果用在 `font-size` 属性上，则相对于元素自身的字体大小。 | 用于组件或模块内部，实现**上下文比例缩放**。例如，在一个组件内，边距和字体大小保持一致的比例关系。 |
| **`rem`** | 相对于**根元素**（即 `<html>` 元素）的字体大小。                     | 用于**全局统一的响应式排版**。只需调整根元素的字体大小，就能等比例缩放整个页面的文本。       |
| **`ch`**  | 数字 `0` 的宽度。                                         | 用于创建**可读性更佳**的文本容器宽度，因为它是基于字体的宽度，有助于控制一行中的字符数。      |

**视口（浏览器窗口）相关单位**

| **`vw`**   | **视口宽度**（Viewport Width）的 1%。  | 用于实现与浏览器窗口宽度**完全挂钩的响应式效果**，例如让标题或图片尺寸随视窗宽度等比例缩放。 |
| ---------- | ------------------------------ | ------------------------------------------------ |
| **`vh`**   | **视口高度**（Viewport Height）的 1%。 | 用于设定占满屏幕高度的元素（如“英雄区”或侧边栏），或确保元素大小随视窗高度变化。        |
| **`vmin`** | 视口**宽度和高度中较小值**的 1%。           | 用于确保元素在横向或纵向屏幕旋转时都能适应视口，避免在小尺寸维度上溢出。             |
| **`vmax`** | 视口**宽度和高度中较大值**的 1%。           | 用于在较大尺寸维度上扩展元素，确保元素在不同屏幕比例上保持视觉上的存在感。            |
|            |                                |                                                  |
### 其他单位

角度，一般用deg来表示
```css
div {
  width: 150px;
  height: 150px;
  transform: rotate(60deg);
}
```

auto : 这是一个不带数字的一种单位，意在填充可用的剩余部分

## 逻辑属性

在定义一个DOM的位置的时候，我们之前只能用物理位置，例如top,left,right,bottom来指定，但是这样的定义是相对于整个viewpoint（视窗）的，这样定义默认书写模式（write mode）是行内（inline）从左到右。行块（block）是从上到下的

但如果是阿拉伯语的书写模式就不一样了，他们的行内（inline）是从右到左的，像是我们的中文古籍，inline是从上到下的

这样该如何定位相对于书写内容（content）的属性呢？这时候就要用逻辑属性，inline始终代表着行内流，block始终代表行块流，inline-start就能代表行首，inline-end就代表着行尾，block-start就代表块手，block-end就代表着块尾

![](https://web.dev/static/learn/css/logical-properties/image/a-diagram-showing-the-di-12ce9bdac4132_1440.png)


定义书写模式：
```css
div {
  writing-mode: vertical-rl; 行块从右到左
  writing-mode: vertical-lr; 行块从左到右
  writing-mode: horizontal-tb; 行块从上到下
}

```

使用逻辑属性，就能直接作用于书写模式上的逻辑属性了

例如margin-block-start：指的是行块之首

因此，在定位margin，padding，border的逻辑位置的时候，使用逻辑属性会非常好用，例如：

```css
.my-element {
  border-block-end: 1px solid red;
  border-inline-end: 1px solid red;
  border-end-end-radius: 1em;
  padding-block:2em;
  margin-inline:2em 0;
}
```


逻辑属性引入了两个新单位： `vi` 和 `vb` 。一个 `vi` 单位是行内方向视口大小的 1%。非逻辑属性的等效单位是 `vw` 。一个 `vb` 单位是块方向视口大小的 1%。非逻辑属性的等效单位是 `vh`




## 间距

### margin

外边距

可以给margin的四边都定制长度
![](https://web.dev/static/learn/css/spacing/image/the-word-trouble-runnin-645c6ed02703c.svg)

可以直接简写(`margin: 20px 40px 30px`) ,如果只设置一个值，就直接引用到四边，如果两个值，就分别应用到x和y的边，如果设置三个值，第一个是top，第二是left+right，第三个是bottom

单位可以用百分比，auto来定义，如果是百分比，就是直接用该盒子的width乘以百分比，如果是auto，那么将用来填充可用区域

```css
.box:nth-child(3) {
  margin-inline: 0 auto; start的margin为0，end的margin为auto，填充可用的剩余区域
}
```


其margin的值也可以为负的，可用于减少盒之间的空间，或者直接元素重叠


**计算两个元素的间距到底为多少**

两个元素之间的边距是由他们之间的margin最大值决定的
例如：

```css
h1 {
    margin-bottom: 2rem;
}
p {
    margin-top: 3rem;
}
```

他们之间的间距为3rem。但其中一个元素使用**绝对定位**的时候，他们之间的margin就会不会折叠，且如果他们之间的父元素用的是[[Flex]]布局的时候，他们之间的margin就不会重叠，而是合并

### padding

padding会占据盒子的内边距区域
在box-sizing属性值不同的时候，padding会对盒子的影响也不同，例如为content-box的时候，width指定的是content的宽度，实际上的宽度为：content+padding+border，如果是border-box的时候，width指定的是content+padding+border的宽度，因此，会导致content收到挤压


padding和margin一样，也可以用绝对属性与逻辑属性来指定方位，属性值也和margin一样，一个值代表应用四周，两个值代表应用x和y轴，三个值代表top，x轴，bottom


## [[定位（position）]]

默认postion属性值为static，这个值会让元素位置由编写的HTML结构决定，是由浏览器自助决定的，此时这个元素上的top,right,left,bottom属性均无效。

而其他relative,absolute,fixed,sticky均是相对于一个基点的定位，他们之间的不同只是在于基点的不同罢了

`position: relative` 元素仍会保持其在文档流中的位置，即基点是是static原来的位置，但是可以使用top,right,left,bottom等属性进行偏移，还可以用于给子元素为 `position:absolute`的元素进行相对定位

`position: absolute` 元素将根据相对父级relative 的位置确定方向值，即基点在父元素为relative的元素上。

`position: fixed` 元素将根据视口确定方向值，即基点在viewport（浏览器窗口），这会导致元素不会随着滚动而变化，像是固定在网页中，也可以搭配`top`、`right`、`bottom` 或 `left`。

`position: sticky` 元素 仅当其处于停靠/卡住状态时才会应用方向值，这是一个动态设置为relative/fixed的属性值，前提是必须搭配`top`、`right`、`bottom` 或 `left`，sticky才能生效，

当页面滚动，父元素开始脱离视口时（即部分不可见），只要与`sticky`元素的距离达到生效门槛，`relative`定位自动切换为`fixed`定位；等到父元素完全脱离视口时（即完全不可见），`fixed`定位自动切换回`relative`定位。
例如：

```css
#toolbar {
  position: sticky; /* 其他浏览器 */
  top: 20px; /* 切换的门槛值*/
}
```

页面滚动，当#toolbar的父元素脱离视口的时候，一旦viewport顶部与#toolbar距离小于20px的门槛值的时候，position会变为fixed，一旦父元素完全脱离整个视口的时候，会变为relative

## 边界 border

边界有这几种属性：width，style，color，radius
可以通过`boder-属性`来定义边框的属性，或者是通过这几个的顺序进行简写

```css
div {
	border: 1px solid red
}
```

其中，如果没指定boder的color，border的color会自动使用字体的color，且默认情况下border为0px

[`border-image`](https://developer.mozilla.org/docs/Web/CSS/border-image) 这个属性还可以直接使用图片作为边框


## 阴影 shadow


box-shadow为HTML元素盒子添加阴影，适用于block和inline元素，

属性值依次为：水平偏移，垂直偏移，模糊半径，扩展半径，颜色

还可以在前面加inset来切换为向内阴影

```css
/* Outer shadow */
.my-element {
    box-shadow: 5px 5px 20px 5px #000;
}

/* Inner shadow */
.my-element {
    box-shadow: inset 5px 5px 20px 5px #000;
}
```

text-shadow为文字创建阴影，其属性顺序也相同，只不过没有inset关键字,也没有扩散半径的值

这两种shadow都可以通过`逗号`来分隔几种类型的shadow类型，可以产生非常炫酷的3D效果

```css
.my-element {
  text-shadow: 1px 1px 0px white,
    2px 2px 0px firebrick;
  color: darkslategray;
}
```

![](https://obsidian-picgo-mio.oss-cn-hangzhou.aliyuncs.com/20251013140101763.png)

当我们想给一些不是文字和DOM盒子的不规则物品添加阴影，例如衣服的时候，我们可以使用drop-shadow来添加阴影

```css
figure img {
  filter: drop-shadow(0px 0px 10px rgba(0 0 0 / 30%))
}
```

## 焦点 focus

当我们在浏览器中使用Tab，或者点击的时候，会看到某些盒子周围会发光，这就是获得了焦点，HTML文档中有一个属性名为tabindex，通过这个index的值，来修改Tab的索引值顺序，但不能小于0，任何小于0的tabindex只能通过编程来访问

我们可以通过outline属性来自定义焦点轮廓样式


## Z-index 

文档需要堆叠/层叠的时候就需要用到z-index这个属性，这个属性决定哪些盒子摆放在上面，即z-index较大者，放在上面

需要注意的是，在Nomal flow的上下文中，也就是该元素为positon:static的时候，z-index会不起作用，z-index只在static以外的值起作用

但如果使用z-index的父元素使用flex或者grid布局的时候，就不用手动指定这些盒子的position了，z-index会自动起作用，因为已经不在Nomal flow当的上下文当中了


### 层叠上下文 Stacking context

这里的z-index的比较只在同一层父级进行比较，不同层级的z-index是不能比较的

```css
.my-element {
  position: relative;
  z-index: -1;
}

.my-element .child {
	position: relative;
	z-index: 0;
}
```

例如这类的my-element，都通过position激活了自身的z-index属性，但child类与my-element类不在同一父层，而是父子的关系，因此尽管父的z-index小于child，但是还是父元素叠在上面，原因是他们两个之间的Stacking context不同

具体的[[层叠等级]]：

1. **背景和边框 (Background & Borders)**：最底层，地基。
2. **负 z-index (-ve z-index)**：`z-index` 为负值的定位元素（Positioned）。
3. **块级盒子 (Block)**：普通的 `div` 等，用于布局。
4. **浮动盒子 (Float)**：`float` 元素。
5. **行内盒子 (Inline)**：`span`、文字内容。
    - _注意：_ 浏览器认为**内容（文字）比布局（块/浮动）更重要**，所以文字默认会浮在 div 上面。
6. **z-index: auto / 0**：`z-index` 为 0 或 auto 的定位元素。
7. **正 z-index (+ve z-index)**：`z-index` > 0 的定位元素（数值越大越靠上）。

---


### 创建上下文

不需要应用 `z-index` 和 `position` 来创建新的 [堆叠上下文](https://developer.mozilla.org/docs/Web/CSS/CSS_Positioning/Understanding_z_index/The_stacking_context) 。您可以通过为创建新复合层的属性（例如 `opacity` 、 `will-change` 和 `transform` ）添加值来创建新的堆叠上下文

[[哪些css属性会创建新的层叠上下文]]

## 锚点定位 Anchor position

### 单个锚点

当时用点击某个元素，然后出现下拉菜单的时候，就会用到锚点定位，即是锚定某个元素为基点，让这个元素相对于这个基点进行定位

这里就需要两个元素都要设置相关属性，一是基点元素设置锚点，属性名为anchor-name：

```css
#anchor {
   anchor-name: --my-anchor; 
}
```

二是为被束缚元素设置属性position-anchor，与此同时这个元素的position必须为absolute或者fixed，目的是需要这个元素有利于正常的文档流之外

```css
#positionedElement {
     position: absolute;
     position-anchor: --my-anchor;
     position-area: end;
}
```

但button里面有个属性为`popovertarget`，他自动设置一个其值为锚点名的“隐式”锚点

```html
<button popovertarget="positionedElement" id="anchor">Anchor</button>
<p popover id="positionedElement" class="box">Positioned Element</p>
```

### 多个锚点

参考
https://web.dev/learn/css/anchor-positioning#scoping_the_potential_anchors
这篇文章

### 锚点定位

提供两种方法进行相对于锚点的定位：
`position-area` and the `anchor()`

positon-area可以使用物理关键字或者使用逻辑属性来相对于锚点进行定位

![](https://obsidian-picgo-mio.oss-cn-hangzhou.aliyuncs.com/20251013161227780.png)
![](https://obsidian-picgo-mio.oss-cn-hangzhou.aliyuncs.com/20251013161239584.png)
![](https://obsidian-picgo-mio.oss-cn-hangzhou.aliyuncs.com/20251013161400733.png)

添加span关键字可以在添加相邻区域，例如下拉菜单的常见写法为：

```css
position-area: block-end span-inline-end
```

https://anchor-tool.com/
这个网站可以用来训练position-area

span-all关键字可以三行或者三列


### anchor函数

`anchor()` 函数接受一个锚点名称和一个锚点方向。如果你的元素有一个默认锚点（无论是通过 `position-anchor` 设置还是隐式设置，例如使用弹出窗口），则可以省略锚点名称。

```css
.positionedElement {
  block-start: anchor(--my-anchor start);
  /*  OR  */
  position-anchor: --my-anchor;
  block-start: anchor(start);
}
```


### 处理overflow

当定位元素溢出的时候，可以用`position-try`值来设置后备值

```css
#positionedElement {
  position: absolute;
  position-anchor: --my-anchor;
  position-area: block-end span-inline-end;
  min-width: max-content;
  position-try: block-end, block-start span-inline-start;
}
```

后备值用flip-等关键词也可以
```css
.positioned-element {
    position-try-fallbacks: flip-start;
}
```

还可以自定义positon-try的值

```css
@position-try --menu-below {
  position-area: bottom span-right;
  margin-top: 1em;
}

#positioned-element {
  position-try: --menu-below;
}
```

在锚点滚动的时候，定位元素也会跟着滚动，当锚点消失在视图之外的时候，如果我们也希望定位元素隐藏时，用`position-visibility: anchors-visible`

## popover and dialog

在button，div等元素中，有一个`popovertarget`属性，这个属性值设置为某个元素的id值的时候，点击设置了`popovertarget`的元素，会弹出那个id元素

那个元素使用popovertargetaction="hide"这个属性，就可以点击的时候隐藏

还可以使用JS中的`showPopover()`, `hidePopover()`, or `togglePopover()`.函数来指定某些元素弹出或者隐藏


### 三种popover类型

被弹出的元素在HTML设置属性的时候会决定出三种不同的类型

```html
<div id="popover" popover>My popover</div>
```

默认类型，即弹出过后，如果有其他弹出的弹窗/点击其他区域/按ESC键盘，就会让这个弹出消失

```html
<div id="popover" popover="manual">My popover</div>
```

手动类型，弹出过后不会自动消失，而是必须手动消失

```html
<div id="popover" popover="hint">My popover</div>
```

提示弹窗类型，通过非点击事件（悬停，焦点）来触发弹窗

### 样式和动画

```css
:popover-open
```

这个[[伪类选择器]]会仅在popover被打开的情况下应用

弹出动画需要分解三个步骤：

8. 初始样式：`@starting-style {popover:popover-open { } }`
9. 弹出后的样式：`popover:popover-open { }`
10. 弹出窗口关闭时的样式`popover { }`  


### 嵌套弹窗

可以在被弹出的popover里面继续设置popovertarget，如此就能实现嵌套弹窗，自动弹窗与提示弹窗都有一个单独的堆栈

## 函数 Function

参考网站：
https://developer.mozilla.org/zh-CN/docs/Web/CSS/CSS_values_and_units/CSS_value_functions

以下会写出可能有用或者有趣的函数

`atan2()` 函数接受两个参数，分别表示相对于原点的点，并返回指向该点的角度。：https://web.dev/learn/css/functions#atan2

算出指向该点的角度，可以实现像是眼球随着鼠标滚动之类的效果

 [`clip-path`](https://developer.mozilla.org/docs/Web/CSS/clip-path) ， [`offset-path`](https://developer.mozilla.org/docs/Web/CSS/offset-path) 和 [`shape-outside`](https://developer.mozilla.org/docs/Web/CSS/shape-outside)可以用来塑形

 transform 函数，它可以倾斜、调整元素的大小，甚至改变元素的深度

## 文本与排版

用@font-face 来引入字体，用font-family来使用具体的字体

```css
@font-face {
  font-family: "Trickster";
  src:
    local("Trickster"),
    url("trickster-COLRv1.otf") format("opentype") tech(color-COLRv1),
    url("trickster-outline.otf") format("opentype"),
    url("trickster-outline.woff") format("woff")
}
```

使用font-style来指定文字的斜体

- nomal：正常，无斜体
- italic：斜体，但是类“草书”的形式
- oblique：斜体，但是较为正式的斜体形式

使用font-weight来指定文字的粗细
关键字有：nomal ,bold ，数值分别为400,700，也可以在@font-face导入字体的时候，直接指定字体的粗细


使用font-size可以指定字体的大小，除了使用长度值以外，也可以使用关键字，从小到大为：
xx-small;x-smal;small;medium;large;x-large;xx-large

在[[em与rem的区别]]当中，区别就是em继承的是父元素的font-size的大小，而rem继承的是根元素的font-size

使用line-height指定元素中的每行高度，可以接受数字，长度，百分比或者关键字，但一般用数字，以避免继承问题

使用letter-spacing控制文本中的水平间距，接受长度值
使用word-spacing更爱单词之间的间距

font的简写形式参考这篇文章：
https://developer.mozilla.org/zh-CN/docs/Web/CSS/font#syntax

使用text-decoration-line以及text-decoration-color可以设置横线：line接受`underline` 、 `overline` 和 `line-through`关键字， [`text-decoration-style`](https://developer.mozilla.org/docs/Web/CSS/text-decoration-style)属性接受关键字 `solid` 、 `double` 、 `dotted` 、 `dashed` 和 `wavy`，用于修饰横线，[`text-decoration-thickness`](https://developer.mozilla.org/docs/Web/CSS/text-decoration-thickness)用于修修改横线的粗细

[`text-indent`](https://developer.mozilla.org/docs/Web/CSS/text-indent)可以为文本设置缩进
[`text-overflow`](https://developer.mozilla.org/docs/Web/CSS/text-overflow)用于处理文字溢出，有两个选项：clip默认，为阶段，第二个`ellipsis`溢出显示省略号


[`white-space`](https://developer.mozilla.org/docs/Web/CSS/white-space)用于处理如何控制元素中的空格
`white-space: pre` 可用于渲染 [ASCII 艺术](https://en.wikipedia.org/wiki/ASCII_art)或仔细缩进的代码块。


 [`word-break`](https://developer.mozilla.org/docs/Web/CSS/word-break)用于控制单词换行时的行为，是将这个单词拦腰斩断：break-all，还是放在下一行nomal(默认)

[`text-align`](https://developer.mozilla.org/docs/Web/CSS/text-align)用于控制块元素或者表单元素在文本中的对齐方式，有如下关键字： `left` 、 `right` 、 `start` 、 `end` 、 `center` 、 `justify` 和 `match-parent` 。

![](https://obsidian-picgo-mio.oss-cn-hangzhou.aliyuncs.com/20251014151734608.png)

 [`text-wrap`](https://developer.mozilla.org/docs/Web/CSS/text-wrap) 来改变元素内文本的换行方式。
 
使用 [`direction`](https://developer.mozilla.org/docs/Web/CSS/direction) 设置文本的方向，可以是 `ltr` （从左到右，默认）或 `rtl` （从右到左）

使用 [`text-shadow`](https://developer.mozilla.org/docs/Web/CSS/text-shadow) 为文本添加阴影。此属性需要三个长度（ `x-offset` 、 `y-offset` 和 `blur-radius` ）和一个颜色。

## [[渐变 Gridiant]]

[`linear-gradient()`](https://developer.mozilla.org/docs/Web/CSS/linear-gradient\(\)) 函数逐步生成一种或多种颜色的图像

```css
.my-element {
    background: linear-gradient(black, white);
}
```

可以传递一个角度或表示角度的关键字。如果您选择使用关键字，请在 `to` 关键字后指定方向，只需在第一个参数上，加入方向，例如`to right`即可

```css
.my-element {
    background: linear-gradient(to right, black, white);
}
```

色标值定义了颜色停止并与其相邻颜色混合的位置。例如，一个渐变以 45 度角开始，从深红色开始，在渐变大小的 30% 处变为浅红色：它看起来像这样。

```css
.my-element {
    background: linear-gradient(45deg, darkred 30%, crimson);
}
```

[`conic-gradient()`](https://developer.mozilla.org/docs/Web/CSS/conic-gradient\(\))圆锥渐变是围绕着中心点进行渐变

[`repeating-linear-gradient()`](https://developer.mozilla.org/docs/Web/CSS/repeating-linear-gradient\(\))重复线性渐变，可以用来做蓝白碗背景的效果（笑）
 [`repeating-radial-gradient()`](https://developer.mozilla.org/docs/Web/CSS/repeating-radial-gradient\(\)) 和 [`repeating-conic-gradient()`](https://developer.mozilla.org/docs/Web/CSS/repeating-conic-gradient\(\)) 。这是其他渐变，具体看MDN文档

渐变的前一个参数，接受in+色彩空间，可以参考
https://developer.chrome.com/docs/css-ui/access-colors-spaces?hl=zh-cn
```css
.my-element {
  background: linear-gradient(in oklch, deeppink, yellow);
}
```

上面这样可以通过切换色彩空间来去除不饱和中间的颜色，因此在渐变不理想的时候可以试试这个

## 滤镜 filter

以下属性接受filter属性

- blur:高斯模糊，唯一参数为radius，只能用长度单位传递
- brightness：增加或则减少元素亮度，只能用百分比
- contrast：对比度，用百分比
- grayscale：给元素上灰度效果，用百分比，默认为1，即完全黑化
- invert：反转元素中的颜色，用百分比，默认为1，即完全反转
- opacity：不透明度，用百分比或者数字
- saturate：饱和度，用数字或者百分比
- sepia：棕褐色色调的滤镜，用数字或则百分比
- hue-rotate：改变[[hsl]]中色盘的角度，例如改变元素颜色120deg
- drop-shadow：与box-shadow几乎相同，添加阴影，但不支持inset
- url：允许通过链接的SVG元素设置过滤[点击此处了解有关 SVG 过滤器的更多信息](https://developer.mozilla.org/docs/Web/SVG/Element/filter)

`backdrop-filter` 和 `filter`能用的属性都一样，只不过`backdrop-filter ` 运用的是background，`filter`运用在整个元素当中

## 混合 blend modes

`mix-blend-mode` 将混合应用于整个元素， `background-blend-mode` 将混合应用于元素的背景。融合背景一般是用于对颜色进行融合

混合模式分为两类：可分离和不可分离。可分离混合模式会分别考虑每个颜色分量（例如 RGB）。不可分离混合模式则会平等地考虑所有颜色分量。
https://web.dev/learn/css/blend-modes
- 可分离：
	- nomal：默认混合模式，不会改变与其他元素的混合方式
	- multipy：像是透明胶片堆叠的效果，亮色的部分更亮，暗的部分更暗，会强调原来的色调
	- screen：与multipy相反的效果，会削弱元素的颜色效果，产生与背景相似的色调
	- overlay：multipy与screen之间的效果，基础深色更深，基础浅色更浅，中等色阶颜色不受影响
	- darken：比较元素与背景的深色亮度，并选择最暗的那一个
	- lighted：与darken相反
	- color-doge：元素中的背景色变亮
	- color-burn：增加对比度
	- hart-light、soft-light、diffence、exclusion
- 不可分离
	- hue、saturation、color、luminosity

设置 [`isolation`](https://developer.mozilla.org/docs/Web/CSS/isolation) 如果将属性设置为 `isolate` ，它将创建一个新的堆叠上下文，从而阻止其与背景层混合，像z-index的堆叠上下文一样。


## 关键帧与动画


[[animation关键字]]就是在动画开始播放与结束以及中间状态下定义某个时态的CSS样式，然后浏览器自动计算出这个过程的动画播放，因此，我们需要定义中间时刻的样式，就需要用到关键帧

结构：
```css
@keywords 自定义关键帧名{
	from {
	
	}
	to {
	
	}
}
```

from to可以用百分比来替代，指代动画进行的百分比时刻

自定义有关键帧名用于传递给animation属性的animation-name值，animation属性是执行动画的执行者，这里写的关键帧就像写好的舞台脚本，递给演员（animation）去真正演绎

animation的各个属性有：
- animation-name：之前所说的自定义关键帧名
- animation-duration：动画持续时间/播放周期
- animation-timing-function：动画移动曲线函数，具体有哪些可以查看MDN文档
- animation-delay：延迟多少秒才开始播放
- animation-iteration-count：执行多少次，infinite为无限次
- animation-direction：设置关键帧的运行方向
- animation-fill-mode：定义关键帧中那些值动画开始前或结束后保留
- animation-play-state：设置动画播放开关

## 过渡 transition

[[transition 与 animation属性的区别]]

[[transition关键字]]也是一种动画，不过是那种在开始与结束中间，只有一个中间状态的特殊动画，一般在给元素设置hover，或者其他状态，或在三种状态下切换时所用的属性

有如下属性：

- transiton-property：指定哪些CSS属性播放转换动画，background-color就只指定背景色，transition-all指定所有可过渡的CSS元素，至于哪些CSS属性可以添加，可以参阅 [MDN 上的可动画 CSS 属性列表](https://developer.mozilla.org/docs/Web/CSS/CSS_animated_properties) ，一般像是颜色，大小之类的可以转换，像是平移旋转需要依赖transform属性
- transition-duration：过渡持续时间
- transition-function：与animation一样的动画函数
- transiton-dely：延迟发生时间


### transform

他是一个专门指定元素**平移（translate），旋转（rotate），缩放（scale）** 的一个CSS属性，与color，background-color类似，但它是一个GPU加速属性，在transition中监听这个属性可以用到GPU加速，而transition监听其他CSS属性却不行，所以transition属性性能较好

有好多关键词比较像，有容易搞混，专开一个：
[[transition，transform，translate关键字在CSS中的区别]]

```css
.square {
  transition: scale 250ms ease 0s, rotate 250ms ease 250ms,
    translate 250ms ease 500ms,
    /* All `transform` transitions will happen over 750ms and start immediately. */
      transform 750ms ease 0s;
}
```

例如这里的transition属性，监听了4个CSS属性，scale，rotate，translate，tranform，并为每个属性设置了过渡动画

### 其他单独的transition-property

`color` 、 `background-color` 和 `border-color`

[`filter`](https://developer.mozilla.org/docs/Web/CSS/filter) 是一个强大的 CSS 属性，可以让你动态添加图形效果。不同的 `filter` 状态之间的转换可以创造出一些令人印象深刻的效果


### transition触发器

需要在开始与结束中有中间态的动画才能使用transition属性，典型示例就是：hover之类的伪类选择器，hover这里设置的CSS样式就是一个中间态，满足transition的要求

以下是一些可以触发元素状态变化的伪类和事件的列表。

- [`:hover`](https://web.dev/learn/css/pseudo-classes#hover) ：当光标位于元素上方时匹配。
- [`:focus`](https://web.dev/learn/css/pseudo-classes#focus_focus-within_and_focus-visible) ：如果元素获得焦点则匹配。

- [`:focus-within`](https://web.dev/learn/css/pseudo-classes#focus_focus-within_and_focus-visible) ：如果元素或其任何后代获得焦点则匹配。
- [`:target`](https://web.dev/learn/css/pseudo-classes#target) ：当当前 URL 的[片段](https://developer.mozilla.org/docs/Web/HTTP/Basics_of_HTTP/Identifying_resources_on_the_Web#fragment)与元素的 `id` 属性值匹配时匹配。
 
- [`:active`](https://web.dev/learn/css/pseudo-classes#active) ：当元素被激活时匹配（通常是当鼠标按下时）。
 
- 通过 JavaScript 更改 `class` ：当使用 JavaScript 更改元素的 CSS `class` 时，CSS 将转换已更改的合格属性。

### 当中间状态也有transition时 - 不对称状态

以hover为例，transition的过渡为：base->hover->base

如果hover的状态以及base状态都设置得有transition，这时候就出现了不对称过渡，

开始base->hover应用的是hover的transition，结束hover-base的时候运用的是base中写的transition

这就是一个典型的例子
```css
.my-element {
  background: red;

  /* This transition is applied on the "exit" transition */
  transition: background 2000ms ease-in;
}

.my-element:hover {
  background: blue;

  /* This transition is applied on the "enter" transition */
  transition: background 150ms ease;
}
```

在对称状态的时候，一般hover中没有设置transition，这时候才回运用base的transition写法


### 动画性能考虑

https://web.dev/articles/animations-guide

## 媒体查询

使用@media关键字可以查询对应的媒体/视口大小，以生效对应的CSS样式

- 查询视口大小可以用范围表示，即max-width
- 朝向也可被查询：orientation:landscape
- hover也可以被查询，运用到hover的意味着用户使用的是某种指点设备，因此触摸盘与键盘导航的设备就不能应用到

用逻辑与创建查询列表：用and关键字可以把所有需要查询的条件相与
```css
@media screen and (min-width: 400px) and (orientation: landscape) {
  body {
    color: blue;
  }
}
```

逻辑“或”可用逗号进行分开，

```css
@media screen and (min-width: 400px), screen and (orientation: landscape) {
  body {
    color: blue;
  }
}
```

逻辑“非”用not关键字，这就直接反转了整个媒体查询的含义

```css
@media not all and (orientation: landscape) {
  body {
    color: blue;
  }
}
```

## CSS当中的坐标系

与数学的坐标系不同，CSS当中的坐标系原点在左上角，但里面有着四种不同的坐标系，分别是

- 被检查元素：offsetX/Y
- 视口：clientX/Y
- 页面：pageX/Y
- 屏幕：screenX/Y

## 包含块

[[包含块]]是一个参照系矩形，当一个元素需要计算自己的大小或者位置的时候，需要根据这个参照矩形来进行计算

**A1. 要素 (核心零件)**
11. **子元素 (Descendant)：** 需要定位或定尺寸的那个元素。
12. **定位属性 (position)：** 子元素的 `position` 属性（fixed, absolute, static, relative）决定了它去认谁做“干爹”（包含块）。
13. **祖先元素 (Ancestor)：** 潜在的包含块候选人。


**A2. 结构 (核心规则 - 也是最容易错的地方)** 包含块是谁？完全取决于子元素的 `position`：
- **情况 1：普通大众 (`static` / `relative`)**
    - **认亲规则：** 包含块就是**最近的祖先块元素**的内容区域 (Content Box)。
    - _白话：_ 乖乖听亲爹的话。
- **情况 2：绝对定位 (`absolute`)**
    - **认亲规则：** 包含块是**最近的、且 `position` 不是 `static` 的祖先元素**的内边距区域 (Padding Box)。
    - _白话：_ 亲爹如果没本事（是 static），就往上找爷爷，直到找到一个有地位（relative/absolute/fixed）的长辈为止。如果大家都平庸，就以**初始包含块**（通常是浏览器窗口的第一屏）为准。
        
- **情况 3：固定定位 (`fixed`)**
    - **认亲规则：** 包含块通常是**视口 (Viewport)**（也就是浏览器窗口本身）。
    - _特例（MDN 重点）：_ 如果某个祖先元素具有 **`transform`**、**`filter`** 或 **`perspective`** 属性（且值不为 none），那么这个祖先就会意外地成为 `fixed` 元素的包含块。**这是 90% 的固定定位失效 Bug 的来源。**

**A3. 系统 (涌现功能)** 这套机制确立了 CSS 的**局部坐标系**。它允许你在一个小的组件内部（比如一个弹窗）进行绝对布局，而不用担心受到外部页面滚动或缩放的影响。



## 格式化上下文

**[[格式化上下文]]** 是页面上的一块**独立渲染区域**。 它决定了其子元素如何排列，以及该区域如何与其他元素相互作用。

一句话本质：**它是一个“结界”。结界里的内政（布局）由结界主说了算，且结界内发生的混乱（如浮动、外边距合并）不会泄露到结界外。**


**A1. 要素 (类型)** MDN 文档提到了几种主要的上下文，这代表不同的“特区规则”：

14. **BFC (Block Formatting Context):** 处理块级盒子。最常用，用于清除浮动、防止 margin 重叠。
15. **IFC (Inline Formatting Context):** 处理行内盒子（文字）。决定文字如何折行、如何对齐。
16. **Flex / Grid Context:** 现代布局产生的上下文，规则更强大。
    

**A2. 结构 (触发条件)** “结界”不是天然存在的，需要用特定的 CSS 咒语召唤（触发）：

- `float` 不为 none。
- `position` 为 absolute 或 fixed。
- `display` 为 inline-block, flex, grid, flow-root 等。
- `overflow` 不为 visible (最常用的黑魔法，如 `overflow: hidden`)。

**A3. 系统 (涌现功能 - BFC 的三大铁律)**

17. **内部箱子垂直放：** 里面还是遵循文档流。
18. **排除浮动：** BFC 区域不会与浮动元素重叠（会自动收缩避开浮动）。
19. **包含浮动：** 计算 BFC 高度时，浮动子元素也参与计算（**这是最重要的功能，用于解决“高度塌陷”**）。






