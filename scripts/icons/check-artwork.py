#!/usr/bin/env python3
"""Check SVG safety, geometric bounds, tone layers, and catalog completeness."""
import importlib.util
import json
import math
from pathlib import Path
import sys
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('geometry',Path(__file__).with_name('adapt-brand.py'))
geometry=importlib.util.module_from_spec(spec);spec.loader.exec_module(geometry)
def exact_bounds(segments):
    samples=[];current=start=(0,0)
    for command,v in segments:
        assert all(math.isfinite(n) for n in v), 'Non-finite SVG coordinate'
        if command=='M': current=start=v; continue
        end=start if command=='Z' else v[-2:]
        samples.extend((current,end))
        if command in ('C','Q'):
            pts=[current]+[v[i:i+2] for i in range(0,len(v),2)]
            roots=set()
            for axis in [0,1]:
                q=[p[axis] for p in pts]
                if command=='Q':
                    denominator=q[0]-2*q[1]+q[2]
                    if abs(denominator)>1e-12: roots.add((q[0]-q[1])/denominator)
                else:
                    a=-q[0]+3*q[1]-3*q[2]+q[3]; b=2*(q[0]-2*q[1]+q[2]);c=q[1]-q[0]
                    if abs(a)<1e-12:
                        if abs(b)>1e-12:roots.add(-c/b)
                    elif b*b-4*a*c>=0:
                        delta=math.sqrt(b*b-4*a*c)
                        roots.update(((-b+delta)/(2*a),(-b-delta)/(2*a)))
            for t in roots:
                if 0<t<1:
                    work=pts
                    while len(work)>1:work=[((1-t)*a[0]+t*b[0],(1-t)*a[1]+t*b[1]) for a,b in zip(work,work[1:])]
                    samples.append(work[0])
        elif command=='A':
            # Retained brand imports can still contain elliptical SVG arcs.
            b=geometry.bounds([('M',current),('A',v)])
            samples.extend(((b[0],b[1]),(b[2],b[3])))
        current=end
    assert samples, 'Empty SVG contour'
    xs,ys=zip(*samples)
    return min(xs),min(ys),max(xs),max(ys)

catalog=json.loads((ROOT/'catalog.json').read_text())
assert len({i['name'] for i in catalog})==len(catalog), 'Duplicate catalog names'
assert {i['name'] for i in catalog}=={p.stem for p in (ROOT/'icons').glob('*.svg')}, 'Catalog drift'
count=0
for item in catalog:
    for style in item['styles']:
        p=ROOT/'icons'/((item['name']+'.svg') if style=='duotone' else f"styles/{style}/{item['name']}.svg")
        root=ET.parse(p).getroot()
        view=list(map(float,root.get('viewBox').split()))
        assert view[:2]==[0,0],p
        bounds=[];alphas=set()
        for node in root.iter():
            if node.get('d'):
                bounds.append(exact_bounds(geometry.parse_path(node.get('d'))))
                alphas.add(float(node.get('opacity','1')))
        assert bounds, f'{p}: empty artwork'
        for x0,y0,x1,y1 in bounds:
            assert x0>=-.015 and y0>=-.015 and x1<=view[2]+.015 and y1<=view[3]+.015, f'{p}: clipped geometry {(x0,y0,x1,y1)}'
        if style=='duotone':
            assert item['defaultTone'] in {'duotone','monochrome'}, f'{p}: missing tone decision'
            if item['defaultTone']=='duotone':
                assert any(0<a<1 for a in alphas) and 1 in alphas, f'{p}: missing surface tone layer'
            else:
                assert alphas=={1}, f'{p}: single-tone symbol contains a faded segment'
        else: assert alphas=={1},f'{p}: monochrome style contains opacity'
        count+=1
for style in ['solid','stroke']:
    expected={i['name'] for i in catalog if style in i['styles']}
    assert expected=={p.stem for p in (ROOT/'icons/styles'/style).glob('*.svg')},f'Orphan {style} drawings'
print(f'{count} drawings: finite geometry, bounds, tone layers, and catalog verified')
