#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
api_scaffold.py - 工业级 API 契约与多端代码脚手架生成器
将结构化 API 描述定义转换为标准 OpenAPI 3.0 (Swagger) YAML、
TypeScript 类型定义、Python Pydantic 校验模型与 Mock 数据。

用法:
  python api_scaffold.py --api-json api_def.json --output-dir ./generated_api
  python api_scaffold.py --demo --output-dir ./demo_api
"""

import sys
import json
import shutil
import argparse
from pathlib import Path

# 确保 Windows 终端 UTF-8 编码正常输出
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


def backup_file(file_path: Path) -> str:
    """在修改前自动创建 .bak 备份副本"""
    if not file_path.exists():
        return ""
    bak_path = file_path.with_suffix(f".bak{file_path.suffix}")
    shutil.copy2(str(file_path), str(bak_path))
    return str(bak_path)


def generate_openapi_yaml(api_data: dict) -> str:
    """生成标准 OpenAPI 3.0 YAML 规范"""
    title = api_data.get("title", "Service API")
    version = api_data.get("version", "1.0.0")
    base_url = api_data.get("base_url", "/api/v1")

    lines = []
    lines.append("openapi: 3.0.3")
    lines.append("info:")
    lines.append(f"  title: \"{title}\"")
    lines.append(f"  version: \"{version}\"")
    lines.append(f"  description: \"{api_data.get('description', 'Auto-generated API specification')}\"")
    lines.append("servers:")
    lines.append(f"  - url: \"{base_url}\"")
    lines.append("paths:")

    for endpoint in api_data.get("endpoints", []):
        path = endpoint.get("path", "/resource")
        method = endpoint.get("method", "get").lower()
        summary = endpoint.get("summary", "Endpoint summary")
        tag = endpoint.get("tag", "Default")

        lines.append(f"  {path}:")
        lines.append(f"    {method}:")
        lines.append(f"      summary: \"{summary}\"")
        lines.append(f"      tags: [\"{tag}\"]")

        # 请求头（如 Idempotency-Key）
        if endpoint.get("idempotent", False):
            lines.append("      parameters:")
            lines.append("        - name: X-Idempotency-Key")
            lines.append("          in: header")
            lines.append("          required: true")
            lines.append("          schema:")
            lines.append("            type: string")
            lines.append("          description: \"防重复提交幂等性 Token\"")

        # 响应体
        lines.append("      responses:")
        lines.append("        '200':")
        lines.append("          description: \"操作成功\"")
        lines.append("          content:")
        lines.append("            application/json:")
        lines.append("              schema:")
        lines.append("                $ref: '#/components/schemas/StandardResponse'")

    # Components 通用响应体
    lines.append("components:")
    lines.append("  schemas:")
    lines.append("    StandardResponse:")
    lines.append("      type: object")
    lines.append("      required: [code, data, msg, trace_id]")
    lines.append("      properties:")
    lines.append("        code:")
    lines.append("          type: integer")
    lines.append("          example: 0")
    lines.append("        msg:")
    lines.append("          type: string")
    lines.append("          example: \"success\"")
    lines.append("        data:")
    lines.append("          type: object")
    lines.append("        trace_id:")
    lines.append("          type: string")
    lines.append("          example: \"req_9a8b7c6d5e\"")

    return "\n".join(lines)


def generate_typescript_types(api_data: dict) -> str:
    """生成 TypeScript 接口类型定义"""
    lines = []
    lines.append("/**")
    lines.append(f" * Auto-generated API TypeScript Contracts - {api_data.get('title', 'Service')}")
    lines.append(" */\n")

    lines.append("/** 全局统一返回体 */")
    lines.append("export interface ApiResponse<T = any> {")
    lines.append("  code: number;")
    lines.append("  msg: string;")
    lines.append("  data: T;")
    lines.append("  trace_id: string;")
    lines.append("}\n")

    lines.append("/** 标准分页请求参数 */")
    lines.append("export interface PaginationQuery {")
    lines.append("  page: number;")
    lines.append("  page_size: number;")
    lines.append("  keyword?: string;")
    lines.append("}\n")

    lines.append("/** 标准分页响应数据 */")
    lines.append("export interface PaginatedData<T> {")
    lines.append("  list: T[];")
    lines.append("  total: number;")
    lines.append("  page: number;")
    lines.append("  page_size: number;")
    lines.append("  has_more: boolean;")
    lines.append("}\n")

    return "\n".join(lines)


def generate_pydantic_models(api_data: dict) -> str:
    """生成 Python Pydantic 请求/响应模型"""
    lines = []
    lines.append("# -*- coding: utf-8 -*-")
    lines.append("from typing import Generic, TypeVar, Optional, List, Any")
    lines.append("from pydantic import BaseModel, Field\n")
    lines.append("T = TypeVar('T')\n")
    lines.append("class ApiResponse(BaseModel, Generic[T]):")
    lines.append("    code: int = Field(0, description='业务状态码, 0 为成功')")
    lines.append("    msg: str = Field('success', description='业务状态提示')")
    lines.append("    data: Optional[T] = Field(None, description='响应数据载荷')")
    lines.append("    trace_id: str = Field(..., description='全链路追踪 ID')\n")
    lines.append("class PaginationQuery(BaseModel):")
    lines.append("    page: int = Field(1, ge=1, description='当前页码')")
    lines.append("    page_size: int = Field(20, ge=1, le=100, description='每页条数')")
    lines.append("    keyword: Optional[str] = Field(None, description='搜索关键词')\n")
    return "\n".join(lines)


def scaffold_api(api_data: dict, out_dir: str) -> str:
    """生成全套 API 契约与脚手架文件"""
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)

    # 1. 生成 openapi.yaml
    openapi_yaml = generate_openapi_yaml(api_data)
    yaml_path = out / "openapi.yaml"
    if yaml_path.exists():
        backup_file(yaml_path)
    yaml_path.write_text(openapi_yaml, encoding="utf-8")

    # 2. 生成 contracts.ts
    ts_content = generate_typescript_types(api_data)
    ts_path = out / "contracts.ts"
    if ts_path.exists():
        backup_file(ts_path)
    ts_path.write_text(ts_content, encoding="utf-8")

    # 3. 生成 schemas.py
    py_content = generate_pydantic_models(api_data)
    py_path = out / "schemas.py"
    if py_path.exists():
        backup_file(py_path)
    py_path.write_text(py_content, encoding="utf-8")

    # 4. 生成 mock_response.json
    mock_data = {
        "code": 0,
        "msg": "success",
        "data": {
            "id": 1001,
            "name": "演示资源",
            "created_at": "2026-08-19T23:50:00Z"
        },
        "trace_id": "req_mock_8f9a2b"
    }
    mock_path = out / "mock_response.json"
    if mock_path.exists():
        backup_file(mock_path)
    mock_path.write_text(json.dumps(mock_data, ensure_ascii=False, indent=2), encoding="utf-8")

    return f"🎉 API 契约与多端脚手架已成功生成至: {out.resolve()}\n包含文件:\n- openapi.yaml (OpenAPI 3.0 规范)\n- contracts.ts (TypeScript 接口契约)\n- schemas.py (Pydantic 校验模型)\n- mock_response.json (标准 Mock 数据)"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="工业级 API 契约与多端代码脚手架生成器")
    parser.add_argument("--api-json", help="输入 API 结构化定义 JSON 文件")
    parser.add_argument("--demo", action="store_true", help="使用内置演示数据生成")
    parser.add_argument("--output-dir", "-o", default="./generated_api", help="输出目录路径")
    args = parser.parse_args()

    if args.demo or not args.api_json:
        demo_data = {
            "title": "Order & Payment Service",
            "version": "1.0.0",
            "base_url": "/api/v1",
            "description": "企业级订单与支付核心接口契约",
            "endpoints": [
                {"path": "/orders", "method": "post", "summary": "创建订单 (带幂等性校验)", "tag": "Order", "idempotent": True},
                {"path": "/orders/{id}", "method": "get", "summary": "查询订单详情", "tag": "Order", "idempotent": False},
                {"path": "/orders", "method": "get", "summary": "分页查询订单列表", "tag": "Order", "idempotent": False}
            ]
        }
        res = scaffold_api(demo_data, args.output_dir)
        print(res)
    else:
        with open(args.api_json, "r", encoding="utf-8") as f:
            data = json.load(f)
        res = scaffold_api(data, args.output_dir)
        print(res)
