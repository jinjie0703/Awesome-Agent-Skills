---
name: api_designer
description: 大厂级 RESTful 与 RPC 接口契约设计技能。自动生成标准 OpenAPI 3.0 (Swagger) 规范、TypeScript 类型契约、Pydantic/Zod 校验器与 Mock 数据，内置统一错误码、幂等性 Token 与防刷流控设计。在需要设计新 API 接口、定义前后端数据契约、编写 OpenAPI 规范或规范化接口返回值时使用。
category: api-and-architecture
tags: [api, rest, openapi, swagger, typescript, pydantic, contract]
---

# API Designer - 大厂级 RESTful & RPC 接口契约架构师

当用户需要**设计新业务接口**、**规范前后端数据交互契约**、**生成 OpenAPI 3.0 (Swagger) 规范**、或**编写 TypeScript/Pydantic 类型模型**时，严格执行以下 SOP。

---

## ⚙️ 第 0 步：环境检查（零外部依赖）

本技能使用的脚手架生成器仅依赖 Python 3.9+ 标准库，无需安装任何第三方包：
```bash
python --version
```

---

## 🚀 标准操作工作流 (SOP)

### 第 1 步：业务资源建模与动词映射 (Resource Modeling)

AI 将用户提出的业务需求抽象为标准的 RESTful 资源集合：
- **资源命名**：统一使用复数名词及连字符（如 `/api/v1/user-orders`）；
- **层级归属**：子资源体现父子从属关系（如 `/api/v1/orders/{order_id}/items`）；
- **动词规范**：严禁在 URL 中出现 `get_`、`create_` 动词，统一使用 `GET`, `POST`, `PUT`, `PATCH`, `DELETE`。

---

### 第 2 步：统一响应体与分页契约设计

所有接口必须遵循大厂统一返回体结构：

```json
{
  "code": 0,
  "msg": "success",
  "data": {},
  "trace_id": "req_8f9a2b"
}
```

- **分页规范**：入参使用 `page` (从 1 起) 与 `page_size` (默认 20)，返回体使用 `{ list, total, page, page_size, has_more }`。

---

### 第 3 步：关键写操作注入幂等性与防御设计

针对支付、下单、转账等写操作：
- 在请求头中必须声明 `X-Idempotency-Key` 防重令牌；
- 明确指出 HTTP 状态码（如创建成功返回 `201 Created`，并发冲突返回 `409 Conflict`，限流返回 `429 Too Many Requests`）。

---

### 第 4 步：调用代码与契约脚手架生成器 (`api_scaffold.py`)

AI 将设计的 API 结构组装为 JSON 数据，调用脚本生成全套多端契约：

```bash
python .agents/skills/api_designer/scripts/api_scaffold.py \
    --api-json api_definition.json \
    --output-dir ./generated_api
```

**脚手架自动生成**：
- `openapi.yaml`：标准 OpenAPI 3.0 / Swagger 接口规范；
- `contracts.ts`：前端开箱即用的 TypeScript 接口类型定义；
- `schemas.py`：后端直接可用的 Python Pydantic 请求/响应校验模型；
- `mock_response.json`：符合规范的 Mock 测试数据。

---

## 📐 输出规范

- 结构严谨、规范统一，符合 RESTful 行业最佳实践；
- 状态码与业务错误码严禁混用（HTTP 状态码表征传输层，JSON `code` 表征业务层）；
- 涉及 URL 路径与字段名加粗显示。
