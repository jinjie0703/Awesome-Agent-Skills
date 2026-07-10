# 🛠️ Awesome-Agent-Skills

精选、实战、开箱即用的 AI Agent 技能库（Skill Directory）。专注于解耦底层复杂文件与长文本推理，赋予大模型可靠、精准的物理作业执行力。

---

## 📦 仓库内容 (Skill List)

本仓库目前收录了以下精选实战技能，每个技能均独立封装在 `.agents/skills/` 目录下：

| 技能名称 | 一句话用途 | 详细文档与工具 |
| :--- | :--- | :--- |
| **[`docx_editor`](file:///.agents/skills/docx_editor/README.md)** | Microsoft Word 文档原子化修改与智能排版。支持论文/公文预设、表格及多级标题排版、精确定位追加段落与无损文字替换。 | [说明书](file:///.agents/skills/docx_editor/README.md) / [AI 接口](file:///.agents/skills/docx_editor/SKILL.md) / `5 个脚本` |
| **[`project_deep_diver`](file:///.agents/skills/project_deep_diver/README.md)** | 秋招/社招面试项目深度挖矿利器。自动扫描本地代码库统计行数与技术指纹，提炼 STAR 亮点，预测 5 层连环拷问并导出一键可打印的面经防御手册。 | [说明书](file:///.agents/skills/project_deep_diver/README.md) / [AI 接口](file:///.agents/skills/project_deep_diver/SKILL.md) / `2 个脚本` |
| **[`conversation-to-knowledge`](file:///.agents/skills/conversation-to-knowledge/README.md)** | 长对话与技术日志知识编辑（Knowledge Editor）。严格遵循“6个月周期法则”与“可迁移测试”，从冗杂日志中萃取可跨项目复用的架构卡片。 | [说明书](file:///.agents/skills/conversation-to-knowledge/README.md) / [AI 接口](file:///.agents/skills/conversation-to-knowledge/SKILL.md) / `双链模板库` |

---

## 📐 核心规范 (Standards & Conventions)

为了保证每一个 Skill 具备工业级稳定性与清晰度，本仓库严格执行以下三项规范：

### 1. 双轨制目录结构 (Dual-Track Protocol)
每个 Skill 文件夹下必须包含：
- **`README.md` (人类说明书)**：阐述解决什么痛点、核心特性矩阵、使用命令与决策流程图。
- **`SKILL.md` (脑机接口文档)**：纯给 AI Agent 后台挂载阅读，干练精简，明确触发条件、环境自检与 SOP 步骤。
- **`scripts/` (原子工具箱)**：具体的 Python 作业脚本，保证功能解耦、命令行可调用。

### 2. 工业防呆与自动备份 (Guardrails)
- **极速依赖自检**：脚本调用前自动检查依赖，推荐使用 `uv pip install --system <package>` 进行极速全局安装。
- **无损回滚**：所有对用户文件进行修改的脚本，在写入前会自动在同目录备份一份 `*.bak.ext` 文件。

### 3. Git 与 AI 协同协议 (AGENTS.md)
本项目配置了统一的贡献规范 [AGENTS.md](file:///AGENTS.md)。人类或 AI 在提交代码时需遵守 Conventional Commits 规范：
- `<type>(<scope>): <subject>`（如：`feat(docx_editor): add support for table formatting`）

---

## 🚀 如何使用 (Quick Start)

### 1. 挂载技能到你的 Agent 工作区
将本仓库克隆到本地，然后将 `.agents/skills/` 目录下的目标技能文件夹拷贝或软链至你所使用的 AI Agent 技能目录中（例如 Cursor、LangChain、或者本地 IDE 插件中心）：
```bash
git clone https://github.com/jinjie0703/Awesome-Agent-Skills.git
```

### 2. 安装底层依赖 (推荐 `uv`)
本仓库中的 Python 脚本工具链推荐使用 `uv` 极速包管理器安装至系统 Python 解释器中：
```bash
# 一键安装 docx_editor 的相关依赖
uv pip install --system python-docx docxtpl lxml

# 注：project_deep_diver 与 conversation-to-knowledge 均为 Python 标准库零依赖，无需额外安装！
```

### 3. 对话触发
挂载并准备好依赖后，只需在日常对 AI 助手下达自然语言指令（如 *“帮我扫一下当前目录这个项目，提炼几个面试亮眼难点并导出手册”*），AI 即会自动读取对应的 `SKILL.md` 并调用 Python 脚本完成复杂作业！

---

## 📄 License
[MIT License](file:///LICENSE)
