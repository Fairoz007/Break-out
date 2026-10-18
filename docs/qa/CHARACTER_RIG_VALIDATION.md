# Character rig validation — Phase 01.5

Date: 18 October 2026 (resumed session). **Functional readiness: PASS. Realistic production readiness: PARTIAL.**

The severe deformation found earlier is resolved. It was not repaired on the old base: that base was replaced after an evaluation. Two working character sets now exist, and both were validated in Blender 5.1.1 and Godot 4.7.2:

| Set | Runtime folder | Characters | Quality tier | Status |
|---|---|---|---|---|
| Microsoft Rocketbox (MIT) | `assets/characters/phase15/rocketbox/` | Adrian, Noah, Rusk (also the guard), Mara, Silas, inmate | Realistic (scanned-quality faces, textured clothing, hair cards) | `PARTIALLY_VERIFIED`, quality tier `REALISTIC_CANDIDATE`, not production ready |
| Quaternius Universal Base Characters (CC0) | `assets/characters/phase15/ubc/` | Adrian, Noah, Rusk, Mara, Silas, guard, inmate | Stylised muscular base with skin-tight shell garments | `FUNCTIONAL_PROXY`, never closes a realistic requirement |
| MPFB retarget (earlier session) | `assets/characters/phase15/*.glb` | 4 | — | `FAILED`, kept for diagnosis |
| MPFB native proxies (earlier session) | `assets/characters/phase15/*_native_proxy.glb` | 2 | — | `SUPERSEDED` |

## Root cause of the earlier deformation

There were five MPFB repair cycles. All of them retargeted UAL clips onto a different skeleton inside Blender, where the bone-axis heuristics and rest-pose differences compound. The base was **fundamentally unsuitable for that pipeline**, so it was not repaired a sixth time. The replacement path was:

1. **Native skeleton (UBC).** The Universal Base Characters kit was already downloaded but had never been evaluated. It shares all 65 joint names with UAL1/UAL2, but its rest rotations differ by up to 17° (neck, clavicles, thumbs, spine_03). The clips are transferred **in glTF space**, which is the same semantics Godot uses: world-space rotation deltas from the UAL rest, `W_t(t) = W_ual(t)·inv(Wrest_ual)·Wrest_t`. The character keeps its own bone lengths, and only the root and pelvis displacement is transferred, scaled by hip height. ([`tools/phase15_ubc_animate.py`](../../tools/phase15_ubc_animate.py))
2. **Realistic rig (Rocketbox Biped, 80 joints).** Uses the same method plus a UAL→`Bip01` bone map and a per-bone swing alignment, because Rocketbox binds in an A-pose and UAL in a T-pose. Without the alignment the arms would be offset by about 45°. Face, jaw and eye joints keep their rest pose. ([`tools/phase15_rocketbox_animate.py`](../../tools/phase15_rocketbox_animate.py))

## Clothing

- **Rocketbox:** the avatars already wear fitted, textured clothing. Prison uniforms are original texture derivatives. [`phase15_rocketbox_recolor.py`](../../tools/phase15_rocketbox_recolor.py) rasterises the top, trouser and foot regions in UV space from each face's dominant skin weight. It keeps exposed skin with a chromaticity test, flattens printed patterns, keeps fold and seam luminance, and recolours trouser hems inside the foot region. Fixed by the repair loop: UV-padding fringes, denim cuffs left blue, and khaki cuffs left untouched. The guard (Security_Male_01) and medical (Medical_Female_01) clothing is unmodified.
- **UBC:** the uniform shell is generated from the body surface with its **skin weights copied verbatim**, offset 9 mm (boots 16 mm, relaxed and pinned at the hem). Body faces fully hidden under the garments are removed. Three repair cycles fixed the material slots (clearing the slots had reset polygon indices), the hair/skin tint, and an ankle gap.

## Evidence

