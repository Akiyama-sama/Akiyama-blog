---
tags:
  - '#pernamant'
---
```css
.e{
	animation:/名字/ /动画时间/ /运动流畅度（linear ease）/ /是否循环播放 infinite/
}
```

例如：
```css
.venus_forearm {
        animation: venus_forearm 2s ease infinite;
        transform-origin: 159.7px 575.7px;
        transform: rotate(15deg);
        overflow: visible;
      }
```
这个需要结合关键帧才能动起来
```css
@keyframes venus_forearm {
        0% {
          transform: rotate(-10deg);
        }
        30% {
          transform: rotate(40deg);
        }

        100% {
          transform: rotate(-10deg);
        }
      }
```


# reference
https://developer.mozilla.org/zh-CN/docs/Web/CSS/animation