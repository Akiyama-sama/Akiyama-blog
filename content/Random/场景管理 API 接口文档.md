---
tags:
  - '#pernamant'
---

#### **通用规范**

1.  **统一响应格式**: 所有 API 接口的返回数据都遵循统一的 JSON 格式 。
    ```json
    {
        "code": 200,         // 状态码, 200 表示成功，其他为失败
        "message": "success",  // 提示信息
        "data": {}             // 响应数据
    }
    ```
2.  **场景状态 (Status)**: 场景的生命周期由状态机管理，主要包含以下状态：
    * `pending`: 场景已创建，等待编排 
    * `building`: 场景编排构建中 
    * `starting`: 场景各容器启动中 
    * `running`: 场景内所有服务成功启动并运行中 
    * `stopped`: 场景被关闭或成功构建后等待启动 
    * `error`: 场景在构建或启动过程中发生错误 
    * `removing`: 场景正在被删除 

---

### 1. 场景列表与详情

#### 1.1 获取场景列表
此接口用于支持“进入场景” 用例，获取并渲染所有已创建的场景卡片。

* **功能描述**: 获取所有已创建的攻防场景列表。
* **接口路径**: `GET /api/v1/scenarios`
* **请求方法**: `GET`
* **请求参数**: 无
* **成功响应示例 (`code: 200`)**:
    ```json
    {
        "code": 200,
        "message": "success",
        "data": {
            "total": 2,
            "items": [
                {
                    "id": "e4e5f65a-1234-5678-9abc-def012345678",
                    "name": "WebLogic CVE-2017-10271 渗透测试",
                    "status": "stopped"
                },
                {
                    "id": "f5d6a7b8-4321-8765-cba9-fed123456789",
                    "name": "PHP-CGI 远程代码执行漏洞复现",
                    "status": "error"
                }
            ]
        }
    }
    ```

#### 1.2 获取特定场景详情
此接口用于支持“场景配置修改”和 **“场景错误重构”** 用例，当用户点击“详细信息”时，调用此接口获取数据以填充表单。

* **功能描述**: 查询单个场景的详细信息，包括名称、描述和端口映射等。
* **接口路径**: `GET /api/v1/scenarios/{scenario_id}`
* **请求方法**: `GET`
* **成功响应示例 (`code: 200`)**:
    ```json
    {
        "code": 200,
        "message": "success",
        "data": {
            "id": "e4e5f65a-1234-5678-9abc-def012345678",
            "name": "WebLogic CVE-2017-10271 渗透测试",
            "description": "### 场景背景...\n这是一个关于 WebLogic ... 的场景。",
            "status": "stopped",
            "port_mappings": {
                "attacker_mcp": "31501:5001",
                "target_service_8080": "38080:8080"
            }
        }
    }
    ```

---

### 2. 场景创建与修改

#### 2.1 创建新场景
此接口用于支持**“场景创建”**用例。

* [cite_start]**功能描述**: 接收用户提交的场景信息及三个必需的压缩包文件 [cite: 3]，在后台启动一个异步的场景构建任务。
* **接口路径**: `POST /api/v1/scenarios`
* **请求方法**: `POST`
* **请求类型**: `multipart/form-data`
* **请求体 (form-data)**:
    * [cite_start]`name` (string, 必选): 场景名称 [cite: 3]。
    * [cite_start]`description` (string, 必选): Markdown 格式的场景说明 [cite: 3]。
    * [cite_start]`hacker_file` (file, 必选): 攻击容器压缩包 [cite: 3]。
    * [cite_start]`defender_file` (file, 必选): 防御容器压缩包 [cite: 3]。
    * [cite_start]`target_file` (file, 必选): 靶机环境压缩包 [cite: 3]。
* **成功响应示例 (`code: 200`)**:
    ```json
    {
        "code": 200,
        "message": "场景创建任务已提交，正在后台构建中",
        "data": {
            "scenario_id": "a1b2c3d4-e5f6-a7b8-c9d0-e1f2a3b4c5d6"
        }
    }
    ```
* **后端核心逻辑**:
    1.  接收请求，创建数据库记录，状态为 `pending`。
    2.  保存并解压文件，立即返回成功响应。
    3.  **后台异步任务**: 更新状态为 `building`，执行构建。成功后状态变为 `stopped`，失败则变为 `error`。

#### 2.2 修改与重构场景
此接口用于支持**“场景配置修改”**和**“场景错误重构”**用例。

* **功能描述**: 更新指定场景的配置。如果更新了附件，则触发重新构建。
* **接口路径**: `PUT /api/v1/scenarios/{scenario_id}`
* **请求方法**: `PUT`
* **请求类型**: `multipart/form-data`
* **请求体 (form-data)**: (所有字段均为可选，前端只提交被修改的字段)
    * `name` (string, 可选): 新的场景名称。
    * `description` (string, 可选): 新的 Markdown 场景说明。
    * `hacker_file` (file, 可选): 新的攻击容器包。
    * `defender_file` (file, 可选): 新的防御容器包。
    * `target_file` (file, 可选): 新的靶机环境包。
* **成功响应示例 (`code: 200`)**:
    * **情况一：仅修改文字信息**
        ```json
        {
            "code": 200,
            "message": "场景信息更新成功",
            "data": {}
        }
        ```
    * **情况二：修改了附件，触发重构**
        ```json
        {
            "code": 200,
            "message": "附件已更新，正在重新构建场景",
            "data": {}
        }
        ```
* **后端核心逻辑**:
    1.  检查请求中是否包含文件。
    2.  **如果包含文件**: 替换旧文件，更新数据库中的文字信息，然后启动与“创建场景”一致的后台异步重构任务（状态变为 `building`）。
    3.  **如果不含文件**: 仅更新数据库中的 `name` 和 `description` 字段。

---

### 3. 场景控制与删除

#### 3.1 控制场景（启动/停止）
此接口用于支持**“场景启动”**用例。

* [cite_start]**功能描述**: 对已存在的场景执行启动 (Start)、关闭 (Stop) 等操作 [cite: 7]。
* **接口路径**: `POST /api/v1/scenarios/{scenario_id}/control`
* **请求方法**: `POST`
* **请求体 (JSON)**:
    ```json
    {
        "action": "start"
    }
    ```
    [cite_start]( `action` 的可选值为: `start`, `stop`, `restart` [cite: 7] )
* **成功响应示例 (`code: 200`)**:
    ```json
    {
        "code": 200,
        "message": "场景启动指令已发送",
        "data": {}
    }
    ```
* **后端核心逻辑**:
    1.  接收 `action` 指令。
    2.  **对于 `start`**: 启动后台异步任务，将状态更新为 `starting`，执行 `docker-compose up`。成功后状态变为 `running`，失败则变为 `error`。

#### 3.2 删除场景
此接口用于支持**“场景删除”**用例。

* [cite_start]**功能描述**: 彻底停止并删除指定的攻防场景及其相关资源 [cite: 7]。
* **接口路径**: `DELETE /api/v1/scenarios/{scenario_id}`
* **请求方法**: `DELETE`
* **成功响应示例 (`code: 200`)**:
    ```json
    {
        "code": 200,
        "message": "场景删除成功",
        "data": {}
    }
    ```
* **后端核心逻辑**:
    1.  将状态更新为 `removing`。
    2.  后台执行 `docker-compose down`，清理容器和网络。
    3.  删除服务器上的场景文件目录。
    4.  从数据库中删除该场景的记录。