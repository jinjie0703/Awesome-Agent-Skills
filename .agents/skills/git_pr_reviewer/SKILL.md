---
name: git_pr_reviewer
description: 代码审查、敏感密钥泄露拦截与标准化 Git PR 提交生成技能。自动提取 git diff 变更，扫描 Secret 泄露与代码异味，生成符合 Conventional Commits 规范的精准提交信息与大厂级 PR 审查报告。在需要审查代码变更、生成 Git Commit 提交信息、或编写 PR 描述时使用。
category: code-quality-and-git
tags: [git, pr, code-review, security, conventional-commits]
---

# Git PR Reviewer - 代码审查与 Git 提交卫士

当用户准备提交代码、需要审查代码修改质量、需要生成规范的 Conventional Commit 提交信息、或者编写 Pull Request (PR) 描述时，严格执行以下 SOP。

---

## ⚙️ 第 0 步：环境检查（零外部依赖）

本技能使用的底层扫描工具仅依赖 Python 3.9+ 标准库与系统 `git` 命令，无需安装任何第三方依赖：
```bash
python --version
git --version
```

---

## 🚀 标准操作工作流 (SOP)

### 第 1 步：物理提取 Git Diff 与安全扫描 (`git_diff_inspect.py`)

AI **必须优先调用**底层扫描脚本获取当前代码变更并执行自动化安全审计：

```bash
# 场景 A: 扫描当前工作区所有改动（未暂存 + 已暂存）并输出 Markdown 简报
python .agents/skills/git_pr_reviewer/scripts/git_diff_inspect.py --markdown

# 场景 B: 仅扫描已暂存 (git add) 的修改
python .agents/skills/git_pr_reviewer/scripts/git_diff_inspect.py --staged --markdown

# 场景 C: 扫描当前分支与主分支 (如 main) 的差量
python .agents/skills/git_pr_reviewer/scripts/git_diff_inspect.py --branch main --markdown
```

**脚本自动扫描项目**：
- 变动文件列表、新增/删除代码行数；
- **高危 Secret 泄露扫描**：自动识别并脱敏拦截 OpenAI Key、AWS 凭据、私钥、数据库连接密码、内部 IP；
- **代码卫生扫描**：捕获残留的 `console.log`、`print()`、`debugger` 与未完成的 `TODO/FIXME`。

---

### 第 2 步：安全门禁与拦截决策 (Security Gate)

- 🚨 **若检测到高危 Secret 泄露**：
  AI **必须立即阻断提交流程**，高亮警告用户所在文件和代码行，提示用户先通过环境变量或 `.env` 清理密钥后再提交！
- 🧹 **若检测到调试残留**：
  友好提示用户确认是否需要清理临时调试日志。

---

### 第 3 步：生成符合规范的 Conventional Commit 提交信息

AI 基于提取到的精确 Diff 语义，生成符合规范的标准 Commit Message：

```text
<type>(<scope>): <subject>

[可选的详细变更要点列表]
```

**规范对照表**（参见 `references/conventional_commits.md`）：
- `feat`: 新增功能 / 新模块
- `fix`: 修复 Bug 或异常崩溃
- `refactor`: 重构代码（不改变外部行为）
- `perf`: 性能调优
- `docs`: 文档或说明更新
- `chore`: 依赖更新或日常琐碎配置维护

---

### 第 4 步：生成标准 Pull Request (PR) 审查报告

根据 `references/pr_template.md` 模板，为用户输出结构化审查报告：
1. **📌 变更概述**：用 2~3 句话讲清改动背景与业务影响；
2. **🛠️ 核心修改模块**：分模块提炼核心改动；
3. **🛡️ 架构与边界评估**：评估是否存在并发安全风险、内存消耗或向后兼容性（Breaking Changes）；
4. **🧪 建议验证方式**：给出最小化的本地测试或运行命令。

---

## 📐 输出规范

- 语气严谨客观，像负责任的资深 Tech Lead 在进行代码评审；
- 格式清晰，避免冗长车轱辘话；
- 涉及文件名、分支名与提交命令一律用代码块 `格式包裹。
