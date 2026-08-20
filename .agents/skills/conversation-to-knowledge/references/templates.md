# Knowledge Note Templates

Choose the template that fits the knowledge naturally. Do not force-fit.
All templates include PKM-ready (Obsidian / Logseq / Notion) YAML Frontmatter for seamless vault integration.

---

## Template A: Decision / Solution (Default)

Use when the knowledge involves a concrete problem, a chosen solution, and explicit reasoning.

```markdown
---
title: "[Clear, Actionable Title — Not 'Chat Summary']"
date: YYYY-MM-DD
type: decision-record
tags: [architecture/topic, domain/subdomain]
aliases: ["Alternative Search Keyphrase"]
status: evergreen
---

# [Clear, Actionable Title]

## Context
[Brief background: what engineering challenge or constraint triggered this?]

## Problem
[The core friction, bottleneck, or decision point.]

## Solution / Decision
[The concrete approach taken or decided upon.]

## Why (Trade-offs & Rationale)
- **Pros**: [Key benefits and operational upsides]
- **Cons & Costs**: [Accepted trade-offs, limitations, or maintenance cost]

## Lessons Learned
[Generalized rules, pitfalls to avoid, or invariants applicable beyond this case.]
```

---

## Template B: Mental Model / Conceptual Framework

Use when the knowledge is a reusable way of thinking, not a specific problem/solution pair.

```markdown
---
title: "[Concept Name]"
date: YYYY-MM-DD
type: mental-model
tags: [framework/mental-model, engineering-principles]
aliases: ["Concept Synonym"]
status: evergreen
---

# [Concept Name]

## One-Liner
[One sentence that captures the core insight.]

## Explanation
[2-3 paragraphs unpacking the mental model.]

## When to Apply
[In what situations should an engineer recall this model?]

## Lessons Learned
[Key takeaways or common mistakes when applying this model.]
```

---

## Template C: Anti-Pattern / Failure Report

Use when the primary value is "what NOT to do" and why.

```markdown
---
title: "[Anti-Pattern Name]: Why [Approach] Fails for [Context]"
date: YYYY-MM-DD
type: anti-pattern
tags: [debugging/anti-pattern, post-mortem]
aliases: ["Failed Pattern Name"]
status: evergreen
---

# [Anti-Pattern Name]: Why [Approach] Fails for [Context]

## Context
[What situation led to trying this approach?]

## What Was Tried
[The approach that was attempted.]

## Why It Failed
[Root cause analysis — the underlying mechanism, not just symptoms.]

## Better Alternative
[What should be done instead, and why it avoids the failure mode.]

## Lessons Learned
[Generalized takeaway.]
```
