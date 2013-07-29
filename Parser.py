#!/usr/bin/env python

import re
import sys

def main():
    fn = sys.argv[1]
    #a = NodeParser()
    #a.extract_nodes(fn)
    b = EdgeParser()
    b.extract_edges(fn)
class NodeParser():
    """Will read nodes from CSV file"""
    def extract_nodes(self,fn):
        """From fn, get csv nodes"""
        with open(fn,'r') as f:
            line = f.readline()
            assert "," in line
            assert re.search("[\W][^,]",line) is None
            nodes = line.split(",")
            nodes = [node for node in nodes if (node!="")]
            print nodes
        assert nodes != []
        nodes = sorted(nodes)
        return nodes

class EdgeParser():
    """Will read edegs from a CSV file"""
    def extract_edges(self,fn):
        """From fn, get edges"""
        new_edges = {}
        with open (fn,'r') as f:
            for line in f:
                try:
                    assert "," in line
                    assert "(" in line
                    assert ")" in line
                except Exception as e:
                    print(e)
                    pass
                edges = line.split("(")
                
                lead = edges[0].strip()
                lead = lead.strip(",")
                new_edges.setdefault(lead,[])
                for edge in edges[1:]:
                    edge = edge.strip("\n")
                    edge = edge.strip(" ")
                    edge = edge.strip(",")
                    edge = edge.strip("\)")
                    edge = edge.split(",")
                    new_edges[lead].append(edge)
        print new_edges

if __name__=="__main__":
    main()

