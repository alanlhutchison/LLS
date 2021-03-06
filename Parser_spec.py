#!/usr/bin/env python

from Parser import NodeParser
from Parser import EdgeParser
from Parser import LLS_Calculator
import unittest
import random
import string

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
        """Make sure there are commas in file"""
        test_passes = False
        try:
            self.parser.extract_nodes("all_commas")
            test_passes = False
        except Exception:
            test_passes = True
        self.assertTrue(test_passes)

    def test_nodes_unique(self):
        """Make sure nodes are unique in list"""
        test_list = []
        for _ in xrange(random.randint(2,100)):
            stng = "".join(random.choice(string.ascii_uppercase + string.digits) for _ in xrange(random.randint(1,10)))
            test_list.append(stng)
        test_string = ",".join(test_list)
        #print test_string
        nodes = self.parser.string_to_nodes(test_string)
        for i in xrange(len(nodes)-1):
            self.assertNotEquals(nodes[i],nodes[i+1])

    def test_assign_no(self):
        """Does assign_no_to_node give dict and list?"""
        test_list = []
        for i in xrange(random.randint(1,100)):
            stng = "".join(random.choice(string.ascii_uppercase + string.digits) for _ in xrange(random.randint(1,10)))
            test_list.append(stng)
        test_string = ",".join(test_list)
        nodes = self.parser.string_to_nodes(test_string)
        dict,size_d = self.parser.assign_no_to_node(nodes)
        nodes = sorted(nodes)
        #print dict
        #print nodes
        for i,node in enumerate(nodes):
            #print i,node,dict[node]
            self.assertEquals(dict[node],i)
            
    def test_assign_node_num(self):
        """Give every node a number value in dict"""
        test_list = []
        for i in xrange(random.randint(2,100)):
            stng = "".join(random.choice(string.ascii_uppercase + string.digits) for _ in xrange(random.randint(1,10)))
            test_list.append(stng)
        test_string = ",".join(test_list)
        nodes = self.parser.string_to_nodes(test_string)
        dict,size_d = self.parser.assign_no_to_node(nodes)
        for item in nodes:
            self.assertTrue(item in dict)


    def test_CompareNodes(self):
        """Does CompareNodes find nodes in the list?"""
        test_list = []
        for i in xrange(random.randint(1,100)):
            stng = "".join(random.choice(string.ascii_uppercase + string.digits) for _ in xrange(random.randint(1,10)))
            test_list.append(stng)
        self.assertTrue(self.parser.CompareNodes(test_list[random.randint(0,len(test_list)-1)],test_list))
        
class ExtractEdges(unittest.TestCase):

    def setUp(self):
        self.parser = EdgeParser()

    def test_read_random_edges(self):
        """Make sure the edges are entered correctly
        Should be in a Node, (Node,#),(Node, #) format)"""
        test = []
        for __ in xrange(random.randint(2,10)):
            test_list = []
            for _ in xrange(random.randint(2,10)):
                stng = "".join(random.choice(string.ascii_uppercase + string.digits) for _ in xrange(random.randint(1,10)))
                test_list.append(stng)
            test.append(test_list)
        file = ""
        line = ""
        for i in xrange(len(test)):
            line = ""
            for j in xrange(len(test[i])):
                if j == 0:
                    line = test[i][j]
                else:
                    line = line +",("+ test[i][j]+","+str(random.random())+")"
            file = file + line + "\n"
        prepared = file.split("\n")
        d = {}
        for line in prepared:
            if line == "":
                pass
            else:
                d = self.parser.line_to_edges(line,d)
        for i in xrange(len(test)):
            lead = test[i][0].split(",")[0]
            self.assertTrue(lead in d)

        def test_EdgeNode2Num(self):
            """Does EdgeNode2Num work the way we want it to?"""
            pass


class LLS_test(unittest.TestCase):
    """Does LLS work properly"""
    def setUp(self):
        self.calc = LLS_Calculator()
    def test_CompareEdges(self):
        """Does CompareEdges work?"""
        d = {}
        for _ in xrange(random.randint(1,10)):
            lead = ""
            for __ in xrange(0,random.randint(2,10)):
                stng = "".join(random.choice(string.ascii_uppercase + string.digits) for ___ in xrange(random.randint(1,10)))
                if lead == "":
                    lead = stng
                    d.setdefault(lead,[])
                else:
                    d[lead].append((stng,random.random()))
            for lead in d.keys():
                opp = d[lead][random.randint(0,len(d[lead])-1)][0]
                self.assertTrue(self.calc.CompareEdges((lead,opp),d))


    def test_num(self):

        d = {}
        for _ in xrange(random.randint(1,10)):
            lead = ""
            for __ in xrange(0,random.randint(2,10)):
                stng = "".join(random.choice(string.ascii_uppercase + string.digits) for ___ in xrange(random.randint(1,10)))
                if lead == "":
                    lead = stng
                    d.setdefault(lead,[])
                else:
                    d[lead].append((stng,random.random()))        

        nodes = []
        #print d
        for lead in d.keys():
            if lead not in nodes:
                nodes.append(lead)
            for hit in d[lead]:
                #print 'hit[0] is ',hit[0]
                if hit[0] not in nodes:
                    nodes.append(hit[0])

                
        data = {}
        for _ in xrange(random.randint(1,10)):
            for lead in d.keys():
                data.setdefault(lead,[])
                for __ in xrange(random.randint(1,len(d[lead]))):
                    edge = d[lead][random.randint(0,len(d[lead])-1)]
                    data[lead].append(edge)
                    for ___ in xrange(random.randint(0,5)):
                        stng = "".join(random.choice(string.ascii_uppercase + string.digits) for ___ in xrange(random.randint(1,10)))
                        edge = (stng,random.random())
                        data[lead].append(edge)
        
        for lead in data.keys():
            if lead not in nodes:
                nodes.append(lead)
            for hit in data[lead]:
                #print 'hit[0] is ',hit[0]
                if hit[0] not in nodes:
                    nodes.append(hit[0])

        length = len(nodes)
        gold = d
        
        
        self.assertGreater(self.calc.numerator(data,gold),0)
        self.assertEquals(type(self.calc.numerator(data,gold)),float)

        self.assertGreater(self.calc.denominator(gold,length),0)
        self.assertEquals(type(self.calc.denominator(data,length)),float)

        self.assertNotEquals(self.calc.LLS(self.calc.numerator(data,gold),self.calc.denominator(gold,length)),0)
        self.assertEquals(type(self.calc.LLS(self.calc.numerator(data,gold),self.calc.denominator(data,length))),float)
        

    def returns_float(self):
        """Prob calculators return a float"""
        num = random.random()
        denom = random.random()
        self.assertTrue(type(self.calc.LLS(num,denom)),float)
                
if __name__ == "__main__":
    unittest.main()
