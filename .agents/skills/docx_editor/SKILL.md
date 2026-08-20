---
name: docx_editor
description: 读取、修改、渲染与智能排版 Microsoft Word (.docx) 文档的工具集与指南。在需要对 Word 文档进行内容概览、排版美化、局部查找替换、或模板数据填空时使用。
---

# Word 文档智能修改与排版指南 (docx_editor)

本 Skill 为 AI Agent 提供了一套解耦的 .docx 处理工具，解决大语言模型直接操作 XML/Zip 导致文档错乱的问题，实现 **“内容读得懂、排版理得清、按需精细化操作、保守防破坏”** 的工作流。

## ⚙️ 第 0 步：前置环境检查与 uv 极速安装规范 (必须优先执行)

AI Agent 在正式调用任何脚本前，**必须先检查用户的本机 Python 环境与相关第三方库**：
1. **环境检测**：
   - 检查 `python --version` 或判断 Python 是否就绪。
   - 检查是否安装了操作核心库：`python -c "import docx, docxtpl"`。
2. **缺失提示与 uv 安装策略**：
   - 如果用户电脑没有 Python 环境或缺少 `python-docx / docxtpl` 依赖，**务必明确告知用户需要装环境**。
   - **推荐安装命令（优先采用现代高效的 `uv` 包管理器安装到全局/系统 Python）**：
     ```bash
     # 检测到缺少依赖时，优先向用户提出通过 uv 安装到当前全局系统 Python 环境：
     uv pip install --system python-docx docxtpl
     
     # 如果用户电脑没有 uv，退回普通 pip：
     pip install python-docx docxtpl
     ```
   - **说明**：推荐 `uv pip install --system` 是因为其安装速度是普通 pip 的 10~100 倍，并能直接注入用户当前的全局 Python 解释器中，供我们的所有工具脚本直接调用。

---

## 🧠 核心原则：排版决策三法则（严格按优先级执行）

在进行任何排版调整前，必须遵循以下优先级决策规则：

### 🥇 优先级 1：【最高优先级】用户明确排版需求
- **规则**：如果用户在指令或对话中**明确指定了排版格式**（例如：“正文用宋体五号，行距1.25倍，一级标题黑体居中”），**绝对且严格按照用户的具体输入执行**！
- **操作方式**：将用户提出的具体样式参数转化为 JSON 配置文件或 CLI 命令行参数，调用 `docx_format.py --custom-config <json_path>` 准确应用。

### 🥈 优先级 2：标准规范文档标准预设
- **规则**：若用户要求“调整排版/排版规范化”，但**没有提出具体的样式参数**，AI 需通过 `docx_inspect.py` 勘察并判定文档类型：
  - **学术论文/毕业论文/期末报告** -> 使用论文预设 (`docx_format.py --preset thesis`)：正文小四宋体/Times New Roman、1.5倍行距、首行缩进 2 字符、标题二级黑体层次分明。
  - **机关公文/正式函件/红头文件** -> 使用公文预设 (`docx_format.py --preset official_doc`)：正文三号仿宋_GB2312、行距 28 磅、一级标题二号宋体/黑体居中。
  - **技术报告/架构设计文档/技术白皮书** -> 使用技术报告预设 (`docx_format.py --preset tech_report`)：正文 11pt 微软雅黑/Segoe UI、1.35倍行距、段落顶格无缩进、标题左对齐层次分明。

### 🥉 优先级 3：【保守防线】不确定，不硬排版（Safe Mode）
- **规则**：如果遇到**自由设计文档、复杂表格文档、艺术性简历、特殊手册**，或者**未能确定目标排版规范**时，**绝对禁止强行对全篇进行排版重置（严禁硬排版）**！
- **操作方式**：
  - 若仅需修改文字内容，仅调用 `docx_replace.py` 或对特定段落进行局部的 `Run` 文本操作。
  - 对于新增段落，自动继承并沿用原文档已有段落的样式与字号，绝不破坏原有上下文的排版和谐。

---

## 🛠️ 工具脚本手册

所有脚本均存放在 `.agents/skills/docx_editor/scripts/` 目录下。调用时请使用当前 Python 解释器。
> **💡 安全保障与演练提示**：
> - 覆盖保存前均会自动为目标文件创建 `*.bak.docx` 备份副本，确保误操作可随时回滚！
> - `docx_format.py` 和 `docx_replace.py` 均支持 `--dry-run` 参数，可在不修改文件的前提下预先统计并汇报变更。

