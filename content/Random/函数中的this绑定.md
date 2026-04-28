---
tags:
  - '#pernamant'
---
## 普通函数的this

普通函数的this有四种常见绑定规则：

1. 默认绑定：一个函数被独立调用，没有任何显视或者隐式绑定的对象时，函数里的this指向全局对象，浏览器中是window对象，Node.js中是global，但在 **严格模式** 下，this绑定的是undefined，避免全局对象被污染
2. 隐式绑定，当函数作为对象的一个方法被调用的时候，this指向拥有这个方法的对象
3. 显式绑定：使用call()  apply() bind() 方法强制指定this的指向
	- **`.call()` 和 `.apply()`**: 立即执行函数，并将`this`绑定到你传入的第一个参数。`.call()`接收一个参数列表，而 `.apply()` 接收一个参数数组。

	- **`.bind()`**: 不会立即执行函数，而是返回一个**新的函数**，这个新函数的 `this` 被永久绑定到你指定的对象。

```js
const person1 = { name: 'Bob' };
const person2 = { name: 'Charlie' };

function introduce(age) {
  console.log(`My name is ${this.name}, and I'm ${age} years old.`);
}

// 使用 .call() 强制绑定
introduce.call(person1, 25); // `this`指向person1，输出: "My name is Bob, and I'm 25 years old."

// 使用 .apply() 强制绑定
introduce.apply(person2, [30]); // `this`指向person2，输出: "My name is Charlie, and I'm 30 years old."

// 使用 .bind() 创建一个新函数
const bobIntro = introduce.bind(person1);
bobIntro(25); // `this`永久绑定到person1，输出: "My name is Bob, and I'm 25 years old."
```

4. new绑定，当这个函数为构造函数的时候，this指向被这个构造函数所实例化的对象

## 箭头函数的this

箭头函数没有自己的`this`绑定。它们会从**外层作用域**继承`this`的值，也就是其**词法作用域**中的`this`。这个规则比前面四条都优先，且这个this值是静态的，捕获后就一直保持不变

这解决了传统函数中 `this` 指向不明确的问题，尤其是在回调函数中。

```js
const person = {
  name: 'David',
  sayHello: function() {
    // 这里的 `this` 隐式绑定到 person
    setTimeout(() => {
      // 箭头函数没有自己的this，它继承了外层函数（sayHello）的this
      console.log(`Hello, my name is ${this.name}`);
    }, 1000);
  }
};

person.sayHello(); // 输出: "Hello, my name is David"
```

如果`setTimeout`内部是一个普通函数，那么`this`会指向`window`，`this.name`会是空字符串。
# reference
