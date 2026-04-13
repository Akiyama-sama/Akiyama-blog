---
date: 2026-04-12
tags:
---
```js
function any(promises){
  return new Promise((resolve,reject)=>{
  const error = []
  let error_count = 0
    promises.forEach((p,index) => {
      Promise.resolve(p).then(res=>{
        resolve(res)
      },err =>{
          error[index] = err
          error_count++
          if
          (error_count === promises.length) new AggregateError(errors, 'All promises were rejected')        }) 
    });
  })
}
```