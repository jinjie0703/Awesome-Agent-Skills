#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
log_inspector.py - 异常日志与崩溃堆栈指纹分析仪
从海量应用日志或报错文本中提取异常链、关键堆栈行、SQL 报错与高危上下文，
并自动对敏感数据（Token / 密码 / 个人信息）进行脱敏处理。

用法:
  python log_inspector.py app_error.log
  python log_inspector.py app_error.log --markdown
  python log_inspector.py app_error.log --output report.json
"""

import sys
import re
import json
import shutil
import argparse
from pathlib import Path

# 确保 Windows 终端 UTF-8 编码正常输出
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


# 常见跨语言异常特征正则
STACK_PATTERNS = [
    ("Python Exception", re.compile(r'Traceback \(most recent call last\):[\s\S]+?(?:(?:[a-zA-Z_]\w*Error|[a-zA-Z_]\w*Exception|Panic):\s*.+)')),
    ("Java / Spring Exception", re.compile(r'(?:Exception in thread "[^"]+"|[\w\.]+(?:Exception|Error)):[\s\S]+?(?:\tat [\w\.\$]+\([^)]+\)\s*)+')),
    ("Node.js / V8 Error", re.compile(r'(?:[a-zA-Z_]\w*Error):\s*.+\n(?:\s+at\s+.+\s*)+')),
    ("Go Panic", re.compile(r'panic:\s*.+\n\ngoroutine \d+ \[.+\]:\n(?:[\w\.\/\(\)]+\n\t.+:\d+ \+0x[0-9a-f]+\n*)+')),
    ("Rust Panic", re.compile(r'thread \'[^\']+\' panicked at [^\n]+(?:\s+stack backtrace:\s*[\s\S]+)?')),
    ("Database / SQL Error", re.compile(r'(?:SQLException|Deadlock found|Lock wait timeout exceeded|duplicate key value violates unique constraint|Table \'[^\']+\' doesn\'t exist|ORA-\d{5}|PG::\w+Error).*', re.IGNORECASE)),
]

# 敏感信息脱敏正则
MASK_PATTERNS = [
    (re.compile(r'(?i)(?:password|passwd|pwd|secret|api_key|token)\s*[:=]\s*[\'"][^\'"]+[\'"]'), r'\1="******"'),
    (re.compile(r'\b(?:\d{4}-){3}\d{4}\b'), '****-****-****-****'),
    (re.compile(r'\b\d{17}[\dXx]\b'), '******************'),
]


def backup_file(file_path: Path) -> str:
    """在修改前自动创建 .bak 备份副本"""
    if not file_path.exists():
        return ""
    bak_path = file_path.with_suffix(f".bak{file_path.suffix}")
    shutil.copy2(str(file_path), str(bak_path))
    return str(bak_path)


def mask_sensitive(text: str) -> str:
    """对日志中的敏感信息进行脱敏"""
    res = text
    for pattern, repl in MASK_PATTERNS:
        res = pattern.sub(repl, res)
    return res


def extract_stack_traces(log_content: str) -> list:
    """从日志文本中提取出所有独立异常堆栈段落"""
    extracted = []
    seen = set()

    for name, pattern in STACK_PATTERNS:
        for match in pattern.finditer(log_content):
            raw_stack = match.group(0).strip()
            # 去重
            fingerprint = raw_stack[:150]
            if fingerprint in seen:
                continue
            seen.add(fingerprint)

            # 提取核心异常类型和描述（通常在第一行或最后一行）
            lines = raw_stack.splitlines()
            first_line = lines[0].strip()
            last_line = lines[-1].strip()

            error_type = "UnknownError"
            error_message = ""

            if name == "Python Exception":
                error_line = last_line
                if ":" in error_line:
                    error_type, error_message = error_line.split(":", 1)
                else:
                    error_type = error_line
            elif name == "Java / Spring Exception":
                error_line = first_line
                if ":" in error_line:
                    error_type, error_message = error_line.split(":", 1)
                else:
                    error_type = error_line
            else:
                error_type = name
                error_message = first_line

            # 提取可能属于业务代码的最核心报错行（非三方库）
            business_code_lines = []
            for l in lines:
                if any(k in l for k in ["site-packages", "node_modules", "java.base", "spring-core", "gopkg.in"]):
                    continue
                if any(k in l for k in ["File ", "at ", ".go:", ".rs:"]):
                    business_code_lines.append(l.strip())

            extracted.append({
                "language_or_engine": name,
                "error_type": error_type.strip(),
                "error_message": error_message.strip(),
                "top_business_frames": business_code_lines[:5],
                "raw_stack_masked": mask_sensitive(raw_stack[:2000]),
            })

    return extracted


def inspect_log(file_path: str) -> dict:
    """分析日志文件"""
    p = Path(file_path)
    if not p.exists():
        return {"error": f"日志文件不存在: {p.resolve()}"}

    try:
        content = p.read_text(encoding="utf-8", errors="ignore")
    except Exception as e:
        return {"error": f"无法读取日志文件: {e}"}

    stacks = extract_stack_traces(content)
    total_lines = len(content.splitlines())

    # 统计关键词频次
    keyword_stats = {
        "ERROR": len(re.findall(r'\b(?:ERROR|FATAL|CRITICAL)\b', content, re.IGNORECASE)),
        "WARN": len(re.findall(r'\b(?:WARN|WARNING)\b', content, re.IGNORECASE)),
        "TIMEOUT": len(re.findall(r'\b(?:Timeout|Timed out|Connection refused)\b', content, re.IGNORECASE)),
        "DEADLOCK": len(re.findall(r'\b(?:Deadlock|Lock wait timeout)\b', content, re.IGNORECASE)),
        "OOM": len(re.findall(r'\b(?:OutOfMemoryError|OOMKilled|Killed)\b', content, re.IGNORECASE)),
    }

    return {
        "file_path": str(p.resolve()),
        "total_lines": total_lines,
        "keyword_stats": keyword_stats,
        "extracted_stack_count": len(stacks),
        "stacks": stacks
    }


def generate_markdown_report(report: dict) -> str:
    """生成易读的 Markdown 诊断报告"""
    lines = []
    lines.append(f"# 🔍 异常堆栈与日志指纹侦查简报")
    lines.append(f"- **目标日志**: `{report['file_path']}`")
    lines.append(f"- **总行数**: {report['total_lines']:,} 行")
    lines.append(f"- **提取到独立异常堆栈**: {report['extracted_stack_count']} 处\n")

    lines.append(f"## 📊 关键字频次统计")
    lines.append(f"| 类别 | 统计频次 | 风险等级 |")
    lines.append(f"| :--- | :---: | :---: |")
    for k, v in report["keyword_stats"].items():
        level = "🔴 高危" if v > 0 and k in ["ERROR", "DEADLOCK", "OOM"] else ("🟡 关注" if v > 0 else "🟢 正常")
        lines.append(f"| `{k}` | {v} | {level} |")

    if report["stacks"]:
        lines.append(f"\n## 🚨 核心异常堆栈指纹分析")
        for i, s in enumerate(report["stacks"], 1):
            lines.append(f"### 异常 #{i}: {s['error_type']}")
            lines.append(f"- **技术栈引擎**: `{s['language_or_engine']}`")
            if s['error_message']:
                lines.append(f"- **错误详情**: `{s['error_message']}`")
            if s['top_business_frames']:
                lines.append(f"- **疑似业务代码触发点**:")
                for frame in s['top_business_frames']:
                    lines.append(f"  - `{frame}`")
            lines.append(f"\n```text\n{s['raw_stack_masked'][:1000]}\n```\n")
    else:
        lines.append(f"\nℹ️ 未在文本中检测到标准的编程语言崩溃堆栈段落。")

    return "\n".join(lines)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="异常日志与崩溃堆栈指纹分析仪")
    parser.add_argument("log_file", help="待分析的日志文件路径")
    parser.add_argument("--output", "-o", help="输出 JSON 分析报告")
    parser.add_argument("--markdown", action="store_true", help="输出 Markdown 可读简报")
    args = parser.parse_args()

    report = inspect_log(args.log_file)

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
        print(generate_markdown_report(report))
    elif not args.output:
        print(json.dumps(report, ensure_ascii=False, indent=2))
