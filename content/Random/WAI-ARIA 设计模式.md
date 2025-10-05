---
tags:
  - '#pernamant'
---
全称为：“Web Accessibility Initiative – Accessible Rich Internet Applications”，由W3C所指定的规范，

主要包含以下几个方面：
- **期望的 HTML 结构与 ARIA 角色**: 应该使用哪些 HTML 标签作为基础？需要为这些标签添加什么 ARIA `role`？
    - _例如，对于一个“选项卡”组件，模式会规定需要一个 `role="tablist"` 的容器，里面包含多个 `role="tab"` 的元素，以及对应的 `role="tabpanel"` 内容区域。_
- **必需的 ARIA 属性和状态**: 需要哪些 `aria-*` 属性来建立元素之间的关系和描述它们的当前状态？
    - _例如，`aria-selected` 用于标识当前激活的选项卡；`aria-controls` 用于将选项卡按钮与其控制的内容面板关联起来。_
- **键盘交互规范**: 用户应该如何只通过键盘来操作这个组件？
    - _例如，对于选项卡，模式规定用户可以使用 `左/右箭头` 在选项卡之间切换，使用 `Tab` 键移入和移出整个选项卡组件，使用 `Enter` 或 `空格键` 激活选项卡。_
- **动态行为**: 当用户与组件交互时，ARIA 属性应该如何动态更新？
    - _例如，当用户点击一个新的选项卡时，应该将前一个选项卡的 `aria-selected` 设置为 `"false"`，新选项卡设置为 `"true"`，并更新 `tabindex` 来管理焦点。



# reference
