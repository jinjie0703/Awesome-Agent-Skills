# 📐 大厂级 RESTful API 设计规范与标准手册

本文档定义了企业级 RESTful API 契约设计的黄金准则。

---

## 🌐 一、 URL 路由设计规范

1. **统一使用名词复数**：`/api/v1/orders`（严禁使用 `/api/v1/createOrder` 或 `/api/v1/get_user`）；
2. **小写与连字符 (kebab-case)**：`/api/v1/user-profiles`；
3. **层级表示归属关系**：`/api/v1/users/{user_id}/orders`；
4. **非 CRUD 动作使用动词后缀**：如取消订单 `/api/v1/orders/{id}/cancel`，发布文章 `/api/v1/articles/{id}/publish`。

---

## 🚦 二、 HTTP 动词与状态码映射

| 动作 | HTTP Method | 成功状态码 | 语义 |
| :--- | :---: | :---: | :--- |
| 查询列表 / 详情 | **GET** | `200 OK` | 幂等、安全 |
| 创建新资源 | **POST** | `201 Created` | 非幂等 |
| 全量覆盖更新 | **PUT** | `200 OK` | 幂等 |
| 增量局部修改 | **PATCH** | `200 OK` | 幂等/非幂等 |
| 删除资源 | **DELETE** | `200 OK` 或 `204 No Content` | 幂等 |

---

## 📦 三、 全局统一 JSON 响应体

```json
{
  "code": 0,
  "msg": "success",
  "data": {
    "id": 1001,
    "status": "PAID"
  },
  "trace_id": "req_a9f8b7c6d5"
}
```

* **`code`**：业务错误码，`0` 表示完全成功，非 `0` 表示业务异常（如 `40001: 余额不足`）；
* **`trace_id`**：微服务全链路追踪唯一 ID，便于日志关联定位；
* **`data`**：核心业务数据载荷。

---

## 🛡️ 四、 接口幂等性设计 (Idempotency)

对于支付、下单、扣减库存等关键写操作：
- 客户端在 Header 中附带全局唯一令牌：`X-Idempotency-Key: <UUID>`；
- 服务端使用 Redis `SETNX` 锁定 10 秒，防止网络抖动导致的重复扣费。
