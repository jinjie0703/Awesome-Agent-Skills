#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
skill_scaffold.py - AI Agent Skill 自动化脚手架生成器
一键创建符合 Awesome-Agent-Skills 双轨制规范与工业级防错防线的技能骨架。

用法:
  python skill_scaffold.py my_skill --type tool_assisted --desc "用于处理某种任务的工具" --lang zh
  python skill_scaffold.py my_skill --type prompt_only --desc "Prompt-only knowledge distillation" --lang en
"""

import sys
import argparse
from pathlib import Path

# 确保 Windows 终端 UTF-8 编码正常输出
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


def generate_skill_md(name: str, desc: str, skill_type: str, lang: str = "zh") -> str:
    """生成符合 AI 脑机接口规范的 SKILL.md"""
    if lang == "en":
        desc_full = f"{desc}. Use when asked to process, inspect, or execute workflows related to {name}." if "Use when" not in desc else desc
        step0_text = """## ⚙️ Step 0: Pre-flight Environment & Dependency Check (Mandatory)

Before executing any script, check the Python environment and dependencies:
1. **Python Check**: `python --version` (Requires Python 3.9+)
2. **Dependency Check**: `python -c "import xxx"` (Replace with your actual packages)
3. **Recommended Fast Installation**:
   ```bash
   uv pip install --system <package_name>
   # Fallback if uv is not available:
   pip install <package_name>
   ```"""
        sop_text = """## 🚀 Standard Operating Procedure (SOP)

### Step 1: Input Perception & Validation
- Parse user requirements and inspect source files/context.

### Step 2: Core Execution
- Execute CLI scripts or structured meta-cognitive reasoning.
```bash
python .agents/skills/{name}/scripts/{name}_core.py <input_path> --output <output_path>
```

### Step 3: Reporting
- Report results, output paths, and generated `*.bak` backup paths to the user."""
    else:
        desc_full = f"{desc}。在需要处理、转换或执行与 {name} 相关的任务时使用。" if "在需要" not in desc and "时使用" not in desc else desc
        step0_text = """## ⚙️ 第 0 步：前置环境检查与 uv 极速安装规范 (必须优先执行)

AI Agent 在正式调用任何脚本前，**必须先检查用户的本机 Python 环境与相关第三方库**：
1. **环境检测**：
   - 检查 `python --version` (推荐 Python 3.9+)。
   - 检查是否安装了核心依赖：`python -c "import xxx"` (替换为实际依赖)。
2. **缺失提示与 uv 安装策略**：
   - 如果缺少依赖，明确提示用户并推荐通过 `uv` 极速安装到全局系统环境：
     ```bash
     uv pip install --system <package_name>
     # 如果用户电脑没有 uv，退回普通 pip:
     pip install <package_name>
     ```"""
        sop_text = """## 🚀 标准操作工作流 (SOP)

### 第 1 步：感知与侦查 (Inspect)
- 检查用户提供的输入文件或参数，判定具体任务类型与边界条件。

### 第 2 步：核心执行 (Execute)
- 调用底层原子脚本或执行深度推理：
```bash
python .agents/skills/{name}/scripts/{name}_core.py <input_path> --output <output_path>
```

### 第 3 步：汇报与交付 (Report)
- 将最终生成的文件路径、自动生成的备份文件路径清晰汇报给用户。"""

    content = f"""---
name: {name}
description: {desc_full}
---

# {name.replace('_', ' ').title()} 指南

本 Skill 为 AI Agent 提供了标准的作业规范与自动化工具。

{step0_text}

---

{sop_text}

---

## 📐 输出规范

- 结构严谨、语气专业干练，不输出客套废话。
- 涉及关键参数或模式时**加粗**显示。
"""
    return content.strip() + "\n"


def generate_readme_md(name: str, desc: str, skill_type: str, lang: str = "zh") -> str:
    """生成面向人类开发者的展示说明书 README.md"""
    title = name.replace('_', ' ').title()
    if lang == "en":
        return f"""# 🛠️ {name} - {title} Skill

