---
date: 2026-05-03
tags:
  - 前端实习挑战
  - 前端
  - 算法
---
**有效 IP 地址** 正好由四个整数（每个整数位于 `0` 到 `255` 之间组成，且不能含有前导 `0`），整数之间用 `'.'` 分隔。

- 例如：`"0.1.2.201"` 和 `"192.168.1.1"` 是 **有效** IP 地址，但是 `"0.011.255.245"`、`"192.168.1.312"` 和 `"192.168@1.1"` 是 **无效** IP 地址。

给定一个只包含数字的字符串 `s` ，用以表示一个 IP 地址，返回所有可能的**有效 IP 地址**，这些地址可以通过在 `s` 中插入 `'.'` 来形成。你 **不能** 重新排序或删除 `s` 中的任何数字。你可以按 **任何** 顺序返回答案。


```ts
function restoreIpAddresses(s: string): string[] {
    const res: string[] = []; // 明确类型

    function backtrack(index: number, path: string[]) {
        const remainChars = s.length - index; // 修正剩余长度计算
        const remainSegments = 4 - path.length;

        // 剪枝
        if (remainChars < remainSegments || remainChars > remainSegments * 3) {
            return;
        }

        // 递归出口
        if (path.length === 4) {
            if (index === s.length) {
                res.push(path.join('.'));
            }
            return;
        }

        for (let len = 1; len <= 3; len++) {
            let end = index + len;
            if (end > s.length) break;

            const currSegment = s.substring(index, end);
            
            // 验证单段合法性（比验证整串更高效）
            if (isValidSegment(currSegment)) {
                path.push(currSegment);    // 选择
                backtrack(end, path);      // 递归：传入 end 作为下一次的 index
                path.pop();                // 回溯
            }
        }
    }

    function isValidSegment(seg: string): boolean {
        if (seg.length > 1 && seg.startsWith('0')) return false;
        const num = Number(seg);
        return num >= 0 && num <= 255;
    }

    backtrack(0, []); // 必须在函数体外启动
    return res;
}
```