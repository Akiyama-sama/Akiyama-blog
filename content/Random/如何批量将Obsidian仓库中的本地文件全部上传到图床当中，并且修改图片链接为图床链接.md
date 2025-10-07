
## 前置条件

 安装了node：
 
```bash
 node -v
```

且使用过[Picgo](https://github.com/Molunerfinn/PicGo)成功上传到图床当中

## 简易教程

进入这个仓库：`https://github.com/Akiyama-sama/obsidian-pic-upload`

```bash
git clone https://github.com/Akiyama-sama/obsidian-pic-upload.git
cd obsidian-pic-upload
npm i
```

进入picgo的配置文件，复制文件的全部内容

![](https://obsidian-picgo-mio.oss-cn-hangzhou.aliyuncs.com/Snipaste_2025-10-07_13-55-38.png)

然后粘贴到`obsidian-pic-upload`目录中的`config.json`文件当中，打开picgo.js
![](https://obsidian-picgo-mio.oss-cn-hangzhou.aliyuncs.com/Snipaste_2025-10-07_14-00-37.png)
把你要修改的Obsidian仓库目录粘贴到红线这里
然后运行脚本
```bash
node picgo.js
```
