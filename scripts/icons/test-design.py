#!/usr/bin/env python3
"""Design regressions discovered by the native per-icon visual audit.

Requires the pinned authoring dependencies, not needed by consumers.
"""
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET
import draw as art

ROOT=Path(__file__).resolve().parents[2]
def layers(name,style='duotone'):
    p=ROOT/'icons'/((name+'.svg') if style=='duotone' else f'styles/{style}/{name}.svg')
    return [(art.path(n.get('d')),float(n.get('opacity','1'))) for n in ET.parse(p).getroot()]
def ink(name,style='solid'):return art.union(*(p for p,a in layers(name,style)))

class DesignRegressionTests(unittest.TestCase):
    def test_arrow_shafts_touch_their_heads(self):
        for direction in ['left','right','up','down','up-left','up-right','down-left','down-right']:
            name='arrow-'+direction
            b,d,*_=art.DRAWINGS[name]
            self.assertGreater(art.op(b,d,art.po.PathOp.INTERSECTION).area,.4,name)
            for style in ['duotone','solid','stroke']:
                self.assertEqual(len(art.components(ink(name,style))),1,(name,style))

    def test_redo_and_left_rotation_are_mirrored_not_rotated(self):
        for left,right in [('undo','redo'),('rotate-left','rotate-right')]:
            for style in ['duotone','solid','stroke']:
                diff=art.op(art.mirror(ink(left,style)),ink(right,style),art.po.PathOp.XOR)
                self.assertLess(diff.area,.015,(left,right,style))

    def test_rotation_secondary_arc_survives_boolean_composition(self):
        # Previously a valid nonempty SVG lost almost its entire secondary arc.
        for name in ['refresh','reset','rotate-left','rotate-right']:
            secondary=art.union(*(p for p,a in layers(name) if a<1))
            self.assertGreater(secondary.area,25,name)
            self.assertGreater(secondary.bounds[3]-secondary.bounds[1],9,name)

    def test_structural_solid_connections_do_not_turn_into_cutout_fragments(self):
        for name in ['lock','trophy','network','workflow','watch','calendar','cpu','bug','signpost']:
            components=art.components(ink(name))
            self.assertEqual(len(components),1,(name,[p.area for p in components]))

    def test_counters_remain_open(self):
        for style in ['duotone','solid','stroke']:
            for name,point in [('settings',(8,8)),('chart-donut',(8,8)),('scissors',(4,4))]:
                self.assertFalse(ink(name,style).contains(point),(name,style))

    def test_solid_identifying_details_survive_structural_classification(self):
        for name,point in [('hourglass',(8,4.7)),('bed',(8,10)),('printer',(8,12)),('lungs',(5.5,8.5))]:
            self.assertFalse(ink(name).contains(point),name)
        # Overlapping cards have filled faces, with clearance around the rear.
        for name,point in [('copy',(9,9)),('folders',(8,10)),('airplay',(8,12))]:
            self.assertTrue(ink(name).contains(point),name)

    def test_rotational_families_are_symmetric(self):
        for name,angle in [('settings',45),('snowflake',60)]:
            shape=ink(name,'stroke')
            diff=art.op(shape,art.transform(shape,angle),art.po.PathOp.XOR)
            self.assertLess(diff.area,.08,name)

    def test_default_layers_do_not_compound_alpha(self):
        for name in art.DRAWINGS:
            source=layers(name)
            for i,(a,alpha) in enumerate(source):
                for b,beta in source[i+1:]:
                    overlap=art.op(a,b,art.po.PathOp.INTERSECTION).area
                    self.assertLess(overlap,.02,(name,overlap))

    def test_non_special_default_compositions_preserve_ink(self):
        special={'chart-donut','camera-off','microphone-off','bell-off','cloud-off','bluetooth-off','wifi-off','eye-off'}
        for name,(body,detail,outlined,*_) in art.DRAWINGS.items():
            if name in special:continue
            expected=art.union(body,detail,art.stroke(body,1.25) if outlined else art.po.Path())
            actual=ink(name,'duotone')
            self.assertLess(abs(expected.area-actual.area),.04,name)

if __name__=='__main__':unittest.main()
