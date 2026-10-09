"""Check a merged PipeCAD .pl against its source files.

Usage:  python3 tools/verify_merge.py merged.pl source1.pl source2.pl ...   (sources in the order they were merged)

Compares every header block, floor and saved result in the merged file with its source, field by field, after
undoing the per-file ID / layerTag offset. Prints any difference other than renamed floors and detectors, checks
that all IDs are unique, and that every results reference points at the same kind of object as in the source.
"PROBLEMS 0" means the design and saved results are unchanged.
"""
import sys, xml.etree.ElementTree as ET
REF={'pipeIds','holeIds','ancillaryIds','pipeDatabase1','pipeDatabase2','holeDatabase1','holeDatabase2'}
m=ET.parse(sys.argv[1]).getroot(); srcs=[ET.parse(f).getroot() for f in sys.argv[2:]]
def idels(r):
    out=[]
    for p in r.iter():
        for c in p:
            if len(c)==0 and (c.tag in('id','detectorId') or (c.tag=='int' and p.tag in REF)): out.append(c)
    return out
def maxid(r): return max([int(e.text) for e in idels(r)]+[-1])
def maxtag(r): return max([abs(int(e.text)) for e in r.iter('layerTag')]+[0])
problems=[]; renames=[]
def same(a,b,doff,toff,where):
    if a.tag!=b.tag or a.attrib!=b.attrib: problems.append(f'{where}: tag/attr {a.tag}{a.attrib} vs {b.tag}{b.attrib}'); return
    if len(a)!=len(b): problems.append(f'{where}/{a.tag}: child count {len(a)} vs {len(b)}'); return
    if len(a)==0:
        ta=(a.text or '').strip(); tb=(b.text or '').strip()
        if a.tag=='layerTag' and tb not in('','0'): v=int(tb); tb=str(v+toff if v>0 else v-toff)
        elif id(b) in ISID and not (b.tag=='int' and tb=='0'): tb=str(int(tb)+doff)
        if ta!=tb:
            if a.tag=='name' and where.split('/')[-1] in('Floor','Detector'): renames.append((where.split('/')[-1],tb,ta))
            else: problems.append(f'{where}/{a.tag}: {tb!r} -> {ta!r}')
    for ca,cb in zip(a,b): same(ca,cb,doff,toff,where+'/'+a.tag)
ISID=set()
for s in srcs:
    for e in idels(s): ISID.add(id(e))
# header = first file except pipecadVersion
for ca,cb in zip(m,srcs[0]):
    if ca.tag in('floorDatabase','resultsDatabase','pipecadVersion'): continue
    same(ca,cb,0,0,'header')
mf=list(m.find('floorDatabase')); mr=list(m.find('resultsDatabase'))
fi=ri=0; doff=0; toff=0
for k,s in enumerate(srcs):
    if k==0: d,t=0,0
    else: d,t=doff,toff
    for f in s.find('floorDatabase'): same(mf[fi],f,d,t,f'file{k+1}'); fi+=1
    for r in s.find('resultsDatabase'): same(mr[ri],r,d,t,f'file{k+1}'); ri+=1
    doff=max(doff, maxid(s)+d+1) if k else maxid(s)+1; toff=max(toff, maxtag(s)+t) if k else maxtag(s)
assert fi==len(mf) and ri==len(mr), ('extra merged items', fi, len(mf), ri, len(mr))
# global integrity: ids unique, every reference resolves to the right kind
ids={}
for p in m.iter():
    for c in p:
        if c.tag=='id' and len(c)==0:
            if c.text in ids: problems.append(f'duplicate id {c.text}')
            ids[c.text]=p.tag
kind={'detectorId':'Detector','pipeIds':'Pipe','pipeDatabase1':'Pipe','pipeDatabase2':'Pipe','holeIds':'Hole','holeDatabase1':'Hole','holeDatabase2':'Hole'}
bad=0
for p in m.iter():
    for c in p:
        k=c.tag if c.tag=='detectorId' else (p.tag if c.tag=='int' and p.tag in REF else None)
        if k and kind.get(k) and ids.get(c.text)!=kind[k]: bad+=1
src_bad=0
for s in srcs:
    sid={}
    for p in s.iter():
        for c in p:
            if c.tag=='id': sid[c.text]=p.tag
    for p in s.iter():
        for c in p:
            k=c.tag if c.tag=='detectorId' else (p.tag if c.tag=='int' and p.tag in REF else None)
            if k and kind.get(k) and sid.get(c.text)!=kind[k]: src_bad+=1
names=[d.find('name').text for d in m.iter('Detector')]
print(f'floors {len(mf)}  detectors {len(names)}  results {len(mr)}  ids {len(ids)} unique  unresolved refs merged={bad} (sources={src_bad})')
print('renames', renames)
print('PROBLEMS', len(problems)); print('\n'.join(problems[:20]))
raw=open(sys.argv[1],'rb').read(); print('CRLF only:', b'\n' not in raw.replace(b'\r\n',b''), '| starts', raw[:40])
sys.exit(1 if problems or bad!=src_bad else 0)
