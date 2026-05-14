---
date: 2026-04-29
tags:
---
[[Promise]]里面的执行器函数本来是被 try catch 包裹的，一旦 throw，会直接变为 rejected 状态，但在异步函数中，例如 setTimeOut 回调中编写，不会捕捉这里的错误，不会变为 rejected 状态，会导致全局错误
