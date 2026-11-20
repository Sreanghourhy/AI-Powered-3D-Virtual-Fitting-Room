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
| 2 | [phase-2-foundation.md](phase-2-foundation.md) | 18 ✅ (auth/consent parts superseded by CR-02) |
| **2R** | [phase-2r-single-user.md](phase-2r-single-user.md) | **7 (new, CR-02)** |
| 3 | [phase-3-capture.md](phase-3-capture.md) | 21 (MacBook camera; P3-00 ✅) |
| 4 | [phase-4-reconstruction.md](phase-4-reconstruction.md) | 16 |
| 5 | [phase-5-profiles-viewer.md](phase-5-profiles-viewer.md) | 9 (rewritten: viewer + local persistence) |
| 6 | [phase-6-try-on.md](phase-6-try-on.md) | 16 |
| 7 | [phase-7-hardening.md](phase-7-hardening.md) | 12 (rewritten: local privacy) |
| 8 | [phase-8-pilot.md](phase-8-pilot.md) | 5 (rewritten: personal evaluation) |
| | **Total** | **121** (34 done: P0 ×5, P1 ×10, P2 ×18, P3-00) |

## Critical path

Development sequence after CR-02 (priority: camera → capture → reconstruction → try-on → viewer):

```text
P2R (remove auth, one fitting room) ─▶ P3 Part B feasibility (P3-01..05) ─▶ 🛑 owner go/no-go
     ▲                                  │
     └── P3-01 may run in parallel ─────┘
 ─▶ P3 Part C capture build ─▶ P4 reconstruction (D1, F11) ─▶ P6 shirt/pants try-on
 ─▶ P5 viewer polish + local persistence ─▶ P7 privacy & reliability ─▶ P8 personal evaluation
```
