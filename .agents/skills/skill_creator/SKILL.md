---
name: skill_creator
description: AI Agent 技能架构师与脚手架工具。指导设计、自动化生成符合双轨制规范（SKILL.md + README.md）的 Agent 技能骨架，并执行工业级安全与规范质检。在需要创建新技能、编写 Skill 规范、或对已有技能进行合规审计时使用。
category: meta-engineering
tags: [skill, agent, scaffold, linter, meta]
---

# Skill Creator - AI Agent 技能架构师

当用户希望**新建一个技能**、**将一段提示词/脚本标准化封装为 Skill**、或**对已有技能进行合规质检**时，严格执行以下标准操作流 (SOP)。

---

## ⚙️ 第 0 步：环境检查（此技能无需额外依赖）

本元技能的脚手架与质检脚本仅依赖 Python 3.9+ 标准库（`os`, `sys`, `json`, `argparse`, `pathlib`, `re`），无需安装任何第三方包：
```bash
python --version
```

---

## 🚀 标准操作工作流 (SOP)

### 第 1 步：架构师需求定型与类型判定 (Classification)

在生成任何代码前，AI 必须根据用户意图，确定新技能的**架构类型（Archetype）**与**语言偏好**：

1. **类型选择**（参见 `references/skill_blueprint.md`）：
   - `prompt_only`（纯推理型）：知识提炼、文案润色、架构决策。不需要编写 Python 脚本。
   - `tool_assisted`（工具驱动型）：文件格式转换、数据清洗、Office 操作。依靠 Python 脚本执行确定性操作。
   - `hybrid`（混合推理型）：代码扫描 + AI 深度推理 + 持久化交付。
2. **语言选择**：
   - 如果是强中文场景（公文排版、国内校招、本土业务）-> `--lang zh`
   - 如果是通用代码/工程场景（Git、Docker、通用技术）-> `--lang en`

---

### 第 2 步：脚手架自动化生成 (`skill_scaffold.py`)

调用脚手架生成器，秒级生成 100% 符合双轨制标准的目录骨架：

```bash
# 示例 1: 生成工具驱动型中文技能
python .agents/skills/skill_creator/scripts/skill_scaffold.py <skill_name> \
    --type tool_assisted \
    --desc "用于某特定业务的工具" \
    --lang zh

# 示例 2: 生成纯推理型英文技能
python .agents/skills/skill_creator/scripts/skill_scaffold.py <skill_name> \
    --type prompt_only \
    --desc "Distill engineering insights from logs" \
    --lang en
```

**脚手架会自动生成并注入以下防错防线**：
- `SKILL.md`：注入规范的 YAML Frontmatter、第 0 步环境检查、SOP 步骤占位符；
- `README.md`：生成面向人类开发者的展示说明书（痛点、特性、CLI 用法）；
- `scripts/`：自动预置 Windows UTF-8 防乱码、`backup_file` 覆盖自动备份与 `argparse` 参数解析。

---

### 第 3 步：填充业务核心逻辑与文档细节

AI 根据具体业务需求，完善生成的骨架：
1. **如果是工具型/混合型**：在 `scripts/` 下编写真实的业务处理逻辑，确保使用 `pathlib.Path` 并保留备份机制；
2. **如果是纯推理型**：在 `references/templates.md` 中编写结构模板（注入 PKM Frontmatter），在 `assets/examples.md` 中编写高质量 Bad vs Good Few-Shot 样本；
3. **完善 `SKILL.md`**：确保 `description` 严格符合 `【角色/能力】 + 【功能清单】 + 【在需要...时使用】` 公式；
4. **完善 `README.md`**：补充真实的痛点分析与使用命令。

---

### 第 4 步：工业级规范与安全质检 (`skill_lint.py`)

完成文件编写后，**必须运行合规质检仪进行自检扫描**：

```bash
python .agents/skills/skill_creator/scripts/skill_lint.py .agents/skills/<skill_name>
```

**质检标准（必须全部 PASS）**：
- [x] `SKILL.md` 与 `README.md` 双轨完备；
- [x] Frontmatter `name` 与目录同名，`description` 具备触发关键词；
- [x] `SKILL.md` 包含第 0 步依赖自检或无需依赖声明；
- [x] Python 脚本具备 Windows UTF-8 编码重配；
- [x] 涉及写文件的脚本具备目标文件覆盖备份机制 (`.bak`)。

如有报错，AI 自行根据质检提示完成修正，直到达到 **100% 工业级完全合规 (PERFECT)**。

---

### 第 5 步：自动注册至全景矩阵

质检通过后，AI 将新技能条目追加登记至根目录 [README.md](file:///c:/Users/25948/Desktop/Awesome-Agent-Skills/README.md) 的中英文 **技能全景矩阵 (Skills Matrix)** 表格中。

---

## 📐 交互规范

- 始终秉承**双轨制哲学**：给 AI 的指令精简无废话，给人类的说明图文并茂。
- 始终把**数据安全（自动备份）**和**跨平台稳定性（UTF-8）**作为最高工程红线。
