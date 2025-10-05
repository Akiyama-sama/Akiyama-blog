---
tags:
  - literature
---
Cache——解决CPU和主存之间速度不匹配而采用的一项 重要技术，由 SRAM 和 控制逻辑 组成

其中 分配给Cache的 地址存放在一个 ==相联存储器CAM== 中，它是按内容 寻址的。

CPU与Cache之 间的数据交换是 以==字==为单位，而 Cache与主存之 间的数据交换是 以==块(行)==为单位


CPU-Cache-主存的交互逻辑：
*  当CPU执行访存 指令时，就把所 要访问的字W的 地址先送到CAM 。由Cache控制 逻辑依据地址判 断此字当前是否 在 cache中
*  如果CAM指出所 要访问的字W在 Cache中，则把 W从Cache传送 到CPU
*  如果W不在 Cache中，则将 W的地址送给主存，从主存传送 到CPU，同时把包含W的由前后 相继的4个字所组成的一行数据 送入Cache中。

# Cache的技术指标——cache的命中率
![file-20241208122141084](https://obsidian-picgo-mio.oss-cn-hangzhou.aliyuncs.com/file-20241208122141084.png)
# Cache的技术指标——系统平均访问时间

![file-20241208122234828](https://obsidian-picgo-mio.oss-cn-hangzhou.aliyuncs.com/file-20241208122234828.png)

例题：[[第3章  存储系统1031.pdf#page=18&selection=0,3,1,7|第3章  存储系统1031, 页面 18]]

# 主存与cache的地址映射——全相联映射
![file-20241208124750304](https://obsidian-picgo-mio.oss-cn-hangzhou.aliyuncs.com/file-20241208124750304.png)

Cache的行内地址=主存的块内地址
块内的存储单位多少位没有指定的话，默认是1B

块号决定块的位置，行号决定Cache的哪一行
主存中的每一块可以映射到Cache中的任意一行

例题：
[[第3章  存储系统1031.pdf#page=27&selection=51,0,55,5|第3章  存储系统1031, 页面 27]]

# 主存与cache的地址映射——直接映射

主存的每一块只可以映射到Cache特定的一行中

![file-20241208131738794](https://obsidian-picgo-mio.oss-cn-hangzhou.aliyuncs.com/file-20241208131738794.png)
模把主存分为32个区，一个区有8个块，区中的每个块只能映射到对应位置的Cache行中

![file-20241208132059144](https://obsidian-picgo-mio.oss-cn-hangzhou.aliyuncs.com/file-20241208132059144.png)

其中，tag就是模

例题：[[第3章  存储系统1031.pdf#page=39&selection=72,0,72,4|第3章  存储系统1031, 页面 39]]


# 主存与cache的地址映射——组相联映射

![file-20241208132801046](https://obsidian-picgo-mio.oss-cn-hangzhou.aliyuncs.com/file-20241208132801046.png)
组内全相联映射，组间直接映射

例题：
[[第3章  存储系统1031.pdf#page=49&selection=0,4,10,0|第3章  存储系统1031, 页面 49]]

# Cache的替换策略

最不经常使用（LFU）算法：将一段时间内被访问次数最少的那行数据替 换出去。
*  每行设置一个计数器，从0开始计数; 
* 每访问一次， 被访行的计数器增1; 
* 需要替换时，将计数值最小的行换出，同时将这些行的计数器都清零。 
* 特点：将计数周期限定在对这些特定行两次替换之间的间隔时间内， 不能严格反映近期访问情况。

近期最少使用（LRU）算法：将近期内长久未被访问过的行替换出去。
* 每行也设置一个计数器; 
* 每访问一次，被访行的计数器清零，其它各行计数增1； 
* 当需要替换时，将计数值最大的行换出。 
* 特点：保护了刚拷贝到cache中的新数据行，使Cache的使用率较高。
随机替换算法
# reference
 