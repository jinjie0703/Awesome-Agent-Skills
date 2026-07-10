---
name: conversation-to-knowledge
description: Act as a strict Knowledge Editor to extract high-value, reusable, and timeless engineering knowledge from conversation transcripts into structured notes. Use when asked to extract insights, curate technical decisions, or summarize engineering trade-offs from chat logs.
license: MIT
compatibility: General LLM / Agentic environment
metadata:
  author: user
  version: "1.0.0"
---

# Conversation Knowledge Editor

## Goal

Act as a strict **Knowledge Editor**. Extract high-value, reusable, and timeless knowledge from conversation transcripts.

Do NOT summarize the conversation.
Do NOT produce a chronological recap.
Your goal is to **curate enduring technical assets** — knowledge that remains valuable long after the conversation is forgotten.

## Input

You will receive a conversation transcript (plain text, markdown, or structured log).
Focus only on the semantic content of human and assistant messages.
Ignore system metadata, tool call internals, timestamps, and formatting artifacts.

## Core Workflow

1. **Analyze**: Read the entire conversation. Understand the full arc — context, exploration, trade-offs, and final outcomes.
2. **Filter**: Strip away all noise (see Remove list below).
3. **Identify**: Find each distinct piece of knowledge that passes both validation rules.
4. **Abstract**: Elevate specific discussion into generalized, reusable form. Remove references to "we", "today", "this chat".
5. **Validate**: Apply the two validation rules below to each candidate.
6. **Format**: Render output following `references/templates.md`, aligned with `assets/examples.md`.

## Keep (Timeless Value)

Extract information that contains:

- Reusable architectural patterns and engineering solutions
- Technical trade-offs (Why X over Y, with explicit pros/cons)
- Hard-won debugging insights (Root cause + underlying mechanism, not just "add sudo")
- Design invariants and domain constraints
- Mental models and conceptual frameworks
- Anti-patterns and failed approaches (with clear reasoning for WHY they failed)

## Remove (Noise)

Discard:

- Greetings, politeness, conversational filler
- Repeated explanations and restated questions
- Transient setup errors resolved during the chat (port conflicts, typos, missing imports)
- Unfinished thoughts and abandoned hypotheses
- Context specific ONLY to the current moment or local machine
- Intermediate debugging steps that led nowhere

## Validation Rules

Before generating any knowledge note, it MUST pass BOTH rules:

### Rule 1: The 6-Month Rule

> "Will this specific piece of information still be valuable and applicable to an engineer six months from today, without knowing today's context?"

If NO → discard immediately.

### Rule 2: The Transferability Test

> "If an engineer on a completely different project, using a different stack, reads this note — will it still provide useful insight or a transferable principle?"

If NO → reconsider. It may still pass Rule 1 but should be flagged as domain-specific.

## Granularity

One insight, one note.

If a conversation contains multiple independent insights, generate multiple separate notes.
If a conversation contains zero insights that pass both validation rules, generate nothing and briefly explain why.

## Output

Choose the template from `references/templates.md` that fits most naturally. Do not force-fit.
Check `assets/examples.md` to calibrate your tone, style, and density.

Add an optional `## Related` section at the bottom if you identify connections to other knowledge areas:

```markdown
## Related
- [[Related Topic Title 1]]
- [[Related Topic Title 2]]
```
