#!/usr/bin/env python3
"""Original rounded artwork. Authoring only: pip install -r scripts/icons/requirements.txt.

B = closed body, D = identifying detail; lines expanded with round caps/joins.
All delivered SVGs contain filled Bézier contours, with no runtime dependencies.
"""
import json
import math
import re
from pathlib import Path
import sys
import xml.etree.ElementTree as ET
import pathops as po
from fontTools.svgLib.path import parse_path
from fontTools.pens.svgPathPen import SVGPathPen

ROOT = Path(__file__).resolve().parents[2]
DRAWINGS = {}
CATEGORY = ''
BOOLEAN_REPAIRS=[]
def op(a,b,kind):
    """Reject numerically inconsistent Skia results before exporting artwork.

    Tangent round contours can produce catastrophic float-precision failures.
    Retry on the same 1e-4 grid used by the exported SVG, then on a 1e-3 grid.
    Area identities guard against silently dropping complete contours.
    """
    a,b=po.simplify(a),po.simplify(b)
    for precision in [None,4,3]:
        if precision is None: aa,bb=a,b
        else:
            def quantize(p):
                pen=SVGPathPen(None,ntos=lambda v:format(v,f'.{precision}f'))
                p.draw(pen)
                return path(pen.getCommands())
            aa,bb=quantize(a),quantize(b)
        result=po.op(aa,bb,kind)
        if kind == po.PathOp.INTERSECTION:
            other=po.op(aa,bb,po.PathOp.UNION).area
            expected=aa.area+bb.area-other
        else:
            intersection=po.op(aa,bb,po.PathOp.INTERSECTION).area
            expected={po.PathOp.UNION:aa.area+bb.area-intersection,
                      po.PathOp.DIFFERENCE:aa.area-intersection,
                      po.PathOp.REVERSE_DIFFERENCE:bb.area-intersection,
                      po.PathOp.XOR:aa.area+bb.area-2*intersection}[kind]
        tolerance=.004+.00005*(aa.area+bb.area)
        if expected >= -tolerance and abs(result.area-expected)<=tolerance:
            if precision is not None: BOOLEAN_REPAIRS.append(precision)
            return result
    raise ValueError(f'Unstable boolean geometry: {kind}; {result.area} != {expected}')

def path(d):
    p = po.Path()
    if d: parse_path(d, p.getPen())
    return p

def union(*ps):
    r = po.Path()
    for p in ps:
        if p: r = op(r, p, po.PathOp.UNION)
    return r

def stroke(d, width=1.35):
    p = path(d) if isinstance(d, str) else po.Path(d)
    # Stroke at authoring resolution so Skia's curve tolerance cannot
    # introduce visibly different widths at different orientations.
    resolution=32
    p=p.transform(resolution,0,0,resolution,0,0)
    p.stroke(width*resolution, po.LineCap.ROUND_CAP, po.LineJoin.ROUND_JOIN, 4)
    p.convertConicsToQuads(.02)
    p=p.transform(1/resolution,0,0,1/resolution,0,0)
    return po.simplify(p)

def rr(x=2,y=2,w=12,h=12,r=2):
    r=min(r,w/2,h/2);k=r*.5522847498
    return path(f'M{x+r} {y}H{x+w-r}C{x+w-r+k} {y} {x+w} {y+r-k} {x+w} {y+r}V{y+h-r}C{x+w} {y+h-r+k} {x+w-r+k} {y+h} {x+w-r} {y+h}H{x+r}C{x+r-k} {y+h} {x} {y+h-r+k} {x} {y+h-r}V{y+r}C{x} {y+r-k} {x+r-k} {y} {x+r} {y}Z')

def soften(p,r=.28):
    # Round sharp convex corners in closed masses; preserve negative counters.
    inset=op(p,stroke(p,2*r),po.PathOp.DIFFERENCE)
    return union(inset,stroke(inset,2*r)) if inset else p

def mirror(p): return p.transform(-1,0,0,1,16,0)


def circle(x=8,y=8,r=6):
    return path(f'M{x-r} {y}a{r} {r} 0 1 0 {2*r} 0a{r} {r} 0 1 0 {-2*r} 0Z')

def line(*points, width=1.35):
    return stroke('M'+'L'.join(f'{x} {y}' for x,y in points),width)

def lines(*ds): return union(*(stroke(d) for d in ds))
def dots(*points,r=.7): return union(*(circle(x,y,r) for x,y in points))
def poly(points): return soften(path('M'+'L'.join(f'{x} {y}' for x,y in points)+'Z'),.22)
def ring(x=8,y=8,r=6,width=1.35): return op(circle(x,y,r),circle(x,y,r-width),po.PathOp.DIFFERENCE)
def transform(p,angle=0,scale=1,dx=0,dy=0):
    a=math.radians(angle); c=math.cos(a)*scale; s=math.sin(a)*scale
    return p.transform(c,s,-s,c,8-8*c+8*s+dx,8-8*s-8*c+dy)

def add(name,b,d=None,outline=True,tags=''):
    assert name not in DRAWINGS, name
    d = d or po.Path()
    if outline and name != 'settings': b=soften(b)
    extent=union(b,d,stroke(b,1.25) if outline else po.Path()).bounds
    x0,y0,x1,y1=extent
    if min(x0,y0)<.65 or max(x1,y1)>15.35:
        scale=min(1,14.7/(x1-x0),14.7/(y1-y0))
        dx=8-(x0+x1)/2;dy=8-(y0+y1)/2
        b=transform(b,scale=scale,dx=dx*scale,dy=dy*scale)
        d=transform(d,scale=scale,dx=dx*scale,dy=dy*scale)
    DRAWINGS[name] = (b,d,outline,CATEGORY,tags)

def shape(name,b,d=None,tags=''): add(name,b,d,True,tags)
def glyph(name,b,d,tags=''): add(name,b,d,False,tags)
def check(x=8,y=8,s=1): return line((x-2.6*s,y),(x-.6*s,y+2*s),(x+3*s,y-2.2*s))
def plus(x=8,y=8,s=1): return lines(f'M{x-2*s} {y}h{4*s}',f'M{x} {y-2*s}v{4*s}')
def cross(x=8,y=8,s=1): return lines(f'M{x-2*s} {y-2*s}l{4*s} {4*s}',f'M{x+2*s} {y-2*s}l{-4*s} {4*s}')
def arrow(angle=0): return transform(lines('M3 8H13','M9 4l4 4-4 4'),angle)

CATEGORY='Navigation'
for name,angle in [('right',0),('down',90),('left',180),('up',270),('up-right',-45),('down-right',45),('down-left',135),('up-left',225)]:
    glyph('arrow-'+name,transform(line((3,8),(13,8)),angle),transform(line((9,4),(13,8),(9,12)),angle))
    glyph('chevron-'+name,transform(line((5,3),(10,8)),angle),transform(line((10,8),(5,13)),angle))
for name,angle in [('left',180),('right',0),('up',270),('down',90)]:
    shape('circle-arrow-'+name,circle(),transform(arrow(),angle, .64))
    glyph('chevrons-'+name,transform(line((2,4),(6,8),(2,12)),angle),transform(line((9,4),(13,8),(9,12)),angle))
glyph('chevrons-up-down',line((5,6),(8,3),(11,6)),line((5,10),(8,13),(11,10)))
glyph('chevrons-in',lines('M2 4l4 4-4 4'),lines('M14 4l-4 4 4 4'))
shape('home',path('M2 7L8 2 14 7V13Q14 14 13 14H3Q2 14 2 13Z'),stroke('M6 14V9H10V14'),'house dashboard start')
shape('compass',circle(),poly([(10.7,5.3),(9,9),(5.3,10.7),(7,7)]))
glyph('external-link',stroke('M9 2H14V7'),stroke('M14 2L7 9M6 3H3Q2 3 2 4V13Q2 14 3 14H12Q13 14 13 13V10'))
glyph('log-in',stroke('M9 2H13Q14 2 14 3V13Q14 14 13 14H9'),union(line((2,8),(10,8)),line((7,5),(10,8),(7,11))))
glyph('log-out',stroke('M7 2H3Q2 2 2 3V13Q2 14 3 14H7'),union(line((6,8),(14,8)),line((11,5),(14,8),(11,11))))
for name,reflect in [('undo',False),('redo',True)]:
    f=mirror if reflect else lambda p:p
    glyph(name,f(stroke('M3 6H9C12 6 14 7.5 14 10S12 13.5 10 13.5')),f(line((6,3),(3,6),(6,9))))
for name,reflect in [('refresh',False),('reset',True),('rotate-left',True),('rotate-right',False)]:
    f=mirror if reflect else lambda p:p
    glyph(name,f(stroke('M12.5 10.5A5.2 5.2 0 1 1 12.5 4.5')),f(line((9.2,4.5),(12.5,4.5),(12.5,1.2))))
glyph('swap-horizontal',lines('M2 4.5H14','M11 1.5l3 3-3 3'),lines('M14 11.5H2','M5 8.5l-3 3 3 3'))
glyph('swap-vertical',lines('M4.5 14V2','M1.5 5l3-3 3 3'),lines('M11.5 2V14','M8.5 11l3 3 3-3'))
glyph('shuffle',stroke('M2 4H4L12 12H14M2 12H4L12 4H14'),lines('M12 2l2 2-2 2','M12 10l2 2-2 2'))
glyph('repeat',stroke('M3 10V5Q3 3 5 3H13M13 6V11Q13 13 11 13H3'),lines('M11 1l2 2-2 2','M5 11l-2 2 2 2'))

CATEGORY='Actions and status'
glyph('plus',line((8,3),(8,13)),line((3,8),(13,8)))
glyph('minus',line((3,8),(8,8)),line((8,8),(13,8)))
glyph('close',line((3,3),(13,13)),line((13,3),(3,13)))
glyph('check',line((2,8),(6,12)),line((6,12),(14,4)))
glyph('check-check',line((1,8),(4,11),(10,4)),line((7,10),(9,12),(15,5)))
for name,detail in [('check',check()),('x',cross()),('plus',plus()),('minus',line((5,8),(11,8))),('info',union(circle(8,5,.7),line((8,7.5),(8,11)))),('help',union(stroke('M6 5.5C6 3 11 3 10 6Q10 7 8 8V9'),circle(8,11.5,.65))),('alert',union(line((8,4.5),(8,8.5)),circle(8,11,.7))),('ellipsis',dots((4.5,8),(8,8),(11.5,8)))]:
    shape('circle-'+name,circle(),detail)
for old,new in [('info','circle-info'),('info-fill','circle-info'),('exclamation-circle-fill','circle-alert'),('ellipsis-circle','circle-ellipsis'),('minus-circle','circle-minus'),('circle-check-fill','circle-check'),('circle-x-fill','circle-x')]:
    b,d,o,c,t = DRAWINGS[new]; add(old,b,d,o,t)
