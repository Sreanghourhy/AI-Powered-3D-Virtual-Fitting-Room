# Task Backlog

Each phase is split into small tasks. **No task should take more than one working day.** If one grows bigger, split it.

## How to read a task

```markdown
### P2-03 · Add FastAPI health endpoint   `S`
**Depends on:** P2-02
- [ ] step 1
- [ ] step 2
**Done when:** a clear, testable result
```

| Size | Meaning |
|------|---------|
| `XS` | ≤ 1 hour |
| `S`  | ≤ half a day |
| `M`  | ≤ 1 day |

- Task ID format: `P<phase>-<number>` (e.g. `P3-05`). Use it in branch names and commits: `git checkout -b p3-05-blur-check`.
- Tick the checkbox `- [x]` when a step is done. A task is done only when its **Done when** line is true.
- 🔒 marks a privacy/security task. Don't skip these, even in the prototype.
- ⚠️ marks a high-risk / research task whose result may change the plan.

## Phase files

| Phase | File | Tasks |
|-------|------|-------|
| 0 | [phase-0-start-today.md](phase-0-start-today.md) | 7 |
| 1 | [phase-1-requirements.md](phase-1-requirements.md) | 10 |
| 2 | [phase-2-foundation.md](phase-2-foundation.md) | 18 |
| 3 | [phase-3-capture.md](phase-3-capture.md) | 21 (re-planned for MacBook camera) |
| 4 | [phase-4-reconstruction.md](phase-4-reconstruction.md) | 16 |
| 5 | [phase-5-profiles-viewer.md](phase-5-profiles-viewer.md) | 11 |
| 6 | [phase-6-try-on.md](phase-6-try-on.md) | 16 |
| 7 | [phase-7-hardening.md](phase-7-hardening.md) | 15 |
| 8 | [phase-8-pilot.md](phase-8-pilot.md) | 9 |

## Critical path

```text
P0 ─▶ P1 ─▶ P2 ─▶ P3 ─▶ P4 (decision D1) ─▶ P5 ─▶ P6 ─▶ P7 ─▶ P8
                         ▲
                         └── Start P4 research (P4-01..P4-04) in parallel with P2
                             so the riskiest unknown is answered early.
```
