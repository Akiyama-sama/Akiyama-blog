---
URL: https://akiyama-sama.github.io/Akiyama-blog/
---
这是一个仅需编辑Markdown文件，就能同步到站点的博客方案，我的站点URL为
https://akiyama-sama.github.io/Akiyama-blog/

效果：
![](https://obsidian-picgo-mio.oss-cn-hangzhou.aliyuncs.com/20251007125341319.png)

自己想做公开站点的契机可以参考：[[重构笔记系统]]，下面的内容主要是如何搭建这套笔记系统

## 简易教程

站点主要是靠的[quartz](https://github.com/jackyzha0/quartz)项目生成，quartz可以识别content目录下的所有md文档语法，与`[[WIKI]]`语法，自动构建出HTML静态页面，我们在`https://github.com/jackyzha0/quartz`这个仓库上面点右上角的Use  this template按钮，点击Create a new repository,输入自己想要的仓库名，再点击Create repository 这样就能创建好自己的博客仓库了

在`git clone 仓库名`到自己计算机想要的目录过后，在用Obsidian打开仓库中的content文件夹作为Obsidian的仓库，在里面编辑的md文件与`[[WIKI]]`语法就能被渲染出来了

需要注意的是Obsidian设置中需要开启使用Wiki链接以及类型为尽可能简短的形式，这样quartz才能正确识别
![](https://obsidian-picgo-mio.oss-cn-hangzhou.aliyuncs.com/20251007132841469.png)

有关如何定制化样式与布局，官方文档：[Quartz 4](https://quartz.jzhao.xyz/#-get-started)写的很详细了，可以作为参考

如果想直接在本地看到效果，我们需要先在控制台进入到clone下来的仓库目录
然后
```bash
cd 仓库目录
npm i
npx quartz create
npx quartz build --serve
```

然后访问`http://localhost:8080/`就能在本地进行预览了

我这里是直接部署在GitHub Pages里面，我们需要在这个目录下`.github/workflows/`添加`deploy.yml`文件，粘贴以下内容：

```yml
name: Deploy Quartz site to GitHub Pages
 
on:
  push:
    branches:
      - v4
 
permissions:
  contents: read
  pages: write
  id-token: write
 
concurrency:
  group: "pages"
  cancel-in-progress: false
 
jobs:
  build:
    runs-on: ubuntu-22.04
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0 # Fetch all history for git info
      - uses: actions/setup-node@v4
        with:
          node-version: 22
      - name: Install Dependencies
        run: npm ci
      - name: Build Quartz
        run: npx quartz build
      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: public
 
  deploy:
    needs: build
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

然后前往GitHub仓库，点击上方的Settings以及左侧栏的Pages，把Build and deployment改为GitHub Actions
![](https://obsidian-picgo-mio.oss-cn-hangzhou.aliyuncs.com/20251007134310031.png)

然后在本地根目录下运行`npx quartz sync`，等待大概十几分钟的时间，就能构建完成了

构建完成的页面网址，可以在上张图片上上面找到，例如我上面图片中的Visit site按钮

我自己迁移的过程可以在[[重构笔记系统]]里面找到，在迁移过程当中，可能会涉及到附件的迁移，我的方案是把附件都上传到图床当中，这样无论是本地还是站点都能使用同一种Markdown的图片写法

[[如何批量将Obsidian仓库中的本地文件全部上传到图床当中，并且修改图片链接为图床链接]]


