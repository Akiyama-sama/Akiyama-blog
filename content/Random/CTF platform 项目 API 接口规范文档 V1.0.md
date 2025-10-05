---
tags:
  - '#pernamant'
---

## 1\. 概述

### 1.1. 目的

为规范本项目后端API接口的设计与实现，确保接口的 **一致性** 、 **可预测性** 和 **易用性** ，特制定本规范。本文档旨在为前后端开发人员提供一个共同遵循的契约，提升开发效率，降低联调成本，并实现API文档的自动化生成。

### 1.2. 核心原则

- **统一响应结构** ：所有API端点均需返回统一的JSON响应结构。
- **数据模型驱动** ：所有接口的返回数据（ `data` 字段）必须有明确的Pydantic数据模型定义，以便自动生成符合OpenAPI规范的文档。
- **HTTP状态码语义化** ：正确使用HTTP状态码来反映操作结果的宏观状态。
- **文档先行/自动生成** ：通过代码（类型注解）自动生成 `openapi.json` ，作为前后端交互的唯一真实来源 (Single Source of Truth)。

## 2\. 统一响应格式

所有API的响应体都必须遵循以下统一格式。我们已经为此定义了标准的Pydantic模型。

### 2.1. Pydantic 模型定义

后端应在项目中引入以下基类，所有API的返回类型注解都应使用 `ApiResponse[T]` 的形式。


```Python
# file: project_utils/response.py

from typing import Any, Generic, Optional, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")

class ApiResponse(BaseModel, Generic[T]):
    """统一API响应格式"""

    code: int = Field(200, description="业务状态码，非HTTP状态码")
    message: str = Field("success", description="响应消息")
    data: Optional[T] = Field(None, description="响应数据")

def success_response(data: Any = None, message: str = "success") -> ApiResponse:
    """成功响应"""
    # 注意：这里的HTTP状态码应在FastAPI路由函数中通过 status_code=200 设置,这里的状态码是业务状态码
    return ApiResponse(code=200, message=message, data=data)

def error_response(code: int, message: str, data: Any = None) -> ApiResponse:
    """通用错误响应"""
    # 注意：具体的HTTP状态码应在FastAPI路由函数中通过 status_code=... 设置
    return ApiResponse(code=code, message=message, data=data)

# ... 其他辅助函数 ...
def bad_request_response(message: str = "请求参数错误") -> ApiResponse:
    """400响应体"""
    return error_response(400, message)

def not_found_response(message: str = "资源不存在") -> ApiResponse:
    """404响应体"""
    return error_response(404, message)

def internal_error_response(message: str = "服务器内部错误") -> ApiResponse:
    """500响应体"""
    return error_response(500, message)
```

### 2.2. 字段说明

- `code` (integer): **业务状态码** 。用于前端判断业务逻辑层面的结果。
	- `200`: 表示业务处理成功。
	- `400`: 请求参数错误（如格式、类型不匹配）。
	- `401`: 未授权。
	- `403`: 已授权但无权限访问。
	- `404`: 请求的资源不存在。
	- `500`: 服务器内部未知错误。
	- `1000+`: 自定义业务错误码（例如： `1001` - 用户名已存在， `1002` - 余额不足）。建议维护一个全局的业务错误码列表。
- `message` (string): 对本次请求结果的简短描述，通常用于向用户展示提示信息。
- `data` (object | array | null): 实际的响应数据。
	- 当请求成功且有数据返回时， `data` 为具体的数据对象或数组。
	- 当请求成功但无数据返回（如删除操作）， `data` 为 `null` 。
	- 当请求失败时， `data` 通常为 `null` ，但也可用于承载额外的错误详情。

## 3\. OpenAPI 规范与数据模型 (Pydantic Model)

这是本规范的核心。为了让前端能够清晰地知道每个接口返回的 `data` 的具体结构， **每一个API端点返回的 `data` 都必须定义一个对应的Pydantic模型** 。

### 3.1. 实施要求

1. **禁止使用 `Any` 或 `dict`** ：在定义返回的 `ApiResponse` 时，必须明确指定泛型 `T` 的具体模型。
	- **错误** 示范: `def get_user() -> ApiResponse[Any]: ...`
	- **正确** 示范: `def get_user() -> ApiResponse[UserSchema]: ...`
2. **定义清晰的数据模型** ：为项目中所有核心业务对象（如用户、产品、订单等）创建Pydantic模型。

### 3.2. 实践示例

