---
tags:
  - '#pernamant'
---
点对点协议 PPP (Point-to-Point Protocol)
拨号上网采用该协议，为用户端和ISP路由器或接入服务器之间建立通信链路
## 封装成帧
PPP帧的格式：
![file-20250105161408982](https://obsidian-picgo-mio.oss-cn-hangzhou.aliyuncs.com/file-20250105161408982.jpg)

## 透明传输
•PPP 在==异步串行传输链路==——逐个字符/字节的传送——使用[[字节填充法]]
•PPP 在==同步串行传输链路==（如SONET/SDH同步光纤网络和同步数字系列 ）——一连串比特连续传送
–采用硬件来完成比特填充 ——[[零比特填充法]]


# reference