[![Skill Version](https://img.shields.io/badge/Skill-v1.0.0-blue.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)]()

> {desc}

---

## 🤔 What Pain Point Does This Solve?

Describe the friction, cognitive overhead, or common mistakes this skill eliminates for developers and AI assistants.

---

## ✨ Key Features

- ⚡ **Atomic Execution**: Standardized CLI utility scripts with zero guesswork;
- 🛡️ **Safety Guardrails**: Automatic `*.bak` backups before modifying local files;
- 🌐 **Cross-Platform**: Fully compatible with Windows, macOS, and Linux.

---

## 📂 Directory Structure

```text
{name}/
├── README.md                 # 👥 Human documentation
├── SKILL.md                  # 🤖 AI Agent SOP & brain-computer interface
└── scripts/                  # 🛠️ Atomic Python scripts
    └── {name}_core.py        # Core operational script
```

---

## 🚀 Quick Start (CLI)

```bash
# 1. Install dependencies
uv pip install --system <package_name>

# 2. Run the script
python scripts/{name}_core.py input_file.ext --output output_file.ext
```

---

## 📄 License
MIT
"""
    else:
        return f"""# 🛠️ {name} - {title} 技能说明书

[![Skill Version](https://img.shields.io/badge/Skill-v1.0.0-blue.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)]()

> {desc}

---

## 🤔 解决什么痛点？

在此描述开发者在日常工作中遇到的繁琐、易出错或高频重复痛点，以及本 Skill 如何将其标准化。

---

## ✨ 核心特性

- ⚡ **原子化脚本驱动**：清晰的 CLI 命令行接口，支持独立终端运行；
- 🛡️ **工业级安全防线**：任何覆盖写操作前均自动生成 `*.bak` 备份副本；
- 🌐 **全平台兼容**：完美支持 Windows (UTF-8 防乱码)、macOS 和 Linux。

---

## 📂 目录与文件结构

```text
{name}/
├── README.md                 # 👥 本说明文档（人类开发者与社区看）
├── SKILL.md                  # 🤖 AI Agent 专用脑机接口文档（SOP 与决策规范）
└── scripts/                  # 🛠️ 底层原子工具脚本库
    └── {name}_core.py        # 核心功能脚本
```

---

## 🚀 快速开始 (CLI)

```bash
# 1. 极速安装依赖 (推荐使用 uv)
uv pip install --system <package_name>

# 2. 命令行调用脚本
python scripts/{name}_core.py input_file.ext --output output_file.ext
```

---

## 📄 License
MIT
"""


def generate_python_script(name: str, desc: str) -> str:
    """生成预置 Windows UTF-8、argparse 与强制备份机制的 Python 工具脚本骨架"""
    return f"""#!/usr/bin/env python3
# -*- coding: utf-8 -*-
\"\"\"
{name}_core.py - {name} 核心操作工具
{desc}

用法:
  python {name}_core.py input.txt --output output.txt
  python {name}_core.py input.txt --dry-run
\"\"\"

import sys
import shutil
import argparse
from pathlib import Path

# 确保 Windows 终端 UTF-8 编码正常输出（防 UnicodeEncodeError 与乱码）
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


def backup_file(file_path: Path) -> str:
    \"\"\"在修改前自动创建 .bak 备份副本，确保数据安全可回滚\"\"\"
    if not file_path.exists():
        return ""
    bak_path = file_path.with_suffix(f".bak{{file_path.suffix}}")
    shutil.copy2(str(file_path), str(bak_path))
    return str(bak_path)


def process_task(input_path: str, output_path: str = None, dry_run: bool = False) -> str:
    \"\"\"核心业务逻辑实现函数\"\"\"
    inp = Path(input_path)
    if not inp.exists():
        return f"错误: 输入文件不存在 - {{inp.resolve()}}"

    save_path = Path(output_path) if output_path else inp

    if dry_run:
        return f"[Dry-Run 模式] 预检成功：输入文件 {{inp.name}} 存在，未执行实际写入。"

    # 自动备份即将被覆盖的目标文件
    bak_msg = ""
    if save_path.exists():
        bak = backup_file(save_path)
        if bak:
            bak_msg = f"（原文件已备份至: {{bak}}）"

    # TODO: 在此处编写具体的业务处理逻辑
    # 示例: 读取并写入
    # content = inp.read_text(encoding="utf-8")
    # save_path.parent.mkdir(parents=True, exist_ok=True)
    # save_path.write_text(content, encoding="utf-8")

    save_path.parent.mkdir(parents=True, exist_ok=True)
    return f"任务处理成功并保存至: {{save_path.resolve()}}{{bak_msg}}"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="{name} 核心操作工具")
    parser.add_argument("input_path", help="输入文件路径")
    parser.add_argument("--output", "-o", help="输出文件路径（可选，默认覆盖原文件）")
    parser.add_argument("--dry-run", action="store_true", help="演练模式：仅做预检，不修改实际文件")
    args = parser.parse_args()

    msg = process_task(args.input_path, args.output, dry_run=args.dry_run)
    print(msg)
"""


def scaffold_skill(name: str, desc: str, skill_type: str = "tool_assisted",
                    lang: str = "zh", target_dir: str = None) -> str:
    """在指定目录脚手架化生成完整的 Skill 目录"""
    # 规范化 skill 命名（下划线 snake_case）
    clean_name = name.strip().lower().replace("-", "_")
    base_dir = Path(target_dir) if target_dir else Path(".agents/skills")
    skill_dir = base_dir / clean_name

    if skill_dir.exists():
        return f"⚠️ 警告: 目录已存在: {skill_dir.resolve()}，请使用新名称或先清理该目录。"

    skill_dir.mkdir(parents=True, exist_ok=True)

    # 1. 生成 SKILL.md
    skill_md = generate_skill_md(clean_name, desc, skill_type, lang=lang)
    (skill_dir / "SKILL.md").write_text(skill_md, encoding="utf-8")

    # 2. 生成 README.md
    readme_md = generate_readme_md(clean_name, desc, skill_type, lang=lang)
    (skill_dir / "README.md").write_text(readme_md, encoding="utf-8")

    # 3. 根据类型生成配套目录与模板文件
    if skill_type in ["tool_assisted", "hybrid"]:
        scripts_dir = skill_dir / "scripts"
        scripts_dir.mkdir(parents=True, exist_ok=True)
        py_script = generate_python_script(clean_name, desc)
        (scripts_dir / f"{clean_name}_core.py").write_text(py_script, encoding="utf-8")
    elif skill_type == "prompt_only":
        ref_dir = skill_dir / "references"
        ref_dir.mkdir(parents=True, exist_ok=True)
        (ref_dir / "templates.md").write_text("# Templates\n\nDefine your reusable output templates here.\n", encoding="utf-8")
        assets_dir = skill_dir / "assets"
        assets_dir.mkdir(parents=True, exist_ok=True)
        (assets_dir / "examples.md").write_text("# Examples\n\nProvide few-shot good and bad examples here.\n", encoding="utf-8")

    return f"🎉 成功创建技能脚手架: {skill_dir.resolve()}\n包含文件:\n- SKILL.md (AI 脑机接口)\n- README.md (人类使用说明)\n" + \
           (f"- scripts/{clean_name}_core.py (预置安全防线的 Python 工具)" if skill_type in ["tool_assisted", "hybrid"] else "- references/templates.md & assets/examples.md")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI Agent Skill 自动化脚手架生成器")
    parser.add_argument("name", help="技能名称 (如 docx_editor, git_reviewer)")
    parser.add_argument("--desc", default="用于自动化执行特定任务的标准化 Agent Skill", help="技能一句话描述 (用于 Frontmatter description)")
    parser.add_argument("--type", choices=["tool_assisted", "prompt_only", "hybrid"], default="tool_assisted", help="技能类型 (tool_assisted: 工具驱动型, prompt_only: 纯推理型, hybrid: 混合型)")
    parser.add_argument("--lang", choices=["zh", "en"], default="zh", help="模板语言 (zh: 中文, en: 英文)")
    parser.add_argument("--dir", default=".agents/skills", help="生成目标根目录 (默认: .agents/skills)")
    args = parser.parse_args()

    result = scaffold_skill(args.name, args.desc, skill_type=args.type, lang=args.lang, target_dir=args.dir)
    print(result)
