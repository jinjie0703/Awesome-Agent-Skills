# 🛡️ git_pr_reviewer - 代码审查与 Git 提交卫士

[![Skill Version](https://img.shields.io/badge/Skill-v1.0.0-blue.svg)]()
[![Python Version](https://img.shields.io/badge/Python-3.9%2B-green.svg)]()
[![No Dependencies](https://img.shields.io/badge/Dependencies-None-brightgreen.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)]()

> 在代码提交前，让 AI 化身严苛的资深 Tech Lead！自动提取 `git diff` 变更，拦截高危 API Key / Secret 泄漏与调试残留，生成符合 Conventional Commits 标准的精准提交信息与大厂级 PR 审查报告！

---

## 🤔 解决什么痛点？

日常开发与提交 Git 时，工程师经常会踩以下高危陷阱：
- ❌ **敏感密钥意外泄露**：手滑把 OpenAI API Key、AWS 密钥、数据库连接密码甚至内部内网 IP 提交到了公开仓库；
- ❌ **调试代码遗留线上**：忘记删除测试用的 `console.log`、`print()`、`debugger` 断点；
- ❌ **提交信息敷衍混乱**：写一堆 `fix bug`、`update code`、`111`，导致后续 Git 历史和线上回滚毫无追溯性；
- ❌ **PR 描述不写背景**：写 PR 时不知如何清晰概括技术变更、风险点与测试方法。

👉 **`git_pr_reviewer` 的解决方案**：提供底层原子扫描脚本 `git_diff_inspect.py` 配合 AI 架构审查 SOP，在提交前筑起一道坚不可摧的安全与质量门禁！

---

## ✨ 核心特性

- 🚨 **高危 Secret 泄露静态拦截**：内置多组高危正则模式库，自动识别并脱敏拦截 LLM Key、AWS 凭据、私钥、数据库密码与内网 IP；
- 🧹 **代码卫生与调试残留扫描**：自动检测 `console.log`、`print(debug)`、`debugger` 与 `TODO/FIXME`；
- 📝 **Conventional Commits 规范生成**：依据提交规范自动推导 `feat`, `fix`, `refactor`, `perf`, `docs` 等精准类型与简短 Subject；
- 📋 **大厂级 PR 审查报告输出**：一键生成带概述、变更清单、安全合规自检与验证命令的标准 PR 描述；
- ⚡ **零外部依赖**：仅依赖 Python 3.9+ 标准库与原生 `git` 命令，全平台开箱即用！

---

## 📂 目录结构

```text
git_pr_reviewer/
├── README.md                      # 👥 本说明文档（给人类开发者看）
├── SKILL.md                       # 🤖 AI Agent 专用审查 SOP 脑机接口
├── references/
│   ├── conventional_commits.md    # 📐 Conventional Commits 规范速查手册
│   └── pr_template.md             # 📋 大厂级 Pull Request 描述模板
└── scripts/
    └── git_diff_inspect.py        # 🛠️ Git Diff 提取与敏感信息静态扫描仪
```

---

## 🚀 快速开始 (CLI)

### 1. 扫描当前工作区的所有修改
```bash
# 输出 Markdown 可读简报
python scripts/git_diff_inspect.py --markdown

# 仅扫描已暂存 (git add) 的修改
python scripts/git_diff_inspect.py --staged --markdown

# 比对当前分支与 main 分支的差量
python scripts/git_diff_inspect.py --branch main --markdown
```

### 2. 导出审查报告为 JSON
```bash
python scripts/git_diff_inspect.py --output pr_report.json
```

---

## 📄 License
MIT
