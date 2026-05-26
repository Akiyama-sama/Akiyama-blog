---
date: 2026-05-21
tags:
aliases:
private: true
---
这是[[create 包]]以及[[esp-mobile]] 包的其中一个依赖，用于表单校验，API 端点生成等等的物料库

```
packages/biz-mobile/src/
├── fields/          ← 字段物料（核心）
│   ├── scene/       ← 场景类字段：投放商品、主播账号、营销目标…
│   ├── setting/     ← 投放设置类字段：出价、预算、速度…
│   ├── creative/    ← 素材类字段：素材列表、素材建设类型…
│   ├── target/      ← 定向类字段：地区、年龄、性别…
│   ├── payment/     ← 支付类字段：优惠券、收银台…
│   └── package/     ← 套餐类字段
├── action/          ← API 请求物料（每个字段的数据来源）
├── validators.ts    ← 公共校验器物料
├── watchers.ts      ← 公共监听器物料
├── atom/            ← 原子级工具物料
└── global/          ← 全局常量/工具物料
```

"物料"= **字段的行为描述 + 数据逻辑**，是 PC 和 Mobile 共享的业务逻辑层，两端的 UI 各自消费它，形成"逻辑共享、视图分离"的架构。


