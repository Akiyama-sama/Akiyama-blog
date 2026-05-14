---
date: 2026-04-04
tags:
  - 前端实习挑战
  - 前端
  - 算法
---
给你链表的头节点 `head` ，每 `k` 个节点一组进行翻转，请你返回修改后的链表。

`k` 是一个正整数，它的值小于或等于链表的长度。如果节点总数不是 `k` 的整数倍，那么请将最后剩余的节点保持原有顺序。

你不能只是单纯的改变节点内部的值，而是需要实际进行节点交换。


```ts
/**
 * Definition for singly-linked list.
 * class ListNode {
 *     val: number
 *     next: ListNode | null
 *     constructor(val?: number, next?: ListNode | null) {
 *         this.val = (val===undefined ? 0 : val)
 *         this.next = (next===undefined ? null : next)
 *     }
 * }
 */

function reverseKGroup(head: ListNode | null, k: number): ListNode | null {
  //第一步，找出从哪里到哪里需要进行翻转，记录下来
  //第二遍，利用上一个反转链表 2 的思路，将每一个从a 到 b 的链表进行反转
  const dommy = new ListNode(0,head)

  let curr = head
  let length = 0
  while(curr){
    length ++
    curr = curr.next
  }

  
  let divisor = Math.floor(length / k)

  curr = head
  let pre = dommy
  while(divisor){
    //循环执行 divisor 次
    for(let i = 0;i<k-1;i++){
        let next= curr.next
        curr.next = next.next
        next.next =pre.next
        pre.next = next
    }

    for(let i=0;i<k;i++){
        //移动 k 次 pre，移动一次 cur
        pre = pre.next
    }
    curr = curr.next
    divisor--
  }
  return dommy.next
};
```