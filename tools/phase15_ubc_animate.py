"""Inject Quaternius UAL clips into the UBC-based character GLBs in glTF space.

Both rigs share the 65 UAL joint names but rest rotations differ by up to ~17 degrees (neck, clavicles,
thumbs, spine_03). Clips are therefore transferred as world-space rotation deltas from the UAL rest pose:
    W_ubc(t) = W_ual(t) * inverse(Wrest_ual) * Wrest_ubc
then converted back to parent-local rotations. Translation tracks are dropped for every joint except
root/pelvis (whose rest-relative displacement is scaled by the pelvis-height ratio), so the target
character keeps its own bone lengths. Scale tracks are dropped. Run with: python -I tools/phase15_ubc_animate.py
"""
import json, math, struct, sys, hashlib
from pathlib import Path
R = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(R / 'tools'))
from phase15_gltf_util import read_glb, write_glb

SRC = R / 'asset_library/converted/phase15_characters/ubc'
OUT = R / 'assets/characters/phase15/ubc'
UAL = {1: R / 'assets/animations/phase15/UAL1_Standard.glb', 2: R / 'assets/animations/phase15/UAL2_Standard.glb'}
CLIPS = {1: ['Idle_Loop', 'Walk_Loop', 'Jog_Fwd_Loop', 'Sprint_Loop', 'Crouch_Idle_Loop', 'Crouch_Fwd_Loop', 'Jump_Start',
             'Jump_Loop', 'Jump_Land', 'Interact', 'PickUp_Table', 'Push_Loop', 'Fixing_Kneeling', 'Sitting_Enter',
             'Sitting_Idle_Loop', 'Sitting_Exit', 'Sitting_Talking_Loop', 'Idle_Talking_Loop', 'Punch_Jab', 'Punch_Cross',
             'Hit_Chest', 'Hit_Head', 'Walk_Formal_Loop', 'Roll', 'Death01'],
         2: ['ClimbUp_1m', 'Chest_Open', 'Hit_Knockback', 'Idle_FoldArms_Loop', 'Idle_No_Loop', 'Yes', 'Idle_Rail_Loop',
             'Idle_TalkingPhone_Loop', 'LayToIdle', 'Walk_Carry_Loop', 'OverhandThrow', 'Consume']}
CHARS = ['adrian_cross', 'noah_reyes', 'prison_guard', 'prisoner_npc', 'tomas_rusk', 'silas_bell', 'mara_sen']
# glTF baseColorFactor multiplies the Quaternius grey hair texture and skin texture (docs/characters appearance)
TINT = {'adrian_cross': {'hair': (0.16, 0.12, 0.09), 'skin': (1.0, 0.97, 0.95)},
        'noah_reyes': {'hair': (0.05, 0.04, 0.035), 'skin': (0.62, 0.46, 0.36)},
        'prison_guard': {'hair': (0.30, 0.24, 0.18), 'skin': (1.0, 0.95, 0.92)},
        'prisoner_npc': {'hair': (0.07, 0.06, 0.05), 'skin': (0.55, 0.40, 0.31)},
        'tomas_rusk': {'hair': (0.22, 0.17, 0.13), 'skin': (0.98, 0.88, 0.82)},
        'silas_bell': {'hair': (0.1, 0.08, 0.07), 'skin': (0.92, 0.78, 0.68)},
        'mara_sen': {'hair': (0.52, 0.52, 0.54), 'skin': (0.78, 0.60, 0.48)}}

# ---------------- quaternion helpers (x, y, z, w) ----------------
def qmul(a, b):
    ax, ay, az, aw = a; bx, by, bz, bw = b
    return (aw*bx + ax*bw + ay*bz - az*by, aw*by - ax*bz + ay*bw + az*bx, aw*bz + ax*by - ay*bx + az*bw, aw*bw - ax*bx - ay*by - az*bz)
def qinv(q): return (-q[0], -q[1], -q[2], q[3])
def qnorm(q):
    n = math.sqrt(sum(x*x for x in q)) or 1.0; return tuple(x/n for x in q)
def qrot(q, v):
    p = qmul(qmul(q, (v[0], v[1], v[2], 0.0)), qinv(q)); return p[:3]