for name,detail in [('triangle-alert',union(line((8,6),(8,9)),circle(8,11.5,.65))),('triangle-alert-fill',union(line((8,6),(8,9)),circle(8,11.5,.65)))]:
    shape(name,path('M7.1 2.5Q8 1 8.9 2.5L14.3 12Q15.2 14 13 14H3Q.8 14 1.7 12Z'),detail)
shape('octagon-alert',poly([(5,1.5),(11,1.5),(14.5,5),(14.5,11),(11,14.5),(5,14.5),(1.5,11),(1.5,5)]),union(line((8,4.5),(8,8.5)),circle(8,11,.7)))
shape('ban',circle(),line((4,4),(12,12)))
shape('checkbox',rr(),check())
shape('checkbox-fill',rr(),check())
shape('square',rr())
shape('circle',circle())
glyph('dot',circle(8,8,4),circle(8,8,1.5))
glyph('ellipsis',dots((3,8),(8,8),(13,8),r=1.1),circle(8,8,1.1))
glyph('ellipsis-vertical',dots((8,3),(8,8),(8,13),r=1.1),circle(8,8,1.1))
shape('search',circle(6.7,6.7,4.7),line((10.3,10.3),(14,14)))
for name,detail in [('zoom-in',plus(6.5,6.5,.75)),('zoom-out',line((4.7,6.5),(8.3,6.5)))]: shape(name,circle(6.7,6.7,4.7),union(line((10.3,10.3),(14,14)),detail))
shape('filter',path('M2 2H14L9.5 7.5V13L6.5 14V7.5Z'),line((5,4.5),(11,4.5)),'funnel refine')
glyph('sort-ascending',lines('M2 4H7','M2 8H6','M2 12H5'),lines('M12 13V3','M9 6l3-3 3 3'))
glyph('sort-descending',lines('M2 4H7','M2 8H6','M2 12H5'),lines('M12 3V13','M9 10l3 3 3-3'))
glyph('sliders',lines('M2 4H14','M2 8H14','M2 12H14'),union(circle(5,4,1.6),circle(11,8,1.6),circle(6,12,1.6)))
shape('toggle-on',rr(1.5,4,13,8,4),circle(10.5,8,2.3))
shape('toggle-off',rr(1.5,4,13,8,4),circle(5.5,8,2.3))
shape('save',path('M3 2H11L14 5V13Q14 14 13 14H3Q2 14 2 13V3Q2 2 3 2Z'),union(stroke('M5 2V6H10V2'),stroke('M5 14V10H11V14')))
shape('trash',rr(4,4,8,10,1),lines('M2.5 4H13.5','M6 2H10','M6.5 7V11','M9.5 7V11'),'delete remove bin')
shape('archive',rr(2.5,5,11,9,1.5),union(rr(1.5,2,13,3,1),line((6,8),(10,8))))
for name,angle in [('download',90),('upload',270)]:
    glyph(name,stroke('M2 10V13Q2 14 3 14H13Q14 14 14 13V10'),transform(arrow(),angle,.75,0,-2))
shape('download-circle-fill',circle(),transform(arrow(),90,.65))
glyph('link',stroke('M6.5 10.5L4.5 12.5A3 3 0 0 1 .5 8.5L4 5Q6 3 8 5'),stroke('M9.5 5.5L11.5 3.5A3 3 0 0 1 15.5 7.5L12 11Q10 13 8 11M5.5 10.5L10.5 5.5'))
glyph('unlink',stroke('M5 11L4 12A3 3 0 0 1 0 8L3 5M11 5L12 4A3 3 0 0 1 16 8L13 11'),lines('M5 1l1 2','M1 5l2 1','M11 15l-1-2','M15 11l-2-1'))
shape('copy',union(rr(1.5,1.5,9,10,1.7),rr(5,5,9.5,9.5,1.7)),stroke(rr(5,5,9.5,9.5,1.7),1.25))
shape('clipboard',rr(3,3,10,11,1.5),union(rr(5.5,1.5,5,3,1),lines('M5.5 7H10.5','M5.5 10H9')))
shape('clipboard-check',rr(3,3,10,11,1.5),union(rr(5.5,1.5,5,3,1),check(8,9,.7)))

CATEGORY='Files and folders'
FILE=path('M4 1.5H9L13.5 6V13Q13.5 14.5 12 14.5H4Q2.5 14.5 2.5 13V3Q2.5 1.5 4 1.5Z')
FOLD=stroke('M9 1.5V6H13.5',1.2)
FOLDER=path('M2 3H6L8 5H14Q15 5 15 6V12Q15 14 13 14H3Q1 14 1 12V4Q1 3 2 3Z')
for name,detail in [('file',FOLD),('file-text',union(FOLD,lines('M5 8H11','M5 10.5H10'))),('file-plus',union(FOLD,plus(8,10,.7))),('file-minus',union(FOLD,line((5.5,10),(10.5,10)))),('file-check',union(FOLD,check(8,10,.65))),('file-x',union(FOLD,cross(8,10,.7))),('file-code',union(FOLD,lines('M6.5 8l-2 2 2 2','M9.5 8l2 2-2 2'))),('file-image',union(FOLD,circle(6,8,.7),line((4.5,12),(7,9.5),(9,11),(11,9)))),('file-table',union(FOLD,stroke('M5 8H11V12H5ZM5 10H11M8 8V12',1))),('file-symlink',union(FOLD,stroke('M5 12V10H10.5M8.5 8l2 2-2 2',1.1))),('file-lock',union(FOLD,rr(5.8,9.8,4.4,3,.6),stroke('M6.6 9.8V8.8A1.4 1.4 0 0 1 9.4 8.8V9.8',1))),('file-audio',union(FOLD,line((9,8),(9,11)),circle(7.8,11.5,1.2))),('file-video',union(FOLD,poly([(6,8),(10,10),(6,12)]))),('file-search',union(FOLD,ring(7,9.5,2,1),line((8.5,11),(10.5,13)))),('file-heart',union(FOLD,path('M8 12.5L5.3 10C3.8 8.5 6.2 7.2 8 9C9.8 7.2 12.2 8.5 10.7 10Z'))),('file-zip',union(FOLD,rr(7.3,7.5,1.4,1.4,.2),rr(8.5,9,1.4,1.4,.2),rr(7.3,10.5,1.4,1.4,.2)))]: shape(name,FILE,detail)
for name,detail in [('folder',line((2,6),(14,6))),('folder-plus',plus(8,10,.8)),('folder-minus',line((5.5,10),(10.5,10))),('folder-check',check(8,10,.7)),('folder-x',cross(8,10,.7)),('folder-heart',path('M8 12.5L5 10C3.5 8.5 6 7 8 9C10 7 12.5 8.5 11 10Z')),('folder-lock',union(rr(6,9,4,3,1),stroke('M7 9V8A1 1 0 0 1 9 8V9',1))),('folder-search',union(ring(7.5,9,2.3,1.2),line((9.2,10.7),(11.3,12.8)))),('folder-code',lines('M6 8l-2 2 2 2','M10 8l2 2-2 2')),('folder-zip',union(rr(7,6.8,1.4,1.4,.2),rr(8.4,8.2,1.4,1.4,.2),rr(7,9.6,1.4,1.4,.2),stroke('M7.6 12H9.4',1)))]: shape(name,FOLDER,detail)
shape('folder-open',FOLDER,path('M2 7H14Q15 7 14.5 8.5L13 13H3Z'))
shape('folders',union(transform(FOLDER,0,.8,-1,-2),transform(FOLDER,0,.8,1,1.5)),stroke(transform(FOLDER,0,.8,1,1.5),1.25))
for name,detail in [('spreadsheet',stroke('M2 6H14M6 2V14M10 6V14M2 10H14',1.2)),('slides',union(lines('M4 5H12','M4 8H7','M4 10.5H7'),rr(9,8,3,4,.5))),('word',lines('M3.5 5l2 6 2.5-5 2.5 5 2-6')),('pdf',stroke('M3.7 10.8V5.2H4.7C6.5 5.2 6.5 8 4.7 8H3.7M7.2 5.2V10.8H8.1C10.4 10.8 10.4 5.2 8.1 5.2ZM10.9 10.8V5.2H13M10.9 8H12.6',.8)),('epub',stroke('M8 5Q5 3 3 4V11Q5 10 8 12Q11 10 13 11V4Q11 3 8 5ZM8 5V12',1)),('zip',lines('M7 3H9','M6 5H8','M7 7H9','M6 9H8','M7 11H9'))]: shape(name,rr(),detail)

CATEGORY='Communication'
BUBBLE=path('M4 2H12Q14 2 14 4V10Q14 12 12 12H7L3 14V12Q2 12 2 10V4Q2 2 4 2Z')
for name,detail in [('message',line((5,6),(11,6))),('message-text',lines('M5 6H11','M5 9H9')),('message-plus',plus(8,7,.8)),('message-check',check(8,7,.7)),('message-heart',path('M8 10L5 7.5C3.5 6 6 4 8 6C10 4 12.5 6 11 7.5Z')),('message-dots',dots((5,7),(8,7),(11,7))),('comment-text',lines('M5 6H11','M5 9H9')),('conversation',lines('M5 6H11','M5 9H9')),('conversation-add',plus(8,7,.8))]: shape(name,BUBBLE,detail)
for name in ['mail','envelope']: shape(name,rr(1.5,3,13,10,2),line((2,4),(8,8.5),(14,4)))
shape('mail-open',path('M1.5 6L8 1.5 14.5 6V13Q14.5 14 13 14H3Q1.5 14 1.5 13Z'),lines('M2 7l6 4 6-4','M2 14l4-4','M14 14l-4-4'))
shape('send',path('M2 2L14 7.2Q15 8 14 8.8L2 14 4 8Z'),line((4,8),(11,8)))
shape('inbox',rr(1.5,2,13,12,2),stroke('M1.5 9H5L6 11H10L11 9H14.5'))
BELL=path('M8 2A4 4 0 0 0 4 6V9L2 12H14L12 9V6A4 4 0 0 0 8 2Z')
shape('bell',BELL,union(line((6,14),(10,14)),line((8,1),(8,2))))
shape('bell-unread',op(BELL,circle(12.5,3,2.9),po.PathOp.DIFFERENCE),union(line((6,14),(10,14)),circle(12.5,3,1.65)))
shape('bell-off',BELL,union(line((6,14),(10,14)),line((2,2),(14,14))))
shape('megaphone',path('M2 6H6L13 2V12L6 9H2Z'),stroke('M5 9L6 14H8L7 10'))
shape('phone-call',path('M3 1.5L6 4.5 4.5 7Q6 10 9 11.5L11.5 10 14.5 13Q13 16 10 14.5C6 13 3 10 1.5 6Q0 3 3 1.5Z'),stroke('M10 2Q14 2 14 6M10 5Q11 5 11 6',1.1))
shape('video-call',rr(1.5,4,9,8,2),path('M11 6L14.5 4V12L11 10Z'))
glyph('at-sign',stroke('M12.3 12.8C5.5 17.8-.2 11 2.2 5C4.5-.7 14.5 1 14.5 7.3C14.5 11 10 11.5 10 8.5V5'),stroke('M10 6C7 3 4 6 5 8.8C6 11.5 10 10.5 10 7',1.2))
glyph('rss',stroke('M2 2A12 12 0 0 1 14 14M2 7A7 7 0 0 1 9 14'),circle(3,13,1.4))

