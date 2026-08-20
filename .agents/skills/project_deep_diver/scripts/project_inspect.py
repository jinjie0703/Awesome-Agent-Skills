#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
project_inspect.py - 项目技术栈与架构指纹扫描仪
自动遍历项目目录，统计代码行数、识别技术栈指纹、提取核心依赖清单，
为 AI Agent 深度挖掘面试项目提供真实的底层素材。

用法:
  python project_inspect.py <project_dir> [--max-depth 5] [--output report.json]
"""

import sys
import os
import json
import argparse
from pathlib import Path
from collections import defaultdict

# 确保 Windows 终端 UTF-8 编码正常输出
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

# ============================================================
# 1. 语言识别映射（后缀 -> 语言名）
# ============================================================
LANG_MAP = {
    ".py": "Python", ".pyx": "Python",
    ".js": "JavaScript", ".mjs": "JavaScript", ".cjs": "JavaScript",
    ".ts": "TypeScript", ".tsx": "TypeScript",
    ".vue": "Vue",
    ".jsx": "React JSX",
    ".java": "Java",
    ".go": "Go",
    ".rs": "Rust",
    ".c": "C", ".h": "C/C++ Header",
    ".cpp": "C++", ".cc": "C++", ".cxx": "C++",
    ".cs": "C#",
    ".rb": "Ruby",
    ".php": "PHP",
    ".swift": "Swift",
    ".kt": "Kotlin", ".kts": "Kotlin",
    ".scala": "Scala",
    ".dart": "Dart",
    ".lua": "Lua",
    ".sh": "Shell", ".bash": "Shell", ".zsh": "Shell",
    ".sql": "SQL",
    ".html": "HTML", ".htm": "HTML",
    ".css": "CSS", ".scss": "SCSS", ".less": "LESS",
    ".md": "Markdown",
    ".yaml": "YAML", ".yml": "YAML",
    ".json": "JSON",
    ".xml": "XML",
    ".proto": "Protobuf",
    ".dockerfile": "Dockerfile",
}

# ============================================================
# 2. 忽略目录与文件
# ============================================================
IGNORE_DIRS = {
    "node_modules", ".git", ".svn", "__pycache__", ".venv", "venv",
    "env", ".env", "dist", "build", ".next", ".nuxt", "target",
    ".idea", ".vscode", ".agents", ".gemini", "vendor",
    "coverage", ".tox", ".mypy_cache", ".pytest_cache",
}

IGNORE_FILES = {".DS_Store", "Thumbs.db", ".gitkeep"}


# ============================================================
# 3. 技术栈指纹检测器
# ============================================================
def detect_tech_fingerprints(project_dir: Path, all_files: list[str]) -> dict:
    """通过关键配置文件识别项目核心技术栈与架构指纹"""
    fingerprints = {
        "frameworks": [],
        "ai_and_llm": [],
        "databases": [],
        "infrastructure": [],
        "security_and_auth": [],
        "microservices_and_mq": [],
        "monorepo": [],
        "package_managers": [],
        "ci_cd": [],
        "key_dependencies": [],
    }

    file_names = {Path(f).name.lower() for f in all_files}
    file_set = {f.lower() for f in all_files}

    # --- Monorepo 检测 ---
    if "pnpm-workspace.yaml" in file_names or "pnpm-workspace.yml" in file_names:
        fingerprints["monorepo"].append("Pnpm Workspaces")
    if "turbo.json" in file_names:
        fingerprints["monorepo"].append("Turborepo")
    if "lerna.json" in file_names:
        fingerprints["monorepo"].append("Lerna")
    if sum(1 for f in file_names if f == "pom.xml") > 1:
        fingerprints["monorepo"].append("Maven Multi-Module")

    # --- 前端 & Node.js 框架 ---
    if "package.json" in file_names:
        fingerprints["package_managers"].append("npm/yarn/pnpm")
        pkg_path = project_dir / "package.json"
        if pkg_path.exists():
            try:
                with open(pkg_path, "r", encoding="utf-8") as f:
                    pkg = json.load(f)
                all_deps = {}
                all_deps.update(pkg.get("dependencies", {}))
                all_deps.update(pkg.get("devDependencies", {}))
                deps_keys_lower = {k.lower() for k in all_deps.keys()}
                fingerprints["key_dependencies"] = list(all_deps.keys())[:30]

                if "vue" in all_deps or "@vue/cli-service" in all_deps:
                    ver = all_deps.get("vue", "unknown")
                    fingerprints["frameworks"].append(f"Vue {ver}")
                if "react" in all_deps:
                    ver = all_deps.get("react", "unknown")
                    fingerprints["frameworks"].append(f"React {ver}")
                if "next" in all_deps:
                    fingerprints["frameworks"].append("Next.js")
                if "nuxt" in all_deps or "@nuxt/core" in all_deps:
                    fingerprints["frameworks"].append("Nuxt.js")
                if "vite" in all_deps:
                    fingerprints["frameworks"].append("Vite")
                if "webpack" in all_deps:
                    fingerprints["frameworks"].append("Webpack")
                if "express" in all_deps:
                    fingerprints["frameworks"].append("Express.js")
                if "nest" in all_deps or "@nestjs/core" in all_deps:
                    fingerprints["frameworks"].append("NestJS")
                if "element-plus" in all_deps or "element-ui" in all_deps:
                    fingerprints["frameworks"].append("Element UI/Plus")
                if "ant-design-vue" in all_deps or "antd" in all_deps:
                    fingerprints["frameworks"].append("Ant Design")
                if "axios" in all_deps:
                    fingerprints["frameworks"].append("Axios (HTTP Client)")
                if "pinia" in all_deps:
                    fingerprints["frameworks"].append("Pinia (State Management)")
                if "vuex" in all_deps:
                    fingerprints["frameworks"].append("Vuex (State Management)")
                if "redux" in all_deps or "@reduxjs/toolkit" in all_deps:
                    fingerprints["frameworks"].append("Redux (State Management)")
                if "tailwindcss" in all_deps:
                    fingerprints["frameworks"].append("TailwindCSS")
                if "typescript" in all_deps:
                    fingerprints["frameworks"].append("TypeScript")
                if "prisma" in all_deps or "@prisma/client" in all_deps:
                    fingerprints["databases"].append("Prisma ORM")
                if "mongoose" in all_deps:
                    fingerprints["databases"].append("MongoDB (Mongoose)")
                if "redis" in all_deps or "ioredis" in all_deps:
                    fingerprints["databases"].append("Redis")

                # AI / LLM 前端或 Node
                if "openai" in deps_keys_lower:
                    fingerprints["ai_and_llm"].append("OpenAI SDK")
                if "langchain" in deps_keys_lower or "@langchain/core" in deps_keys_lower:
                    fingerprints["ai_and_llm"].append("LangChain.js")
                if "jsonwebtoken" in deps_keys_lower or "jwt-decode" in deps_keys_lower:
                    fingerprints["security_and_auth"].append("JWT")
                if "socket.io" in deps_keys_lower or "ws" in deps_keys_lower:
                    fingerprints["microservices_and_mq"].append("WebSocket")
                if "kafkajs" in deps_keys_lower:
                    fingerprints["microservices_and_mq"].append("KafkaJS")
                if "amqplib" in deps_keys_lower:
                    fingerprints["microservices_and_mq"].append("RabbitMQ (amqplib)")
                if "@grpc/grpc-js" in deps_keys_lower:
                    fingerprints["microservices_and_mq"].append("gRPC (Node.js)")
            except Exception:
                pass

    # --- Python 后端与 AI 栈 ---
    if "requirements.txt" in file_names:
        fingerprints["package_managers"].append("pip")
        req_path = project_dir / "requirements.txt"
        if req_path.exists():
            try:
                with open(req_path, "r", encoding="utf-8") as f:
                    deps = [line.strip().split("==")[0].split(">=")[0].split("<=")[0].split("~=")[0].lower()
                            for line in f if line.strip() and not line.startswith("#")]
                fingerprints["key_dependencies"].extend(deps[:30])
                if "django" in deps:
                    fingerprints["frameworks"].append("Django")
                if "flask" in deps:
                    fingerprints["frameworks"].append("Flask")
                if "fastapi" in deps:
                    fingerprints["frameworks"].append("FastAPI")
                if "celery" in deps:
                    fingerprints["infrastructure"].append("Celery (Async Task Queue)")
                if "redis" in deps:
                    fingerprints["databases"].append("Redis")
                if "pymysql" in deps or "mysqlclient" in deps:
                    fingerprints["databases"].append("MySQL")
                if "psycopg2" in deps or "asyncpg" in deps:
                    fingerprints["databases"].append("PostgreSQL")
                if "sqlalchemy" in deps:
                    fingerprints["databases"].append("SQLAlchemy ORM")
                if "pymongo" in deps:
                    fingerprints["databases"].append("MongoDB")
                if "tortoise-orm" in deps:
                    fingerprints["databases"].append("Tortoise ORM (Async)")

                # AI / LLM 栈
                if "langchain" in deps or "langchain-core" in deps:
                    fingerprints["ai_and_llm"].append("LangChain (LLM Orchestration)")
                if "llama-index" in deps or "llamaindex" in deps:
                    fingerprints["ai_and_llm"].append("LlamaIndex (RAG Framework)")
                if "openai" in deps:
                    fingerprints["ai_and_llm"].append("OpenAI Python SDK")
                if "ollama" in deps:
                    fingerprints["ai_and_llm"].append("Ollama (Local LLM)")
                if "vllm" in deps:
                    fingerprints["ai_and_llm"].append("vLLM (High-throughput Serving)")
                if "chromadb" in deps:
                    fingerprints["ai_and_llm"].append("ChromaDB (Vector DB)")
                if "pymilvus" in deps or "milvus" in deps:
                    fingerprints["ai_and_llm"].append("Milvus (Vector DB)")
                if "qdrant-client" in deps:
                    fingerprints["ai_and_llm"].append("Qdrant (Vector DB)")
                if "pinecone-client" in deps:
                    fingerprints["ai_and_llm"].append("Pinecone (Vector DB)")
                if "transformers" in deps or "torch" in deps:
                    fingerprints["ai_and_llm"].append("PyTorch / HuggingFace Transformers")

                # 安全 & RPC & MQ
                if "pyjwt" in deps or "python-jose" in deps:
                    fingerprints["security_and_auth"].append("JWT (PyJWT/JOSE)")
                if "casbin" in deps:
                    fingerprints["security_and_auth"].append("Casbin (RBAC/ABAC)")
                if "grpcio" in deps:
                    fingerprints["microservices_and_mq"].append("gRPC (Python)")
                if "pika" in deps:
                    fingerprints["microservices_and_mq"].append("RabbitMQ (Pika)")
                if "confluent-kafka" in deps or "kafka-python" in deps:
                    fingerprints["microservices_and_mq"].append("Kafka (Python)")
            except Exception:
                pass

    if "pyproject.toml" in file_names:
        fingerprints["package_managers"].append("pyproject (PEP 621)")

    # --- Java / Spring ---
    if "pom.xml" in file_names:
        fingerprints["package_managers"].append("Maven")
        fingerprints["frameworks"].append("Java (Maven Project)")
    if "build.gradle" in file_names or "build.gradle.kts" in file_names:
        fingerprints["package_managers"].append("Gradle")
        fingerprints["frameworks"].append("Java/Kotlin (Gradle Project)")
    # Spring Boot / Spring Cloud
    if any("springboot" in f or "spring-boot" in f for f in file_set):
        fingerprints["frameworks"].append("Spring Boot")
    if any("springcloud" in f or "spring-cloud" in f for f in file_set):
        fingerprints["microservices_and_mq"].append("Spring Cloud")
    if any("nacos" in f for f in file_set):
        fingerprints["microservices_and_mq"].append("Nacos (Registry & Config)")
    if any("dubbo" in f for f in file_set):
        fingerprints["microservices_and_mq"].append("Apache Dubbo")
    if any("sa-token" in f for f in file_set):
        fingerprints["security_and_auth"].append("Sa-Token")
    if any("spring-security" in f for f in file_set):
        fingerprints["security_and_auth"].append("Spring Security")
    if any("mybatis" in f for f in file_set):
        fingerprints["databases"].append("MyBatis / MyBatis-Plus")

    # --- Go ---
    if "go.mod" in file_names:
        fingerprints["package_managers"].append("Go Modules")
        fingerprints["frameworks"].append("Go")
        go_mod_path = project_dir / "go.mod"
        if go_mod_path.exists():
            try:
                with open(go_mod_path, "r", encoding="utf-8") as f:
                    mod_text = f.read().lower()
                if "gin-gonic/gin" in mod_text:
                    fingerprints["frameworks"].append("Gin (Go)")
                if "gorm.io/gorm" in mod_text:
                    fingerprints["databases"].append("GORM")
                if "google.golang.org/grpc" in mod_text:
                    fingerprints["microservices_and_mq"].append("gRPC (Go)")
                if "golang-jwt/jwt" in mod_text:
                    fingerprints["security_and_auth"].append("JWT (Go)")
            except Exception:
                pass

    # --- Rust ---
    if "cargo.toml" in file_names:
        fingerprints["package_managers"].append("Cargo")
        fingerprints["frameworks"].append("Rust")

    # --- 基础设施 ---
    if "dockerfile" in file_names or any(f.endswith("dockerfile") for f in file_set):
        fingerprints["infrastructure"].append("Docker")
    if "docker-compose.yml" in file_names or "docker-compose.yaml" in file_names:
        fingerprints["infrastructure"].append("Docker Compose")
    if "nginx.conf" in file_names or any("nginx" in f for f in file_set):
        fingerprints["infrastructure"].append("Nginx")
    if "kubernetes" in file_names or any("k8s" in f for f in file_set) or any(f.endswith(".k8s.yaml") for f in file_set):
        fingerprints["infrastructure"].append("Kubernetes")

    # --- CI/CD ---
    if any(".github/workflows" in f for f in all_files):
        fingerprints["ci_cd"].append("GitHub Actions")
    if ".gitlab-ci.yml" in file_names:
        fingerprints["ci_cd"].append("GitLab CI")
    if "jenkinsfile" in file_names:
        fingerprints["ci_cd"].append("Jenkins")

    # 去重
    for key in fingerprints:
        fingerprints[key] = list(dict.fromkeys(fingerprints[key]))

    return fingerprints


# ============================================================
# 4. 代码行数统计器
# ============================================================
def count_lines(file_path: Path) -> int:
    """安全统计单个文件的行数"""
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return sum(1 for _ in f)
    except Exception:
        return 0


def scan_project(project_dir: str, max_depth: int = 5) -> dict:
    """深度扫描项目目录，生成完整技术侦查报告"""
    root = Path(project_dir).resolve()
    if not root.exists() or not root.is_dir():
        return {"error": f"目录不存在或非文件夹: {project_dir}"}

    lang_stats = defaultdict(lambda: {"files": 0, "lines": 0})
    all_files = []
    total_files = 0
    total_lines = 0
    dir_structure_top = []

    for dirpath, dirnames, filenames in os.walk(root):
        # 计算当前深度
        rel = Path(dirpath).relative_to(root)
        depth = len(rel.parts)
        if depth > max_depth:
            dirnames.clear()
            continue

        # 过滤忽略目录
        dirnames[:] = [d for d in dirnames if d not in IGNORE_DIRS]

        # 收集顶层结构
        if depth <= 1:
            for d in sorted(dirnames):
                dir_structure_top.append(f"📁 {rel / d}/")
            for fn in sorted(filenames):
                if fn not in IGNORE_FILES:
                    dir_structure_top.append(f"📄 {rel / fn}")

        for fn in filenames:
            if fn in IGNORE_FILES:
                continue
            fp = Path(dirpath) / fn
            rel_path = str(fp.relative_to(root)).replace("\\", "/")
            all_files.append(rel_path)
            total_files += 1

            ext = fp.suffix.lower()
            # Dockerfile 特殊处理
            if fn.lower() == "dockerfile" or fn.lower().endswith(".dockerfile"):
                lang = "Dockerfile"
            else:
                lang = LANG_MAP.get(ext)

            if lang:
                lines = count_lines(fp)
                lang_stats[lang]["files"] += 1
                lang_stats[lang]["lines"] += lines
                total_lines += lines

    # 排序：按代码行数降序
    sorted_langs = sorted(lang_stats.items(), key=lambda x: x[1]["lines"], reverse=True)

    # 技术栈指纹
    fingerprints = detect_tech_fingerprints(root, all_files)

    # 主语言判定
    code_langs = [item for item in sorted_langs
                  if item[0] not in {"Markdown", "JSON", "YAML", "XML", "SQL", "HTML", "CSS", "SCSS", "LESS"}]
    primary_language = code_langs[0][0] if code_langs else (sorted_langs[0][0] if sorted_langs else "Unknown")

    report = {
        "project_path": str(root),
        "primary_language": primary_language,
        "total_files": total_files,
        "total_code_lines": total_lines,
        "language_breakdown": {lang: stats for lang, stats in sorted_langs},
        "tech_fingerprints": fingerprints,
        "top_level_structure": dir_structure_top[:40],
    }

    return report


# ============================================================
# 5. Markdown 简报生成
# ============================================================
def generate_markdown_brief(report: dict) -> str:
    """将扫描报告转换为 Markdown 简报"""
    lines = []
    lines.append(f"# 🔍 项目技术侦查报告")
    lines.append(f"**扫描路径**: `{report['project_path']}`\n")
    lines.append(f"## 📊 基础数据")
    lines.append(f"- **主语言**: {report['primary_language']}")
    lines.append(f"- **文件总数**: {report['total_files']}")
    lines.append(f"- **代码总行数**: {report['total_code_lines']:,}\n")

    lines.append(f"## 🗂️ 语言构成")
    lines.append(f"| 语言 | 文件数 | 行数 | 占比 |")
    lines.append(f"| :--- | :---: | :---: | :---: |")
    total = max(report["total_code_lines"], 1)
    for lang, stats in report["language_breakdown"].items():
        pct = round(stats["lines"] / total * 100, 1)
        lines.append(f"| {lang} | {stats['files']} | {stats['lines']:,} | {pct}% |")

    fp = report["tech_fingerprints"]
    lines.append(f"\n## 🧬 技术栈与架构指纹")
    if fp.get("frameworks"):
        lines.append(f"- **主框架/核心库**: {', '.join(fp['frameworks'])}")
    if fp.get("ai_and_llm"):
        lines.append(f"- **AI / 大模型与向量库**: {', '.join(fp['ai_and_llm'])}")
    if fp.get("monorepo"):
        lines.append(f"- **多包/Monorepo 体系**: {', '.join(fp['monorepo'])}")
    if fp.get("security_and_auth"):
        lines.append(f"- **安全与认证鉴权**: {', '.join(fp['security_and_auth'])}")
    if fp.get("microservices_and_mq"):
        lines.append(f"- **微服务/RPC/消息队列**: {', '.join(fp['microservices_and_mq'])}")
    if fp.get("databases"):
        lines.append(f"- **数据库/ORM/缓存**: {', '.join(fp['databases'])}")
    if fp.get("infrastructure"):
        lines.append(f"- **基础设施与容器**: {', '.join(fp['infrastructure'])}")
    if fp.get("package_managers"):
        lines.append(f"- **包管理器**: {', '.join(fp['package_managers'])}")
    if fp.get("ci_cd"):
        lines.append(f"- **CI/CD 流水线**: {', '.join(fp['ci_cd'])}")

    if fp.get("key_dependencies"):
        lines.append(f"\n## 📦 核心依赖清单 (Top 20)")
        for dep in fp["key_dependencies"][:20]:
            lines.append(f"- `{dep}`")

    lines.append(f"\n## 🏗️ 顶层目录结构")
    for item in report["top_level_structure"][:30]:
        lines.append(f"- {item}")

    return "\n".join(lines)


def backup_file(file_path: Path) -> str:
    """在修改前自动创建 .bak 备份副本"""
    if not file_path.exists():
        return ""
    import shutil
    bak_path = file_path.with_suffix(f".bak{file_path.suffix}")
    shutil.copy2(str(file_path), str(bak_path))
    return str(bak_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="项目技术栈与架构指纹扫描仪")
    parser.add_argument("project_dir", help="待扫描的项目根目录路径")
    parser.add_argument("--max-depth", type=int, default=5, help="最大扫描深度 (默认 5)")
    parser.add_argument("--output", "-o", help="输出 JSON 报告文件路径 (可选)")
    parser.add_argument("--markdown", action="store_true", help="同时输出 Markdown 格式简报")
    args = parser.parse_args()

    report = scan_project(args.project_dir, args.max_depth)

    if "error" in report:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        sys.exit(1)

    if args.output:
        out_path = Path(args.output)
        bak_msg = ""
        if out_path.exists():
            bak = backup_file(out_path)
            if bak:
                bak_msg = f"（原报告已备份至: {bak}）"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"JSON 报告已保存至: {out_path}{bak_msg}")

    if args.markdown:
        md = generate_markdown_brief(report)
        print(md)
    elif not args.output:
        print(json.dumps(report, ensure_ascii=False, indent=2))
