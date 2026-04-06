---
name: scarlett-context-pull
description: Scarlett's lean startup check. All skills are pre-loaded -- no repo checks, no drive pulls, no skill discovery needed. Run at the start of every task. For Trinity context, use pull_trinity_context.sh to read and deposit_trinity_context.sh to write.
---
# Skill: scarlett-context-pull

## Startup (every task)
```bash
bash /home/ubuntu/skills/scarlett-context-pull/scripts/scarlett_context_pull.sh
```

## Trinity Context Pull (on-demand only)
Run only when the user explicitly asks for Trinity's context or updates.
```bash
bash /home/ubuntu/skills/scarlett-context-pull/scripts/pull_trinity_context.sh
```

## Trinity Context Deposit (post-task)
Run at the end of a task or chat session to record the current context snapshot to Trinity's Shared Drive.
```bash
bash /home/ubuntu/skills/scarlett-context-pull/scripts/deposit_trinity_context.sh
```

## Protocol Version
Scarlett Protocol v6.1 — March 2026. Lean startup. Everything pre-loaded. Context recording enabled.
