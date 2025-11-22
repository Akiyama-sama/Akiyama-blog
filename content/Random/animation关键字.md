---
date: 2025-11-20
tags:
  - "#CSS"
---
是在动画开始播放与结束以及中间状态下定义某个时态的CSS样式，然后浏览器自动计算出这个过程的动画播放，因此，我们需要定义中间时刻的样式，就需要用到关键帧

结构：
```css
@keywords 自定义关键帧名{
	from {
	
	}
	to {
	
	}
}
```

from to可以用百分比来替代，指代动画进行的百分比时刻

自定义有关键帧名用于传递给animation属性的animation-name值，animation属性是执行动画的执行者，这里写的关键帧就像写好的舞台脚本，递给演员（animation）去真正演绎

animation的各个属性有：
- animation-name：之前所说的自定义关键帧名
- animation-duration：动画持续时间/播放周期
- animation-timing-function：动画移动曲线函数，具体有哪些可以查看MDN文档
- animation-delay：延迟多少秒才开始播放
- animation-iteration-count：执行多少次，infinite为无限次
- animation-direction：设置关键帧的运行方向
- animation-fill-mode：定义关键帧中那些值动画开始前或结束后保留
- animation-play-state：设置动画播放开关
