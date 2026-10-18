"""Minimal GLB/glTF reader-writer helpers (no third-party deps)."""
import json,struct
from pathlib import Path
def read_glb(p):
    b=Path(p).read_bytes();assert b[:4]==b'glTF'
    o=12;js=None;bin_=b''
    while o<len(b):
        ln,t=struct.unpack_from('<II',b,o);c=b[o+8:o+8+ln];o+=8+ln
        if t==0x4E4F534A:js=json.loads(c)
        elif t==0x004E4942:bin_=c
    return js,bytearray(bin_)
def write_glb(p,js,bin_):
    j=json.dumps(js,separators=(',',':')).encode();j+=b' '*((4-len(j)%4)%4)
    bin_=bytes(bin_)+b'\0'*((4-len(bin_)%4)%4)
    out=b'glTF'+struct.pack('<II',2,12+8+len(j)+8+len(bin_))+struct.pack('<II',len(j),0x4E4F534A)+j+struct.pack('<II',len(bin_),0x004E4942)+bin_
    Path(p).write_bytes(out)
