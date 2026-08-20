# 🕵️ bug_hunter - 线上疑难杂症与根因排查侦探

[![Skill Version](https://img.shields.io/badge/Skill-v1.0.0-blue.svg)]()
[![Python Version](https://img.shields.io/badge/Python-3.9%2B-green.svg)]()
[![No Dependencies](https://img.shields.io/badge/Dependencies-None-brightgreen.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)]()

> 告别盲猜式 Debug！化身大厂资深 SRE 与排障专家，自动提取海量日志中的崩溃堆栈指纹，构建纯文本根因假设树，秒级定位业务破裂点，输出最小复现用例 (MRE) 与工业级防御性修复补丁！

---

## 🤔 解决什么痛点？

在开发与线上运维时，排查疑难杂症通常痛苦不堪：
- ❌ **海量日志抓不住重点**：几万行日志里充斥着第三方框架的无效堆栈，找不到真正触发异常的业务代码行；
- ❌ **盲猜式 Debug**：普通 AI 经常不看日志细节瞎建议“重启试试/升级包版本”，浪费大量时间；
- ❌ **治标不治本**：只打了个临时补丁，到了高并发或极端网络抖动时再次暴雷；
- ❌ **日志敏感数据泄露**：把带线上真实用户密码或 Token 的日志直接贴给 AI 带来合规隐患。

👉 **`bug_hunter` 的解决方案**：通过底层脚本 `log_inspector.py` 自动脱敏并剥离噪音堆栈，AI 严格遵从 **“现象 ➔ 堆栈指纹 ➔ ASCII 假设树 ➔ 10行极简复现 (MRE) ➔ 防御性补丁 ➔ 防回归单测”** 完整闭环！

---

## ✨ 核心特性

- 🔬 **跨语言堆栈指纹分析 (`log_inspector.py`)**：支持自动识别并解析 Python, Java/Spring, Node.js, Go Panic, Rust Panic 以及 SQL 数据库死锁/超时报错；
- 🛡️ **敏感信息自动脱敏**：在解析时自动对日志中出现的 Password, API Key, Token 与身份证/卡号进行掩码处理；
- 📐 **全平台纯文本 ASCII 假设树**：无需 Mermaid 渲染支持，直观展示排障推演链路；
- 💻 **10行极简复现用例 (MRE)**：自动剥离庞杂业务依赖，生成可 100% 稳定复现现场的脱水测试脚本；
- 🛡️ **工业级防御性修复**：附带超时控制、空指针防护、资源自动释放与防回归单元测试。

---

## 📂 目录结构

```text
bug_hunter/
├── README.md                      # 👥 本说明文档（给人类开发者看）
├── SKILL.md                       # 🤖 AI Agent 专用 5 步根因排查 SOP
├── references/
│   └── debug_playbook.md          # 📐 RCA 根因排查标准方法论手册
└── scripts/
    └── log_inspector.py           # 🛠️ 日志堆栈提取与敏感信息脱敏分析仪
```

---

## 🚀 快速开始 (CLI)

### 1. 扫描与分析日志文件
```bash
# 输出 Markdown 可读简报
python scripts/log_inspector.py /path/to/server_error.log --markdown

# 导出 JSON 结构化报告
python scripts/log_inspector.py /path/to/server_error.log --output error_report.json
```

---

## 📄 License
MIT
