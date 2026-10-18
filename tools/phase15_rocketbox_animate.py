"""Evaluation: transfer UAL clips onto Rocketbox Biped rigs in glTF space.
Differences from the UBC transfer: bone-name map (UAL -> Bip01), and Rocketbox binds in an A-pose while UAL
rest is a T-pose, so each mapped bone gets a swing alignment A (target rest direction -> UAL rest direction):
    W_t(t) = W_ual(t) * inverse(Wrest_ual) * A * Wrest_t
Unmapped target joints (face, eyes, jaw) keep their rest local rotation. Pelvis displacement is scaled by hip height.
python -I tools/phase15_rocketbox_animate.py"""
import json, math, sys, hashlib
from pathlib import Path
R = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(R / 'tools'))
from phase15_gltf_util import read_glb, write_glb
from phase15_ubc_animate import qmul, qinv, qnorm, qrot, accessor, add_accessor, parents, rest, sample, UAL, CLIPS

SRC = R / 'asset_library/converted/phase15_characters/rocketbox'
OUT = R / 'asset_library/converted/phase15_characters/rocketbox/animated'
STEMS = ['male_adult_01', 'security_male_01', 'medical_female_01']
if len(sys.argv) > 1: STEMS = sys.argv[1:]
MAP = {'pelvis': 'Bip01 Pelvis', 'spine_01': 'Bip01 Spine', 'spine_02': 'Bip01 Spine1', 'spine_03': 'Bip01 Spine2', 'neck_01': 'Bip01 Neck', 'Head': 'Bip01 Head'}
for s, S in (('l', 'L'), ('r', 'R')):
    MAP.update({f'clavicle_{s}': f'Bip01 {S} Clavicle', f'upperarm_{s}': f'Bip01 {S} UpperArm', f'lowerarm_{s}': f'Bip01 {S} Forearm', f'hand_{s}': f'Bip01 {S} Hand',
                f'thigh_{s}': f'Bip01 {S} Thigh', f'calf_{s}': f'Bip01 {S} Calf', f'foot_{s}': f'Bip01 {S} Foot', f'ball_{s}': f'Bip01 {S} Toe0'})
    for fi, fn in enumerate(['thumb', 'index', 'middle', 'ring', 'pinky']):
        for k, suf in enumerate(['', '1', '2']):
            MAP[f'{fn}_0{k+1}_{s}'] = f'Bip01 {S} Finger{fi}{suf}'
CHILD = {'pelvis': 'spine_01', 'spine_01': 'spine_02', 'spine_02': 'spine_03', 'spine_03': 'neck_01', 'neck_01': 'Head'}
for s in 'lr':
    CHILD.update({f'clavicle_{s}': f'upperarm_{s}', f'upperarm_{s}': f'lowerarm_{s}', f'lowerarm_{s}': f'hand_{s}', f'hand_{s}': f'middle_01_{s}',
                  f'thigh_{s}': f'calf_{s}', f'calf_{s}': f'foot_{s}', f'foot_{s}': f'ball_{s}'})
    for fn in ['thumb', 'index', 'middle', 'ring', 'pinky']:
        CHILD[f'{fn}_01_{s}'] = f'{fn}_02_{s}'; CHILD[f'{fn}_02_{s}'] = f'{fn}_03_{s}'

def world_rest_full(js, par, i):
    """(rotation, uniform scale, position) of node i at rest."""
    chain = []
    while i is not None: chain.append(i); i = par.get(i)
    q, s, p = (0, 0, 0, 1), 1.0, (0.0, 0.0, 0.0)
    for k in reversed(chain):
        n = js['nodes'][k]; r, t = rest(n); sc = n.get('scale', (1, 1, 1))[0]
        p = tuple(p[j] + s * qrot(q, t)[j] for j in range(3)); q = qmul(q, r); s *= sc
    return q, s, p

def swing(a, b):
    """Shortest-arc quaternion rotating unit vector a onto b."""
    na = math.sqrt(sum(x*x for x in a)); nb = math.sqrt(sum(x*x for x in b)); a = [x/na for x in a]; b = [x/nb for x in b]
    d = sum(x*y for x, y in zip(a, b))
    if d > 0.999999: return (0, 0, 0, 1)
    c = (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])
    if d < -0.999999: return (1, 0, 0, 0)
    return qnorm((*c, 1 + d))

