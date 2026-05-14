---
date: 2026-04-12
tags:
  - 前端实习挑战
  - 前端
  - 手撕题
  - JavaScript
---
```js
class Scheduler {
    //并发限制数
    limit
    runningCount
    queue = []

    constructor(limit){
        this.limit = limit
    }

    add = (task)=>{
        return new Promise((resolve,reject)=>{
            this.queue.push(async ()=>{
                try {
                    const result = await task()
                    resolve(result)
                } catch (error) {
                   reject(error) 
                }
            })
            this.runNext()
        })
    }

    runNext = ()=>{
        //达到了并发限制，直接不做
        if(this.runningCount>this.limit) return
        //没有达到，直接从队头出，开始执行
        this.runningCount++
        const task = this.queue.shift()
        if(task){
            task().finally(()=>{
                this.runningCount--
                this.runNext()
            })
        }
    }
}

const sleep = (ms,n) => new Promise(resolve => {
    setTimeout(()=>{
        console.log(`任务${n} 开始执行`)
    },ms)
})

const task1 = sleep(1000,'1')
const task2= sleep(1000,'2')
const task3 = sleep(1000,'3')

const scheduler = new Scheduler(2)
const res1=scheduler.add(task1)
const res2=scheduler.add(task2)
const res3=scheduler.add(task3)

let time = 0
const timeId = setInterval(()=>{
    console.log(`现在是第 ${time++} s`)
},1000)

Promise.all([res1,res2,res3]).then(()=>{
    console.log('所有任务完成 ----')
    clearInterval(timeId)
})

```