CATEGORY='People and accessibility'
HEAD=circle(8,4.5,2.5); SHOULDERS=path('M2.5 14V12Q2.5 8.5 8 8.5Q13.5 8.5 13.5 12V14Z')
shape('user',union(SHOULDERS,HEAD))
shape('circle-user',circle(),union(circle(8,6,2),stroke('M3.5 12Q8 6.5 12.5 12')))
shape('users',union(circle(5,4.5,2.2),circle(11.5,5.5,1.8),path('M1 14V12Q1 8.5 5 8.5Q9 8.5 9 12V14ZM9 14V12Q9 10 11.5 10Q15 10 15 13V14Z')),line((9,12),(9,14)))
shape('user-plus',union(transform(SHOULDERS,0,.8,-2,0),transform(HEAD,0,.8,-2,0)),plus(12,8,.8))
shape('user-check',union(transform(SHOULDERS,0,.8,-2,0),transform(HEAD,0,.8,-2,0)),check(12,8,.6))
shape('user-x',union(transform(SHOULDERS,0,.8,-2,0),transform(HEAD,0,.8,-2,0)),cross(12,8,.7))
shape('contact',rr(2,1.5,12,13,2),union(circle(8,6,2),stroke('M5 11Q8 8 11 11'),lines('M1 5H3','M1 11H3')))
glyph('accessibility',circle(8,2.5,1.5),lines('M2 6L8 7 14 6','M8 7V10','M8 10L4 14','M8 10L12 14'))
glyph('wheelchair',ring(6,10,4,1.3),union(circle(7,2,1.4),stroke('M7 4V8H11L13 13H15')))
for name,detail in [('smile',stroke('M5 9Q8 13 11 9')),('frown',stroke('M5 11Q8 7 11 11')),('meh',line((5,10),(11,10)))]: shape(name,circle(),union(dots((5.5,6),(10.5,6)),detail))
HAND=union(rr(3,7.5,11,6.5,3),rr(2.7,3.3,1.5,6,.75),rr(6,1.5,1.5,7.8,.75),rr(9.3,2.3,1.5,7,.75),rr(12.6,4.3,1.5,5.5,.75),path('M5.5 13L1.4 9Q.2 7.6 1.5 6.8Q2.3 6.3 3.2 7.4L5.5 9Z'))
shape('hand',HAND)
shape('thumbs-up',path('M5 7L8 2Q10 1 10 4L9.5 6H13Q15 6 14 9L12.5 14H5Z'),rr(1.5,7,3.5,7,1))
shape('thumbs-down',transform(DRAWINGS['thumbs-up'][0],180),transform(DRAWINGS['thumbs-up'][1],180))

CATEGORY='Security'
SHIELD=path('M8 1.5Q11 3 14 3V7Q14 12 8 14.5Q2 12 2 7V3Q5 3 8 1.5Z')
for name,detail in [('shield',po.Path()),('shield-check',check()),('shield-x',cross()),('shield-alert',union(line((8,5),(8,8)),circle(8,10.5,.7))),('shield-keyhole',union(circle(8,6.5,1.5),line((8,7),(8,10.5))))]: shape(name,SHIELD,detail)
for name,shackle in [('lock','M4.5 7V5A3.5 3.5 0 0 1 11.5 5V7'),('lock-open','M4.5 7V5A3.5 3.5 0 0 1 11.5 5')]: shape(name,rr(2.5,7,11,7,1.8),union(stroke(shackle),circle(8,10,1),line((8,10),(8,12))))
shape('key',circle(5,5,3.5),union(circle(5,5,1),stroke('M7.5 7.5L14 14M11 11L13 9M13 13L15 11')))
glyph('fingerprint',stroke('M1.8 7.5A6.2 6.2 0 0 1 14.2 7.5Q14.2 11 13 13M3.8 10V7.5A4.2 4.2 0 0 1 12.2 7.5Q12.2 12 10.8 14',1.1),stroke('M5.5 13.5Q7.4 11 6.7 8A1.35 1.35 0 0 1 9.4 8Q10 11 8.5 14M1.8 10Q2.2 13 3 14',1.1))
shape('eye',path('M1 8Q8-3 15 8Q8 19 1 8Z'),ring(8,8,2.5,1.35))
shape('eye-off',DRAWINGS['eye'][0],union(DRAWINGS['eye'][1],line((2,2),(14,14))))
shape('scan',rr(4,4,8,8,2),lines('M1 5V1H5','M11 1H15V5','M1 11V15H5','M11 15H15V11','M6 8H10'))
shape('qr-code',union(rr(1.5,1.5,5,5,1),rr(9.5,1.5,5,5,1),rr(1.5,9.5,5,5,1)),union(rr(3,3,2,2,.3),rr(11,3,2,2,.3),rr(3,11,2,2,.3),lines('M10 10H14V14H12','M10 13V14')))
shape('badge-check',path('M8 1L10 2.5 12.5 2.5 13.5 5 15 8 13.5 10 12.5 13 10 13.5 8 15 6 13.5 3.5 13 2.5 10 1 8 2.5 5 3.5 2.5 6 2.5Z'),check())

CATEGORY='Time and planning'
for name,detail in [('clock',line((8,4),(8,8),(11,10))),('alarm-clock',union(line((8,4),(8,8),(11,8)),lines('M2 3l2-2','M12 1l2 2','M3 14l1-2','M12 12l1 2'))),('history',union(line((8,4),(8,8),(11,9)),line((1.5,1.5),(1.5,5),(5,5))))]: shape(name,circle(8,8,5.8),detail)
shape('timer',circle(8,9,5),union(line((8,9),(10,6.5)),lines('M6 1H10','M8 1V4','M12 4l1-1')))
shape('hourglass',path('M3 2H13Q13 6 9.5 8Q13 10 13 14H3Q3 10 6.5 8Q3 6 3 2Z'),lines('M3 2H13','M3 14H13','M6 5H10','M6 12l2-2 2 2'))
CAL=rr(2,3,12,11,2); CALTOP=lines('M5 1.5V4.5','M11 1.5V4.5','M2 6H14')
for name,detail in [('calendar',dots((5,9),(8,9),(11,9),(5,12),(8,12))),('calendar-days',dots((5,9),(8,9),(11,9),(5,12),(8,12),(11,12))),('calendar-check',check(8,10,.7)),('calendar-plus',plus(8,10,.8)),('calendar-x',cross(8,10,.7)),('calendar-clock',union(ring(9,10,2.7,1),stroke('M9 8.5V10H10.5',1))),('calendar-range',line((5,10),(11,10)))]: shape(name,CAL,union(CALTOP,detail))
shape('list-todo',rr(1.5,2,13,12,2),lines('M3.5 5l1 1 2-2','M8 5H12','M3.5 10l1 1 2-2','M8 10H12'))
shape('notebook',rr(3,1.5,10.5,13,1.5),lines('M1.5 4H4.5','M1.5 8H4.5','M1.5 12H4.5','M6.5 5H11','M6.5 8H10'))
shape('sticky-note',path('M2 2H14V10L10 14H2Z'),stroke('M10 14V10H14M5 5H11M5 8H9',1.2))
shape('flag',path('M3 2Q6 0 9 2T14 2V9Q11 11 8 9T3 9Z'),line((3,2),(3,14)))
shape('bookmark',path('M4 2H12V14L8 11 4 14Z'))
shape('bookmark-plus',path('M4 2H12V14L8 11 4 14Z'),plus(8,6,.7))
shape('pin',path('M5 2H11L10 6 13 9H3L6 6Z'),line((8,9),(8,14)))
shape('target',circle(),union(ring(8,8,3.5,1.25),circle(8,8,1.2)))
shape('trophy',path('M4 2H12V6Q12 10 8 11Q4 10 4 6Z'),stroke('M4 3H1V5Q1 8 4 8M12 3H15V5Q15 8 12 8M8 11V14M5 14H11'))

CATEGORY='Media'
for name,detail in [('play',poly([(6,4.5),(12,8),(6,11.5)])),('pause',union(rr(5,4.5,2,7,.5),rr(9,4.5,2,7,.5))),('stop',rr(5,5,6,6,1))]: shape(name,circle(),detail)
for name,source in [('pause-circle-fill','pause'),('play-circle','play'),('stop-circle','stop')]:
    b,d,o,c,t=DRAWINGS[source];add(name,b,d,o,t)
glyph('skip-forward',poly([(2,3),(10,8),(2,13)]),line((13,3),(13,13)))
glyph('skip-back',poly([(14,3),(6,8),(14,13)]),line((3,3),(3,13)))
shape('volume',path('M2 6H5L9 2V14L5 10H2Z'),stroke('M12 4Q16 8 12 12M11 6Q13 8 11 10'))
shape('volume-off',path('M2 6H5L9 2V14L5 10H2Z'),cross(12.5,8,.6))
shape('microphone',rr(5,1.5,6,9,3),stroke('M2.5 7V8A5.5 5.5 0 0 0 13.5 8V7M8 13.5V15M5.5 15H10.5',1.2))
shape('microphone-off',rr(5,1.5,6,9,3),stroke('M2.5 7V8A5.5 5.5 0 0 0 13.5 8V7M8 13.5V15M2 2L14 14',1.2))
shape('headphones',path('M2 8A6 6 0 0 1 14 8V12H11V8H5V12H2Z'),union(rr(1.5,7,3.5,6,1.4),rr(11,7,3.5,6,1.4)))
glyph('music',stroke('M6 12V3L13 1.5V10'),union(circle(4,12,2),circle(11,10,2),line((6,5),(13,3.5))))
shape('image',rr(1.5,2,13,12,2),union(circle(5,5.5,1.3),line((2,12),(6.5,8),(9,10),(11,7.5),(14,11))))
shape('camera',path('M2 4H5L6 2H10L11 4H14V13H2Z'),union(ring(8,8.5,3,1.35),circle(12,6,.65)))
shape('camera-off',DRAWINGS['camera'][0],union(DRAWINGS['camera'][1],line((2,2),(14,14))))
shape('video',rr(1.5,2,13,12,2),union(poly([(6,5),(11,8),(6,11)]),lines('M4 2V14','M12 2V14')))
shape('film',rr(1.5,2,13,12,1),lines('M5 2V14','M11 2V14','M1.5 6H5','M1.5 10H5','M11 6H14.5','M11 10H14.5'))
shape('radio',rr(1.5,5,13,9,2),union(line((3,5),(12,1.5)),ring(5.5,9.5,2.2,1.2),lines('M10 8H12','M10 11H12')))
shape('tv',rr(1.5,4,13,9,2),lines('M5 1l3 3 3-3','M5 15H11'))
shape('cast',rr(1.5,2,13,11,2),union(stroke('M2 7A7 7 0 0 1 9 14M2 10A4 4 0 0 1 6 14'),circle(2,14,1)))
shape('airplay',rr(1.5,2,13,10,2),poly([(8,8),(13,14),(3,14)]))
glyph('waveform',lines('M2 6V10','M5 3V13','M8 1V15','M11 4V12','M14 6V10'),line((8,5),(8,11)))
shape('disc',circle(),union(ring(8,8,1.5,.9),stroke('M4 5Q5 3.5 7 3M12 11Q11 12.5 9 13',1.2)))
glyph('podcast',ring(8,6.5,5,1.3),union(circle(8,6,1.7),rr(6,9,4,6,2)))

