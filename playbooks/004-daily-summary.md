# 004 - Daily summary

**Cadence:** Daily (scheduled). Set this up as a recurring routine in Claude Code
so it runs each morning.

A short morning briefing of your day, built from Google Calendar. Read-only.

## Tools & permissions
- Google Calendar, **read-only**: `list_calendars`, `list_events`, `get_event`.
  Calendar writes (`create_event`, `update_event`, `delete_event`) are denied in
  `.claude/settings.json` and this playbook never needs them.

## Scope
- **In:** today's events on your calendar(s), summarised in your voice.
- **Out:** any change to the calendar; other days; email or other connectors.

## Steps
1. Read today's events from Google Calendar (`list_events` for today; use
   `list_calendars` first if there is more than one calendar).
2. Summarise: how many meetings, the first and the last, and any back-to-back runs.
3. Flag what needs attention: a meeting with guests but no location or video link,
   or two events that overlap.
4. Keep it tight, a few lines, in your voice (`context/VOICE.md`).

## Rules
- Read-only: change nothing on the calendar. If something looks wrong, surface it
  in the briefing rather than acting on it.

## Output / End-of-run report
- Present the briefing in chat. For a scheduled run you can end with
  `scripts/session-token-cost.py` to record what it cost.

## Done when
- The briefing covers today's events and flags any location-less or clashing
  meetings, or says the day is clear.
