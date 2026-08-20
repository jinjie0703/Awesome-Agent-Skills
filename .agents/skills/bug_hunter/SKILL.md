---
name: bug_hunter
description: 线上疑难杂症、死锁、高并发 Race Condition 与日志根因排查技能。自动提取崩溃堆栈指纹，构建根因假设树，生成最小复现用例 (MRE) 与工业级防御性修复补丁。在遇到复杂报错、排查线上 Bug、分析日志异常或排查性能瓶颈时使用。
category: debugging-and-troubleshooting
tags: [debug, rca, root-cause, log-analysis, stacktrace, race-condition]
---

# Bug Hunter - 线上疑难杂症与根因排查侦探

当用户提供报错日志、遇到程序崩溃、接口 500、偶发性死锁、内存泄露或高并发 Race Condition 时，严格执行以下 5 步根因排查 SOP。

---

## ⚙️ 第 0 步：环境检查（零外部依赖）

本技能使用的日志分析工具仅依赖 Python 3.9+ 标准库，无需安装任何第三方依赖：
```bash
python --version
```

---

## 🚀 标准操作工作流 (5 步根因推导 SOP)

### 第 1 步：日志物理侦查与堆栈指纹提取 (`log_inspector.py`)

当用户提供了日志文件或控制台长文本时，优先调用底层分析工具：

```bash
# 扫描日志并输出 Markdown 结构化简报
python .agents/skills/bug_hunter/scripts/log_inspector.py <log_file_path> --markdown
```

**脚本自动完成**：
- 识别 Python / Java / Node.js / Go Panic / SQL 数据库异常；
- 剥离上百行第三方库框架噪音，精准锁定最先触发异常的**业务代码文件名与行号**；
- 自动对日志中出现的密码、Token、身份证与卡号进行脱敏。

---

### 第 2 步：构建纯文本 ASCII 根因假设树 (Hypothesis Tree)

AI 基于异常指纹与业务场景，推导 2~3 个最可能的深层机理假设，并使用纯文本 ASCII 树状图清晰呈现（**严禁使用 Mermaid 语法**）：

```text
               ┌── 假设 A: 数据库连接池耗尽 (长事务阻塞 / 连接未释放)
  [崩溃根因] ──┼── 假设 B: 高并发写 Race Condition (未加互斥锁导致脏读)
               └── 假设 C: 跨微服务序列化字段缺失 (反序列化 NullPointerException)
```

---

### 第 3 步：编写最小可复现用例 (Minimal Reproducible Example - MRE)

为验证假设，给出一段 **10~20 行脱水可执行代码**，剥离复杂的业务表和 RPC 调用，能稳定触发相同的崩溃现场。

---

### 第 4 步：工业级防御性修复补丁 (Defensive Patch)

给出清晰的代码修复方案（使用 Markdown `diff` 代码块）：
```diff
- 原先脆弱、容易崩溃的代码行
+ 增加前置防御判空、超时控制或互斥锁机制的代码行
```

**修复必须满足三大防御准则**：
1. **边界保护**：空指针防御、数组越界兜底、无效状态拦截；
2. **资源释放**：使用 `try-finally` 或 `with` 上下文管理器确保连接/句柄 100% 释放；
3. **超时与降级**：网络 IO 与锁获取必须配置显式超时时间。

---

### 第 5 步：防回归单元测试与长效防线 (Post-Mortem)

- 提供 1~2 个针对该极端边界场景的单元测试用例（如超时重试、并发并发抢占测试）；
- 给出 1 条避免团队日后再次踩坑的架构级改进建议。

---

## 📐 格式与输出红线

1. **🚫 严禁使用 Mermaid 语法**：一律使用纯文本 ASCII 字符树状图展示排查假设；
2. **严禁盲猜**：修复建议必须紧扣日志中的真实报错堆栈，明确指出出问题的代码行；
3. **关键函数与异常名加粗**突出显示。
