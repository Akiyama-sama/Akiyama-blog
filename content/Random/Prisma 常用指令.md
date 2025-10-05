---
tags:
  - '#pernamant'
---
在 **Prisma** 的实际开发中，有一系列常用指令可以帮助你**管理数据库、生成代码、运行查询**。下面是最常用的 **Prisma CLI 指令**，并附上适用场景和示例

---

## **1. 安装 Prisma**

如果你的项目还没安装 Prisma，可以用下面的命令：

```sh
npm install prisma --save-dev  # 安装 Prisma
npx prisma init                 # 初始化 Prisma
```

 `npx prisma init` 会创建：

- `prisma/schema.prisma` 文件（数据库 schema 定义）
- `.env` 文件（用于配置数据库连接）

---

## ** 2. 数据库相关指令**

### **(1) 创建数据库**

```sh
npx prisma db push
```

 **作用**：同步 `schema.prisma` 到数据库，并创建数据库表（不生成迁移文件）。

### **(2) 创建数据库迁移（推荐方式）**

```sh
npx prisma migrate dev --name init
```

**作用**：

- 生成数据库迁移（migrations）。
- 适用于本地开发，数据库结构有变动时使用。

---

## **3. 代码生成**

### **(3) 生成 Prisma Client**

```sh
npx prisma generate
```

**作用**：

- 生成 Prisma Client，使得你可以在代码中使用 **Prisma API 进行数据库操作**。

### **(4) 预览数据库数据**

```sh
npx prisma studio
```

 **作用**：

- 打开 **Prisma Studio**（一个 Web 界面），可以直观地查看、修改数据库中的数据。

---

## ** 4. 查询和调试**

### **(5) 运行 Prisma 查询**

如果你不想写代码，只想在 CLI 里直接查询数据库：

```sh
npx prisma db execute --file=query.sql
```

 **作用**：

- 直接执行 `query.sql` 里的 SQL 语句，适用于调试。

---

## **5. 清理数据库**

### **(6) 重置数据库**

```sh
npx prisma migrate reset
```

**作用**：

- **删除所有数据** 并重新应用迁移，适用于开发环境。

---

## ** 6. 常见组合命令**

 **新建数据库 + 生成迁移**

```sh
npx prisma migrate dev --name init
npx prisma generate
```

**同步数据库结构（不生成迁移）**

```sh
npx prisma db push
```

 **打开 Prisma Studio（可视化数据库管理）**

```sh
npx prisma studio
```

 **清空数据库并重新应用迁移**

```sh
npx prisma migrate reset
```

---

## **总结**

| **指令**                                 | **作用**                  | **适用场景**        |
| -------------------------------------- | ----------------------- | --------------- |
| `npx prisma init`                      | 初始化 Prisma              | 第一次使用 Prisma    |
| `npx prisma db push`                   | 同步数据库 schema（不生成迁移）     | 快速创建表，但不适合生产环境  |
| `npx prisma migrate dev --name <name>` | 创建数据库迁移                 | 适用于本地开发         |
| `npx prisma generate`                  | 生成 Prisma Client        | 每次修改 schema 后运行 |
| `npx prisma studio`                    | 打开 Prisma Studio（管理数据库） | 需要手动查看/修改数据库数据  |
| `npx prisma migrate reset`             | 清空数据库并重新应用迁移            | 适用于开发环境重置数据库    |

**这些是 Prisma 最常用的指令，你可以在实际项目中结合使用，提高开发效率！**
npx prisma generate
npx prisma db pull  # 让 Prisma 重新同步数据库结构
npx prisma studio   # 查看是否能正确加载 Idea 表
