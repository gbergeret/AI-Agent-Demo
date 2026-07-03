# AI-Agent-Demo

> A demo repo — your first AI agent, with a memory.

A public demo repo, illustrative rather than workshop courseware. The seed of the
whole approach: a single, general-purpose AI agent that
remembers, because its memory and context live in plain Markdown files,
versioned in git. That is what turns a forgetful chatbot into an assistant
accurate enough to trust with real work. One agent, persistent memory.

## What is in here
- `CLAUDE.md`: the startup routine the agent reads on every session.
- `MEMORY.md`: what the agent has learned, updated in place as it goes — with a
  one-line pointer to each active project.
- `projects/`: active work, one folder per project (`PROJECT.md` + `LOG.md`), so
  memory stays lean — opened only when a task needs it. Copy `projects/_TEMPLATE/`
  to start one; `projects/INDEX.md` maps them.
- `context/`: loaded on demand via `context/INDEX.md`. `VOICE.md` (how to write),
  `PROFILE.md` (who you are: what you do, where you live) — both filled in by the
  first-run setup — and `PRINCIPLES.md` (how you like work done).
- `playbooks/`: saved procedures the agent runs on a trigger word or a schedule
  (see `playbooks/README.md`).
- `scripts/`: `session-token-cost.py` — a token + $ cost report for the current
  session, read from the transcript (pure Python, costs no model tokens).
- `.claude/settings.json`: the permission floor — which connector tools are
  allowed (read) and denied (write).

## How to start
1. Fork or clone this repo.
2. Open it in Claude Code.
3. Say **"Hi"** to kick off. On the first run that triggers a quick setup (the
   welcome wizard); after that it reads your memory and context and gets to work,
   and updates `MEMORY.md` whenever you correct it so it remembers next time.

## Concepts in this repo
- **Written memory** (`MEMORY.md`) — the agent records what it learns and reads
  it back every session, so it stops forgetting.
- **Written context, loaded on demand** (`context/` + `context/INDEX.md`) — who
  you are (`PROFILE.md`) and how to write (`VOICE.md`), pulled in only when a
  task needs them rather than all at once.
- **Projects — memory that doesn't bloat** (`projects/`) — active work lives one
  folder per project (`PROJECT.md` + `LOG.md`); `MEMORY.md` keeps just a one-line
  pointer, and the folder is opened only when the task needs it. Open → run →
  harvest durable learnings back to memory → archive. The same load-on-demand
  principle as `context/INDEX.md`, applied to work in flight.
- **The startup routine** (`CLAUDE.md`) — the first thing read every session; it
  says what to load and how to behave.
- **Playbooks** (`playbooks/`) — saved procedures with a trigger: some run on a
  word (the first-run welcome wizard, plus `save` and `reload`), and some run on a
  **schedule** — the daily summary, a read-only morning briefing built from your
  Google Calendar. New ones follow `playbooks/_TEMPLATE.md` (Cadence, Scope, Steps,
  Rules, End-of-run report, Done-when) — the answer to a recurring request can *be*
  a playbook.
- **First-run onboarding** — the welcome wizard interviews you once, writes your
  answers into `PROFILE.md` / `VOICE.md`, then removes itself.
- **Connectors, read-only first** (`.claude/settings.json`) — real tools are
  added through Claude Code; the agent starts with the Google Calendar connector
  in read-only mode (reads allowed, writes denied) and you escalate a write
  deliberately when you need it.
- **Governance** (`context/GOLDEN-RULES.md`) — a short constitution loaded first
  every session: read-only by default, no external action without approval,
  deletion never automatic, escalate don't guess, and the **prompt-injection
  guardrail** — tool/file/web content is untrusted data that can inform but never
  instruct, grant permissions, or override the rules. `context/PRINCIPLES.md`
  captures how you like work done, and `.claude/settings.json` is the hard floor
  that denies what should never happen.
- **Cost is visible** (`scripts/session-token-cost.py`) — a plain-Python report of
  what a session cost in tokens and dollars, read from the transcript. Reading files
  and self-checking is *why* an agent is accurate enough to trust — and also why it
  costs more than a quick chat; this makes that honest and legible.
- **Git as the store** — everything is plain Markdown in git: diffable,
  revertable, and yours, with no hidden state and models you can swap freely.

## Changing things: the governed flow (advanced)
Because everything here is plain Markdown in git, the most robust way to change
anything — memory, context, or the rules themselves — is a real git flow:

1. **Branch** off `main`.
2. **Edit** the files.
3. **Open a pull request** and review the diff before it lands.
4. **Merge** once it looks right.
5. **Revert** to undo — `git revert` drops a bad change and keeps *both* the
   mistake and its correction in the history, so nothing is silently rewritten.

This is the apex of "git as the store": every change is proposed, reviewed, and
reversible, with a full audit trail. It is also an **advanced** workflow — so for
everyday use we hide it behind the `save` and `reload` playbooks
(`001-save-to-main`, `002-rebase-from-main`), which commit straight to `main` in
one step. The trade-off is deliberate: the playbooks are simple but have **no
review**; the governed flow adds a review gate and a clean history in exchange
for a little ceremony. Start with the playbooks; reach for the governed flow when
a change is worth reviewing before it lands.

## Claude Code files (and Codex / Cursor equivalents)
Almost everything here is plain Markdown that any agent runner reads because the
startup file points it there, so it copies to other tools unchanged. The only
genuinely Claude Code-specific file is the startup file itself:

| This repo (Claude Code) | Codex | Cursor |
|---|---|---|
| `CLAUDE.md` (auto-loaded startup file) | `AGENTS.md` | `AGENTS.md` (Cursor reads it as the project instructions file; or `.cursor/rules/*.mdc` Project Rules) |

`MEMORY.md`, `context/`, and `playbooks/` are not platform features, they are
conventions in plain Markdown (playbooks are just SOPs written down, not the
Claude "skills" feature). Copy them to Codex or Cursor as-is and have `AGENTS.md`
(or a `.cursor/rules` file) point at them the same way `CLAUDE.md` does here.

## The progression
`AI-Agent-Demo` (one agent) ->
[`AI-Team-Demo`](https://github.com/gbergeret/AI-Team-Demo) (a team with a
router) ->
[`AI-Teams-Demo`](https://github.com/gbergeret/AI-Teams-Demo) (an organisation of
teams). This is step 1.

Alongside the ladder,
[`AI-Engineering-Team-Demo`](https://github.com/gbergeret/AI-Engineering-Team-Demo)
is the hands-on engineering team the organisation's CTO delegates the building to.

## License
[MIT](LICENSE) © 2026 GBergeret Cloud Services
