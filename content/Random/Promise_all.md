---
date: 2026-04-12
tags:
  - 前端实习挑战
  - 前端
  - 手撕题
  - JavaScript
---
```js
function all(promises){
  return new Promise((resolve,reject)=>{
  const result = []
  let count = 0
    promises.forEach((p,index) => {
      Promise.resolve(p).then(res=>{
        result[index] = res
        count ++
        if(count === promises.length) resolve(result)
      },error =>{
          reject(error)
        }) 
    });
  })
}

```

