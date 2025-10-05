---
tags:
  - '#pernamant'
  - '#算法'
---
多模匹配算法（Aho-Corasick）中文名叫AC自动机算法。

## 简介
输入：匹配词库，匹配字符串
输出：找出字符串中出现过的所有匹配词

## 算法

### 预处理
1. [[Trie树]]的构建（将词库变成树这样的数据结构）
2. Fail指针的构建：当某个节点匹配失败的时候，可以重新指向可能匹配的最近分支上

## 匹配
匹配字符串进行匹配




# reference
https://www.bilibili.com/video/BV1Ag41117YU/?spm_id_from=333.337.search-card.all.click
[[唱歌背单词AI初次开发]]