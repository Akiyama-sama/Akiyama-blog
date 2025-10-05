---
tags:
  - '#literature'
---
## 灵感来源
[[600-闪念笔记/2025-3/你敢说我就敢拍API]]
[[DareChain 宣传文档]]
## DareChain命名
Dare表示这是一个你敢说我就敢做的单词表示
Chain 链条，表示这是广大网友头脑风暴所构成的一个链条

## 技术选型
因为会涉及到数据库就会用到后端，这次学学next.js作为全栈开发
用[clerk](https://clerk.com/)来做登录认证
gpt提到了数据库部分用
Prisma + PostgreSQL
🚀 **Prisma 让数据库操作简单（自动生成 API）**  
🚀 **PostgreSQL 提供强大的数据库功能（支持 JSON、全文搜索）**  
🚀 **Next.js + Prisma + PostgreSQL = 高效全栈开发**
[[Prisma 在项目中的实践]]
[[Prisma 常用指令]]
[[DareChain Prompt]]

## MVP阶段

Idea字段
```
model Idea {
  id String @id @default(uuid())
  chineseContent String
  englishContent String?  
  createTime DateTime @default(now())
}
```

## 1.0版本
![[20250312-0913-24.9188240.mp4]]


## 在Vercel上部署，且能让国内用户访问
教程
https://juejin.cn/post/7301193497247727652
* 在阿里云注册了一个域名darechain.fun
* 在Cloudflare请求DNS代理服务，让其DNS的服务替换掉阿里云自己的DNS服务
* 在Cloudflare配置代理服务，让请求在其上面代理，重定向到vercel上面的服务器