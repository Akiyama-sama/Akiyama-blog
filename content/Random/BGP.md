---
tags:
  - '#pernamant'
---
BGP 是不同自治系统的路由器之间交换路由信息的协议。
只能是力求选择出一条能够==到达目的网络且比较好的路由==（不能兜圈子），而并非要计算出一条最佳路由。

采用了路径向量 (path vector) 路由选择协议。
Q：为什么不用内部网关协议[[RIP]]或者[[OSPF]]？
A：因为因特网规模太大，计算最短路由的算力不划算。

eBGP (external BGP) 连接：运行 eBGP 协议，在不同 AS 之间交换路由信息。
iBGP (internal BGP) 连接：运行 iBGP 协议， 在 AS 内部的路由器之间交换 BGP 路由信息。


即：
在 AS 内部运行：
* 内部网关协议 IGP（可以是协议 OSPF 或 RIP）。
* 协议 iBGP。
在 AS 之间运行：
* 协议 eBGP。

## BGP路由

BGP 路由 = [ 前缀, BGP属性 ] = [ 前缀, AS-PATH, NEXT-HOP ]
前缀：跳到哪一个子网（CIDR记法）
BGP属性：自治系统路径，下一跳

==在属性 AS-PATH 中，不允许出现相同的 AS 号







# reference
