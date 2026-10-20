"""Copy every animation of an animated GLB onto a rest-pose GLB of the same rig (glTF level, nodes matched by name).

Used after a Blender garment/hair rebuild of a character (tools/phase05_adrian_garment.py): Blender exports the new
mesh at rest; the 37 clips are copied byte-for-byte from the previous shipped GLB. Refuses to run unless every
animated node exists in the target and its rest TRS matches the source (so local-space keys mean the same pose).
python -I tools/phase05_copy_clips.py <animated_src.glb> <rest_target.glb> <out.glb>
"""
import json, sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from phase15_gltf_util import read_glb, write_glb

COMP = {5126: 4, 5123: 2, 5121: 1, 5125: 4, 5122: 2, 5120: 1}
NCOMP = {'SCALAR': 1, 'VEC2': 2, 'VEC3': 3, 'VEC4': 4, 'MAT4': 16}


def acc_bytes(js, bin_, ai):
    a = js['accessors'][ai]
    bv = js['bufferViews'][a['bufferView']]
    size = COMP[a['componentType']] * NCOMP[a['type']]
    stride = bv.get('byteStride', size)
    start = bv.get('byteOffset', 0) + a.get('byteOffset', 0)
    if stride == size:
        return bytes(bin_[start:start + size * a['count']])
    return b''.join(bytes(bin_[start + i * stride:start + i * stride + size]) for i in range(a['count']))


def trs(n):
    return (tuple(n.get('translation', (0, 0, 0))), tuple(n.get('rotation', (0, 0, 0, 1))), tuple(n.get('scale', (1, 1, 1))))


def main(src, dst, out):
    sjs, sbin = read_glb(src)
    tjs, tbin = read_glb(dst)
    tname = {n.get('name'): i for i, n in enumerate(tjs['nodes'])}
    worst = 0.0
    for anim in sjs.get('animations', []):
        for ch in anim['channels']:
            sn = sjs['nodes'][ch['target']['node']]
            if sn.get('name') not in tname:
                raise SystemExit('target lacks animated node %r' % sn.get('name'))
            tn = tjs['nodes'][tname[sn['name']]]
            for a, b in zip(trs(sn), trs(tn)):
                d = max(abs(x - y) for x, y in zip(a, b))
                # quaternion sign ambiguity
                if len(a) == 4:
                    d = min(d, max(abs(x + y) for x, y in zip(a, b)))
                worst = max(worst, d)
    if worst > 1e-3:
        raise SystemExit('rest TRS differs between source and target by %g' % worst)
    tjs['animations'] = []
    tjs.setdefault('accessors', [])
    tjs.setdefault('bufferViews', [])
    cache = {}

    def copy_acc(ai):
        if ai in cache:
            return cache[ai]
        a = dict(sjs['accessors'][ai])
        data = acc_bytes(sjs, sbin, ai)
        while len(tbin) % 4:
            tbin.append(0)
        tjs['bufferViews'].append({'buffer': 0, 'byteOffset': len(tbin), 'byteLength': len(data)})
        tbin.extend(data)
        a['bufferView'] = len(tjs['bufferViews']) - 1
        a.pop('byteOffset', None)
        tjs['accessors'].append(a)
        cache[ai] = len(tjs['accessors']) - 1
        return cache[ai]

    for anim in sjs.get('animations', []):
        na = {'name': anim.get('name'), 'samplers': [], 'channels': []}
        for s in anim['samplers']:
            na['samplers'].append({'input': copy_acc(s['input']), 'output': copy_acc(s['output']),
                                   'interpolation': s.get('interpolation', 'LINEAR')})
        for ch in anim['channels']:
            na['channels'].append({'sampler': ch['sampler'],
                                   'target': {'node': tname[sjs['nodes'][ch['target']['node']]['name']], 'path': ch['target']['path']}})
        tjs['animations'].append(na)
    tjs['buffers'][0]['byteLength'] = len(tbin) + (-len(tbin)) % 4
    write_glb(out, tjs, tbin)
    print('COPY_CLIPS', json.dumps({'clips': len(tjs['animations']), 'rest_trs_max_dev': worst, 'out': str(out)}))


if __name__ == '__main__':
    main(*sys.argv[1:4])
