"""Generate original code-native UI/VFX art resources, no gameplay behavior."""
from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[1]
U=R/'assets/ui/phase15';V=R/'assets/vfx/phase15';L=R/'asset_library/licenses/phase15_ui';M=R/'asset_library/manifests'
icons={
'player_one':'<circle cx="16" cy="10" r="5"/><path d="M6 28v-5a10 10 0 0120 0v5"/><path d="M16 18v8"/>',
'player_two':'<circle cx="16" cy="10" r="5"/><path d="M6 28v-5a10 10 0 0120 0v5"/><path d="M12 19v7m8-7v7"/>',
'interact':'<circle cx="16" cy="16" r="12"/><path d="M10 16h12m-6-6v12"/>',
'hold':'<path d="M10 27V14a2 2 0 014 0v5V7a2 2 0 014 0v12V11a2 2 0 014 0v10a7 7 0 01-7 7z"/>',
'partner_wait':'<circle cx="16" cy="16" r="12"/><path d="M12 10v12m8-12v12"/>',
'objective':'<path d="M8 28V4l18 3-18 9"/>',
'checkpoint':'<path d="M5 16l7 7L27 8"/>',
'retry':'<path d="M6 12a11 11 0 112 13M6 4v9h9"/>',
'sound':'<path d="M4 12h5l7-6v20l-7-6H4zM21 10a9 9 0 010 12m4-16a14 14 0 010 20"/>',
'alarm':'<path d="M7 24h18l-3-4V12a6 6 0 00-12 0v8zM13 28h6M16 2v2"/>',
'crouch':'<circle cx="20" cy="6" r="3"/><path d="M18 11l-5 7 8 3-3 8M13 18l-8 6m12-11h10"/>',
'climb':'<path d="M7 3v26M25 3v26M7 8h18M7 16h18M7 24h18"/>',
}
records=[]
def record(aid,name,path,license='Project original',source=None,category='ui'):
    p=R/path
    records.append(dict(asset_id=aid,asset_name=name,category=category,source_url=source,creator='Project original' if not source else 'Noto contributors',license=license,license_file='asset_library/licenses/phase15_ui/ORIGINAL_ASSETS.md' if not source else 'asset_library/licenses/phase15_ui/NotoSans_OFL.txt',attribution_required=False,original_file=path,original_checksum=hashlib.sha256(p.read_bytes()).hexdigest(),runtime_file=path,format=p.suffix[1:],polygon_count_if_known=None,texture_resolution_if_known=None,skeleton_type_if_applicable=None,animation_compatibility='static resource; no gameplay',required_by_scene=['CH01_M%02d_SC01'%i for i in range(1,7)],download_status='CREATED' if not source else 'DOWNLOADED',import_status='NOT TESTED',validation_status='PARTIALLY_VERIFIED',notes='Generated original asset. Engine loading and visual QA pending.' if not source else 'Unmodified font; distribute OFL license. Engine loading and half-screen preview pending.',priority='IMPORTANT'))
for name,content in icons.items():
    p=U/f'{name}.svg'
    p.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 32 32"><g fill="none" stroke="#f1eadb" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{content}</g></svg>')
    record('UI15_'+name.upper(),name,p.relative_to(R).as_posix())
(U/'subtitle_panel.tres').write_text('''[gd_resource type="StyleBoxFlat" format=3]
[resource]
bg_color = Color(0.025, 0.03, 0.035, 0.93)
border_width_left = 3
border_color = Color(0.85, 0.64, 0.3, 1)
content_margin_left = 18.0
content_margin_right = 18.0
content_margin_top = 10.0
content_margin_bottom = 10.0
corner_radius_top_left = 3
corner_radius_top_right = 3
corner_radius_bottom_left = 3
corner_radius_bottom_right = 3
''')
record('UI15_SUBTITLE_PANEL','Subtitle background style','assets/ui/phase15/subtitle_panel.tres')
record('UI15_NOTO_SANS','Noto Sans variable font','assets/ui/phase15/noto_sans_variable.ttf','OFL-1.1','https://github.com/google/fonts/tree/main/ofl/notosans')
(V/'alarm_emissive.tres').write_text('''[gd_resource type="StandardMaterial3D" format=3]
[resource]
albedo_color = Color(0.55, 0.015, 0.008, 1)
roughness = 0.35
emission_enabled = true
emission = Color(1, 0.03, 0.01, 1)
emission_energy_multiplier = 2.0
''')
record('VFX15_ALARM_MATERIAL','Steady red alarm lens material','assets/vfx/phase15/alarm_emissive.tres',category='vfx')
(V/'dust_process.tres').write_text('''[gd_resource type="ParticleProcessMaterial" format=3]
[resource]
emission_shape = 3
emission_box_extents = Vector3(1, 0.6, 1)
direction = Vector3(0, 1, 0)
spread = 70.0
initial_velocity_min = 0.015
initial_velocity_max = 0.05
gravity = Vector3(0, 0.008, 0)
scale_min = 0.002
scale_max = 0.008
color = Color(0.6, 0.56, 0.48, 0.18)
''')
record('VFX15_DUST_PROCESS','Low velocity dust particle settings','assets/vfx/phase15/dust_process.tres',category='vfx')
photo='assets/textures/phase15_story/elena_harbor_photo.png'
record('TEX15_ELENA_PHOTO','Elena fictional pre-disappearance photograph',photo,'AI generated project asset',category='texture')
records[-1]['original_file']='asset_library/original_downloads/phase15_story/elena_harbor_photo.png'
records[-1]['notes']='Built-in imagegen; original fictional adult. Visually inspected, 1536x1024. Source prompt in license record. No third-party stock license asserted.'
(L/'ORIGINAL_ASSETS.md').write_text('''# Phase 01.5 project-original resources

The 12 SVG icons, subtitle style and two VFX material resources were authored for BREAKOUT: NO WAY BACK. They contain no external image/font code. These are project-owned source deliverables, no external attribution required. Noto Sans is separate, unmodified, and distributed under included OFL-1.1.

Elena photograph: created using the built-in imagegen tool on 18 October 2026, original fictional adult, no reference image. Not a downloaded stock photograph; no CC0 assertion. Original PNG retained under original_downloads/phase15_story. Generated output is supplied as project art under the user's applicable image-generation terms.

Prompt: Create one photorealistic snapshot texture for fictional thriller BREAKOUT NO WAY BACK: ordinary candid waist-up family photograph of Elena Reyes, fictional 30-year-old Latina signals engineer, warm brown skin, dark hair loosely tied back, practical muted blue work shirt, gently amused at camera by coastal harbor, BEFORE disappearance. Natural unretouched everyday face, subtle analog grain, overcast sea background blurred. Flat landscape3:2 image, no borders/hands/text/logos/wounds/poster/recognizable celebrity.

Tool: built-in imagegen. Final project texture: assets/textures/phase15_story/elena_harbor_photo.png. This does not establish a production 3D character likeness.
''')
(M/'phase15_ui_records.json').write_text(json.dumps(records,indent=2))
print(len(records),'UI/VFX/story resources authored/acquired')
