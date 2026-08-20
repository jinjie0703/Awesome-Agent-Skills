# 🌐 api_designer - 大厂级 RESTful & RPC 接口契约架构师

[![Skill Version](https://img.shields.io/badge/Skill-v1.0.0-blue.svg)]()
[![Python Version](https://img.shields.io/badge/Python-3.9%2B-green.svg)]()
[![No Dependencies](https://img.shields.io/badge/Dependencies-None-brightgreen.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)]()

> 一键将模糊的业务需求，转化为工业级 RESTful API 契约与多端工程脚手架！自动生成标准 OpenAPI 3.0 YAML、TypeScript 类型契约、Pydantic 校验模型与 Mock 数据！

---

## 🤔 解决什么痛点？

日常前后端协同与接口设计时，常常存在诸多混乱：
- ❌ **路由乱象丛生**：URL 动词混用（如 `/getUser`、`/api/delete_order`），严重违反 RESTful 规范；
- ❌ **返回体格式不统一**：有的返回纯数组，有的返回字典，缺少全局错误码 `code` 与全链路追踪 `trace_id`；
- ❌ **忽视并发安全**：关键的支付、下单接口缺少防重复提交的幂等性（Idempotency-Key）设计；
- ❌ **多端类型同步繁琐**：后端改了字段，前端手写 TypeScript 类型容易产生拼写错误和类型漂移。

👉 **`api_designer` 的解决方案**：提供一套完整的 API 契约生成与规范化设计引擎，一键同步生成 OpenAPI YAML、TypeScript 接口与 Pydantic 校验类！

---

## ✨ 核心特性

- 📜 **标准 OpenAPI 3.0 规范生成**：自动生成完整的 Swagger / OpenAPI YAML 文件，支持直接导入 Postman / Apifox；
- 💻 **TypeScript 前端类型同步**：自动输出带泛型响应体、分页入参和实体属性的 `contracts.ts`；
- 🐍 **Python Pydantic 后端模型**：自动生成带字段校验、默认值与中文文档注释的 `schemas.py`；
- 🛡️ **生产级防御设计**：内置 `X-Idempotency-Key` 幂等性令牌声明与全链路 `trace_id`；
- ⚡ **零外部依赖**：仅使用 Python 3.9+ 标准库，全平台快速运行！

---

## 📂 目录结构

```text
api_designer/
├── README.md                      # 👥 本说明文档（给人类开发者看）
├── SKILL.md                       # 🤖 AI Agent 专用接口设计 SOP 脑机接口
├── references/
│   └── api_standards.md           # 📐 大厂级 RESTful API 设计规范标准手册
└── scripts/
    └── api_scaffold.py            # 🛠️ OpenAPI 3.0 / TypeScript / Pydantic 生成器
```

---

## 🚀 快速开始 (CLI)

### 1. 使用内置示例生成演示 API 脚手架
```bash
python scripts/api_scaffold.py --demo --output-dir ./demo_api
```

### 2. 基于自定义 JSON 定义生成契约
```bash
python scripts/api_scaffold.py --api-json my_api.json --output-dir ./output_api
```

---

## 📄 License
MIT
