---
tags:
  - '#pernamant'
---

docker是一种虚拟化容器技术，用于解决为了运行一台服务，而在各个设备，环境中配置繁琐的问题。

docker有三个重要的概念：
* [[Dockerfile]]
* [[镜像image]]
* [[容器container]]
docker根据”菜谱” Dockerfile做菜，根据这个菜谱，可以做出来和菜谱里面成品“图片”一样的菜，这张图片就是镜像image，但这个菜还没做出来，要真正把这道菜做出来，叫做容器container。可以根据这张镜像，做出来好几道一模一样的菜，每道菜之间没有关联，即每个container之间互不影响


如果我想创建多个docker，运行这么多步骤，很是繁琐，因此有docker-compose.yaml这样的配置文件，一键`docker compose up -d`

## 具体过程

**创建镜像**

编写Dockerfile
在与Dockerfile同级的目录下执行
```
docker build -t <镜像名称>:<标签> .
```
这里的 `.` 是指的是在命令目录下搜索Dockerfile来执行构建[[镜像image]]

**创建容器**

```
docker run -p <主机端口>:<容器端口> --name <容器名称> <镜像名称>:<标签>
```
-p是port端口 
-d是可以让容器在后台运行，就不会占用shell面板

**查看正在运行的容器**
```
docker ps
```


## docker compose

```
docker-compose down
```
关闭compose 

```
docker-compose up
```

开启 compose，
```
-d 后台运行
--build 重新构建再运行
```













# reference
