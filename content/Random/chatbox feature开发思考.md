---
date: 2025-12-18
tags: 
---
# feature 功能概述

- 支持原生chatbox聊天功能
- 支持选项替代消息：即点击选项算是发了一条消息
- 支持前端卡渲染：消息组件的渲染不是写死的，而是这个游戏（引擎）作者自己写好的消息模板，把这个模版套在对话当中，以实现作者最大程度上的创作自由。在竞品 [PVESO](https://pveso.com/)当中，他们采用了JSON美化这一实现方式，JSON 模板渲染基于 **LiquidJS** ，支持插值，条件判断、循环、过滤器等常用语法；采取沙箱执行，避免任意 JS 代码。我认为这个可以借鉴一下
- chatbox与galgame模式切换：需要支持会话切换为galgame模式，即响应的一个消息中，以换行符为切割点，一块一块的向用户展示，即点击后展示下一块消息


# 遇到的问题

因为目前后端接口还没有支持前端美化，但产品这里提出来未来可能需要支持前端美化的功能，因此写之前需要考虑到可维护，可拓展的消息组件设计。以及切换galgame模式，对我来说是一项不小的挑战。

# 类型定义

```ts
export interface EnginePlayResponse {
  data: EnginePlayData
  success: boolean
}

export interface EnginePlayData {
  currentScene: CurrentScene
  session: Session //历史会话
}
//当前最新消息以及选项
export interface CurrentScene {
  choices: CurrentChoice[]
  context: string //未来可能用```json ```来进行包裹,利用LiquidJS来进行渲染
  memoryUpdates: string
  metadata: Metadata
}

  

export interface CurrentChoice {
  id: string
  risk: string //用不到
  text: string
}

  

export interface Metadata {
  characters: any[]
  time: string
}

  

export interface Session {
  createdAt: string
  currentStep: number
  engineId: string
  id: string //sessionId
  storyHistory: StoryHistory
  updatedAt: string
  userChoices: UserChoices //用不上
  userId: string
}

  

export interface StoryHistory {
  events: HistoryEvent[]
}

  

export interface HistoryEvent {
  id: string
  type: string
  content: string
  choices: HistoryChoice[]
  outcome: string
  metadata: HistoryMetadata
  timestamp: string

}

export interface HistoryChoice {
  id: string
  text: string
  description: string //用不到
  risk: string //用不到
  consequence: string //用不到
}

export interface HistoryMetadata {
  contentLength: number
  format: string
  interactiveStory: string
  raw_content: string
  suggestedActions: string
}

export interface UserChoices {
  choices: any[]
}
```
# 业务流程

1. 进入时调用`/api/v1/engine-play/start`接口获取id，即会话id
2. 拿着这个id调用`/engine-play/sessions/{sessionId}`这个接口获取整个会话的数据，拿着这个数据渲染出之前的历史对话，历史选项/对话，当前消息，当前选项。
3. 用户发起消息前，调用`/payment/check-balance`查询余额，有余额再允许用户发起消息
4. 发起消息有两种模式：手写消息进行发送/用户点击选项发送。根据用户的喜好，调用流式/非流式的`/engine-play/sessions/{sessionId}/choice`发送消息的接口，然后根据流式/非流的接口，通过不同的渲染逻辑，来渲染出最新消息，即`CurrentScene`这个最新消息
5. 用户可以选择不同的渲染模式，切换为默认模式（chatbox）/（galgame）模式
6. 就算用户退出这个会话，也可以在另外一个路由，获取自己进行过的会话列表，然后再进入这个会话。


