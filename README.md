# 🛠️ Awesome-Agent-Skills

[English](#english) | [中文](#中文)

---

<a name="english"></a>
## 🇺🇸 English

### 💡 Background & Purpose

When using AI (LLMs, Cursor, Claude, etc.) in daily engineering workflows, we often repeat complex multi-step tasks. Relying on ad-hoc prompts every time is inefficient and prone to errors.

**Awesome-Agent-Skills** is dedicated to **curating daily AI Standard Operating Procedures (SOPs) into standardized, reusable Agent Skills**. By turning common AI workflows into robust, structured skills, any AI assistant can execute complex tasks reliably with zero setup friction.

### 📐 Skill Structure & Conventions

Every skill lives under `.agents/skills/<skill_name>/` and follows our **Dual-Track Protocol**:

```text
.agents/skills/<skill_name>/
├── README.md       # 👥 For Humans: Documentation, use cases, and CLI examples
├── SKILL.md        # 🤖 For AI Agents: Concise brain-computer interface (SOP & rules)
└── scripts/        # 🛠️ For Execution: Atomic Python/Shell utility scripts
```

**Key Guardrails:**
- **Environment Dependency Check**: Every `SKILL.md` verifies required packages first (recommends `uv pip install --system`).
- **Automatic Backups**: Scripts modifying local files must automatically create `*.bak` backups before writing.
- **Conventional Commits**: All contributions follow exact rules defined in [AGENTS.md](./AGENTS.md).

### 📦 Skills Directory

All skills are organized inside the **[.agents/skills/](./.agents/skills)** directory. Feel free to browse the directory directly to explore available skills and their dedicated documentations!

### 🚀 Quick Start

#### 1. Mount to AI Workspace (Recommended)
Copy or symlink any skill directory directly into your AI agent or IDE rules folder (e.g., `.agents/skills/` or `.cursor/rules/`):
```bash
git clone https://github.com/jinjie0703/Awesome-Agent-Skills.git
```

#### 2. Run CLI Scripts Directly
You can also run the atomic scripts independently via terminal:
```bash
cd .agents/skills/docx_editor
uv pip install --system python-docx docxtpl lxml
python scripts/docx_inspect.py /path/to/document.docx
```

---

<a name="中文"></a>
## 🇨🇳 中文

### 💡 背景与初衷

在日常使用 AI（如 LLM、Cursor、Claude 等）结对编程或处理复杂任务时，我们往往需要反复重复多步骤的作业流程（SOP）。每次都从零编写提示词不仅效率低下，且容易出错和产生幻觉。

**Awesome-Agent-Skills** 的核心目的就是：**沉淀日常使用 AI 的 SOP，将其封装为标准化、可复用的 Agent 技能库**。把日常好用的 AI 工作流沉淀成清晰的“流程规范 + 底层脚本”，让任何 AI 助手都能开箱即用、高效准确地完成复杂作业。

### 📐 技能目录规范

所有技能模块统一存放在 `.agents/skills/<skill_name>/` 目录下，严格遵从**双轨制协议 (Dual-Track Protocol)**：

```text
.agents/skills/<skill_name>/
├── README.md       # 👥 人类开发者说明书（解决的痛点、核心特性、命令行用法）
├── SKILL.md        # 🤖 AI 脑机接口文档（简明干练，包含触发条件、环境自检与 SOP 步骤）
└── scripts/        # 🛠️ 底层脚本工具箱（高效可靠的原子化 Python/Shell 脚本）
```

**核心安全防线：**
- **环境检查优先**：每个 `SKILL.md` 的第一步执行依赖自检（强推使用 `uv pip install --system` 极速安装）。
- **强制回滚备份**：任何修改用户本地文件的脚本，在操作前必须自动生成 `*.bak` 备份，确保安全无损。
- **协同提交规范**：所有人与 AI 的贡献均需遵循 [AGENTS.md](./AGENTS.md) 中约定的 Conventional Commits 提交规范。

### 📦 技能库目录

所有技能模块均收录在 **[.agents/skills/](./.agents/skills)** 目录下。欢迎直接进入该目录浏览各技能模块及其对应说明文档！

### 🚀 快速使用

#### 1. 挂载至 Agent 工作区 (推荐)
直接将所需技能文件夹复制或软链至你的 AI 助手工作区或 IDE 插件目录（如 `.agents/skills/` 或 `.cursor/rules/`）：
```bash
git clone https://github.com/jinjie0703/Awesome-Agent-Skills.git
```

#### 2. 命令行独立调用
你也可以直接通过命令行调用每个技能下的原子工具脚本：
```bash
cd .agents/skills/docx_editor
uv pip install --system python-docx docxtpl lxml
python scripts/docx_inspect.py /path/to/document.docx
```

---

## 🤝 Contributing / 贡献指南

欢迎将你日常积累的 AI 优秀 SOP 沉淀为 Skill！请务必遵循 **双轨制结构** 与 **[AGENTS.md](./AGENTS.md)** 规范提交 Pull Request，一起共建简洁高效的 AI 技能库！

---

## 📄 License
[MIT License](./LICENSE)