CATEGORY='Layout'
WINDOW=rr(1.5,2,13,12,2)
for name,detail in [('app-window',union(line((1.5,5.5),(14.5,5.5)),dots((4,3.8),(6,3.8),r=.4))),('browser',union(line((1.5,5.5),(14.5,5.5)),line((7,3.8),(12,3.8)))),('panel-left',stroke('M6 2V14')),('panel-right',stroke('M10 2V14')),('panel-top',stroke('M2 6H14')),('panel-bottom',stroke('M2 10H14')),('columns',stroke('M8 2V14')),('rows',stroke('M2 8H14')),('layout-dashboard',stroke('M8 2V14M2 9H8M8 6H14')),('layout-grid',stroke('M8 2V14M2 8H14')),('layout-sidebar',stroke('M6 2V14M2 6H6M2 9H6')),('table',stroke('M2 6H14M2 10H14M6 2V14M10 2V14',1.1))]: shape(name,WINDOW,detail)
glyph('maximize',lines('M2 6V2H6','M10 14H14V10'),lines('M10 2H14V6','M2 10V14H6'))
glyph('minimize',lines('M2 6H6V2','M10 14V10H14'),lines('M10 2V6H14','M2 10H6V14'))
glyph('fullscreen',lines('M1.5 5V1.5H5','M11 14.5H14.5V11'),lines('M11 1.5H14.5V5','M1.5 11V14.5H5'))
shape('picture-in-picture',WINDOW,rr(8,8,5,4,1))
glyph('layers',path('M1 9L8 13 15 9V11L8 15 1 11Z'),path('M1 5L8 1 15 5 8 9Z'))
shape('multiplexer',union(rr(1.5,1.5,9.5,9.5,2),rr(5,5,9.5,9.5,2)),union(stroke(rr(5,5,9.5,9.5,2),1.25),lines('M10 5V14.5','M5 10H14.5')))

CATEGORY='Editing and design'
shape('pencil',path('M2 10L10 2Q11 1 12 2L14 4Q15 5 14 6L6 14 1.5 14.5Z'),stroke('M9 3L13 7M2 10L6 14'))
shape('eraser',path('M2 8L8 2Q9 1 10 2L14 6Q15 7 14 8L8 14H5L2 11Q1 10 2 8Z'),stroke('M5 5L11 11M8 14H14'))
shape('paintbrush',path('M5 9L10 2Q12 0 14 2Q16 4 14 6L7 11Z'),path('M5 9Q1 9 2 12Q2 14 1 15Q7 15 7 11Z'))
shape('palette',path('M8 1.5C0 1.5-1 13 6 14.5Q10 15 9 12Q8 10 11 10C17 11 16 1.5 8 1.5Z'),dots((5,5),(9,4),(12,6),(3.5,8)))
SWATCH=rr(2,2,4.5,12,1)
SWATCH_DIAGONAL=SWATCH.transform(.7071,.7071,-.7071,.7071,9.553,-.257)
shape('swatch',union(SWATCH,SWATCH_DIAGONAL,rr(2,9.5,12,4.5,1)),union(stroke(rr(2,9.5,12,4.5,1),1.1),stroke(SWATCH_DIAGONAL,1.1),circle(4.25,11.75,.65)))
glyph('crop',stroke('M4 1V12H15'),stroke('M1 4H12V15'))
shape('ruler',transform(rr(1.5,5,13,6,1),-45),transform(lines('M4 5V7','M7 5V8','M10 5V7'),-45))
glyph('scissors',union(ring(4,4,2.5,1.35),ring(4,12,2.5,1.35)),lines('M6 5.5L14 13','M6 10.5L14 3'))
shape('pen-tool',path('M2 14L4 5L10 2L14 6L11 12Z'),union(circle(8,8,1.15),line((2,14),(7.2,8.8)),line((10,2),(14,6))))
shape('pipette',path('M3 10L10 3 13 6 6 13 2 14Z'),stroke('M9 2L14 7M11 2L14 5M4 9L7 12'))
glyph('bold',stroke('M4 2.5V13.5',1.7),stroke('M4 2.5H8.5C12.5 2.5 12.5 7.5 8.5 7.5H4M8.5 7.5C13.5 7.5 13.5 13.5 8.5 13.5H4',1.7))
glyph('italic',lines('M7 2H13','M3 14H9'),line((10,2),(6,14)))
glyph('underline',stroke('M3 2V7A5 5 0 0 0 13 7V2'),line((2,14),(14,14)))
glyph('strikethrough',stroke('M12 3Q5-1 4 4Q3 6 6 7M10 9Q15 10 11 13Q7 16 3 12'),line((1,8),(15,8)))
glyph('font',line((2,13),(8,2),(14,13)),line((4,9),(12,9)))
for name,align in [('align-left','left'),('align-center','center'),('align-right','right'),('align-justify','justify')]:
    ds=[]
    for i,w in enumerate([12,8,12,8]):
        if align=='justify':w=12
        x=2 if align in ['left','justify'] else 14-w if align=='right' else (16-w)/2
        ds.append(line((x,3+i*3),(x+w,3+i*3)))
    glyph(name,union(ds[0],ds[2]),union(ds[1],ds[3]))
glyph('list',dots((2,4),(2,8),(2,12)),lines('M5 4H14','M5 8H14','M5 12H14'))
glyph('list-ordered',lines('M2 2V6','M1 9H3L1 13H3'),lines('M6 4H14','M6 11H14'))
glyph('indent',lines('M2 2H14','M2 14H14','M9 6H14','M9 10H14'),line((2,5),(5,8),(2,11)))
glyph('outdent',lines('M2 2H14','M2 14H14','M9 6H14','M9 10H14'),line((5,5),(2,8),(5,11)))
glyph('wrap',lines('M2 3H14','M2 13H6'),stroke('M2 7H11A3 3 0 0 1 11 13H9M11 10L8 13 11 15'))
glyph('quote',rr(1.5,3,5,5,1),union(rr(9.5,3,5,5,1),stroke('M6.5 8Q6.5 12 2.5 13M14.5 8Q14.5 12 10.5 13')))
glyph('hash',lines('M6 2L4 14','M12 2L10 14'),lines('M2 6H14','M1 10H13'))
shape('text-cursor',rr(1.5,4,8,8,1),lines('M10 2H14','M12 2V14','M10 14H14'))
shape('text-select',rr(2,2,12,12,1),lines('M5 5H11','M8 5V11','M6 11H10'))

