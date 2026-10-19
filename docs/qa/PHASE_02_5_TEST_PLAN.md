# Phase 02.5 reproducible test plan

19 October 2026. Run one Godot job at a time. Use dedicated `--save-slot=phase025_*` arguments. Preserve existing user saves and prior evidence. Automated state coverage, graphical inspection and physical-controller acceptance are separate gates.

## Automated regression

Engine: `C:/Program Files (x86)/Steam/steamapps/common/Godot Engine/godot.windows.opt.tools.64.exe`; launch from project root. The Steam launcher can return before the real engine exits; require final JSON/log markers and inspect the actual process.

```powershell
$G = 'C:\Program Files (x86)\Steam\steamapps\common\Godot Engine\godot.windows.opt.tools.64.exe'
python -I tools/phase02_export_data.py --check
python -I tests/phase02/test_completion_audit.py
& $G --headless --path . --fixed-fps 60 res://tests/phase025/gameplay_regressions.tscn
& $G --headless --path . res://tests/phase025/save_validation.tscn
& $G --headless --path . --fixed-fps 60 res://tests/phase02/run_tests.tscn -- --save-slot=phase025_final_suite
& $G --headless --path . --fixed-fps 60 res://tests/phase025/checkpoint_regressions.tscn -- --save-slot=phase025_checkpoint_suite
& $G --path . --resolution 1280x720 res://tests/phase025/movement_visual.tscn
```

Assertions: canonical145 lines/36 shots/19 objectives/six missions; state and save idempotence; independent routed inputs; player collisions and speed; headroom-aware crouch; jump/landing; recovery after traversal; wall-safe spring-arm and cinematic return; guard occlusion and selected solo gates. Checkpoint test drives a fresh chapter using routed input, reads actual disk saves and reconstructs all12 ordinary checkpoints. It does not complete gameplay after every restored save.

## Full graphical regression

```powershell
& $G --path . --resolution 1280x720 --log-file tests/phase025/evidence/full_normal_gfx.log -- --autopilot --new --save-slot=phase025_normal_gfx --report=tests/phase025/evidence/full_normal_gfx.json --shots=tests/phase025/evidence/shots_full_normal --timeout=4000
```

Require reason `chapter_complete`, all six mission completions,19 distinct objective completions,36 shot activations and a readable rendered end card. Inspect captured gameplay, faces, animation motion, cameras, subtitles and contacts while running. Do not infer art acceptance from event counts. No speed multiplier. Real wall-frame cadence includes screenshot readback/loading; desktop activity is uncontrolled. This is a synthetic driver with access to internal enabled items/navigation, not a human usability test.

## Interactive menu and controls

1. Launch with no `--new`/`--autopilot`. Activate New Game using the visible button. Verify the normal menu path, both spawned humans and both ready prompts. Confirm separately with E/O or each controller's A.
2. P1 keyboard/mouse: WASD; E interact; Alt jog; Shift sprint; Space jump; C crouch; R recover; X skip; Esc pause. P2 fallback: IJKL; arrows look; O interact; U jog; H sprint; M jump; N crouch; Y recover; B skip; P pause.
3. Controller: left/right sticks; A interact; LB jog; L3/RT sprint; X jump; B crouch; Y recover; Back skip; Start pause. Test keyboard+controller, then two different controllers. Move and look with each device while the other player stays still; reject any cross-control.
4. Walk into a wall, move diagonally, jump/land, crouch under clearance and attempt to stand. Reject floating feet, T-pose, severe sliding, collision penetration or abrupt broken skeletons. Check narrow walls and camera return after every cinematic. Confirm crouched head-height framing.
5. Pause from either device. Resume, open settings/devices, restart checkpoint and return to main menu. Disconnect each controller and check controlled pause/reassignment. Test both controls and menus at1280×720 and1920×1080.
6. Continue from a valid save. Test a copied corrupt/incompatible save in a dedicated slot: Continue must be unavailable without crashing. Never corrupt the user's normal slot.

## Authored mission and negative checks

| Mission | Required normal sequence | Negative/retry checks |
|---|---|---|
| New Blood | Parallel property/badge observations, receipt acknowledgment, Rusk escort, adjacent cell inspections, pipe exchange and final receipt cinematic | One ready vote cannot progress; wrong actor cannot use partner-only item; falling behind causes escort wait and recovery |
| Trouble in the Yard | Confrontation, Adrian mediation hold, Noah's ball distraction, joint alcove exchange/work call | Solo intervention/distraction cannot satisfy partner gate; early hold release and missed distraction recover |
| The Workshop | Isolation lever held while screen cleared; Noah holds lamp while Adrian reads; restore machine state, obtain shim and hand off information | Wrong actor denied; early release resets progress; no moving-machine entry or mission completion shortcut |
| Lights Out | Shim/panel work, scripted chase traversal, partner brace, hatch/flush actions, patrol-gap stealth route | Guard line of sight accumulates detection, cover occludes it; detection restores checkpoint; traversal restart/recovery restores body collision |
| Behind the Walls | Separate catwalk/floor routes, handset exchange, brake held while selector B/power activates grille, reunion and evidence | Wrong selector trips breaker; early brake release cannot open grille; solo actor cannot finish both routes; phone/hand and machine contacts reviewed visually |
| The Betrayal | Simultaneous handles, ambush/capture, separated solitary scenes and ordered pipe replies, ending card | One handle cannot finish; one pipe response cannot skip partner reply; continue from completed save gives ending; return-to-menu button works |

For all12 ordinary checkpoints also continue through the next meaningful interaction after restore, verify objective text, inventory and patrol state, then repeat in exported build. Initial reconstruction-only evidence does not close this manual continuation checklist.

## Visual and build acceptance

- Compare five valid same-camera environment pairs in `tests/phase025/evidence/{before_valid,after_valid}` using `comparison_manifest.json`. The older `before/after` sets are failed harness evidence and invalid.
- Review each visible asset against the visual audit classifications and source/license records. Downloaded bulk assets are outside runtime and cannot count as integrated graphics.
- Review all36 shots in motion, subtitle timing, gameplay unlock, facial performance and hand/partner/prop contact. Generic substitute clips do not close bespoke performance requirements.
- Export a fresh Windows executable with the Windows Desktop preset, retain previous build, record binary/source hashes, then test launch/menu/New Game and the full input-driven chain on that exact binary. Test physical two-controller completion separately.
- A failed mandatory visual, hardware, executable or progression gate keeps Phase02.5 **INCOMPLETE**. Repair each defect up to five attempts; preserve failed evidence and record blockers.
