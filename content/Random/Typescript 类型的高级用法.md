---
date: 2025-10-25
tags: 
---
首先是泛型，泛型理解为传递给函数的一种“类型”参数

```ts
interface Map<T,P> = (T) => P
```

然后是extends关键字，他不是[[面向对象编程]]中的继承extends关键字，而是一种后者是否是前者的“超集”的含义

```ts
interface Animal {
	name:string
}

interface Dog extends Animal {
	color:string
}
```
这里的Dog是Animal的超集，Animal中的所有属性Dog都有，除了Animal的属性，还添加了color属性，除了这些，还可以作为表达式使用

```ts
type feature ={
	color:string	
}

interface Animal<T> = T extends feature ? Dog : never
```

如果传递过来的T是feature的超集，那么就会推断Animal为Dog类型，否则是never类型

结合`infer`关键字，可以结合出强大的类型操作，infer顾名思义就是推断，推断是不是这个类型

```ts
interface A<T> = T extends Array<infer B> ? B : never
```

这里的代码就是推断传递过来的T是否是元素包含B的数组，如果是，那么A的类型为B，否则为never

还有 `in keyof [as ..]`  关键字，in keyof用于遍历一个类型的所有属性的键，后面的as 部分是给这个键来起别名的

```ts
interface A<T> {
	[P in keyof T]
}

```

A这个类型会遍历传递过来的T的所有属性键，并添加到自己的属性当中，并且还可以用as来为这些属性键依次起别名


下面的示例是 typeof 以及 keyof 的配合组合，可以仅编辑一个对象，就能进行类型推断枚举，相较于枚举 emun 关键字，他还可以作为值使用（对象本身），还可以类型推断，是比较推崇的做法，这里是在 orval 学习到的

```ts
export type OriginpointengineInternalApiHandlersResCode = typeof OriginpointengineInternalApiHandlersResCode[keyof typeof OriginpointengineInternalApiHandlersResCode];

// eslint-disable-next-line @typescript-eslint/no-redeclare
export const OriginpointengineInternalApiHandlersResCode = {
  CodeSuccess: 1000,
  CodeInvalidParam: 1001,
  CodeNeedLogin: 1100,
  CodeInvalidToken: 1101,
  CodeTokenExpired: 1102,
  CodeUserNotFound: 1200,
  CodeUsernameTaken: 1201,
  CodeEmailTaken: 1202,
  CodeAccountNotActive: 1203,
  CodeInvalidCredentials: 1204,
  CodeVerificationFailed: 1205,
  /** 手机号已被使用 */
  CodePhoneTaken: 1206,
  /** 手机号未注册 */
  CodePhoneNotRegistered: 1207,
  /** 手机号已绑定 */
  CodePhoneBound: 1208,
} as const;
```



# reference

https://www.youtube.com/watch?v=bnTAOB3P6nM&t=807s
https://www.youtube.com/watch?v=EcCTIExsqmI