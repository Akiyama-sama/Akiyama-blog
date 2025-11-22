---
date: 2025-10-22
tags: 
---
$\texttt{position: relative}$ / $\texttt{absolute}$ / $\texttt{fixed}$ / $\texttt{sticky}$ 且 $\texttt{z-index}$ 不为 $\texttt{auto}$，或者设置了 $\texttt{opacity} < 1$、$\texttt{transform}$

这些因素会让这个盒子创建新的堆叠上下文

如何记忆：

- position的上面属性都是脱离了正常文档流
- capacity会使盒子半透明化，为了隔离这种影响会创建一个新的上下文。
- transform也跟opacity一样。