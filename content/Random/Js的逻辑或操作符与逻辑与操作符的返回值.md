---
tags:
  - '#pernamant'
---
## ||的返回值规则

如果第一个为true，返回第一个值，第一个为false返回第二个的值

```js
console.log(false || true);       // true
console.log(0 || 42);             // 42
console.log('' || 'default');     // "default"
console.log(null || 'fallback');  // "fallback"
console.log(undefined || 'ok');   // "ok"
console.log(false || 0 || 'foo'); // "foo"
console.log('' || 0 || NaN);      // NaN

```

## && 的返回值

如果第一个值为 false 返回第一个操作数的值，如果第一个为true，返回第二个的值

```js
console.log(true && false);       // false
console.log(42 && 0);             // 0
console.log('foo' && 'bar');      // "bar"
console.log('hello' && 123);      // 123
console.log(true && 'ok');        // "ok"
console.log(1 && 2 && 3);         // 3
console.log('' && 'fallback');    // ""
console.log(null && 'should not reach'); // null

```

# reference