CATEGORY='Technology and development'
shape('terminal',WINDOW,lines('M4 6l3 3-3 3','M9 12H12'))
shape('terminal-stack',union(transform(WINDOW,0,.8,-1,-1.5),transform(WINDOW,0,.8,1,1.5)),union(stroke(transform(WINDOW,0,.8,1,1.5),1.2),lines('M6 8l2 2-2 2','M10 12H12')))
shape('code-block',WINDOW,lines('M5 6l-2 2 2 2','M11 6l2 2-2 2','M9 5l-2 6'))
glyph('code',lines('M5 4L1 8 5 12','M11 4L15 8 11 12'),line((9,2),(7,14)))
glyph('braces',stroke('M6 2H5Q4 2 4 4V6Q4 8 2 8Q4 8 4 10V12Q4 14 6 14'),stroke('M10 2H11Q12 2 12 4V6Q12 8 14 8Q12 8 12 10V12Q12 14 10 14'))
glyph('command',union(ring(3.5,3.5,2,1.25),ring(12.5,3.5,2,1.25),ring(3.5,12.5,2,1.25),ring(12.5,12.5,2,1.25)),stroke('M5.5 3.5V12.5M10.5 3.5V12.5M3.5 5.5H12.5M3.5 10.5H12.5',1.25))
shape('cpu',rr(4,4,8,8,1.5),union(rr(6.5,6.5,3,3,.5),lines('M5 1V4M8 1V4M11 1V4M5 12V15M8 12V15M11 12V15M1 5H4M1 8H4M1 11H4M12 5H15M12 8H15M12 11H15',)))
shape('database',path('M2 4C2 0 14 0 14 4V12C14 16 2 16 2 12Z'),stroke('M2 4C2 8 14 8 14 4M2 8C2 12 14 12 14 8'))
shape('server-rack',rr(2,1.5,12,13,2),union(lines('M2 6H14','M2 10H14'),dots((5,4),(5,8),(5,12)),lines('M9 4H11','M9 8H11','M9 12H11')))
shape('cloud',path('M4.2 13C-.2 13 .2 6.5 4.2 6.5C4.3 .7 12.7 .5 13 6.5C17 7 16.5 13 12.3 13Z'))
shape('cloud-upload',DRAWINGS['cloud'][0],transform(arrow(),270,.55,0,1))
shape('cloud-download',DRAWINGS['cloud'][0],transform(arrow(),90,.55,0,1))
shape('monitor',rr(1.5,2,13,9,1.5),lines('M8 11V14','M5 14H11','M2 8H14'))
shape('laptop',rr(3,2,10,9,1),path('M2 11H14L15 14H1Z'))
shape('phone',rr(4,1,8,14,2),union(line((6.5,3),(9.5,3)),line((7,13),(9,13))))
shape('phone-android',rr(4,1,8,14,1.5),union(circle(8,3,.5),dots((6,13),(8,13),(10,13),r=.4)))
shape('simulator',rr(4,1,8,14,2),union(poly([(6.5,5.5),(10,8),(6.5,10.5)]),line((7,13),(9,13))))
shape('tablet',rr(2.5,1,11,14,2),circle(8,12.5,.65))
shape('keyboard',rr(1,4,14,9,1.5),union(dots(*[(x,y) for x in [3.5,6.5,9.5,12.5] for y in [6.5,9]],r=.55),line((5,11),(11,11))))
shape('mouse',rr(4,1,8,14,4),line((8,3.5),(8,6)))
shape('watch',rr(4,4,8,8,2),union(lines('M5 4V1H11V4','M5 12V15H11V12'),line((8,6),(8,8),(10,9))))
shape('printer',rr(1.5,5,13,7,2),union(stroke('M4 5V1.5H12V5M4 10H12V14.5H4Z'),circle(12,7.5,.65)))
shape('usb',path('M5 6H11V14H5Z'),union(stroke('M6 6V1.5H10V6'),line((7,9),(9,9))))
shape('hard-drive',rr(1.5,3,13,10,2),union(line((2,9),(14,9)),dots((11,11),(13,11),r=.5)))
shape('battery',rr(1,4,12,8,1.5),union(rr(3,6,6,4,.5),line((15,6.5),(15,9.5))))
shape('battery-charging',rr(1,4,12,8,1.5),union(poly([(8,4.8),(4,8.5),(7,8.5),(5.5,11.5),(10,7.5),(7,7.5)]),line((15,6.5),(15,9.5))))
glyph('wifi',stroke('M1 5Q8-1 15 5M3.5 8Q8 4 12.5 8M6 11Q8 9 10 11'),circle(8,13,1))
glyph('bluetooth',stroke('M7 1.5V14.5L12 10.5 3 3.5'),stroke('M7 1.5L12 5.5 3 12.5'))
shape('network',union(rr(5.5,1,5,4,1),rr(1,11,5,4,1),rr(10,11,5,4,1)),stroke('M8 5V8H3.5V11M8 8H12.5V11'))
shape('git-branch',union(circle(4,3,1.5),circle(4,13,1.5),circle(12,3,1.5)),stroke('M4 4.5V11.5M12 4.5V5Q12 9 4 9',1.25))
shape('git-merge',union(circle(3.5,3,1.5),circle(3.5,13,1.5),circle(12.5,3,1.5)),stroke('M3.5 4.5V11.5M12.5 4.5V5Q12.5 8.5 6.5 8.5M8.5 6.5L6.5 8.5 8.5 10.5',1.2))
shape('git-pull-request',union(circle(4,3,1.5),circle(4,13,1.5),circle(12,13,1.5)),stroke('M4 4.5V11.5M12 11.5V6Q12 3 9 3M10 1L8 3 10 5',1.25))
shape('git-commit',circle(8,8,3),lines('M1 8H5','M11 8H15'))
shape('bug',rr(4,4,8,10,4),lines('M8 5V13','M5 4L3 2','M11 4L13 2','M4 7H1','M12 7H15','M4 10H1','M12 10H15','M5 13L3 15','M11 13L13 15'))
shape('bot',rr(2,4,12,10,3),union(line((8,1),(8,4)),dots((5.5,8),(10.5,8),r=1),line((6,11),(10,11))))
shape('agents',union(rr(1,2,9,8,2),rr(5,6,9,8,2)),union(stroke(rr(5,6,9,8,2),1.15),dots((7.5,9.5),(11.5,9.5),r=.65),line((8,12),(11,12)),line((5.5,1),(5.5,2))))
shape('brain',path('M8 3C4-1 1 3 2 6C-1 8 1 12 4 12C4 16 8 15 8 13C8 15 12 16 12 12C15 12 17 8 14 6C15 3 12-1 8 3Z'),stroke('M8 3V13M4 5Q4 7 6 7M12 9Q10 9 10 11'))
shape('extension',path('M2 3H6C4.5-.5 11.5-.5 10 3H13V6C16.5 4.5 16.5 11.5 13 10V13H10C11.5 9.5 4.5 9.5 6 13H2V10C5.5 11.5 5.5 4.5 2 6Z'))
shape('wrench',path('M9 2Q12 0 14 2L11 5 12 7 15 4Q16 9 11 10L5 15Q2 16 1 13L7 7Q6 4 9 2Z'),circle(4,12.5,.9))
GEAR_TOOTH=path('M8 8L6.201388 3.657766Q6.75 3.45 6.75 2.95V1.7Q6.75 1.25 7.2 1.25H8.8Q9.25 1.25 9.25 1.7V2.95Q9.25 3.45 9.798612 3.657766Z')
GEAR=union(*(transform(GEAR_TOOTH,i*45) for i in range(8)))
shape('settings',op(GEAR,circle(8,8,2.4),po.PathOp.DIFFERENCE))
glyph('power',stroke('M4.1 3.8A5.8 5.8 0 1 0 11.9 3.8'),line((8,1.5),(8,7.5)))
glyph('spinner',stroke('M13 11A5.8 5.8 0 1 1 8 2.2',1.35),stroke('M8 2.2A5.8 5.8 0 0 1 13.8 8',1.35))
for name,n in [('gauge-low',-70),('gauge-medium',-25),('gauge-high',25),('gauge-max',65)]:
    end=(8+4*math.sin(math.radians(n)),10-4*math.cos(math.radians(n)))
    shape(name,path('M2 13A7 7 0 1 1 14 13Z'),union(line((8,10),end),circle(8,10,1),lines('M3 8H4','M12 8H13')))
shape('logs',WINDOW,union(dots((4,5),(4,8),(4,11),r=.5),lines('M6 5H12','M6 8H10','M6 11H11')))
shape('diff',rr(1.5,2,13,12,2),union(plus(8,5,.7),line((6,11),(10,11))))
glyph('fold-vertical',lines('M2 8H14'),lines('M5 2l3 3 3-3','M5 14l3-3 3 3'))
shape('cursor',path('M3 1.5L14 9 9 10 6 14Z'),line((9,10),(11,14)))
shape('themes',circle(),path('M8 2A6 6 0 0 1 8 14Z'))
shape('lightbulb',path('M5 11C5 9 2.5 8 2.5 6A5.5 5.5 0 0 1 13.5 6C13.5 8 11 9 11 11Z'),lines('M5.5 13H10.5','M6.5 15H9.5','M8 11V7','M6 6l2 1 2-1'))
STAR=path('M8 1.5L10 5.7 14.5 6.3 11.2 9.5 12 14 8 11.8 4 14 4.8 9.5 1.5 6.3 6 5.7Z')
shape('star',STAR)
shape('sparkles',path('M6 3.5Q6.8 8.2 11.5 9Q6.8 9.8 6 14.5Q5.2 9.8 .5 9Q5.2 8.2 6 3.5Z'),union(path('M12 1L13 3.5 15.5 4.5 13 5.5 12 8 11 5.5 8.5 4.5 11 3.5Z'),circle(3,2,.7)))
shape('zap',path('M9 1L2 9H7L6 15 14 6H9Z'))

CATEGORY='Charts and analytics'
for name,detail in [('chart-bar',union(rr(3,8,2.5,5,.5),rr(7,4,2.5,9,.5),rr(11,6,2.5,7,.5))),('chart-line',line((3,11),(6,7),(9,9),(13,4))),('chart-area',poly([(3,12),(3,10),(6,6),(9,8),(13,3),(13,12)])),('trending-up',lines('M2 12L6 8 9 10 14 3','M10 3H14V7')),('trending-down',lines('M2 4L6 8 9 6 14 13','M10 13H14V9'))]: glyph(name,lines('M2 2V14H14'),detail)
shape('chart-pie',circle(),stroke('M8 2V8H14'))
shape('chart-donut',ring(8,8,6,2.5),path('M8 2A6 6 0 0 1 14 8H10.5A2.5 2.5 0 0 0 8 5.5Z'))
shape('activity',WINDOW,line((1.5,8),(5,8),(7,4),(9,12),(11,8),(14.5,8)))
shape('workflow',union(poly([(8,1),(11,4),(8,7),(5,4)]),rr(1,11,5,4,1),rr(10,11,5,4,1)),stroke('M8 7V9H3.5V11M8 9H12.5V11'))
glyph('git-compare',lines('M5 14V2L2 5'),lines('M11 2V14L14 11'))

CATEGORY='Finance and commerce'
shape('credit-card',rr(1.5,3,13,10,2),lines('M1.5 6H14.5','M4 10H7','M10 10H12'))
shape('wallet',rr(1.5,3,13,11,2),union(rr(9,7,5.5,4,1),circle(11,9,.6),stroke('M3 3L11 1V3')))
shape('banknote',rr(1,3,14,10,1),union(ring(8,8,2.3,1.2),dots((3.5,8),(12.5,8))))
shape('coins',path('M2 5C2 2 10 2 10 5V11C10 14 2 14 2 11Z'),stroke('M2 5C2 8 10 8 10 5M2 8C2 11 10 11 10 8M11 7C15 6 16 9 14 10V13Q12 15 9 14'))
shape('receipt',path('M3 1.5L5 3 7 1.5 9 3 11 1.5 13 3V14.5L11 13 9 14.5 7 13 5 14.5 3 13Z'),lines('M5.5 6H10.5','M5.5 9H10.5','M8 12H10.5'))
shape('shopping-bag',rr(2.5,5,11,9,2),stroke('M5 6V4A3 3 0 0 1 11 4V6'))
shape('shopping-cart',path('M3 4H15L13 10H5Z'),union(stroke('M1 1.5H2.5L5 10'),circle(6,13.5,1.2),circle(12,13.5,1.2)))
shape('basket',path('M1 6H15L13 14H3Z'),lines('M4 6L7 2','M12 6L9 2','M6 9V11.5','M10 9V11.5'))
AWNING=path('M3 2H13L14.5 6Q14.5 8 12.3 8Q10.2 8 10.2 6Q10.2 8 8 8Q5.8 8 5.8 6Q5.8 8 3.7 8Q1.5 8 1.5 6Z')
shape('store',union(rr(2.5,6,11,8.5,1),AWNING),union(stroke(AWNING,1.1),stroke('M6.3 14V10H9.7V14',1.1),lines('M6.5 2L5.8 6','M9.5 2L10.2 6')))
shape('tag',path('M2 2H8L14 8Q15 9 14 10L10 14Q9 15 8 14L2 8Z'),circle(5,5,1))
shape('gift',rr(2,6,12,8,1),union(stroke('M8 6V14M1 6H15V9H1ZM8 6C1 6 3 0 6 2L8 6C15 6 13 0 10 2Z',1.2)))
shape('package',path('M1.5 4.5L8 1.5 14.5 4.5V11.5L8 14.5 1.5 11.5Z'),stroke('M1.5 4.5L8 8 14.5 4.5M8 8V14.5M5 3L11.5 6.3'))
shape('barcode',rr(1.5,3,13,10,1),lines('M4 5V11','M6 5V11','M9 5V11','M12 5V11'))
shape('percent',circle(),union(line((5,11),(11,5)),circle(5,5,1),circle(11,11,1)))
shape('dollar',circle(),stroke('M10.5 5Q5 2 5 6Q5 8 8 8Q12 8 11 10Q10 13 5 11M8 3V13',1.2))
shape('euro',circle(),stroke('M11 4Q5 2 5 8Q5 14 11 12M3 7H10M3 9H9',1.2))
shape('pound',circle(),stroke('M5 12H11M4.5 8H10M6 12V6Q6 3 10 4',1.2))

