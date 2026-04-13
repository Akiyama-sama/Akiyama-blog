---
date: 2026-04-12
tags:
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