### 1. 勘察与内容感知 (`docx_inspect.py`)
在执行修改或排版前，**第一步必运行此脚本**，以获取文档结构、现有格式与 Markdown 预览（支持普通段落和表格内容提取）。
```bash
python .agents/skills/docx_editor/scripts/docx_inspect.py <docx_path> [--preview-lines 100]
```
- **输出内容**：段落数、表格数、页面边距、主导字体与字号、表格内容 Markdown 预览、正文大纲结构简报。

### 2. 智能原子排版引擎 (`docx_format.py`)
用于全局或局部的格式规范化与排版重置（完整支持 H1~H4 标题层级、正文及表格内段落排版，并具备 `rPr` 节点自动保护机制）。
```bash
# 方式 A：使用预设（论文 thesis、公文 official_doc 或技术报告 tech_report）
python .agents/skills/docx_editor/scripts/docx_format.py <docx_path> --preset thesis --output <out_path>
python .agents/skills/docx_editor/scripts/docx_format.py <docx_path> --preset tech_report --output <out_path>

# 方式 B：预检演练模式（Dry-Run）
python .agents/skills/docx_editor/scripts/docx_format.py <docx_path> --preset tech_report --dry-run

# 方式 C：根据用户的具体排版指令，使用命令行参数精准排版
python .agents/skills/docx_editor/scripts/docx_format.py <docx_path> \
    --body-font "宋体" --body-font-ascii "Times New Roman" --body-size 12 \
    --line-spacing 1.5 --first-line-indent 2 \
    --h1-font "黑体" --h1-size 18 --h1-align center \
    --h2-font "黑体" --h2-size 15 --h3-font "黑体" --h3-size 14 \
    --output <out_path>

# 方式 D：通过 JSON 配置文件批量定义复杂样式（针对用户给出的超细致要求）
python .agents/skills/docx_editor/scripts/docx_format.py <docx_path> --custom-config style_config.json --output <out_path>
```

### 3. 精准无损替换工具 (`docx_replace.py`)
在所有段落、表格、页眉页脚中安全替换文本，深度遍历 `runs` 并保持原字号、颜色与加粗样式不变。
```bash
python .agents/skills/docx_editor/scripts/docx_replace.py <docx_path> --old "旧文本" --new "新文本" [--output <out_path>] [--dry-run]
```

### 4. 模板变量填充 (`docx_template.py`)
针对 `{{ variable }}` Jinja2 占位符格式的通用模板填充（如实习证明、合同模版），支持 `--json-file` 文件传参避免转义异常。
```bash
python .agents/skills/docx_editor/scripts/docx_template.py <template_path> --json-file data.json --output <out_path>
```

### 5. 新增段落与内容插入工具 (`docx_insert.py`)
在文档的指定位置插入新的段落或文本，新段落自动继承上下文已有段落的字体与样式。
```bash
# 在指定关键词段落后插入
python .agents/skills/docx_editor/scripts/docx_insert.py <docx_path> --after-text "第二章结论" --content "这是新增的总结段落" --output <out_path>

# 在指定段落序号后插入或在文末追加
python .agents/skills/docx_editor/scripts/docx_insert.py <docx_path> --at-end --content "文末追加的致谢内容" --output <out_path>
```

---

## 🚀 标准操作工作流 (SOP)

0. **环境检查 (Env Check)**：先通过 `python -c "import docx, docxtpl"` 检查依赖。如缺失，明确提示用户并使用 `uv pip install --system python-docx docxtpl` (或 `pip`) 安装。
1. **侦查 (Inspect)**：执行 `docx_inspect.py` 了解内容概况、表格数据和已有格式。
2. **决策 (Decide)**：
   - 如果用户给出了明确排版规则 -> 将规则组装为参数调用 `docx_format.py`。
   - 如果属于标准论文/公文且要求规范化 -> 调用对应 `--preset`。
   - 如果是局部改字 -> 调用 `docx_replace.py`。
   - 如果需要在特定位置插入新内容 -> 调用 `docx_insert.py`。
   - 如果是标准模版数据填空 -> 调用 `docx_template.py`。
   - 如果排版不确定 -> **触发保守防线**，仅改文字或继承上下文，不改动无关样式。
3. **执行与报告 (Execute & Report)**：运行脚本并将最终生成的文件路径、自动生成的 `.bak.docx` 备份路径及调整重点清晰汇报给用户。
