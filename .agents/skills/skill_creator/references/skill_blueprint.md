# 📐 Agent Skill 设计蓝图与标准规范库

本文档为编写高质量、高鲁棒性、工业级合规的 AI Agent Skills 提供架构蓝图与范式参考。

---

## 🏛️ 一、 三大技能架构模式 (Skill Architecture Archetypes)

### 1. 纯元认知推理型 (Prompt-Only Engine)
* **适用场景**：知识提炼、代码架构评审、业务文案润色、思维链决策、逻辑论证。
* **特点**：**零外部代码依赖**，纯靠大语言模型极其严密的元认知提示词与 Few-Shot 样本进行高质量推理。
* **目录标准**：
  ```text
  my_skill/
  ├── README.md                      # 人类说明书
  ├── SKILL.md                       # AI 脑机接口（严格的过滤规则、检验法则、推理链）
  ├── assets/
  │   └── examples.md                # 黄金 Few-Shot 样本库（Bad vs Good 样例标杆）
  └── references/
      └── templates.md               # 产出结构模板库（带 PKM YAML Frontmatter）
  ```

---

### 2. 工具辅助执行型 (Tool-Assisted Engine)
* **适用场景**：Office 文档处理、音视频转码、数据清洗、爬虫、二进制文件转换。
* **特点**：大模型负责理解人类意图并组装参数，底层由一组**高度确定性、原子化、自带防错防线**的 Python/Shell 脚本执行。
* **目录标准**：
  ```text
  my_skill/
  ├── README.md                      # 人类说明书（CLI 用法、特性矩阵、参数说明）
  ├── SKILL.md                       # AI 脑机接口（第 0 步环境自检、SOP、脚本参数表）
  └── scripts/
      ├── <skill>_inspect.py         # 侦查感知脚本（只读，获取元数据简报）
      ├── <skill>_process.py         # 核心处理脚本（带 --dry-run 与 .bak 自动备份）
      └── <skill>_export.py          # 格式化导出脚本
  ```

---

### 3. 混合推理全栈型 (Hybrid Engine)
* **适用场景**：真实项目深挖、代码库架构重构、线上故障根因排查。
* **特点**：物理脚本扫描事实 → AI 深度认知推理 → 脚本持久化导出精美交付物。
* **目录标准**：
  ```text
  my_skill/
  ├── README.md                      # 人类说明书
  ├── SKILL.md                       # 包含扫描、推理模块、连环追问与交付 SOP
  └── scripts/
      ├── project_inspect.py         # 物理事实扫描仪
      └── playbook_generator.py      # 交付物生成器（带覆盖备份）
  ```

---

## ✍️ 二、 Frontmatter `description` 黄金编写公式

Agent 运行时根据 `description` 进行语义匹配，决定是否激活技能。

$$\text{Description} = \text{【角色/能力定位】} + \text{【核心功能清单】} + \text{【明确触发条件 (Use when... / 在...时使用)】}$$

### 优质范例：
* **中文工具型**：
  ```yaml
  description: 读取、修改、渲染与智能排版 Microsoft Word (.docx) 文档的工具集与指南。在需要对 Word 文档进行内容概览、排版美化、局部查找替换、或模板数据填空时使用。
  ```
* **英文推理型**：
  ```yaml
  description: Act as a strict Knowledge Editor to extract high-value, reusable, and timeless engineering knowledge from conversation transcripts into structured notes. Use when asked to extract insights, curate technical decisions, or summarize engineering trade-offs from chat logs.
  ```

---

## 🛡️ 三、 工业级防错防线标准代码段

任何为技能编写的 Python 脚本，必须标配以下三大防护代码：

### 1. Windows 终端 UTF-8 防乱码与防崩溃
```python
import sys
# 放在所有 import 之后的脚本最顶部
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")
```

### 2. 覆盖写前强制 `.bak` 备份机制
```python
import shutil
from pathlib import Path

def backup_file(file_path: Path) -> str:
    """在覆盖写操作前自动创建 .bak 副本，确保数据安全可回滚"""
    if not file_path.exists():
        return ""
    bak_path = file_path.with_suffix(f".bak{file_path.suffix}")
    shutil.copy2(str(file_path), str(bak_path))
    return str(bak_path)
```

### 3. 安全路径与目录自动创建
```python
# 永远使用 pathlib.Path，并在保存前自动创建父级目录
save_path = Path(output_path).resolve()
save_path.parent.mkdir(parents=True, exist_ok=True)
```
