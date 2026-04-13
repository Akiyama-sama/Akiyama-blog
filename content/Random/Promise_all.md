---
date: 2026-04-12
tags:
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