CATEGORY='Work and education'
shape('briefcase',rr(1.5,5,13,9,2),stroke('M5 5V2H11V5M1.5 8Q8 12 14.5 8M8 9V11'))
shape('building',rr(3,1.5,10,13,1),union(dots(*[(x,y) for x in [6,10] for y in [4,7,10]],r=.7),stroke('M6.5 14V12H9.5V14')))
shape('landmark',path('M1 6L8 1.5 15 6Z'),lines('M1 14H15','M3 8V12','M8 8V12','M13 8V12'))
shape('presentation',rr(1.5,2,13,9,1),lines('M8 11V15','M5 15L8 12 11 15','M4 8L7 5 9 7 12 4'))
shape('book',rr(3,1.5,10,13,1),stroke('M3 11H13M5 1.5V11M6.5 5H10'))
shape('book-open',path('M8 3Q4 1 1.5 2V13Q4 12 8 14Q12 12 14.5 13V2Q12 1 8 3Z'),line((8,3),(8,14)))
shape('graduation-cap',path('M1 6L8 2 15 6 8 10Z'),stroke('M4 8V11Q8 15 12 11V8M15 6V11'))
shape('award',circle(8,6,4.5),union(path('M5 10L3 15 8 13 13 15 11 10Z'),circle(8,6,1.5)))
shape('medal',circle(8,10,4.5),union(path('M3 1H6L8 5 10 1H13L10 6H6Z'),circle(8,10,1.5)))
shape('lightbulb-on',DRAWINGS['lightbulb'][0],union(DRAWINGS['lightbulb'][1],lines('M1 2L2 3','M14 3L15 2')))
shape('flask',path('M5 1H11V3H10V7L14 13Q15 15 12 15H4Q1 15 2 13L6 7V3H5Z'),union(line((5,10),(11,10)),dots((7,12),(10,13),r=.5)))
shape('test-tube',path('M4.5 1.5H11.5V10.5A3.5 3.5 0 0 1 4.5 10.5Z'),lines('M3.5 1.5H12.5','M4.5 8H11.5','M9 4.5H11'))
ORBIT=stroke('M8 1A3 7 0 1 0 8 15A3 7 0 1 0 8 1Z',1)
glyph('atom',union(ORBIT,transform(ORBIT,60),transform(ORBIT,-60)),circle(8,8,1.3))
shape('rocket',path('M5 11C4 4 9 1 14 1C15 6 12 12 5 11Z'),union(ring(10,5,1.7,1),stroke('M5 6H2L1 11H5M10 11V14L5 15V11M4 12L2 14')))
glyph('infinity',stroke('M8 8C0-3-3 18 8 8'),stroke('M8 8C19-3 16 18 8 8'))

CATEGORY='Health and fitness'
HEART=path('M8 14L2.7 8.7C-1.2 4.8 4.3 .2 8 4C11.7 .2 17.2 4.8 13.3 8.7Z')
shape('heart',HEART)
shape('heart-pulse',HEART,line((2,8),(5,8),(6.5,5),(8.5,11),(10,8),(14,8)))
shape('medical-cross',rr(),plus(8,8,1.5))
shape('first-aid',rr(1.5,4,13,10,2),union(plus(8,9,1),stroke('M5 4V1.5H11V4')))
shape('pill',transform(rr(4,1,8,14,4),45),transform(line((4,8),(12,8)),45))
glyph('stethoscope',stroke('M2 2V6A4 4 0 0 0 10 6V2M2 2H3M9 2H10'),union(ring(13,8.5,1.6,1.1),stroke('M6 10V11.5Q6 14.5 9.5 14.5T13 11.5V10')))
shape('thermometer',path('M6 3A2 2 0 0 1 10 3V9A3.5 3.5 0 1 1 6 9Z'),union(line((8,5),(8,11)),circle(8,11.5,1.3)))
shape('bandage',transform(rr(1,4,14,8,3),-45),union(transform(rr(5,5.5,6,5,1),-45),transform(dots((3,7),(3,9),(13,7),(13,9),r=.45),-45)))
shape('hospital',union(rr(3.5,1.5,9,13,1),rr(1,7,3,7.5,.5),rr(12,7,3,7.5,.5)),union(plus(8,5,.7),stroke('M6.5 14.5V10.5H9.5V14.5',1.1)))
glyph('dumbbell',union(rr(1,4,3,8,1),rr(12,4,3,8,1)),union(line((4,8),(12,8)),lines('M5 5V11','M11 5V11')))
shape('weight',path('M5 6.5H11L14 13Q14.6 14.5 12.5 14.5H3.5Q1.4 14.5 2 13Z'),stroke('M5.5 6.5V4A2.5 2.5 0 0 1 10.5 4V6.5'))
SOLE=path('M3.8 9.7C1.2 9.2 .8 6.6 2.1 4.3C3.1 2.8 5.8 3.1 5.8 5.4C5.8 6.7 4.2 7.1 4.4 8.5Q4.6 9.7 3.8 9.7Z')
glyph('footprints',union(SOLE,transform(SOLE,0,1,7,-2)),union(rr(2.7,11.2,2.5,2.7,1.2),rr(9.7,9.2,2.5,2.7,1.2)))
shape('bed',rr(1.5,6,13,6,1),union(rr(3,3,4,4,1),rr(9,3,4,4,1),lines('M1.5 3V14','M14.5 8V14','M2 10H14')))
shape('moon',path('M10.7 1.8A6.4 6.4 0 1 0 14.2 10.7A5.2 5.2 0 0 1 10.7 1.8Z'))
shape('apple',path('M8 5C1 1 0 9 4 13C5.5 15 6.5 13.5 8 13.5S10.5 15 12 13C16 9 15 1 8 5Z'),stroke('M8 5Q8 1 11 1'))
shape('droplet',path('M8 1C6 5 2 7 2 10A6 6 0 0 0 14 10C14 7 10 5 8 1Z'),stroke('M5 10Q5 12 7 12'))
shape('lungs',path('M6 5Q3 3 2 8Q-1 15 5 14Q7 13 7 10V5ZM10 5Q13 3 14 8Q17 15 11 14Q9 13 9 10V5Z'),stroke('M8 1V6M5 9L8 6 11 9'))

CATEGORY='Maps and travel'
PIN=path('M8 15C4 10 2 8 2 6A6 6 0 0 1 14 6C14 8 12 10 8 15Z')
shape('map-pin',PIN,ring(8,6,2.1,1.2))
shape('map',path('M1.5 3L6 1.5 10 3 14.5 1.5V13L10 14.5 6 13 1.5 14.5Z'),lines('M6 1.5V13','M10 3V14.5'))
shape('navigation',path('M14 2L9 14 6 9 1 6Z'),line((6,9),(10,5)))
shape('globe',circle(),stroke('M2 8H14M8 2C3 5 3 11 8 14C13 11 13 5 8 2',1.2))
glyph('route',stroke('M3 3H10Q15 3 14 7Q14 10 8 10H6Q2 10 3 14'),union(circle(3,3,1.5),circle(3,14,1.5)))
shape('car',path('M3 6L5 2H11L13 6 14.5 7V12H1.5V7Z'),union(stroke('M3 6H13M2 12V14M14 12V14'),dots((4,9),(12,9),r=.9)))
shape('truck',union(rr(1.5,3,8,8.5,1),path('M9.5 6H12.5L14.5 9V11.5H9.5Z')),union(ring(4.5,12,1.8,1.15),ring(12,12,1.8,1.15),stroke('M9.5 6V11.5M10 8.5H14',1.1)))
shape('bus',rr(3,1.5,10,12,2),union(stroke('M3 6H13M3 10H13M5 1.5V6M11 1.5V6M4 13V15M12 13V15'),dots((5,8),(11,8),r=.65)))
shape('train',rr(3,1,10,12,3),union(stroke('M3 6H13M8 1V6M5 13L3 15M11 13L13 15'),dots((5.5,9.5),(10.5,9.5),r=.8)))
glyph('bicycle',union(ring(4,11,3,1.1),ring(12,11,3,1.1)),stroke('M4 11L7 5 11 5 12 11 7 11 5 4H3M10 2H13',1.2))
shape('plane',path('M8 1Q9 1 9 3V6L15 10V12L9 10V13L11 15H5L7 13V10L1 12V10L7 6V3Q7 1 8 1Z'))
shape('ship',path('M1 9L8 7 15 9 13 13H3Z'),stroke('M4 8V3H12V8M7 3V1H9M1 15Q3 13 5 15Q7 13 9 15Q11 13 13 15H15'))
shape('suitcase',rr(3,4,10,10,2),union(stroke('M6 4V1.5H10V4M5 6V12M11 6V12M5 14V15M11 14V15')))
shape('ticket',path('M1 3H15V6C11 6 11 10 15 10V13H1V10C5 10 5 6 1 6Z'),lines('M10 5V6','M10 8V9','M10 11V12'))
shape('tent',poly([(8,2),(15,14),(1,14)]),stroke('M8 2V14M8 8L4.5 14M8 8L11.5 14'))
shape('mountain',poly([(1,14),(6,3),(9,8),(11,5),(15,14)]),line((4,7.5),(6,9),(7.5,7)))
shape('signpost',poly([(1.5,3),(11.5,3),(14.5,6),(11.5,9),(1.5,9)]),lines('M7 1V3','M7 9V15'))
shape('parking',rr(),stroke('M6 12V4H9A2 2 0 0 1 9 8H6',1.5))
shape('fuel',rr(2,2,8,12,1),union(rr(4,4,4,4,.5),stroke('M10 6H12V12Q15 15 15 11V6L12 3')))

CATEGORY='Weather and nature'
shape('sun',circle(8,8,3.5),lines('M8 1V2','M8 14V15','M1 8H2','M14 8H15','M3 3l1 1','M12 12l1 1','M3 13l1-1','M12 4l1-1'))
shape('sunrise',path('M3 12A5 5 0 0 1 13 12Z'),lines('M1 12H15','M3 14.5H13','M8 1.3V4.8','M5.7 3.6L8 1.3 10.3 3.6','M1 8H2','M14 8H15'))
shape('sunset',path('M3 12A5 5 0 0 1 13 12Z'),lines('M1 12H15','M3 14.5H13','M8 1.3V4.8','M5.7 2.5L8 4.8 10.3 2.5','M1 8H2','M14 8H15'))
for name,detail in [('cloud-rain',lines('M4 12L3 15','M8 12L7 15','M12 12L11 15')),('cloud-snow',dots((4,13),(8,14),(12,13))),('cloud-lightning',path('M9 9L5 13H8L7 16 12 11H9Z')),('cloud-fog',lines('M2 12H14','M4 15H12'))]:
    shape(name,transform(DRAWINGS['cloud'][0],0,.85,0,-2),detail)
