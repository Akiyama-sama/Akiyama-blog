---
date: 2026-05-21
tags:
aliases:
private: true
---
需求网址：[网址](https://docs.corp.kuaishou.com/d/home/fcAATyy6W5blHb6DrpwlDPuR7)

主要负责做平台触点 AI 形象升级这块，步骤：
- 先去找到十个触点的位置，有的是在全码的仓库的组件库，有的是低码仓库的组件库，有的低码组件库的位置分散在各个位置当中，目前锁定两个低代码仓库当中：
	- Ad-create-comps
	- Esp-lowcow-components
	 找到位置过后，在进行一个技术设计，给出一般技术方案过后再与 mentor 进行技术评审，评审完毕过后再进行一个执行
- 再翻一翻小圆的文档看看组件是如何设计，然后看本仓库的组件是如何设计的，主要按照仓库的组件来设计

调研了一下，可以用一下步骤：
1. 在 @ad/create-assets 里新增 ConceptExplainPopover 并导出。
2. 同时把 @ad/create-assets 内部已有触点先替换成这个组件。
3. 发布/升级 @ad/create-assets 版本。
4. kuaishou-frontend-esp-create 和 kuaishou-frontend-esp 升级依赖版本后，在本地触点里 import 新组件接入。


[[快手 - 需求 - 平台触点 AI 形象升级 概念 hover 新组件]]

这个需求主要是让我找各个触点在哪儿，通过去各个仓库，各个包去找，这样就能快速熟悉各个包之间的依赖关系

所以不仅仅是做一个新组件那么简单，还要更改已有的一些组件，引入这个新组件，还要考虑白名单、微前端等各种 edge case，看这些仓库的代码简直是一种享受，各种类型定义得明明白白，非常容易定位查找。

