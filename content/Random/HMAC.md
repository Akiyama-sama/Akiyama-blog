---
date: 2025-11-23
tags: 
---
全称为：Hash-based Message Authentication Code

就是在传输数据的时候，用**数据+会话密钥**计算的hash值，再附带在传输数据的末尾当中，这样客户端或者服务端在接受数据的时候可以自行计算hash值，如果没变，说明没有进行篡改