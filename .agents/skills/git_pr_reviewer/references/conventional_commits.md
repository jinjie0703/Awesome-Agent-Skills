# 📐 Conventional Commits 规范标准与速查手册

本技能严格遵循 [Conventional Commits 1.0.0](https://www.conventionalcommits.org/) 规范生成提交信息。

---

## 🔤 提交格式标准

```text
<type>(<optional scope>): <subject>

[optional body]

[optional footer(s)]
```

---

## 🏷️ 核心类型 (`<type>`) 速查表

| Type | 说明 | 适用场景范例 |
| :--- | :--- | :--- |
| **`feat`** | 引入新功能 / 新模块 | `feat(auth): add OAuth2 PKCE login support` |
| **`fix`** | 修复 Bug / 缺陷 | `fix(parser): resolve null pointer crash on empty input` |
| **`perf`** | 性能优化 | `perf(cache): add Redis multi-tier caching layer` |
| **`refactor`**| 重构（既不加新功能，也不修 Bug） | `refactor(logger): simplify structured output formatting` |
| **`docs`** | 文档更新 | `docs(readme): update API parameters table` |
| **`style`** | 格式变动（不影响代码逻辑） | `style(lint): fix indentation and trailing whitespace` |
| **`test`** | 增加或重构测试用例 | `test(unit): add boundary tests for date parser` |
| **`build`** | 构建系统或外部依赖变动 | `build(deps): upgrade vite to 5.4.0` |
| **`ci`** | CI/CD 配置文件与流水线变动 | `ci(github): add automated testing workflow` |
| **`chore`** | 其他日常琐碎维护 | `chore(gitignore): ignore local debug cache directory` |
| **`revert`**| 回滚先前的提交 | `revert: revert "feat(auth): add OAuth2 support"` |

---

## 📐 编写黄金法则

1. **Subject 动词使用小写**（如 `add`, `fix`, `update`, `optimize`），字数控制在 50 字符以内；
2. **末尾严禁加句号 `.`**；
3. **破坏性变更 (Breaking Change)**：在 `<type>` 后加 `!` 或在 Footer 声明 `BREAKING CHANGE: ...`。
