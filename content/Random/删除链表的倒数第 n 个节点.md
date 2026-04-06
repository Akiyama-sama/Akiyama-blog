---
date: 2026-04-02
tags:
---
给你一个链表，删除链表的倒数第 `n` 个结点，并且返回链表的头结点

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

function removeNthFromEnd(head: ListNode | null, n: number): ListNode | null {
    const dommy = new ListNode(0,head)
    let curr = head
    let length = 0
    while(curr){
        length++
        curr = curr.next
    }
    
    curr = dommy
    for(let i =0;i<length-n;i++){
        curr = curr.next
    }

    let next = curr.next

    curr.next = next?.next
    return dommy.next 
};
```

双指针法

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

function removeNthFromEnd(head: ListNode | null, n: number): ListNode | null {
    //快慢指针法：slow and fast相差 n 个节点，fast 先走，fast 走到末尾，说明此时 slow 就是倒数第 n 个的前驱节点
    const dommy = new ListNode(0,head)
    let slow = dommy
    let fast = dommy

    //fast 先走 n 步
    for(let i = 0;i<n;i++){
        fast  = fast.next
    }
    
    while(fast && fast.next){
        //同时走，直到 fast.next 为空，此时 slow为倒数 第 n 个前驱节点
        fast = fast.next
        slow = slow.next
    }

    //删除倒数第 n 个节点
    if (slow && slow.next) {
        slow.next = slow.next.next;
    }
    return dommy.next
};
```