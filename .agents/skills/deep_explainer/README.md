# 💡 deep_explainer - 深度技术导师与第一性原理讲解

[![Skill Version](https://img.shields.io/badge/Skill-v1.0.0-blue.svg)]()
[![No Dependencies](https://img.shields.io/badge/Dependencies-None-brightgreen.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)]()

> 让 AI 成为你的顶尖技术导师！告别枯燥的教科书念经与冗长胶水代码，采用**费曼学习法 + 5 层递进式认知阶梯**，将任何硬核技术概念拆解得深入浅出、透彻清晰！

---

## 🤔 解决什么痛点？

在日常使用 Agentic IDE（如 Cursor / Claude / Antigravity）写代码时，我们经常会遇到陌生的底层原理与架构概念。传统 AI 的解释往往让人痛苦：
- ❌ **满屏黑话**：用一个更难懂的名词去解释当前的名词，看完依然云里雾里；
- ❌ **跳过为什么**：不讲历史背景与诞生痛点，直接扔一堆 100 多行的生产级样板代码；
- ❌ **Mermaid 渲染翻车**：在无渲染插件的编辑器中输出 Mermaid 代码块，只能看到一堆乱码；
- ❌ **把技术吹成银弹**：只夸优点，对生产环境下的翻车隐患和架构权衡（Trade-offs）只字不提。

👉 **`deep_explainer` 的解决方案**：通过**“生活类比 ➔ 痛点倒推 ➔ ASCII数据流 ➔ 极简代码 ➔ 权衡避坑 ➔ 苏格拉底测验”**的 5 层渐进认知骨架，让你用最短时间彻底吃透技术本质！

---

## ✨ 核心特性

- 🌟 **费曼生活化类比 (Feynman Analogy)**：拒绝开篇黑话，用 10 岁小孩能听懂的常识建立第一直觉；
- 🚨 **痛点倒推法 (Pain-Point Framing)**：还原技术诞生的历史困境，讲透“为什么业界非要发明它”；
- 📐 **全平台纯文本 ASCII 框图**：彻底抛弃 Mermaid，在任何终端与 Markdown 编辑器下都能 100% 完美呈现清晰的数据流动与架构关系；
- 💻 **20行极简脱水代码 (MRE)**：剥离无关胶水代码，只展现最核心算法思想并配逐行白话注释；
- ⚖️ **大厂实战权衡矩阵 (Trade-offs)**：客观讲透致命缺点、边界场景与生产翻车陷阱；
- 🤔 **苏格拉底互动思考题**：提炼 1 个真实的边界故障场景，激活你的主动回忆与深度思考。

---

## 📂 目录结构

```text
deep_explainer/
├── README.md                      # 👥 本说明文档（给人类开发者看）
├── SKILL.md                       # 🤖 AI Agent 专用 5 层递进教学 SOP
├── references/
│   ├── explanation_framework.md   # 📐 5 层渐进式讲解标准骨架与评分维度
│   └── templates.md               # 📄 带有 PKM Frontmatter 的笔记模板
└── assets/
    └── examples.md                # 🌟 Few-Shot 黄金讲解案例（好回答 vs 糟糕回答对比）
```

---

## 🚀 如何触发与使用？

无需安装任何环境依赖！当你在日常开发中遇到任何不理解的概念时，直接向 AI 提问即可自动触发：

```text
🗣️ 用户提问范例：
- "怎么理解 Redis 的 Redlock 分布式锁？"
- "深入讲讲 Kafka 为什么读写吞吐量这么高？底层原理是什么？"
- "什么是 IO 多路复用 (epoll)？和 select 有什么区别？"
- "RAG 里的 ParentDocumentRetriever 是什么原理？为什么比普通切分好？"
- "OAuth2 PKCE 模式究竟解决了什么安全漏洞？"
```

AI 将自动激活 `deep_explainer` 技能，为你输出一份图文并茂、条理清晰的 5 层深度剖析卡片！

---

## 📄 License
MIT
