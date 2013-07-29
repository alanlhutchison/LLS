#!/usr/bin/env python

from Parser import NodeParser
import unittest

class ExtractNodes(unittest.TestCase):
    """Make sure nodes are pulled out correctly"""
    def setUp(self):
        self.parser = NodeParser()
    def test_commas(self):
        """Make sure that commas are in the file"""
        test_passes = False
        try: 
            self.parser.extract_nodes("no_commas")
            test_passes = False
        except Exception as e:
            print(e)
            test_passes = True
        self.assertTrue(test_passes)
    def test_no_empty(self):
        """Make sure there are no empty nodes"""
        test_passes = False
        try:
            self.parser.extract_nodes("all_commas")
            test_passes = False
        except:
            test_passes = True
        self.assertTrue(test_passes)

    def test_find_node(self):
        """Make sure there are only alphanumeric nodes in file"""
        test_passes = False
        try:
            self.parser.extract_nodes("bad_nodes")
            test_passes = False
        except Exception:
            test_passes = True
        self.assertTrue(test_passes)

    def test_assign_node_num(self):
        """Give every node a number value in dict"""

class ExtractEdges(unittest.TestCase)

    def test_read_random_edges(self):
        """Make sure the edges are entered correctly
        Should be in a Node, (Node,#),(Node, #) format)"""
        pass

    def 


    



if __name__ == "__main__":
    unittest.main()
