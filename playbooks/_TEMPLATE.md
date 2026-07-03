# NNN - <Playbook name>

**Cadence:** On-demand (say "<trigger>") — *or* — Scheduled (e.g. daily; set it up
as a recurring routine in Claude Code). Pick one and delete the other.

<One line: what this playbook is for.>

## Tools & permissions
- <which tools / connectors it uses, at what tier — read-only unless a write is
  explicitly allowed in `.claude/settings.json`>.

## Scope
- **In:** <what it covers>.
- **Out:** <what it deliberately does not touch>.

## Steps
1. <step>
2. <step>

## Rules
- <constraints — e.g. read-only, never send, ask before acting if unsure>.

## Output / End-of-run report
- <what it produces, and where it goes>.
- For a scheduled run you can end with `scripts/session-token-cost.py` to record
  what it cost.

## Done when
- <the definition of done — the check that says this run is complete>.