SNOW_ARM=stroke('M8 1.5V8M5.8 3.3L8 5.5 10.2 3.3',1.1)
glyph('snowflake',union(*(transform(SNOW_ARM,i*60) for i in range(6))),circle(8,8,1.1))
glyph('wind',stroke('M1 5H10Q14 5 13 2Q12 0 10 2M1 8H13Q16 8 15 11Q14 13 12 11'),stroke('M2 11H7Q10 11 9 14Q8 16 6 14'))
shape('umbrella',path('M1 8A7 7 0 0 1 15 8Q12 6 10 8Q8 6 6 8Q3 6 1 8Z'),stroke('M8 8V12Q8 16 11 14M8 1V2'))
shape('rainbow',path('M1 13V9A7 7 0 0 1 15 9V13H12V9A4 4 0 0 0 4 9V13Z'),stroke('M5.5 13V9A2.5 2.5 0 0 1 10.5 9V13'))
shape('leaf',path('M2 13C0 3 8 1 14 2C15 10 10 16 2 13Z'),stroke('M2 13L11 5M6 9V5M6 9H10'))
shape('tree',path('M8 1L14 7H11L15 12H1L5 7H2Z'),line((8,10),(8,15)))
shape('flower',path('M8 4C3-2-1 5 4 8C-1 13 6 17 8 12C12 17 17 11 12 8C17 3 10-1 8 4Z'),ring(8,8,2.2,1.3))
shape('sprout',path('M8 10C2 10 1 6 2 3C7 3 9 5 8 10C8 4 11 2 15 3C15 8 12 10 8 10Z'),line((8,8),(8,15)))
shape('flame',path('M8 1C7 6 3 4 2 9C0 16 15 17 14 9Q13 5 11 4Q12 8 9 8Q7 7 8 1Z'),path('M8 8C8 11 5 10 5 12C5 16 12 15 11 12Z'))
RECYCLE_ARM=stroke('M5 4L7 1.7Q8 1 8.7 2.2L11 6M8 5.3L11 6 11.5 3',1.15)
glyph('recycle',union(RECYCLE_ARM,transform(RECYCLE_ARM,120)),transform(RECYCLE_ARM,240))
shape('paw',path('M4 11Q8 5 12 11Q15 16 10 14Q8 13 6 14Q1 16 4 11Z'),union(circle(2,6,1.5),circle(6,3,1.5),circle(10,3,1.5),circle(14,6,1.5)))
shape('fish',path('M12 8C8-1 1 3 1 8C1 13 8 17 12 8L15 4V12Z'),union(circle(4,7,.7),stroke('M8 4Q10 8 8 12')))

CATEGORY='Home and food'
shape('coffee',rr(2,5,9,8,2),stroke('M11 6H13Q17 9 11 11M1 15H13M4 1V3M8 1V3'))
shape('cup',path('M3 2H13L11 14H5Z'),line((4,5),(12,5)))
glyph('utensils',stroke('M2 1.5V5Q2 7 4 7T6 5V1.5M4 1.5V14.5'),union(path('M13.5 1.5C10 1.5 9.5 5 9.5 8H13.5Z'),line((13.5,1.5),(13.5,14.5))))
shape('pizza',path('M1 3Q8-1 15 3L8 15Z'),union(stroke('M2 5Q8 2 14 5'),dots((6,7),(10,6),(8,11),r=.8)))
shape('cake',rr(2,7,12,7,1),union(stroke('M2 10Q4 12 6 10Q8 12 10 10Q12 12 14 10M5 7V4M11 7V4'),circle(5,2,.8),circle(11,2,.8)))
shape('wine',path('M4 1.5H12V6A4 4 0 0 1 4 6Z'),stroke('M8 10V14M5 14H11M4 5H12'))
shape('bottle',path('M6 1H10V5L12 8V14H4V8L6 5Z'),lines('M6 3H10','M4 10H12'))
shape('chef-hat',path('M4 9C-1 9 0 3 4 3Q8-2 12 3C16 3 17 9 12 9V14H4Z'),stroke('M4 11H12M7 8V10M10 7V10'))
shape('sofa',rr(3,3,10,8,2),union(rr(1,7,4,6,1),rr(11,7,4,6,1),lines('M5 10H11','M3 13V15','M13 13V15')))
shape('lamp',path('M5 2H11L14 9H2Z'),lines('M8 9V14','M5 14H11'))
shape('door-open',path('M3 3L11 1V15L3 13Z'),union(stroke('M11 3H14V13H11'),circle(8.5,8,.65)))
shape('key-round',circle(5,5,3.5),union(circle(5,5,1),stroke('M7.5 7.5L14 14H11V11H9V9')))
shape('plug',rr(4,5,8,5,2),stroke('M5.5 1V5M10.5 1V5M8 10V15'))
BLADE=path('M7.2 7.3C3 7 2.5 3 5.2 2.5C8.8 1.5 10.5 4.5 8.7 7.5Z')
shape('fan',circle(8,8,6),union(*(transform(BLADE,i*120) for i in range(3)),circle(8,8,1)))
shape('gamepad',path('M4 4H12Q14 4 15 11Q16 15 12 13L10 11H6L4 13Q0 15 1 11Q2 4 4 4Z'),union(plus(5,8,.65),dots((10.5,7),(12.5,9),r=.7)))
shape('puzzle',DRAWINGS['extension'][0])
glyph('music-note',DRAWINGS['music'][0],DRAWINGS['music'][1])
shape('bell-ring',BELL,union(line((6,14),(10,14)),lines('M1 3L2 2','M14 2L15 3')))

CATEGORY='Editing and design'
glyph('paperclip',stroke('M11 6L6 11Q4 12 4 10L10 4Q13 1 14 5Q15 7 12 10L8 14Q3 17 1 12Q0 9 3 6L8 1'),stroke('M10 4L4 10Q4 12 6 11L11 6'))
CATEGORY='Technology and development'
glyph('ssh',lines('M1.5 5V1.5H5','M11 14.5H14.5V11'),transform(arrow(),scale=.75))
CATEGORY='Actions and status'
shape('refresh-circle-fill',circle(),transform(union(DRAWINGS['refresh'][0],DRAWINGS['refresh'][1]),scale=.62))

CATEGORY='Actions and status'
glyph('menu',lines('M2 3H14','M2 13H14'),line((2,8),(14,8)))
CATEGORY='Technology and development'
for name,level in [('battery-full',8),('battery-low',2),('battery-empty',0)]:
    shape(name,rr(1,4,12,8,1.5),union(rr(3,6,level,4,.5) if level else po.Path(),line((15,6.5),(15,9.5))))
glyph('wifi-off',DRAWINGS['wifi'][0],union(DRAWINGS['wifi'][1],line((2,2),(14,14))))
glyph('bluetooth-off',DRAWINGS['bluetooth'][0],union(DRAWINGS['bluetooth'][1],line((2,2),(14,14))))
shape('cloud-off',DRAWINGS['cloud'][0],line((2,2),(14,14)))
shape('git-fork',union(circle(3,3,1.7),circle(13,3,1.7),circle(8,13,1.7)),stroke('M3 5V6Q3 8 8 8Q13 8 13 6V5M8 8V11'))
CATEGORY='Files and folders'
for name,angle in [('folder-upload',270),('folder-download',90)]:shape(name,FOLDER,transform(arrow(),angle,.5,0,2))
for name,angle in [('file-upload',270),('file-download',90)]:shape(name,FILE,union(FOLD,transform(arrow(),angle,.45,0,2)))
CATEGORY='Communication'
for name,detail in [('mail-check',check(8,9.8,.55)),('mail-plus',plus(8,9.8,.6))]:
    shape(name,rr(1.5,3,13,10,2),union(line((2,4),(8,6.3),(14,4)),detail))
shape('bell-plus',BELL,union(plus(8,7,.7),line((6,14),(10,14))))
CATEGORY='Media'
shape('image-plus',DRAWINGS['image'][0],union(line((2,12),(6,8),(10,12)),plus(11,5,.65)))
for name,angle in [('fast-forward',0),('rewind',180)]:
    glyph(name,transform(poly([(1.5,3),(8,8),(1.5,13)]),angle),transform(poly([(8,3),(14.5,8),(8,13)]),angle))
CATEGORY='Security'
shape('scan-face',rr(3.5,3.5,9,9,3),union(lines('M1 5V1H5','M11 1H15V5','M1 11V15H5','M11 15H15V11','M6 10Q8 12 10 10'),dots((6,6.5),(10,6.5),r=.55)))
shape('shield-lock',SHIELD,union(rr(5.5,7,5,4,1),stroke('M6.5 7V5.5A1.5 1.5 0 0 1 9.5 5.5V7',1.1)))
CATEGORY='Editing and design'
glyph('text-size',lines('M1 4H9','M5 4V13'),lines('M10 8H15','M12.5 8V13'))
for name,mark in [('heading-1',stroke('M12 6L14 4V13')),('heading-2',stroke('M11 6Q11 3 14 4Q16 5 13 8L11 12H15'))]:
    glyph(name,lines('M2 3V13','M8 3V13','M2 8H8'),mark)
CATEGORY='Time and planning'
shape('bookmark-check',path('M4 2H12V14L8 11 4 14Z'),check(8,6,.55))
shape('calendar-heart',CAL,union(CALTOP,path('M8 12.5L5 10C3.5 8 6 7 8 9C10 7 12.5 8 11 10Z')))
CATEGORY='Finance and commerce'
shape('yen',circle(),stroke('M5 4L8 8 11 4M8 8V12M5 8H11M5 10H11',1.1))

# Format glyph corrections found during the individual legacy-art review.
# Retain the existing brand-container treatment and attribution.
BRAND_REFINEMENTS={
    'svg':stroke('M5.5 5.5Q2.5 4.5 2.5 6.5Q2.5 7.5 4 8Q6 8.5 5 10Q4 11.5 2 10M6.5 5.5L8 10.5 9.5 5.5M14 6Q11 4.5 11 8Q11 11.5 14 10V8.5H12.7',.8),
    'html':op(poly([(3.5,3),(12.5,3),(11.2,12),(8,13),(4.8,12)]),stroke('M10.3 5H6L5.7 8H10L9.6 10.5 8 11 6.2 10.5',1.05),po.PathOp.DIFFERENCE),
    'yml':stroke('M3 4.5L5 7.5 7 4.5M5 7.5V11.5M9 5H13M9 8H13M9 11H12',1.1),
}


