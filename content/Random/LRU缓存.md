---
date: 2026-04-05
tags:
  - 前端实习挑战
  - 前端
  - 算法
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

golang版本

```go
package geecache

import "container/list"

type Node struct {
	key   string
	value Value
}
type Value interface {
	Len() int
}

type LRU struct {
	maxBytes  int64
	currBytes int64
	cache     map[string]*list.Element
	ll        *list.List
	OnEvicted func(key string, value Value) //删除节点后的回调
}

func NewLRU(maxBytes int64) *LRU {
	return &LRU{
		maxBytes:  maxBytes,
		currBytes: 0,
		cache:     make(map[string]*list.Element),
		ll:        list.New(), //双向链表
	}
}

func (l *LRU) Get(key string) (value Value, ok bool) {
	//去找是否有这个 key，有的话直接返回，并且把那个节点放在双向链表的队头，没有返回 false
	if ele, ok := l.cache[key]; ok {
		//把这个节点放在队头
		l.ll.MoveToFront(ele)
		kv := ele.Value.(*Node)
		return kv.value, true
	}
	return nil, false
}

func (l *LRU) RemoveTail() {
	ele := l.ll.Back()
	if ele != nil {
		l.ll.Remove(ele)
		kv := ele.Value.(*Node)
		delete(l.cache, kv.key)
		l.currBytes -= int64(len(kv.key)) + int64(kv.value.Len())

		if l.OnEvicted != nil {
			l.OnEvicted(kv.key, kv.value)
		}
	}
}

func (l *LRU) Put(key string, val Value) {
	//看 cache 有没有这个节点，有的话直接更新到队头，并更新这个节点的 val和内存大小，没有的话直接新增一个节点到队头，并且如果超出了最大内存，直接删除节点直到小于最大内存位置
	if ele, ok := l.cache[key]; ok {
		//有
		l.ll.MoveToFront(ele)
		kv := ele.Value.(*Node)
		//更新内存的值
		l.currBytes += int64(val.Len()) - int64(kv.value.Len())
		//更新缓存的值
		kv.value = val

	} else {
		//没有,把这个节点加进去
		node := Node{key, val}
		ele := l.ll.PushFront(&node)
		l.cache[key] = ele
		l.currBytes += int64(len(key)) + int64(val.Len())
	}
	//while 循环，无论是更新val 还是新增节点，都可能超出内存
	for l.maxBytes != 0 && l.maxBytes < l.currBytes {
		l.RemoveTail()
	}
}

```