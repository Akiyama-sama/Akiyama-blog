---
date: 2026-04-20
tags:
---

## 1. 属性修饰类 (Transformation)
这类工具主要用于修改对象属性的可选性或只读状态。

* **`Partial<T>`**: 将 `T` 的所有属性变为**可选**。
* **`Required<T>`**: 将 `T` 的所有属性变为**必选**（移除 `?` 修饰符）。
* **`Readonly<T>`**: 将 `T` 的所有属性变为**只读**，防止被重新赋值。

```typescript
interface User {
  id: number;
  name: string;
  age?: number;
}

type OptionalUser = Partial<User>; // 所有属性可选
type ReadonlyUser = Readonly<User>; // 所有属性不可修改
```

---

## 2. 结构过滤类 (Selection/Exclusion)
这类工具用于从现有对象或联合类型中挑选、剔除特定的部分。

### 针对对象类型 (Object)
* **`Pick<T, K>`**: 从 `T` 中只挑选出指定的属性 `K`。
* **`Omit<T, K>`**: 从 `T` 中剔除指定的属性 `K`，保留剩下的。

### 针对联合类型 (Union)
* **`Exclude<T, U>`**: 从 `T` 中移除可以赋值给 `U` 的类型。
* **`Extract<T, U>`**: 从 `T` 中提取可以赋值给 `U` 的类型（求交集）。

```typescript
type Props = { id: string; title: string; content: string };

type Preview = Pick<Props, 'title' | 'content'>; // 只要 title 和 content
type WithoutId = Omit<Props, 'id'>;               // 删掉 id
```

---

## 3. 映射与构造类 (Construction)
用于从零开始或通过映射关系构建新结构。

* **`Record<K, T>`**: 构造一个对象类型，其键为 `K`，值为 `T`。常用于定义字典或映射。
* **`NonNullable<T>`**: 从 `T` 中排除 `null` 和 `undefined`。

```typescript
// 定义一个以字符串为键，User对象为值的对象
const userMap: Record<string, User> = {
  "admin": { id: 1, name: "Alice" }
};
```

---

## 4. 函数相关类 (Function)
专门用于提取函数类型的元数据。

* **`ReturnType<T>`**: 获取函数类型 `T` 的**返回值类型**。
* **`Parameters<T>`**: 以元组形式获取函数类型 `T` 的**参数类型**。
* **`ConstructorParameters<T>`**: 获取构造函数的参数类型。
* **`InstanceType<T>`**: 获取构造函数实例的类型。

```typescript
function getUser() {
  return { id: 1, name: "Bob" };
}

type UserResult = ReturnType<typeof getUser>; // { id: number, name: string }
```

---

## 5. 字符串模版类 (String Manipulation)
TypeScript 还提供了一些用于处理字符串字面量类型的工具：

* **`Uppercase<S>`**: 转大写。
* **`Lowercase<S>`**: 转小写。
* **`Capitalize<S>`**: 首字母大写。
* **`Uncapitalize<S>`**: 首字母小写。

---

## 总结对比

| 工具函数 | 作用 | 适用对象 |
| :--- | :--- | :--- |
| `Partial` / `Required` | 改变属性可选性 | Object |
| `Pick` / `Omit` | 筛选或剔除属性 | Object |
| `Exclude` / `Extract` | 过滤联合类型 | Union |
| `Record` | 快速创建键值对映射 | Any |
| `ReturnType` | 获取返回类型 | Function |