def svg_path(p):
    pen=SVGPathPen(None,ntos=lambda v:format(v,'.4f').rstrip('0').rstrip('.') if v else '0')
    p.draw(pen)
    return pen.getCommands()

def svg(layers):
    rows=['<svg fill="none" viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg">']
    for p,opacity in layers:
        if not p:continue
        rows.append(f'  <path d="{svg_path(p)}" fill="currentColor"'+(f' opacity="{opacity}"' if opacity!=1 else '')+'/>')
    return '\n'.join(rows+['</svg>',''])


def svg_comparison_key(text):
    """Ignore only the order of identical closed contours in recipe checks.

    Skia can emit disjoint contours in a different order on Linux/x86 and
    macOS/ARM. Filled closed contours have the same winding result in either
    order. Keep every command, coordinate, winding direction, layer order and
    attribute byte exact. Canonical distributed SVG bytes remain unchanged.
    """
    def sort_closed_contours(match):
        data=match.group(1)
        contours=re.findall(r'M[^M]*',data)
        if not contours or ''.join(contours)!=data or any(not c.endswith('Z') for c in contours):
            return match.group(0)
        return ' d="'+''.join(sorted(contours))+'"'
    return re.sub(r' d="([^"]*)"',sort_closed_contours,text)


def components(p):
    """Connected filled components, keeping counters with their outer contour."""
    contours=list(po.simplify(p).contours)
    outer=[c for c in contours if not c.clockwise]
    for hole in (c for c in contours if c.clockwise):
        parents=[i for i,c in enumerate(outer) if op(c,hole,po.PathOp.INTERSECTION).area >= hole.area*.999]
        if parents:
            i=min(parents,key=lambda i:outer[i].area)
            outer[i]=op(outer[i],hole,po.PathOp.DIFFERENCE)
    return outer

def stacked_solid(back,front,detail=None):
    rear=union(back,stroke(back,1.25));fore=union(front,stroke(front,1.25))
    clearance=union(fore,stroke(fore,1.5))
    if detail:
        inset=op(fore,stroke(fore,1.8),po.PathOp.DIFFERENCE)
        fore=op(fore,op(detail,inset,po.PathOp.INTERSECTION),po.PathOp.DIFFERENCE)
    return union(op(rear,clearance,po.PathOp.DIFFERENCE),fore)

def main():
    check_mode='--check' in sys.argv
    failed=[]
    def write(p,text):
        target=ROOT/p
        if check_mode:
            if not target.exists() or svg_comparison_key(target.read_text())!=svg_comparison_key(text):
                failed.append(str(p))
        else:
            target.parent.mkdir(parents=True,exist_ok=True);target.write_text(text)
    catalog=[]
    for name,(b,d,outline,category,tags) in sorted(DRAWINGS.items()):
        outer=stroke(b,1.25) if outline else po.Path()
        # Filled bodies carry the secondary tone; contours and identifying
        # details share the primary tone. Union prevents opacity stacking.
        boundary=op(outer,d,po.PathOp.DIFFERENCE) if outer else po.Path()
        duo=[(op(b,union(boundary,d),po.PathOp.DIFFERENCE),.24),(union(boundary,d),1)] if outline else [(op(b,d,po.PathOp.DIFFERENCE),.4),(d,1)]
        mono=union(outer,d) if outline else union(b,d)
        # Large closed detail regions need their own contour in Stroke; a
        # filled basket or folder flap would otherwise hide the interior.
        if name in {'folder-open','video-call','picture-in-picture','headphones'}:
            mono=union(outer,stroke(d,1.1))
        elif name in {'layers','skip-forward','skip-back','fast-forward','rewind'}:
            mono=union(stroke(b,1.25),stroke(d,1.25))
        elif name == 'qr-code':
            mono=union(outer,lines('M10 10H14V14H12','M10 13V14'))
        elif name == 'quote':
            mono=union(stroke(b,1.25),stroke(rr(9.5,3,5,5,1),1.25),stroke('M6.5 8Q6.5 12 2.5 13M14.5 8Q14.5 12 10.5 13'))
        if outline:
            filled=union(b,outer)
            # Structural details remain attached. Only interior details become
            # counters; never XOR a handle, stem, wheel or connector off its body.
            interior=op(filled,stroke(filled,1.8),po.PathOp.DIFFERENCE)
            structural=[];counters=[]
            for component in components(d):
                exterior=op(component,filled,po.PathOp.DIFFERENCE)
                if exterior.area > component.area*.12:
                    structural.append(component)
                else: counters.append(component)
            cut=op(union(*counters),interior,po.PathOp.INTERSECTION)
            solid=union(op(filled,cut,po.PathOp.DIFFERENCE),*structural)
        else: solid=union(b,d)
        if name in {'skip-forward','skip-back'}:
            mono=union(stroke(b,1.15),d)
        if name in {'fast-forward','rewind'}:
            mono=union(stroke(b,1.05),stroke(d,1.05))
        if name in {'thumbs-up','thumbs-down'}:
            mono=union(outer,stroke(d,1.1))
        if name in {'chart-bar','chart-area'}:
            mono=union(b,stroke(d,1.05))
        if name == 'fan': mono=union(outer,stroke(d,1.05))
        if name == 'utensils':
            knife=path('M13.5 1.5C10 1.5 9.5 5 9.5 8H13.5Z')
            mono=union(b,stroke(knife,1.2),line((13.5,8),(13.5,14.5)))
        if name == 'chart-donut':
            # Preserve the central aperture in every style. The quarter segment
            # is a filled annular sector, not a second opaque disc.
            annulus=op(circle(8,8,6),circle(8,8,3.3),po.PathOp.DIFFERENCE)
            sector=op(annulus,rr(8,1,7,7,.01),po.PathOp.INTERSECTION)
            duo=[(op(annulus,sector,po.PathOp.DIFFERENCE),.3),(sector,1)]
            solid=op(annulus,lines('M8 1.5V4.7','M11.3 8H14.5'),po.PathOp.DIFFERENCE)
            mono=union(stroke(circle(8,8,6),1.1),stroke(circle(8,8,3.3),1.1),lines('M8 2V4.7','M11.3 8H14'))
        if name == 'lungs':
            solid=union(op(union(b,outer),stroke('M5 9L7 7M9 7L11 9',1.1),po.PathOp.DIFFERENCE),line((8,1),(8,6)))
        if name == 'hourglass':
            solid=op(union(b,outer),union(rr(5.4,4,5.2,1.4,.5),poly([(6,12),(8,10),(10,12)])),po.PathOp.DIFFERENCE)
        if name == 'bed':
            solid=op(solid,stroke('M3 10H13',1.1),po.PathOp.DIFFERENCE)
        if name == 'printer':
            solid=op(solid,rr(5,10.7,6,3.1,.3),po.PathOp.DIFFERENCE)
        if name == 'folder-open':
            flap=soften(path('M2 7H14Q15 7 14.5 8.5L13 13H3Z'))
            solid=union(op(union(b,outer),union(flap,stroke(flap,1.4)),po.PathOp.DIFFERENCE),flap)
        if name == 'airplay':
            foreground=poly([(8,8),(13,14),(3,14)])
            clearance=union(foreground,stroke(foreground,1.5))
            solid=union(op(union(b,outer),clearance,po.PathOp.DIFFERENCE),foreground)
        if name == 'copy':
            solid=stacked_solid(rr(1.5,1.5,9,10,1.7),rr(5,5,9.5,9.5,1.7))
        if name == 'folders':
            solid=stacked_solid(transform(FOLDER,0,.8,-1,-2),transform(FOLDER,0,.8,1,1.5))
        if name == 'terminal-stack':
            solid=stacked_solid(transform(WINDOW,0,.8,-1,-1.5),transform(WINDOW,0,.8,1,1.5),lines('M6 8l2 2-2 2','M10 12H12'))
        if name == 'multiplexer':
            solid=stacked_solid(rr(1.5,1.5,9.5,9.5,2),rr(5,5,9.5,9.5,2),lines('M10 5V14.5','M5 10H14.5'))
        if name == 'swatch':
            solid=stacked_solid(stacked_solid(SWATCH,SWATCH_DIAGONAL),rr(2,9.5,12,4.5,1),circle(4.25,11.75,.65))
        if name == 'store':
            solid=op(union(b,outer),union(rr(6.3,10,3.4,6,.2),stroke('M6.5 2L5.8 6M9.5 2L10.2 6',.8)),po.PathOp.DIFFERENCE)
        if name in {'camera-off','microphone-off','bell-off','cloud-off','bluetooth-off','wifi-off','eye-off'}:
            slash=line((2,2),(14,14)); clearance=line((2,2),(14,14),width=2.65)
            duo=[(op(p,clearance,po.PathOp.DIFFERENCE),a) for p,a in duo]+[(slash,1)]
            mono=union(op(mono,clearance,po.PathOp.DIFFERENCE),slash)
            solid=union(op(solid,clearance,po.PathOp.DIFFERENCE),slash)
        write(Path('icons')/(name+'.svg'),svg(duo))
        for style,layers in {
            'solid':[(solid,1)],
            'stroke':[(mono,1)],
        }.items():
            write(Path('icons/styles')/style/(name+'.svg'),svg(layers))
        catalog.append(dict(name=name,category=category,tags=tags.split(),origin='original',styles=['duotone','solid','stroke']))
    brands=json.loads((ROOT/'scripts/icons/brands.json').read_text())
    actual={p.stem for p in (ROOT/'icons').glob('*.svg')}
    unknown=actual-set(DRAWINGS)-set(brands)
    if unknown:failed.append('Uncategorized artwork: '+', '.join(sorted(unknown)))
    for name in brands:
        file=ROOT/'icons'/(name+'.svg')
        if name in BRAND_REFINEMENTS:
            frame=path('M8 0C1.42 0 0 1.42 0 8S1.42 16 8 16S16 14.58 16 8S14.58 0 8 0Z')
            write(file.relative_to(ROOT),svg([(frame,.2),(BRAND_REFINEMENTS[name],1)]))
        r=ET.parse(file).getroot()
        if not any(0<float(n.get('opacity','1'))<1 for n in r.iter()):
            failed.append('Unreviewed single-tone icon: '+file.stem)
        catalog.append(dict(name=file.stem,category='Brands',tags=[],origin='legacy',styles=['duotone']))
    write(Path('catalog.json'),json.dumps(sorted(catalog,key=lambda i:i['name']),indent=2)+'\n')
    if failed:sys.exit('\n'.join(failed))
    print(f'{len(DRAWINGS)} original drawings; {len(catalog)} total icons')
if __name__=='__main__':main()
