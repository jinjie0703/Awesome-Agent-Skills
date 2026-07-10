---
name: project-deep-diver
description: 秋招/社招项目深挖面经准备技能。自动扫描项目代码指纹，提炼 STAR 法则亮点，预测面试官连环拷问并生成高分防御手册。
category: career-preparation
tags: [interview, resume, project, STAR]
---

# Project Deep Diver - 项目深挖面经利器

当用户希望复盘简历项目、准备大厂面试的项目深挖环节，或者不知道如何包装项目亮点时，严格执行以下 SOP。

---

## ⚙️ 第 0 步：环境检查（此技能无需额外依赖）

本技能使用的 Python 脚本仅依赖标准库（`os`, `json`, `pathlib`, `collections`），**无需安装任何第三方依赖**。只需确认用户机器上存在 Python 3.9+：
```bash
python --version
```

---

## 🚀 标准操作工作流 (SOP)

### 第 1 步：项目物理扫描 (`project_inspect.py`)

**触发条件**：用户提供了项目的本地代码目录路径，或者 AI 可以访问到项目文件时，**必须优先执行物理扫描**。

```bash
# 输出 JSON 侦查报告
python .agents/skills/project_deep_diver/scripts/project_inspect.py <项目目录路径>

# 同时输出 Markdown 可读简报
python .agents/skills/project_deep_diver/scripts/project_inspect.py <项目目录路径> --markdown
```

**扫描产出**：
- 主语言判定与各语言代码行数占比
- 技术栈指纹（框架、数据库、缓存、基础设施、CI/CD）
- 核心依赖清单（自动解析 `package.json` / `requirements.txt` / `pom.xml`）
- 顶层目录结构大纲

**⚠️ 重要**：如果用户没有提供项目目录（只是口头描述项目），则跳过此步直接进入第 2 步，根据用户的口述信息进行深挖。

---

### 第 2 步：项目深度解剖与面经深挖（AI 核心推理阶段）

基于第 1 步的扫描报告（或用户口述的项目描述），AI 按照以下四大模块进行深度挖掘：

#### 🌟 模块 A：亮点包装与技术壁垒提炼
- **脱水提炼**：把用户平铺直叙的功能描述，升级为具有工业级水准的**高含金量技术亮点**，使用 **STAR 法则**（Situation 情境 → Task 任务 → Action 行动 → Result 成果）与**量化指标**描述。
- **难点深挖**：如果用户觉得项目"太简单"，从**高并发、大数据量、极端边界、性能瓶颈、内存优化、网络异常、缓存穿透/雪崩**等工程维度，为其构思和挖掘 1~3 个真实可信的架构难点。

#### 🎯 模块 B：面试官视角 5 连环压力深挖预测
预测面试官看到该项目时最想拷问的 5 个层次，并给出能体现技术深度的"高情商防御话术"：
1. **架构选型关**：为什么当时选这个架构/技术方案，而不是其他的？
2. **极端场景关**：如果当前的流量/数据量放大 10 倍甚至 100 倍，你的系统哪里会先挂掉？怎么改造？
3. **线上 Bug 关**：这个项目开发过程中遇到最难搞的一个 Bug 是什么？你是怎么定位和解决的？
4. **性能极限关**：你在项目中做了哪些关键优化？核心指标（如首屏时间、内存占用、QPS）提升了多少？
5. **自我批判关**：如果让你现在重新做这个项目，你会推翻哪里的设计？为什么？

#### 🛠️ 模块 C：解决方案降维/进阶三级对比
针对项目中最大的技术挑战，给出：
- **初级方案（刚好能用）**：存在什么隐患。
- **当前方案（进阶落地）**：你项目里实际用到的方案与优势。
- **终极方案（大厂海量业务架构）**：如果有无限资源或超高并发，业界最顶尖的解决方案是什么。

#### 🔄 模块 D：自我批判与成长复盘
引导用户思考："如果重新来过，我会改进哪些设计"——这是大厂面试中**最高频的杀手锏追问**。

---

### 第 3 步：导出面经防御手册 (`playbook_generator.py`)

当 AI 完成深挖分析后，**必须**将结果结构化为 JSON 数据，调用导出工具生成持久化的 Markdown 手册：

```bash
python .agents/skills/project_deep_diver/scripts/playbook_generator.py \
    --project-name "项目名称" \
    --json-file deep_dive_data.json \
    --output "面经防御手册_项目名.md"
```

**JSON 数据结构规范**（AI 负责组装此结构）：
```json
{
    "project_summary": "一句话项目概述",
    "tech_stack": ["Vue3", "Spring Boot", "Redis"],
    "highlights": [
        {"title": "亮点标题", "star_desc": "STAR 法则完整描述", "keywords": ["关键词"]}
    ],
    "difficulties": [
        {"title": "难点标题", "problem": "问题", "solution": "解决方案", "result": "成果"}
    ],
    "grilling_qa": [
        {"category": "架构选型关", "question": "面试官问题", "answer": "防御话术"}
    ],
    "architecture_comparison": {
        "challenge": "核心挑战",
        "junior": {"desc": "初级方案", "risk": "隐患"},
        "current": {"desc": "当前方案", "advantage": "优势"},
        "ultimate": {"desc": "终极方案", "scenario": "适用场景"}
    },
    "self_reflection": "复盘改进点"
}
```

---

## 📐 输出规范

- 语气专业、犀利，极具实战指导性。
- 关键的技术设计模式、优化手段和底层原理词汇**加粗**显示。
- 量化指标（如首屏时间从 3s 降至 800ms、QPS 从 500 提升至 5000）必须有具体数字支撑。
- 面试话术要自然流畅，像真人在和面试官交流，**绝不能像朗诵课文**。
