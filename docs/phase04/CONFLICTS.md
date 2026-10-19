# Phase 04 requirement conflicts

Each conflict names the authoritative source and the resolution actually implemented. No requirement is dropped.

| # | Phase 04 prompt | Conflicting canonical source | Authoritative | Resolution |
|---|---|---|---|---|
| C1 | §7 "Horizontal split-screen" | `docs/technical/COOP_REQUIREMENTS.md`, `GAME_DESIGN.md`, `README.md`: "local vertical split-screen" | Canonical design docs for the default; the Phase 04 prompt for the capability | Both layouts supported: vertical (side-by-side) stays the default; horizontal (top/bottom) is a player setting (`Settings.split_mode`, Settings menu). P04-COOP-001 covers the option. |
| C2 | §8 "Combat reactions" animation | `STORY.md` tone and Chapter 1 mission specs: stealth; capture in M06 is an authored event, "not a failure", no combat system | Mission specifications | Hit/flinch reactions are used where the screenplay stages contact (M02 shove, M06 capture). No combat mechanic is added to Chapter 1. |
| C3 | §8 "Pull", "Climb", "Cooperative assistance" | Phase 03 research: paired/aligned two-actor animation is a documented authoring blocker (ANIM03-03) | Phase 04 prompt (must be addressed) | Implement with available retargeted clips where they read correctly (Push/Pull at handles, crouch-crawl traversal); paired contact choreography stays a recorded blocker if no licensed source exists. |
| C4 | §9 "Doors" on the bus | Screenplay CH01_M01_CS01_SH01: bus arrives (doors closed); prisoners are already inside intake when play starts | Screenplay for staging | Doors are modelled as separate leaves and open after the arrival stop in SH01; no new gameplay through the bus. |
| C5 | §6 "Players cannot fall through or become trapped" | — | Phase 04 prompt | `player.gd` recover (Y < -15) + R/Y recover input already exist; verified by regression tests and full-chapter runs. |
