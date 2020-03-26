#!/usr/bin/python

import json
import xml.etree.ElementTree as ET
from collections import defaultdict
import re


class FilterModule(object):

    def etree_to_dict(self, t):
        d = {t.tag: {} if t.attrib else None}
        children = list(t)
        if children:
            dd = defaultdict(list)
            for dc in map(self.etree_to_dict, children):
                for k, v in dc.items():
                    dd[k].append(v)
            d = {t.tag: {k: v[0] if len(v) == 1 else v
                         for k, v in dd.items()}}
        if t.attrib:
            d[t.tag].update(('@' + k, v)
                            for k, v in t.attrib.items())
        if t.text:
            text = t.text.strip()
            if children or t.attrib:
                if text:
                  d[t.tag]['#text'] = text
            else:
                d[t.tag] = text
        return d

    def filters(self):
        return {
            'from_xml': self.from_xml,
            'xml_to_json': self.xml_to_json,
            'xml_sub_elem': self.xml_sub_elem
        }
    
    def xml_sub_elem(self,data,elem,ns):
        root = ET.fromstring(data)
        c=root.find(elem,ns)
        if c:
            return ET.tostring(c,encoding='unicode')
        else:
            return "Empty"

    def from_xml(self, data):
        root = ET.ElementTree(ET.fromstring(data)).getroot()
        return self.etree_to_dict(root)

    def xml_to_json(self, data):
        return json.dumps(self.from_xml(data))