def slerp(a, b, t):
    d = sum(x*y for x, y in zip(a, b))
    if d < 0: b = tuple(-x for x in b); d = -d
    if d > 0.9995: return qnorm(tuple(x + (y-x)*t for x, y in zip(a, b)))
    th = math.acos(d); s = math.sin(th)
    return tuple((math.sin((1-t)*th)*x + math.sin(t*th)*y)/s for x, y in zip(a, b))

COMP = {5126: ('f', 4)}
NCOMP = {'SCALAR': 1, 'VEC3': 3, 'VEC4': 4, 'MAT4': 16}
def accessor(js, bin_, i):
    a = js['accessors'][i]; bv = js['bufferViews'][a['bufferView']]
    n = NCOMP[a['type']]; off = bv.get('byteOffset', 0) + a.get('byteOffset', 0); stride = bv.get('byteStride', 4*n)
    return [struct.unpack_from('<%df' % n, bin_, off + k*stride) for k in range(a['count'])]

def add_accessor(js, bin_, rows, typ):
    while len(bin_) % 4: bin_.append(0)
    off = len(bin_); n = NCOMP[typ]
    for r in rows: bin_ += struct.pack('<%df' % n, *r)
    js['bufferViews'].append({'buffer': 0, 'byteOffset': off, 'byteLength': len(bin_) - off})
    acc = {'bufferView': len(js['bufferViews']) - 1, 'componentType': 5126, 'count': len(rows), 'type': typ}
    if typ == 'SCALAR': acc['min'] = [min(r[0] for r in rows)]; acc['max'] = [max(r[0] for r in rows)]
    js['accessors'].append(acc); return len(js['accessors']) - 1

def parents(js):
    p = {}
    for i, n in enumerate(js['nodes']):
        for c in n.get('children', []): p[c] = i
    return p

def rest(n): return tuple(n.get('rotation', (0, 0, 0, 1))), tuple(n.get('translation', (0, 0, 0)))

def world_rest(js, par, i):
    q = (0, 0, 0, 1); chain = []
    while i is not None: chain.append(i); i = par.get(i)
    for k in reversed(chain): q = qmul(q, rest(js['nodes'][k])[0])
    return q

def world_rest_pos(js, par, i):
    chain = []
    while i is not None: chain.append(i); i = par.get(i)
    q = (0, 0, 0, 1); p = (0, 0, 0)
    for k in reversed(chain):
        r, t = rest(js['nodes'][k])  # node-local units; armature-level scale applies equally to tracks
        p = tuple(p[j] + qrot(q, t)[j] for j in range(3)); q = qmul(q, r)
    return p

def sample(times, values, t, rot):
    if t <= times[0]: return values[0]
    if t >= times[-1]: return values[-1]
    lo = max(k for k in range(len(times)) if times[k] <= t); hi = min(lo + 1, len(times) - 1)
    u = 0 if times[hi] == times[lo] else (t - times[lo]) / (times[hi] - times[lo])
    return slerp(values[lo], values[hi], u) if rot else tuple(a + (b-a)*u for a, b in zip(values[lo], values[hi]))