假设我们需要一个获取用户信息的接口 `GET /users/{user_id}` 。

**第1步：为用户数据定义Pydantic模型**


```Python
# file: schemas/user.py

from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

class UserSchema(BaseModel):
    id: int = Field(..., description="用户ID")
    username: str = Field(..., description="用户名")
    email: EmailStr = Field(..., description="用户邮箱")
    created_at: datetime = Field(..., description="创建时间")

    class Config:
        orm_mode = True # 如果使用ORM，此项可方便地从数据库模型转换
```

**第2步：在FastAPI路由函数中使用该模型和 `ApiResponse`**



```Python
# file: api/endpoints/user.py

from fastapi import APIRouter, HTTPException
from ..schemas.user import UserSchema
from ..utils.response import ApiResponse, success_response, not_found_response
from ..crud import user_crud # 假设的数据库操作模块

router = APIRouter()

@router.get(
    "/users/{user_id}",
    response_model=ApiResponse[UserSchema], # **关键步骤1：指定响应模型**
    summary="获取单个用户信息"
)
def read_user(user_id: int) -> ApiResponse[UserSchema]:
    """
    根据用户ID获取用户的详细信息。
    - 如果用户存在，返回用户信息。
    - 如果用户不存在，返回404错误。
    """
    db_user = user_crud.get_user(user_id=user_id)
    if db_user is None:
        # FastAPI会自动处理HTTPException，将其转换为HTTP 404响应。
        # 但为了统一格式，我们应该返回统一的JSON结构。
        # 更好的做法是在依赖或中间件中捕获HTTPException并转换为我们的格式。
        # 这里为了演示，我们手动返回。
        # 注意：在 FastAPI 中，最好是直接 raise HTTPException，
        # 然后通过 exception_handler 来统一转换成 ApiResponse 格式。
        # 但为清晰起见，此处直接返回 ApiResponse 对象。
        # 在实际项目中，需要配置 status_code。
        # from fastapi import Response
        # response.status_code = 404
        raise HTTPException(status_code=404, detail="User not found")

    # **关键步骤2：使用辅助函数返回标准格式**
    return success_response(data=db_user)

# 建议：添加一个全局异常处理器来捕获HTTPException并转换为我们的格式
from fastapi import Request
from fastapi.responses import JSONResponse

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response(code=exc.status_code, message=exc.detail).dict(),
    )
```

**第3步：生成 `openapi.json`**

当后端项目按上述规范编写后，在项目根目录下创建python文件，复制并且运行脚本：


```Python
# file: generate_openapi.py
from fastapi.openapi.utils import get_openapi
from json import dumps
from hacker_lab.api import app # 替换为您的FastAPI应用实例

def generate_openapi_json():
    openapi_schema = get_openapi(
        title="HackerLab API",
        version="1.0.0",
        description="智能攻防靶场管理API",
        routes=app.routes,
    )
    
    with open("openapi.json", "w", encoding="utf-8") as f:
        f.write(dumps(openapi_schema, ensure_ascii=False, indent=2))

if __name__ == "__main__": 
    generate_openapi_json()
```

### 3.3. openapi.json 预期结果

生成的 `openapi.json` 中，对于 `/users/{user_id}` 接口的 `200` 响应，其结构会非常清晰：


```json
{
  "paths": {
    "/users/{user_id}": {
      "get": {
        "summary": "获取单个用户信息",
        "responses": {
          "200": {
            "description": "Successful Response",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/ApiResponse_UserSchema_"
                }
              }
            }
          }
        }
      }
    }
  },
  "components": {
    "schemas": {
      "UserSchema": {
        "title": "UserSchema",
        "required": ["id", "username", "email", "created_at"],
        "type": "object",
        "properties": {
          "id": { "title": "Id", "description": "用户ID", "type": "integer" },
          "username": { "title": "Username", "description": "用户名", "type": "string" },
          "email": { "title": "Email", "description": "用户邮箱", "type": "string", "format": "email" },
          "created_at": { "title": "Created At", "description": "创建时间", "type": "string", "format": "date-time" }
        }
      },
      "ApiResponse_UserSchema_": {
        "title": "ApiResponse[UserSchema]",
        "type": "object",
        "properties": {
          "code": { "title": "Code", "description": "状态码", "default": 200, "type": "integer" },
          "message": { "title": "Message", "description": "响应消息", "default": "success", "type": "string" },
          "data": { "$ref": "#/components/schemas/UserSchema" }
        }
      }
    }
  }
}
```

