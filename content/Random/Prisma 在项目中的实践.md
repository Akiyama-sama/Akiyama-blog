---
tags:
  - '#pernamant'
---
## 什么是prisma
prisma是一款现代ORM（对象关系映射），Prisma 简化了对象与数据库表之间的映射，让开发者在代码中操作对象，底层自动转成 SQL 查询，这款工具可以连接关系型数据库，例如mysql，postgresql，甚至是文档型数据库mongodb ，prisma会对外提供一个实例的API，用于开发者间接，简单的进行crud的操作。

## Prisma 的核心工作流程

Prisma 的工作方式和传统 ORM（如 Sequelize、TypeORM）稍有不同，主要分为 3 层：

**Schema 定义（prisma/schema.prisma）**

- 你在这里定义数据库模型：

```prisma
prismamodel User {
  id       String @id @default(uuid())
  email    String @unique
  password String
  ideas    Idea[]
}
```

 **代码生成（Prisma Client）**

- 运行 `npx prisma generate`，Prisma 生成一个 **强类型 API** 供 TypeScript 使用。

 **数据库查询（Prisma Client）**

- 你在代码中这样操作数据库：

```ts
tsconst user = await prisma.user.findUnique({
  where: { email: "test@example.com" },
});
```

 **这和 SQL 语句相比，明显更简洁、可读性更高**，同时**内置类型安全**。



## 创建Prisma实例
每次操作数据库的时候会经常创建一个Prisma实例，索性直接在全局创建

```ts
// lib/prisma.ts
import { PrismaClient } from '@prisma/client'
import { withAccelerate } from '@prisma/extension-accelerate'

// 创建PrismaClient实例
const prisma = new PrismaClient().$extends(withAccelerate())

// 添加到global对象以防止热重载时创建多个实例
const globalForPrisma = global as unknown as { prisma: typeof prisma }

// 仅在非生产环境中将prisma添加到global对象
if (process.env.NODE_ENV !== 'production') globalForPrisma.prisma = prisma

export default prisma
```


## prisma环境变量

```
DATABASE_URL="postgresql://postgres:Cheng15023182754*@localhost:5432/postgres?schema=idea"
```



# reference
