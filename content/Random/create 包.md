---
date: 2026-05-21
tags:
aliases:
private: true
---
[[create 包  简要讲解]]
依赖图
```txt
packages/create        -> PC 应用
  依赖:
    @ad/create-biz
    @ad/create-mobile-biz
    @ad/create-component
    
    //上面是内部有，在 monorepo 里面的
    //而下面的这个表单包是在仓库中没有，在另外一个内网仓库的，用于表单验证
    @ad/ad-create-core ← 快手内部另一个仓库发布的
		表单引擎，提供 useModule/SchemaModule/FieldRender
		这是 biz 包和 create 包的"胶水层"
	@ad/create-runtime — 广告创编表单低代码运行时
	@ad/canal-react-runtime — Canal 大运河通用低代码运行时

```
## 经典表单模块 data flow

```txt
UI Components → Actions → Atoms (MobX) → API Calls (Swagger) → Backend
                    ↓
                Validators → Fields System → Form Rendering
```

其中[[biz 包]]就是像[[biz-mobile包]]那样，仅仅负责这个业务对象的封装，包括Validators,actions,api calls等等，create 包仅导入以及使用、组装

以广告计划页当中的表单验证为例：
[[create 包 - 广告计划页面例子]]

- 用 Mobox来对一个领域模型进行建模，包括基本的 state,action ，利用MobX的 obsover 来对整个组件进行包裹，以达到响应式更新的效果。
- 用户操作 UI 触发 onChange，表单引擎（@ad/ad-create-core）检测到字段变化，由于 biz 包里的 watchers 早已挂载，表单引擎执行对应的 watcher 函数处理业务联动，watcher 执行完后再通过 MobX action 将结果同步到 groupValues，触发 observer 组件重渲染
```
用户 onChange → 触发表单引擎 → 执行注册好的 biz watcher →  表单引擎内部状态更新后执行 MobX 的回调 setGroupValues() → MobX 触发 action 更新 groupValues
```
- 提交表单时，先是 [[biz 包]]里的 validators 挂在到表单引擎当中，由表单引擎来触发validators函数，用于校验表单各个字段的合法性
- 最后用本身在[[create 包]]里面写好的 formator 为后端匹配的 DTO 模型给 create包里面的 Swagger 生成的 API 端点发送接口

需要注意的是，这里通过[[MobX]]的**分层领域模型模式**来对不同层级的状态、各个状态的 action 进行管理

例如：
```txt
GlobalStore (单例)       ← 账户级全局状态
    └── CreateStore (页面级)  ← 创编流程总协调
          ├── CampaignModel   ← 广告计划领域
          ├── CustomModel     ← 广告组/创意领域（自定义）
          ├── HostingModel    ← 广告组/创意领域（托管）
          └── BatchModel      ← 广告组/创意领域（批量托管）
```


## 低代码模块

低代码运行时通过 moduleId 从 Canal 服务端拉取 Schema，通过dependencies 将本地包（react、mobx、@m-ui/react 等）注入给 Schema 中的动态代码使用，通过 params.actions 把业务逻辑（服务调用、状态更新）暴露给 Schema，实现了"外壳固定 + 内容服务端下发"的动态化能力。


有以下几个主要低代码场景：

### 一、广告创编表单低代码运行时

**核心组件**

| 组件 / 函数                     | 来自                 | 作用                                   |
| --------------------------- | ------------------ | ------------------------------------ |
| AdCreateReactRuntimeFC      | @ad/create-runtime | 直接渲染低代码 Schema 表单的 FC 组件             |
| createCommonFetchSchema     | @ad/create-runtime | 封装 Schema 拉取逻辑（通过 window.canalFetch） |
| consumeKmiPluginApiPrefetch | @ad/create-runtime | 接入 KMI 插件的 Schema 预请求能力              |
| ConfigParams                | @ad/create-runtime | 向 Runtime 传入的参数类型定义                  |
1. StoreWideProduct/index.tsx — 全站商品推广
2. StoreWideLive/index.tsx — 全站直播推广
3. ConfigCreate/index.tsx — 配置式创编（H5 App 一键流创编）
4. components/AdESPCreateReactRuntimeFC — 封装的通用运行时组件

### 二、Canal 大运河通用低代码运行时

@ad/canal-react-runtime
在 create 应用中**直接被用于 AI 小牛机器人场景**，小牛 AI 一键创编机器人(V1/V2)

### 三、@ad-rome/touch-runtime 和 @ad-rome/esp-pc-scence 相关运行时依赖

整体架构图：

```txt
create 应用
├── App.tsx
│   └── RomePCEspScenceProvider (@ad-rome/esp-pc-scence)  ← 全局 Context
│       └── EspRobot2 (CanalReactRuntimeFC)               ← Canal 大运河运行时 (AI 客服机器人)
│
├── SuperCreate
│   ├── StoreWideProduct → AdCreateReactRuntimeFC         ← 全站商品推广表单 (低代码)
│   ├── StoreWideLive    → AdCreateReactRuntimeFC         ← 全站直播推广表单 (低代码)
│   └── index.tsx        → EspRobot + MarketingTouch      ← AI 机器人 + 营销触点
│
├── Create
│   └── CampaignFormGroup → AdESPCreateReactRuntimeFC     ← 计划表单 (白名单渐进切换)
│
└── ConfigCreate → AdCreateReactRuntimeFC                 ← H5 一键流场景 (低代码)
```

> 这套低代码系统的本质是：**把「表单是什么」从代码里抽离到服务端 Schema 里，通过依赖注入向 Schema 的执行沙箱提供所需能力（UI 组件、业务函数、工具包），同时对外暴露控制句柄（container ref）供外部系统（如 AI 机器人）命令式操控表单状态。**

核心设计模式是 **IoC（控制反转）+ DI（依赖注入）**，宏观上是**微内核架构**。这和你见过的 VSCode 插件系统、Webpack loader 体系是同一套思想的不同表现形式。

