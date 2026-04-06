---
date: 2026-04-05
tags:
---

```ts
class Node {
    key: number
    pre : Node | null = null
    next : Node |null = null
    val :number
    constructor(key:number,val:number){
        this.key = key
        this.val = val
    }

}

class LRUCache {
    //双向链表，最近用的节点放在靠近最近哨兵节点的 next，最不常用的放在最不常用节点的 pre
     head: Node 
     tail: Node
     map:Map<number,Node>
     capacity: number

    constructor(capacity: number) {
        this.capacity = capacity
        this.map = new Map()
        this.head = new Node(0,0)
        this.tail = new Node(0,0)
        this.head.next = this.tail;
        this.tail.pre = this.head;
    }

    get(key: number): number {
        if(!this.map.has(key)) return -1
        const node = this.map.get(key)
        this.returnToHead(node)
        return node.val
        
    }

    put(key: number, value: number): void {
        if(this.map.has(key)){
            const node = this.map.get(key)
            node.val = value
            this.map.set(key,node)
            this.returnToHead(node)
        }else {
            const node = new Node(key,value)
            this.map.set(key,node)
            this.addNodeToHead(node)
            if(this.map.size>this.capacity){
                const lru =  this.removeTail()
                this.map.delete(lru.key)
                
            }
        }
    }

    // 头部添加节点
    addNodeToHead(node:Node){
        const curr = this.head.next
        node.pre = this.head
        node.next = curr
        curr.pre = node
        this.head.next = node
    }
    //删除指定地方的节点
    removeNode(node:Node){
        const pre = node.pre
        const next = node.next
        pre.next = next
        next.pre = pre
        return node
    }
    //删除队尾的节点
    removeTail():Node{
        const curr = this.tail.pre
        const node = this.removeNode(curr)
        return node
    }

    //把某个节点放到链表头部：即删除这个节点+加到节点头部
    returnToHead(node:Node){
        this.removeNode(node)
        this.addNodeToHead(node)
    }

}

/**
 * Your LRUCache object will be instantiated and called as such:
 * var obj = new LRUCache(capacity)
 * var param_1 = obj.get(key)
 * obj.put(key,value)
 */
```