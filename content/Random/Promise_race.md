---
date: 2026-04-12
tags:
  - 前端实习挑战
  - 前端
  - 手撕题
  - JavaScript
---
```js
function race(promises){
  return new Promise((resolve,reject)=>{
  promises.forEach((p,index) => {
      Promise.resolve(p).then(res=>{
         resolve(result)
      },error =>{
          reject(error)
        }) 
    });
  })
}
```