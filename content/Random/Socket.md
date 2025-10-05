---
tags:
  - '#pernamant'
---
[[Socket]]是操作系统提供给应用程序（进程）的一套接口（API），通过调用socket相关的函数（例如 `socket()`, `bind()`, `listen()`, `connect()`, `accept()`, `send()`, `recv()`, `close()` 等），来使用[[TCP IP模型]]进行网络通信。没有这套API，进程是无法进行网络通信的，也就无法在不同的主机间进行通信

值得注意的是，Socket与端口号是完全不同的两个概念，端口号用于在[[TCP IP模型]]的传输层中，用于标识主机特定的进程，而Socket是一套API，需要通信的数据会通过这套API来传递给传输层，以此进行网络通信

在传输层的不同协议中，Socket会调用不同的API来进行不同主机进程间的通信

同一主机不同进程之间
实现本地进程间通信： 「本地字节流 socket 」类型是 AF_LOCAL 和 SOCK_STREAM，「本地数据报 socket 」类型是 AF\_LOCAL 和 SOCK\_DGRAM。





# reference
[[../Knowlege/计算机大类/计算机操作系统/计算机操作系统 - INDEX]]