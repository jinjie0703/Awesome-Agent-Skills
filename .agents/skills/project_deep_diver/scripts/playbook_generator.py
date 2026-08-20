#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
playbook_generator.py - 面经防御手册生成器
将 AI 深度挖掘出的项目亮点、连环拷问预测与防御话术，
自动格式化并保存为标准化的 Markdown 面经手册。

用法:
  python playbook_generator.py --project-name "万方数据平台" --json-file deep_dive_data.json --output playbook.md
  python playbook_generator.py --project-name "万方数据平台" --json '{"highlights": [...], ...}' --output playbook.md
"""

import sys
import json
import shutil
import argparse
from pathlib import Path
from datetime import datetime

# 确保 Windows 终端 UTF-8 编码正常输出
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


def backup_file(file_path: Path) -> str:
    """在修改前自动创建 .bak.md 备份副本"""
    if not file_path.exists():
        return ""
    bak_path = file_path.with_suffix(".bak.md")
    shutil.copy2(str(file_path), str(bak_path))
    return str(bak_path)


def generate_playbook(project_name: str, data: dict, output_path: str) -> str:
    """
    根据结构化数据生成面经防御手册 Markdown 文档。

    data 结构预期:
    {
        "project_summary": "一句话项目概述",
        "tech_stack": ["Vue3", "Spring Boot", "Redis", ...],
        "highlights": [
            {"title": "亮点标题", "star_desc": "STAR 法则描述", "keywords": ["关键词1", ...]}
        ],
        "difficulties": [
            {"title": "难点标题", "problem": "问题描述", "solution": "解决方案", "result": "优化成果"}
        ],
        "grilling_qa": [
            {"category": "架构选型关", "question": "面试官问题", "answer": "高分防御话术"}
        ],
        "architecture_comparison": {
            "challenge": "核心挑战描述",
            "junior": {"desc": "初级方案", "risk": "隐患"},
            "current": {"desc": "当前方案", "advantage": "优势"},
            "ultimate": {"desc": "终极方案", "scenario": "适用场景"}
        },
        "self_reflection": "如果重新来过，我会改进的地方"
    }
    """

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = []

    # ========== 封面 ==========
    lines.append(f"# 🎯 面经防御手册 - {project_name}")
    lines.append(f"> 📅 生成时间: {now}")
    lines.append(f"> 🤖 由 AI Agent (project_deep_diver) 自动深挖生成\n")
    lines.append("---\n")

    # ========== 项目概述 ==========
    if data.get("project_summary"):
        lines.append(f"## 📋 项目一句话概述")
        lines.append(f"{data['project_summary']}\n")

    if data.get("tech_stack"):
        lines.append(f"**核心技术栈**: {' / '.join(data['tech_stack'])}\n")

    lines.append("---\n")

    # ========== 亮点提炼 ==========
    highlights = data.get("highlights", [])
    if highlights:
        lines.append(f"## 🌟 项目亮点与技术壁垒提炼 (STAR 法则)\n")
        for i, h in enumerate(highlights, 1):
            lines.append(f"### 亮点 {i}: {h.get('title', '未命名')}")
            if h.get("star_desc"):
                lines.append(f"{h['star_desc']}\n")
            if h.get("keywords"):
                lines.append(f"**关键技术词**: {', '.join(f'`{k}`' for k in h['keywords'])}\n")

        lines.append("---\n")

    # ========== 技术难点 ==========
    difficulties = data.get("difficulties", [])
    if difficulties:
        lines.append(f"## 🔥 核心技术难点与攻克过程\n")
        for i, d in enumerate(difficulties, 1):
            lines.append(f"### 难点 {i}: {d.get('title', '未命名')}")
            if d.get("problem"):
                lines.append(f"**❌ 问题**: {d['problem']}")
            if d.get("solution"):
                lines.append(f"**✅ 解决方案**: {d['solution']}")
            if d.get("result"):
                lines.append(f"**📈 优化成果**: {d['result']}\n")

        lines.append("---\n")

    # ========== 5 连环拷问 ==========
    qa_list = data.get("grilling_qa", [])
    if qa_list:
        lines.append(f"## 🎯 面试官 5 连环压力深挖预测与防御话术\n")
        category_icons = {
            "架构选型关": "🏗️",
            "极端场景关": "🔥",
            "线上Bug关": "🐛",
            "性能极限关": "⚡",
            "自我批判关": "🔄",
        }
        for i, qa in enumerate(qa_list, 1):
            cat = qa.get("category", f"第{i}关")
            icon = category_icons.get(cat, "❓")
            lines.append(f"### {icon} 第{i}关: {cat}")
            lines.append(f"**🗣️ 面试官**: {qa.get('question', '')}\n")
            lines.append(f"**💬 高分防御话术**:\n")
            lines.append(f"{qa.get('answer', '')}\n")

        lines.append("---\n")

    # ========== 方案对比 ==========
    arch = data.get("architecture_comparison", {})
    if arch:
        lines.append(f"## 🛠️ 解决方案降维/进阶三级对比\n")
        lines.append(f"**核心挑战**: {arch.get('challenge', '未指定')}\n")

        lines.append(f"| 方案级别 | 描述 | 备注 |")
        lines.append(f"| :---: | :--- | :--- |")

        junior = arch.get("junior", {})
        current = arch.get("current", {})
        ultimate = arch.get("ultimate", {})

        lines.append(f"| 🟡 初级方案 | {junior.get('desc', '-')} | ⚠️ {junior.get('risk', '-')} |")
        lines.append(f"| 🟢 当前方案 | {current.get('desc', '-')} | ✅ {current.get('advantage', '-')} |")
        lines.append(f"| 🔵 终极方案 | {ultimate.get('desc', '-')} | 🎯 {ultimate.get('scenario', '-')} |")
        lines.append("")
        lines.append("---\n")

    # ========== 自我反思 ==========
    if data.get("self_reflection"):
        lines.append(f"## 🔄 自我批判与成长复盘")
        lines.append(f"{data['self_reflection']}\n")
        lines.append("---\n")

    # ========== 尾部 ==========
    lines.append(f"*本手册由 `project_deep_diver` 技能自动生成。祝面试顺利！🚀*")

    content = "\n".join(lines)

    # 保存与备份
    out = Path(output_path)
    bak_msg = ""
    if out.exists():
        bak = backup_file(out)
        if bak:
            bak_msg = f"（原手册已备份至: {bak}）"
            
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(content)

    return f"面经防御手册已成功生成并保存至: {out.resolve()}{bak_msg}"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="面经防御手册生成器")
    parser.add_argument("--project-name", required=True, help="项目名称 (如 '万方数据平台')")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--json", dest="json_str", help="传入的 JSON 字符串")
    group.add_argument("--json-file", dest="json_file", help="传入的 JSON 数据文件路径 (推荐)")

    parser.add_argument("--output", "-o", required=True, help="输出 Markdown 手册路径")
    args = parser.parse_args()

    try:
        if args.json_file:
            with open(args.json_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = json.loads(args.json_str)
    except Exception as e:
        print(f"错误: JSON 解析失败 - {e}")
        sys.exit(1)

    msg = generate_playbook(args.project_name, data, args.output)
    print(msg)
