# CLAUDE.md

The startup routine. Read this first, on every session.

## First run: the welcome wizard
On the first session, if `playbooks/000-welcome-wizard.md` exists and the name in
`context/PROFILE.md` is not set yet, run that playbook before anything else. It
onboards you, then deletes itself, so this happens only once.

## Load on every session
1. `context/GOLDEN-RULES.md`: the constitution. Read it first; it overrides
   everything here.
2. `MEMORY.md`: what you have learned and the work in flight. Active work lives in
   `projects/` (one folder per project; see `projects/README.md`), so memory holds
   only a one-line pointer — open a project's folder only when the task needs it.
3. `context/INDEX.md`: the map of context. Load the context files a task needs
   from there (for example `context/VOICE.md` to write, `context/PROFILE.md` to
   recall who the user is), rather than loading everything every time.

## Connectors
Real tools are added through Claude Code (its connector directory). Read-only
first: add the Google Calendar connector, and `.claude/settings.json` allows only
its read tools (`list_calendars`, `list_events`, `get_event`) and denies the
write ones. Add a write later, deliberately, by moving it from deny to allow.

## Playbooks
Playbooks in `playbooks/` are saved procedures. Some run on demand (when the user
uses a trigger word), some run on a schedule (a Cadence). The list lives in
`playbooks/README.md`. Available now:
- "save" (or "save to main") -> run `playbooks/001-save-to-main.md`
- "reload" (or "rebase from main") -> run `playbooks/002-rebase-from-main.md`
- daily (scheduled) -> run `playbooks/003-daily-summary.md`: a morning calendar briefing.

## Keep memory current
When I correct you, or you learn something new, update `MEMORY.md` in place.
Replace what is outdated, do not just pile new lines on top. Memory should
always reflect the latest state.

## How we work
- If a request is ambiguous, ask before acting.
- Lead with the answer, then add the detail.
