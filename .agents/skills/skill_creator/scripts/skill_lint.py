#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
skill_lint.py - AI Agent 技能工业级合规与安全质检仪
扫描指定的 Skill 目录，依据 Awesome-Agent-Skills 规范和 AGENTS.md 准则进行合规度审查。

用法:
  python skill_lint.py .agents/skills/docx_editor
  python skill_lint.py .agents/skills/ --all
"""

import sys
import re
import argparse
from pathlib import Path

# 确保 Windows 终端 UTF-8 编码正常输出
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


def parse_frontmatter(content: str) -> dict:
    """提取 Markdown 顶部的 YAML Frontmatter"""
    if not content.startswith("---"):
        return {}
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}
    fm_raw = parts[1].strip()
    fm = {}
    for line in fm_raw.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        k, v = line.split(":", 1)
        fm[k.strip()] = v.strip().strip("\"'")
    return fm


def lint_skill(skill_dir: Path) -> dict:
    """对单个 Skill 目录进行深度规范审查"""
    folder_name = skill_dir.name
    results = {
        "skill": folder_name,
        "path": str(skill_dir.resolve()),
        "passed": [],
        "warnings": [],
        "errors": []
    }

    if not skill_dir.exists() or not skill_dir.is_dir():
        results["errors"].append(f"目录不存在或非文件夹: {skill_dir}")
        return results

    # 1. 双轨制结构检查 (Dual-Track Protocol)
    skill_md = skill_dir / "SKILL.md"
    readme_md = skill_dir / "README.md"

    if not skill_md.exists():
        results["errors"].append("缺少 AI 脑机接口文档: SKILL.md (致命缺陷)")
    else:
        skill_content = skill_md.read_text(encoding="utf-8", errors="ignore")
        fm = parse_frontmatter(skill_content)
        
        # 2. Frontmatter 检查
        if not fm:
            results["errors"].append("SKILL.md 缺少有效的 YAML Frontmatter (--- ... ---)")
        else:
            fm_name = fm.get("name", "")
            fm_desc = fm.get("description", "")

            if not fm_name:
                results["errors"].append("Frontmatter 缺少 'name' 字段")
            elif fm_name.replace("-", "_") != folder_name.replace("-", "_"):
                results["warnings"].append(f"Frontmatter 'name' ({fm_name}) 与文件夹名 ({folder_name}) 不一致，建议统一")
            else:
                results["passed"].append("Frontmatter 'name' 与目录命名一致")

            if not fm_desc:
                results["errors"].append("Frontmatter 缺少 'description' 触发语义字段")
            elif len(fm_desc) < 15:
                results["warnings"].append("Frontmatter 'description' 过于简略，建议补充具体动作与触发条件")
            elif "在需要" not in fm_desc and "时使用" not in fm_desc and "Use when" not in fm_desc and "when asked" not in fm_desc:
                results["warnings"].append("Frontmatter 'description' 建议包含明确的触发条件 (如 '在需要...时使用' 或 'Use when asked to...')")
            else:
                results["passed"].append("Frontmatter 'description' 具备清晰触发词")

        # 3. 前置环境自检检查 (Step 0)
        has_env_check = any(kw in skill_content for kw in ["第 0 步", "Step 0", "前置环境检查", "Pre-flight", "python --version", "uv pip install", "无需额外依赖", "Pure Prompt"])
        if has_env_check:
            results["passed"].append("SKILL.md 包含前置环境/依赖自检规范 (Step 0)")
        else:
            results["warnings"].append("SKILL.md 未明确发现第 0 步环境检查 (Step 0) 或无需依赖说明")

    if not readme_md.exists():
        results["errors"].append("缺少面向人类开发者的说明书: README.md (违反双轨制规范)")
    else:
        readme_content = readme_md.read_text(encoding="utf-8", errors="ignore")
        if len(readme_content) < 50:
            results["warnings"].append("README.md 内容过少，建议补充痛点分析、核心特性与命令行使用示例")
        else:
            results["passed"].append("README.md 结构完整")

    # 4. Python 脚本审查 (Scripts Audit)
    scripts_dir = skill_dir / "scripts"
    if scripts_dir.exists() and scripts_dir.is_dir():
        py_files = list(scripts_dir.glob("*.py"))
        for py_file in py_files:
            code = py_file.read_text(encoding="utf-8", errors="ignore")
            
            # Windows UTF-8 检查
            if "sys.stdout.reconfigure" in code or "TextIOWrapper" in code or "utf-8" in code:
                results["passed"].append(f"脚本 {py_file.name} 具备终端 UTF-8 编码防乱码配置")
            else:
                results["warnings"].append(f"脚本 {py_file.name} 缺少 sys.stdout.reconfigure(encoding='utf-8')，在 Windows 控制台可能发生 UnicodeEncodeError")

            # 覆盖写备份检查 (Backup Mechanism)
            is_writer = any(kw in code for kw in ["open(", ".write_text(", ".save(", "shutil.copy", "json.dump("]) and ("'w'" in code or '"w"' in code or ".save(" in code)
            if is_writer:
                has_backup = "backup_file" in code or ".bak" in code or "bak_path" in code
                if has_backup:
                    results["passed"].append(f"脚本 {py_file.name} 实现了目标覆盖写自动备份机制 (.bak)")
                else:
                    results["warnings"].append(f"脚本 {py_file.name} 包含写文件操作，但未发现 *.bak 自动备份机制 (违反 AGENTS.md 安全红线)")

            # Pathlib 规范检查
            if "pathlib" in code or "Path(" in code:
                results["passed"].append(f"脚本 {py_file.name} 使用 pathlib.Path 处理路径")
            else:
                results["warnings"].append(f"脚本 {py_file.name} 建议优先使用 pathlib.Path 替代硬编码或 os.path")

    return results


def print_lint_report(report: dict):
    """格式化打印质检审查简报"""
    print(f"\n========================================================")
    print(f"🔍 技能合规质检报告: {report['skill']}")
    print(f"📁 路径: {report['path']}")
    print(f"========================================================")

    if report["passed"]:
        print(f"✅ 通过项 ({len(report['passed'])}):")
        for item in report["passed"]:
            print(f"   [PASS] {item}")

    if report["warnings"]:
        print(f"\n🟡 优化建议与警告 ({len(report['warnings'])}):")
        for item in report["warnings"]:
            print(f"   [WARN] {item}")

    if report["errors"]:
        print(f"\n🔴 阻断性违规项 ({len(report['errors'])}):")
        for item in report["errors"]:
            print(f"   [FAIL] {item}")
        print(f"\n❌ 质检结论: 不合规 (请修正上述阻断项)")
    elif report["warnings"]:
        print(f"\n⚠️  质检结论: 基本合规 (存在可优化建议)")
    else:
        print(f"\n🎉 质检结论: 100% 工业级完全合规 (PERFECT)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI Agent 技能工业级合规与安全质检仪")
    parser.add_argument("target_path", nargs="?", default=".agents/skills", help="待审查的技能目录路径 (如 .agents/skills/docx_editor)")
    parser.add_argument("--all", action="store_true", help="全量扫描 .agents/skills/ 目录下的所有技能")
    args = parser.parse_args()

    target = Path(args.target_path)

    if args.all or (target.is_dir() and target.name == "skills"):
        skills_dirs = [d for d in target.iterdir() if d.is_dir() and not d.name.startswith(".")]
        total = len(skills_dirs)
        has_error = False
        print(f"🚀 开始全量扫描 {total} 个技能模块...\n")
        for s_dir in skills_dirs:
            rep = lint_skill(s_dir)
            print_lint_report(rep)
            if rep["errors"]:
                has_error = True
        sys.exit(1 if has_error else 0)
    else:
        rep = lint_skill(target)
        print_lint_report(rep)
        sys.exit(1 if rep["errors"] else 0)