| Check | Result | Evidence |
|---|---|---|
| Export → reload in a fresh Blender scene | PASS, 13/13 | `tools/phase15_ubc_render.py`, `tools/phase15_rocketbox_render.py`; `asset_library/manifests/phase15_characters_previews/ubc/`, `…/rocketbox_eval/` |
| Neutral (rest) pose | PASS: UBC T-pose, Rocketbox A-pose bind; transferred clips start from the UAL rest | `*__REST_00_*.png` |
| Walk, run (jog), sprint, crouch idle/walk, jump, interaction, push, climb renders, front and side | PASS: intact limbs, shoulders, elbows and knees; garments visible; no observed clipping at preview scale | contact sheets `sheet_<char>_{front,side}.png` (viewed for every character) |
| All 37 clips at mid-clip | PASS on UBC Adrian and Rocketbox Adrian | `…/all_clips/{ubc_adrian,rocketbox_adrian}/sheet_all_clips.png` |
| Face close-ups | Rocketbox: realistic faces, eyes and hair cards render. UBC: stylised | `…/rocketbox_eval/heads/heads_sheet.png` |
| Godot 4.7.2 import | PASS, 13/13: 0 errors on stderr | `asset_library/manifests/phase15/godot_import_final3_*.log` |
| Godot skeleton, skin, materials | PASS: Rocketbox 80 bones, UBC 65; every mesh skinned to its skeleton; 0 null materials | `…/godot/godot_character_report.json` |
| Godot animation playback (gl_compatibility renderer, real GPU) | PASS: 37 clips per character; 17 flagged looping (Godot strips the `_Loop` suffix on import); 14 poses × 2 views rendered and inspected | `…/godot/gsheet_*.png` |
| Scale | PASS: Adrian 1.84 m, Noah 1.78 m, Rusk 1.83 m, Mara 1.67 m, Silas 1.80 m, inmate 1.79 m; the guard is 1.82 m (UBC only) | `convert_report.json`, `build_report.json` |
| Asset inspection scene | Characters stand at the correct floor level beside the modules (placed by their foot-level origin) | `asset_library/manifests/phase15/inspection/zoneD_characters_*.png` |

## Remaining limits (why production is PARTIAL)

- **Facial animation:** Rocketbox `_facial.fbx` files with 176 blendshapes are preserved, but the runtime GLBs were converted from the non-facial FBX. Lip-sync and facial performance are not available yet.
- **Materials:** specular maps were replaced by a constant roughness of 0.62. There is no calibrated PBR conversion.
- **Likeness** has not been approved by art direction:
  - Mara's avatar is younger and dark-haired (the brief says 46 with silver-streaked hair).
  - Rusk is of average build, not heavy.
  - Noah's skin is darker than "warm brown" and his hair is not wavy.
  - Adrian's overshirt is a recoloured sweater, not a layered garment.
  - Scars, burns and the chipped incisor are not authored.
- **Crowd variety:** there is one realistic guard identity, shared by Rusk and the guards, and two inmate identities.
- **Not tested:** foot sliding, root motion, blend transitions, contacts against real geometry, and close-up lighting in Godot.
- **Licensing:** Rocketbox is MIT. The licence notice must ship with the game (`asset_library/licenses/phase15_discovery/microsoft_rocketbox/LICENSE.md`).

## Reproduce

```powershell
$B = "C:\Program Files\Blender Foundation\Blender 5.1\blender.exe"
& $B -b --factory-startup --python tools/phase15_ubc_build.py ; python -I tools/phase15_ubc_animate.py
& $B -b --factory-startup --python tools/phase15_rocketbox_convert.py ; python -I tools/phase15_rocketbox_animate.py rb_adrian_cross rb_noah_reyes rb_prisoner_npc rb_silas_bell rb_tomas_rusk rb_mara_sen
python -I tools/phase15_rocketbox_records.py ; python -I tools/phase15_ubc_records.py
& $B -b --factory-startup --python tools/phase15_rocketbox_render.py ; & $B -b --factory-startup --python tools/phase15_ubc_render.py
```

Recolour inputs (`uvdump.json`, `spec.json`) are under `asset_library/converted/phase15_characters/rocketbox/recolor/<avatar>/`, and the avatar config is in `…/rocketbox/avatars.json`. Godot checks are listed in the [validation report](../assets/ASSET_VALIDATION_REPORT.md).

## History (earlier session, preserved)

MPFB 2.0.18 human derivatives with original shirt, trouser and boot geometry went through five repair cycles: world-rest compensation, local-rotation transfer, hierarchy-ordered compensation, and a native sine-walk proxy. They failed visual acceptance with collapsed upper arms, clothing occluded by the body, and a rigid A-pose. Those files and the `prison_humanoid_*.blend` sources remain for diagnosis, marked `FAILED` or `SUPERSEDED` in the manifest. Two unreferenced intermediate builds (`guard_base.glb`, `inmate_base.glb`) were moved, not deleted, to `asset_library/rejected/phase15_characters/`.
