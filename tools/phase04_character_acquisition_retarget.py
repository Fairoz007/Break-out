from pathlib import Path
R=Path.cwd()
s=(R/'tools/mixamo_20261019_retarget_trial.py').read_text()
s=s.replace('align[n]), wt_rest[n][0])','(0, 0, 0, 1)), wt_rest[n][0])')
# Replacement must act on inspected transfer code, not wrapper string.
s=s.replace('namespace=dict(rocket.__dict__);','transfer_code=transfer_code.replace("align[n]", "(0, 0, 0, 1)")\nnamespace=dict(rocket.__dict__);')
s=s.replace("OUT=SRC/'retarget_trials'", "OUT=R/'assets/characters/phase04_realistic/evaluation'")
s=s.replace("M=R/'asset_library/manifests/mixamo_20261019'", "M=OUT")
exec(compile(s,str(R/'tools/phase04_character_acquisition_retarget.py'),'exec'))
