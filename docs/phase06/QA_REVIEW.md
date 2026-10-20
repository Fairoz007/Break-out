# Phase 06 independent QA review

Reviewer: an independent read-only QA sub-agent (separate context; told not to trust the reports and to verify files,
code and evidence), 20 October 2026, reviewing commit `4884b8d`.

**Verdict: APPROVED_WITH_CONDITIONS** for the Phase 06 audio work as it stands in the Linux session. Not a release
approval: the Windows exe was not run, the 14 pending cues are not generated, and no human has listened.

## Conditions and what was done

| # | Sev | Finding | Action (after review) |
|---|---|---|---|
| 1 | **S1** | Both ElevenLabs keys are in git history (commit `be68b4a`) of a **public** repository → scrapable now | Cannot be fixed in code: **owner must rotate/revoke both keys**. D06-001 raised to S1. History rewrite optional after rotation |
| 2 | S3 | Ducking not restored when quitting to the menu mid-line | Fixed: `DialogueDirector._exit_tree()` un-ducks |
| 3 | S3 | Music would keep playing in the main menu | Fixed: `main.gd` `_show_menu()` fades music out |
| 4 | S3 | Scene one-shots fire under the pause menu; they are 2D, not positional | Fixed: spot timer is pausable. Docs corrected ("non-positional") |
| 5 | S4 | Asphalt footsteps never played (court overlay has no collider) | Fixed: surface zones (`surface_zone` group); runs now log 156 asphalt steps |
| 6 | S4 | Same cue twice in one moment (two cell doors, detection per player) | Fixed: a cue repeated within 120 ms plays once |
| 7 | S4 | Radio bed fed the Dialogue analyser (jaws moved with radio) and the Voice slider | Fixed: Radio sends to Ambience |
| 8 | S4 | Phantom landing step when an action ended in the air | Fixed: passes the real grounded state |
| 9 | S4 | Manifest gaps: 60 empty `trigger_code` cells; footstep rows used a pattern; legacy `footstep` cue not reported | Footstep rows list real files; audit reports `footstep`; `trigger_code` gaps remain (runtime column is the trigger evidence) |
| 10 | S4 | Godot imported docs CSVs as translations (26 generated files committed) | Fixed: `docs/.gdignore`, generated files removed |
| 11 | S4 | Wording beyond evidence ("playing" with the dummy driver; parse 72/72; missing QA_REVIEW.md) | Fixed: "take loaded and its player started", 73/73, this file |
| 12 | S4 | One exported-run report predated the final export | Re-exported and re-ran after the fixes (SESSION_STATE) |

## Claims the reviewer confirmed

145 takes decode, SHA-256 match the manifest, text equals the screenplay, one distinct voice per speaker; chapter
runs reach `chapter_complete` with 0 script errors and cover 145/145 IDs; no key in tracked files or in either
exported binary; `.secrets/` ignored and export-excluded; manifests match disk; the 14 pending cues are absent and
hooked; audit reproducible; regressions as reported; docs honest about human review, the exe, assets and limits.