def transfer(tjs, tbin, ujs, ubin, clip):
    anim = next(a for a in ujs['animations'] if a['name'] == clip)
    up = parents(ujs); tp = parents(tjs)
    joints = [ujs['nodes'][j]['name'] for j in ujs['skins'][0]['joints']]
    un = {ujs['nodes'][j]['name']: j for j in ujs['skins'][0]['joints']}
    tn = {tjs['nodes'][j]['name']: j for j in tjs['skins'][0]['joints']}
    tracks = {}
    for ch in anim['channels']:
        s = anim['samplers'][ch['sampler']]
        tracks[(ujs['nodes'][ch['target']['node']]['name'], ch['target']['path'])] = (
            [x[0] for x in accessor(ujs, ubin, s['input'])], accessor(ujs, ubin, s['output']))
    times = sorted({t for (nm, path), (ts, _) in tracks.items() if path == 'rotation' for t in ts})
    # topological order (parents first)
    def depth(i, par):
        d = 0
        while i in par: i = par[i]; d += 1
        return d
    order = sorted(joints, key=lambda nm: depth(un[nm], up))
    wr_u = {nm: world_rest(ujs, up, un[nm]) for nm in joints}
    wr_t = {nm: world_rest(tjs, tp, tn[nm]) for nm in joints}
    ratio = world_rest_pos(tjs, tp, tn['pelvis'])[1] / world_rest_pos(ujs, up, un['pelvis'])[1]
    out_rot = {nm: [] for nm in joints}; out_tr = {'root': [], 'pelvis': []}
    for t in times:
        wu = {}; wt = {}
        for nm in order:
            i = un[nm]; pu = up.get(i)
            local = sample(*tracks[(nm, 'rotation')], t, True) if (nm, 'rotation') in tracks else rest(ujs['nodes'][i])[0]
            parent_w = wu.get(ujs['nodes'][pu]['name']) if pu is not None and ujs['nodes'][pu]['name'] in wu else world_rest(ujs, up, pu) if pu is not None else (0, 0, 0, 1)
            wu[nm] = qmul(parent_w, local)
            target_w = qmul(qmul(wu[nm], qinv(wr_u[nm])), wr_t[nm])
            pt = tp.get(tn[nm])
            tparent_w = wt.get(tjs['nodes'][pt]['name']) if pt is not None and tjs['nodes'][pt]['name'] in wt else world_rest(tjs, tp, pt) if pt is not None else (0, 0, 0, 1)
            wt[nm] = target_w
            out_rot[nm].append(qnorm(qmul(qinv(tparent_w), target_w)))
        for nm in ('root', 'pelvis'):
            ur, ut = rest(ujs['nodes'][un[nm]]); _, tt = rest(tjs['nodes'][tn[nm]])
            cur = sample(*tracks[(nm, 'translation')], t, False) if (nm, 'translation') in tracks else ut
            d = tuple((cur[j] - ut[j]) * ratio for j in range(3))
            # express displacement in the target parent's rest frame
            pu, pt = up.get(un[nm]), tp.get(tn[nm])
            d = qrot(qmul(qinv(world_rest(tjs, tp, pt)), world_rest(ujs, up, pu)), d)
            out_tr[nm].append(tuple(tt[j] + d[j] for j in range(3)))
    tin = add_accessor(tjs, tbin, [(x,) for x in times], 'SCALAR')
    samplers = []; channels = []
    for nm in joints:
        samplers.append({'input': tin, 'output': add_accessor(tjs, tbin, out_rot[nm], 'VEC4'), 'interpolation': 'LINEAR'})
        channels.append({'sampler': len(samplers)-1, 'target': {'node': tn[nm], 'path': 'rotation'}})
    for nm, rows in out_tr.items():
        samplers.append({'input': tin, 'output': add_accessor(tjs, tbin, rows, 'VEC3'), 'interpolation': 'LINEAR'})
        channels.append({'sampler': len(samplers)-1, 'target': {'node': tn[nm], 'path': 'translation'}})
    tjs.setdefault('animations', []).append({'name': clip, 'samplers': samplers, 'channels': channels})
    return {'clip': clip, 'frames': len(times), 'duration_s': round(times[-1] - times[0], 4), 'pelvis_ratio': round(ratio, 4)}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    libs = {k: read_glb(v) for k, v in UAL.items()}
    report = {}
    for stem in CHARS:
        js, b = read_glb(SRC / (stem + '_rest.glb'))
        assert {js['nodes'][j]['name'] for j in js['skins'][0]['joints']} == {libs[1][0]['nodes'][j]['name'] for j in libs[1][0]['skins'][0]['joints']}
        clips = [transfer(js, b, *libs[lib], c) for lib, names in CLIPS.items() for c in names]
        js['buffers'][0]['byteLength'] = len(b) + ((4 - len(b) % 4) % 4)
        for m in js['materials']:
            key = 'hair' if m['name'].startswith('MI_Hair') else 'skin' if m['name'].lower().startswith('mi_superhero') else None
            if key: m.setdefault('pbrMetallicRoughness', {})['baseColorFactor'] = [*TINT[stem][key], 1.0]
        js.setdefault('asset', {})['extras'] = {'phase15': 'UBC CC0 body + original uniform shell; UAL CC0 clips via world-delta transfer'}
        out = OUT / (stem + '.glb'); write_glb(out, js, b)
        report[stem] = {'file': str(out.relative_to(R)).replace('\\', '/'), 'sha256': hashlib.sha256(out.read_bytes()).hexdigest(), 'clips': clips}
    (SRC / 'animate_report.json').write_text(json.dumps(report, indent=2))
    print(json.dumps({k: (v['file'], len(v['clips'])) for k, v in report.items()}))

if __name__ == '__main__':
    main()
