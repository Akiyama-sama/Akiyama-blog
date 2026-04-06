---
date: 2026-04-04
tags:
---
给定一个已排序的链表的头 `head` ， _删除原始链表中所有重复数字的节点，只留下不同的数字_ 。返回 _已排序的链表_

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

function deleteDuplicates(head: ListNode | null): ListNode | null {
    const dommy  = new ListNode(0,head)
    let curr = head
    let pre = dommy
    
    
    while(curr && curr.next){
        if(curr.val === curr.next.val) {
            let x = curr.val

            while(curr && curr.val == x){
                curr = curr.next
            }
            pre.next  = curr

        }else {
            pre = pre.next
            curr = curr.next
        }
    }

    return dommy.next
};
```