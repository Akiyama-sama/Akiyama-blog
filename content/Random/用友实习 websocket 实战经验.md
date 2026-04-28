---
date: 2026-04-15
tags:
---
**结论**
这个 `/machine` 不是普通“页面切换”，而是一个“后端流程配置 + 前端 WebSocket 事件驱动”的状态机。前端本地只保存少量核心状态，比如 `step / flows / record / recordList / points / progress / exception`，真正的推进很多时候不是点按钮后直接跳页，而是先发接口，再等后端通过 WebSocket 把“当前步骤”推回来，所以它非常适合写成你那条“基于 WebSocket 的多步骤流程状态机”。核心入口在 [routes/index.js](/Users/mac/Develop/work/yongyou/ib-iv-fe/ucf-apps/ibd/igs/scheme/src/routes/index.js#L395)、[machine/IndexView](/Users/mac/Develop/work/yongyou/ib-iv-fe/ucf-apps/ibd/igs/scheme/src/routes/machine/components/IndexView/index.js#L46)、[machine/model.js](/Users/mac/Develop/work/yongyou/ib-iv-fe/ucf-apps/ibd/igs/scheme/src/routes/machine/model.js#L39)。

**状态机骨架**
- 设备初始化：页面通过 `machine_id` 查询设备配置，拿到 `mached / flowGroups / flows`，默认先加载第一个流程组。[IndexView](/Users/mac/Develop/work/yongyou/ib-iv-fe/ucf-apps/ibd/igs/scheme/src/routes/machine/components/IndexView/index.js#L49) [model.js](/Users/mac/Develop/work/yongyou/ib-iv-fe/ucf-apps/ibd/igs/scheme/src/routes/machine/model.js#L105)
- 状态定义：`step` 存的其实是“当前 flow 在数组里的索引”，真正的业务步骤码是 `flows[step].step`，这点很关键。[IndexView](/Users/mac/Develop/work/yongyou/ib-iv-fe/ucf-apps/ibd/igs/scheme/src/routes/machine/components/IndexView/index.js#L141) [model.js](/Users/mac/Develop/work/yongyou/ib-iv-fe/ucf-apps/ibd/igs/scheme/src/routes/machine/model.js#L179)
- 流程可配置：自助机管理页里 `flowGroups` 是可配置的，默认步骤来自 `group.def`，说明这个状态机不是纯前端硬编码，而是“设备配置驱动”。[machinep/Edit](/Users/mac/Develop/work/yongyou/ib-iv-fe/ucf-apps/ibd/igs/scheme/src/routes/machinep/components/Edit/index.js#L369)
- 双流程组：从首页能进入 `group.id == '1'` 的“判级主流程”，也能进入 `group.id == '2'` 的“进展查询流程”；切组时还会把 `mached.id` 拼上 `,groupId`，回首页再恢复旧 id。[GradeTypeView](/Users/mac/Develop/work/yongyou/ib-iv-fe/ucf-apps/ibd/igs/scheme/src/routes/machine/components/GradeTypeView/index.js#L32) [AuthenticationModelView](/Users/mac/Develop/work/yongyou/ib-iv-fe/ucf-apps/ibd/igs/scheme/src/routes/machine/components/GradeTypeView/AuthenticationModelView/index.js#L47)

```mermaid
stateDiagram-v2
    [*] --> "0 首页"
    "0 首页" --> "1 身份/手动录入": "点击判级"
    "0 首页" --> "6 判级总览": "进展查询 + 口令验证"
    "1 身份/手动录入" --> "2 卸料点": "chengnan_back 后端推送"
    "2 卸料点" --> "3 停车确认": "toGrading + WS"
    "3 停车确认" --> "3 停车确认": "重新校验"
    "3 停车确认" --> "4 入场预报": "开始/恢复判级"
    "4 入场预报" --> "5 隐藏确认态": "本地切到确认弹窗"
    "5 隐藏确认态" --> "6 判级总览": "确认后 toGrading + WS"
    "6 判级总览" --> "7_0 详情": "选择车次"
    "7_0 详情" --> "6 判级总览": "返回"
    "7_0 详情" --> "7_0 详情": "WS 增量刷新"
    "任意状态" --> "10 异常页": "后端推送其他状况"
    "任意状态" --> "首页/复位": "fallback=1 或首页"
```

**完整自助机流程**
1. 首页 `step=0`：欢迎页只有两个入口，“判级”和“进展查询”，并先校验是否处于工作时间。[GradeTypeView](/Users/mac/Develop/work/yongyou/ib-iv-fe/ucf-apps/ibd/igs/scheme/src/routes/machine/components/GradeTypeView/index.js#L47)
2. 判级入口进入主流程组：切到 `group 1`，本地 `step + 1` 进入步骤 1。[GradeTypeView](/Users/mac/Develop/work/yongyou/ib-iv-fe/ucf-apps/ibd/igs/scheme/src/routes/machine/components/GradeTypeView/index.js#L53)
3. 步骤 1 现在不是身份证扫描，而是直接走“手工录入车牌号/毛重/计量单号”。这里还会先调用 `getMeasureId` 自动取计量单号，确认后调用 `chengnanBack`。[ManualInputView](/Users/mac/Develop/work/yongyou/ib-iv-fe/ucf-apps/ibd/igs/scheme/src/routes/machine/components/ManualInputView/index.js#L40) [service.js](/Users/mac/Develop/work/yongyou/ib-iv-fe/ucf-apps/ibd/igs/scheme/src/routes/machine/service.js#L169)
4. 这里有个重要特征：录完并不会本地自己跳到下一页，而是等后端通过 WebSocket 回推 `step == "2"`，再进入“选择卸料点”。[IndexView](/Users/mac/Develop/work/yongyou/ib-iv-fe/ucf-apps/ibd/igs/scheme/src/routes/machine/components/IndexView/index.js#L195)
5. 步骤 2 选择卸料点：用户点某个有效卸料点，写入 `record.pointId / point`，然后发 `toGrading`。[PointsView](/Users/mac/Develop/work/yongyou/ib-iv-fe/ucf-apps/ibd/igs/scheme/src/routes/machine/components/PointsView/index.js#L44)
6. 步骤 3 停车确认：后端推送 `record.vehiclePositionConfirmation`。如果是 `1`，说明停车位置合格，可以“开始判级/恢复判级”；如果不是，则只能“重新校验”；如果是 `2`，前端会弹出等待校验结果的异常模态。[LocalConfirmView](/Users/mac/Develop/work/yongyou/ib-iv-fe/ucf-apps/ibd/igs/scheme/src/routes/machine/components/LocalConfirmView/index.js#L48) [ExceptionView](/Users/mac/Develop/work/yongyou/ib-iv-fe/ucf-apps/ibd/igs/scheme/src/routes/machine/components/ExceptionView/index.js#L77)
7. 步骤 4 入场预报：选择料型和预报等级。这里也很像状态机设计，不是立刻调用后端，而是先把 `materialType / erGrading / step` 写进 store，进入一个隐藏确认态。[EnterGradeView](/Users/mac/Develop/work/yongyou/ib-iv-fe/ucf-apps/ibd/igs/scheme/src/routes/machine/components/EnterGradeView/index.js#L42)
8. 步骤 5 隐藏确认态：`flows[step].display == '1'` 时不会单独渲染页面，而是覆盖一个 `InfoConfirmModelView` 确认弹窗。确认后才真正发 `toGrading` 进入下一步。[IndexView](/Users/mac/Develop/work/yongyou/ib-iv-fe/ucf-apps/ibd/igs/scheme/src/routes/machine/components/IndexView/index.js#L384) [InfoConfirmModelView](/Users/mac/Develop/work/yongyou/ib-iv-fe/ucf-apps/ibd/igs/scheme/src/routes/machine/components/InfoConfirmModelView/index.js#L42)
9. 步骤 6 判级总览：后端推送 `recordList` 后，前端展示车次列表。点某条记录进入详情页 `7_0`。[IndexView](/Users/mac/Develop/work/yongyou/ib-iv-fe/ucf-apps/ibd/igs/scheme/src/routes/machine/components/IndexView/index.js#L207) [RecordSelectView](/Users/mac/Develop/work/yongyou/ib-iv-fe/ucf-apps/ibd/igs/scheme/src/routes/machine/components/RecordSelectView/index.js#L31)
10. 步骤 `7_0` 详情：这里是实时判级结果页，左侧视频/抓拍图，右侧基本信息、判级详情和操作按钮。状态 `onStatus` 决定是否直播、是否允许“结束判级”、是否允许“数据录入”。[ResultView](/Users/mac/Develop/work/yongyou/ib-iv-fe/ucf-apps/ibd/igs/scheme/src/routes/machine/components/ResultView/index.js#L491) [ResultView](/Users/mac/Develop/work/yongyou/ib-iv-fe/ucf-apps/ibd/igs/scheme/src/routes/machine/components/ResultView/index.js#L530)
11. `step == "10"`：统一异常/其他状况页，由后端直接推异常文案。[IndexView](/Users/mac/Develop/work/yongyou/ib-iv-fe/ucf-apps/ibd/igs/scheme/src/routes/machine/components/IndexView/index.js#L232)

**WebSocket 如何驱动状态变换**
- WebSocket 连接地址按设备号拼成 `/websocket/machine/{machineId}`，页面一加载设备成功后就会建立连接。[IndexView](/Users/mac/Develop/work/yongyou/ib-iv-fe/ucf-apps/ibd/igs/scheme/src/routes/machine/components/IndexView/index.js#L513)
- `status == 1` 是业务态推进，`messageBody` 里带 `step / record / recordList / pointList / exception`，前端按步骤码更新 store。[IndexView](/Users/mac/Develop/work/yongyou/ib-iv-fe/ucf-apps/ibd/igs/scheme/src/routes/machine/components/IndexView/index.js#L195)
- `status == 2` 表示同一台设备重复登录，直接把 `step` 打成 `-1`，走错误页。[IndexView](/Users/mac/Develop/work/yongyou/ib-iv-fe/ucf-apps/ibd/igs/scheme/src/routes/machine/components/IndexView/index.js#L237)
- `status == 3` 是服务端心跳响应，前端重启一轮心跳检测；前端每 5 秒发一次 `"isOnLine"`，超时没收到回包就主动 `close()` 触发重连。[IndexView](/Users/mac/Develop/work/yongyou/ib-iv-fe/ucf-apps/ibd/igs/scheme/src/routes/machine/components/IndexView/index.js#L245) [IndexView](/Users/mac/Develop/work/yongyou/ib-iv-fe/ucf-apps/ibd/igs/scheme/src/routes/machine/components/IndexView/index.js#L293)
- 底层 `Websocket` 组件本身还做了断线自动重连，使用指数退避重建连接，所以这里其实是“组件级重连 + 业务级心跳”双保险。[Websocket](/Users/mac/Develop/work/yongyou/ib-iv-fe/ucf-common/src/components/Websocket/index.js#L27)
- `status == 5` 是详情/总览页增量刷新，不改大步骤，只把最新 `record` merge 进当前 `recordList`，非常适合实时判级中的渐进式结果展示。[IndexView](/Users/mac/Develop/work/yongyou/ib-iv-fe/ucf-apps/ibd/igs/scheme/src/routes/machine/components/IndexView/index.js#L252)
- `status == 10` 会在 10 秒后自动刷新整页，属于最终兜底。[IndexView](/Users/mac/Develop/work/yongyou/ib-iv-fe/ucf-apps/ibd/igs/scheme/src/routes/machine/components/IndexView/index.js#L261)

**异常兜底与人工补录**
- 前端自己会先做一次“步骤合法性校验”：如果当前 flow 的 `nextId` 和用户点的下一步不匹配，就弹 `showProgressModal`，阻止非法跳转。[model.js](/Users/mac/Develop/work/yongyou/ib-iv-fe/ucf-apps/ibd/igs/scheme/src/routes/machine/model.js#L185)
- 停车未确认、恢复判级中、多次异常消息都会累计进 `progress[]`，由 `ExceptionView` 统一做进度展示，这个就是“异常兜底面板”。[ExceptionView](/Users/mac/Develop/work/yongyou/ib-iv-fe/ucf-apps/ibd/igs/scheme/src/routes/machine/components/ExceptionView/index.js#L38)
- 结果页支持人工补录，但只在非“判级中”状态开放；打开前会先 `getRecordById` 拉一次最新记录，避免旧数据编辑。[ResultView](/Users/mac/Develop/work/yongyou/ib-iv-fe/ucf-apps/ibd/igs/scheme/src/routes/machine/components/ResultView/index.js#L481) [model.js](/Users/mac/Develop/work/yongyou/ib-iv-fe/ucf-apps/ibd/igs/scheme/src/routes/machine/model.js#L288)
- 补录内容包括人工级别占比、人工扣杂、毛重、皮重，前端会校验“占比和=100”“人工扣杂必填”“重量非负”。[EditModal](/Users/mac/Develop/work/yongyou/ib-iv-fe/ucf-apps/ibd/igs/scheme/src/routes/machine/components/EditModal/index.js#L123)
- 保存后不会只关弹窗，而是再次 `getRecordById`，把最新结果回填到 `record` 和 `recordList`，这正对应你说的“人工补录刷新”。[model.js](/Users/mac/Develop/work/yongyou/ib-iv-fe/ucf-apps/ibd/igs/scheme/src/routes/machine/model.js#L310)

**一句话概括这个自助机状态机**
它本质上是一个“设备配置驱动的流程状态机”：前端根据 `flowGroups/flows` 决定可执行步骤，以 `step(index)` 和 `flow.step(业务码)` 双层状态建模；用户动作只负责触发 `start/back/calc/stop/pause` 等事件，真正的状态推进由 WebSocket 回推完成，同时叠加了心跳保活、断线重连、重复登录拦截、异常进度弹窗和人工补录后的记录重拉刷新。

**如果你要把项目亮点写得更准**
可以改成这版：

- 基于设备配置 `flowGroups/flows` 与 WebSocket 事件回推，构建废钢智能判级自助终端多步骤流程状态机，串联设备初始化、身份录入、卸料点选择、停车校验、预报确认、判级总览与结果详情等核心节点，并实现心跳保活、断线重连、重复登录拦截、异常进度兜底及人工补录后记录刷新，支撑现场复杂判级流程闭环。

如果你愿意，我下一步可以继续帮你把这套流程整理成“面试可讲版本”，包括“状态定义、事件、转移条件、为什么用 WebSocket 而不是轮询”三段话。