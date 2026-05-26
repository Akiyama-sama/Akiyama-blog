---
date: 2026-05-21
tags:
aliases:
private: true
---
[[create 包架构图]]
## `create` 应用层核心解读

### 一、两种运行模式：独立部署 vs 微前端子应用

这是 `create` 和 `esp-mobile` **最大的区别**——`create` 同时支持两种运行模式：

```46:46:packages/create/src/app.tsx
const isMicro = (window as any).__POWERED_BY_QIANKUN__;
```

| 模式 | 触发条件 | 初始化路径 |
|---|---|---|
| **独立部署**（正常访问磁力金牛） | `__POWERED_BY_QIANKUN__` 为 false | `defaultInit()` — 完整流程 |
| **微前端子应用**（被小店等宿主加载） | `__POWERED_BY_QIANKUN__` 为 true | `microInit()` — 轻量流程 |

---

### 二、`defaultInit()` — 独立模式完整启动顺序

```49:133:packages/create/src/app.tsx
```

**① UC SDK 初始化**（`init()`）
与 mobile 不同，PC 端的 UC 登录拦截器非常简洁，只配置了：
- `interceptorUnLogged` → 未登录跳 `/welcome`
- `interceptorAccount` → 未选账号跳 `/welcome`（黑名单排除 CDN 域名）
- `interceptorShopAccount` → 电商子账号 215 错误专用处理
- `enable_ad_login_api: true`, `appName: 'bid'`, `subBiz: 'pc'`

**② `initUser(global, history)`** — 核心鉴权流程（见下节）

**③ 版本判断** `getSystemVersion()`
```101:109:packages/create/src/app.tsx
const systemVersion = window.localStorage.getItem('LAST_USED_SYSTEM_VERSION');
if (!global.isPcV3User && global?.user?.userId) {
    return ESystemVersion.V2;   // 非 V3 白名单用户强制 V2
} else {
    return systemVersion || ESystemVersion.V3; // 有记录取记录，否则默认 V3
}
```

**④ 后台并行数据加载**
```111:115:packages/create/src/app.tsx
global.getABTestList();        // AB 实验列表
global.fetchUserQuota();       // 创意配额
if (global.whiteList.unitBudgetQuotaSwitch) {
    global.fetchUnitQuota();   // 广告组预算配额（白名单才拉）
}
```

**⑤ 水印** — 等首屏 FMP 上报后异步执行，避免阻塞渲染

---

### 三、`initUser()` — 权限校验详解

```78:159:packages/create/src/utils/user.ts
```

**两处关键差异（对比 esp-mobile）：**

1. **PC 端先 `login()` 再拉数据**，而 mobile 是先注册拦截器（`registerLoginService`）、再靠 axios 拦截器自动拦截。PC 是主动式，mobile 是被动式。

2. **错误码分支更细**，PC 需要处理附身登录（CRM/代理商）失败的多种情况：

```116:157:packages/create/src/utils/user.ts
```

| 错误码 | 场景 | 处理方式 |
|---|---|---|
| `RESULT_LOGIN (109)` | 登录态失效 | uc sdk 自动处理 + 埋点 |
| `RESULT_MULTIPLE_ACCOUNTS (209)` | 多账号 | uc sdk 处理 + 埋点 |
| `LOGIN_ERROR_CODE.isSuixintuiAccount` | 随心推账号无权限 | Modal.error 提示 |
| `LOGIN_ERROR_CODE.noPermission` | 附身无权限 | Modal.error + 跳 /welcome |
| 其他 | 未知错误 | throw 抛出 → `defaultInit` catch → 渲染 ErrorCatch |

---

### 四、路由体系

共 **9 条路由**，全部是 BrowserRouter（非 Hash），路径都以 `/niucreate` 为前缀（微应用部署隔离需要）：

| 路径 | 组件 | 说明 |
|---|---|---|
| `/` 或 `/niucreate` | `Create` | **标准版 PC 创编**（你截图中看到的界面） |
| `/niucreate/simple` | `CreateSimple` | 极简版创编（小店风格，步骤流） |
| `/niucreate/super` | `SuperCreate` | **V3 版本 / 小店子账号专用**（全新 UI） |
| `/niucreate/live-setting` | `LiveSetting` | 直播设置页 |
| `/niucreate/storeCreate` 或 `/storeCreate` | `CreateStoreWide` | 全站创编（两个 path 是 nginx 切流时兼容旧路由） |
| `/niucreate/cidCreate` | `cidCreate` | CID 广告创编 |
| `/niucreate/CombinationHostingModal` | `HostingModalCreate` | 组合托管弹窗形态 |

> `/storeCreate` 和 `/niucreate/storeCreate` 指向同一组件，注释里明确说明是"切 nginx 时使用"，避免业务中断。

---

### 五、微前端子应用模式（qiankun）

```192:223:packages/create/src/app.tsx
```

当被小店（kwai-shop）等宿主通过 qiankun 加载时，触发生命周期：

- **`mount(props)`**：接收宿主传来的 `accountId`、`x7User`（直播间/主播信息）等，存入 `microStore`
- 初始化走 `microInit()`，**跳过 UC SDK 登录**（宿主已处理登录态）
- `rootContainer` 根据 `microStore` 的参数决定渲染哪个组件：

```159:190:packages/create/src/app.tsx
// 路径是 /storeCreate → CreateStoreWide
// 小店子账号 V3 开关 + 是管理员 → SuperCreate
// 否则 → CreateSimple（标准极简版）
```

---

### 六、`Create` 页面的核心结构（标准版）

`Create/index.tsx` 里有一个关键的 `VERSIONS` 映射表（约 30+ 条），按「营销目标 × 流量场域 × 投放方式」三个维度组合成 `EVersion` 枚举键，对应不同的 `moduleGroups` 组件：

```103:146:packages/create/src/pages/Create/index.tsx
// 举例：
EVersion.productProductSaleShowCustom → <ProductProductSaleShowCustom />  // 商品售卖-通投-自定义
EVersion.liveLivingRoomDealSearchHost → <LiveLivingRoomDealSearchHost />  // 直播成交-搜索-托管
```

用户在 UI 上选择「营销目标→投放场景→流量场域→投放方式」后，`store.version` 随之变化，React 根据这个 key 渲染对应的 `moduleGroups` 组件树——这是标准版创编的核心路由机制（**逻辑路由**，不是 URL 路由）。

---

### 七、Provider 层嵌套（非微前端模式）

```
LoggerProvider          (埋点日志 Context)
  RomePCEspScenceProvider  (罗马营销 SDK：注入 request/context/logger/history)
    HelmetProvider      (动态 <title> 管理)
      Root              (ErrorBoundary)
        Header / SuperHeader
        <routes 子页面>
        EspRobot2 (AI 客服，条件渲染)
    ConfigProvider (m-ui, zh_CN)
```

**与 mobile 的关键差异**：PC 端多了 `HelmetProvider`（动态 SEO title）、`Root`（class 组件版 ErrorBoundary），以及 `EspRobot2` AI 客服浮层是在根组件全局挂载的（而非某个页面内）。