def transfer(tjs, tbin, ujs, ubin, clip):
    anim = next(a for a in ujs['animations'] if a['name'] == clip)
    up, tp = parents(ujs), parents(tjs)
    un = {ujs['nodes'][j]['name']: j for j in ujs['skins'][0]['joints']}
    tn = {tjs['nodes'][j]['name']: j for j in tjs['skins'][0]['joints']}
    tracks = {}
    for ch in anim['channels']:
        s = anim['samplers'][ch['sampler']]
        tracks[(ujs['nodes'][ch['target']['node']]['name'], ch['target']['path'])] = ([x[0] for x in accessor(ujs, ubin, s['input'])], accessor(ujs, ubin, s['output']))
    times = sorted({t for (nm, path), (ts, _) in tracks.items() if path == 'rotation' for t in ts})
    def depth(i, par):
        d = 0
        while i in par: i = par[i]; d += 1
        return d
    uorder = sorted(un, key=lambda n: depth(un[n], up)); torder = sorted(tn, key=lambda n: depth(tn[n], tp))
    wu_rest = {n: world_rest_full(ujs, up, un[n]) for n in un}; wt_rest = {n: world_rest_full(tjs, tp, tn[n]) for n in tn}
    inv_map = {v: k for k, v in MAP.items() if v in tn}
    align = {}
    for u, t in MAP.items():
        if t not in tn: continue
        c = CHILD.get(u)
        if c and MAP.get(c) in tn:
            du = [wu_rest[c][2][j] - wu_rest[u][2][j] for j in range(3)]; dt = [wt_rest[MAP[c]][2][j] - wt_rest[t][2][j] for j in range(3)]
            align[t] = swing(dt, du)
        else:
            align[t] = align.get(MAP.get(next((k for k, v in CHILD.items() if v == u), ''), ''), (0, 0, 0, 1))  # leaf: inherit parent's swing
    k = wt_rest['Bip01 Pelvis'][2][1] / wu_rest['pelvis'][2][1]
    out = {n: [] for n in tn}; ptr = []
    pelvis_parent = tp.get(tn['Bip01 Pelvis'])
    pq, ps, _ = world_rest_full(tjs, tp, pelvis_parent) if pelvis_parent is not None else ((0, 0, 0, 1), 1.0, (0, 0, 0))
    for t in times:
        wu, pu = {}, {}
        for n in uorder:
            i = un[n]; par = up.get(i); pn = ujs['nodes'][par]['name'] if par is not None else None
            local = sample(*tracks[(n, 'rotation')], t, True) if (n, 'rotation') in tracks else rest(ujs['nodes'][i])[0]
            loct = sample(*tracks[(n, 'translation')], t, False) if (n, 'translation') in tracks else rest(ujs['nodes'][i])[1]
            if pn in wu: pw, pp = wu[pn], pu[pn]
            elif par is not None: pw, _, pp = world_rest_full(ujs, up, par)
            else: pw, pp = (0, 0, 0, 1), (0, 0, 0)
            wu[n] = qmul(pw, local); pu[n] = tuple(pp[j] + qrot(pw, loct)[j] for j in range(3))
        wt = {}
        for n in torder:
            i = tn[n]; par = tp.get(i); pn = tjs['nodes'][par]['name'] if par is not None else None
            pw = wt[pn] if pn in wt else world_rest_full(tjs, tp, par)[0] if par is not None else (0, 0, 0, 1)
            if n in inv_map:
                u = inv_map[n]
                w = qmul(qmul(qmul(wu[u], qinv(wu_rest[u][0])), align[n]), wt_rest[n][0])
            else:
                w = qmul(pw, rest(tjs['nodes'][i])[0])
            wt[n] = w; out[n].append(qnorm(qmul(qinv(pw), w)))
        d = [(pu['pelvis'][j] - wu_rest['pelvis'][2][j]) * k for j in range(3)]
        d = qrot(qinv(pq), d); d = [x / ps for x in d]
        r0 = rest(tjs['nodes'][tn['Bip01 Pelvis']])[1]
        ptr.append(tuple(r0[j] + d[j] for j in range(3)))
    tin = add_accessor(tjs, tbin, [(x,) for x in times], 'SCALAR'); samplers, channels = [], []
    for n in tn:
        samplers.append({'input': tin, 'output': add_accessor(tjs, tbin, out[n], 'VEC4'), 'interpolation': 'LINEAR'})
        channels.append({'sampler': len(samplers) - 1, 'target': {'node': tn[n], 'path': 'rotation'}})
    samplers.append({'input': tin, 'output': add_accessor(tjs, tbin, ptr, 'VEC3'), 'interpolation': 'LINEAR'})
    channels.append({'sampler': len(samplers) - 1, 'target': {'node': tn['Bip01 Pelvis'], 'path': 'translation'}})
    tjs.setdefault('animations', []).append({'name': clip, 'samplers': samplers, 'channels': channels})
    return {'clip': clip, 'frames': len(times), 'hip_ratio': round(k, 4)}

if __name__ == '__main__':
    OUT.mkdir(parents=True, exist_ok=True); libs = {k: read_glb(v) for k, v in UAL.items()}; rep = {}
    for stem in STEMS:
        js, b = read_glb(SRC / (stem + '_rest.glb'))
        clips = [transfer(js, b, *libs[lib], c) for lib, names in CLIPS.items() for c in names]
        js['buffers'][0]['byteLength'] = len(b) + ((4 - len(b) % 4) % 4)
        p = OUT / (stem + '.glb'); write_glb(p, js, b)
        rep[stem] = {'file': str(p.relative_to(R)).replace('\\', '/'), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest(), 'clips': clips}
    old = json.loads((OUT / 'animate_report.json').read_text()) if (OUT / 'animate_report.json').exists() else {}
    old.update(rep); (OUT / 'animate_report.json').write_text(json.dumps(old, indent=1)); print({k: len(v['clips']) for k, v in rep.items()})
