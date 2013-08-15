#!/usr/bin/env python

import sys
from math import log
import numpy as np
from numpy import matrix 
import scipy
from scipy import sparse
import random
import string as st
from operator import itemgetter
import pickle
import time

import cProfile
import memory_profiler

def main():
    fn_dict = sys.argv[1]
    fn_gold = sys.argv[2]
    fns_exp = sys.argv[3:]

    input_spear_staph(fn_dict,fn_gold,fns_exp)
    #input2(fn_dict,fn_gold,fns_exp)

@profile
def input_spear_staph(fn_dict,fn_gold,fns_exp):

    edge_maker = simple_thresh
    d_nodes = node_parser(fn_dict)    
    d_gold_edges = simple_edge_parser(fn_gold)
    m_gold = dict2matrix(d_nodes,d_gold_edges,fn_gold+".Graph")
    g_gold = Graph(d_nodes,m_gold,edge_maker)

    #gs_exp = []
    """Next will be to make these different parsing choices flags"""

    ### TURN THIS INTO A MAP
    ### CAN'T BECAUSE NEED TWO INPUT FUNCTIONs
    #gs_exp = map(file2graph,fns_exp)

    gold_bin = g_gold.give_edges()
    del g_gold
    

    results = serial_LLS_comparison(d_nodes,gold_bin,fns_exp,edge_maker,fn_gold)
    serial_weighted_sum(results,fn_gold)
    
def serial_LLS_comparison(d_nodes,gold_bin,fns_exp,edge_maker,fn_gold):
    results = []
    print fns_exp
    for fn in fns_exp:
        print fn
        #d_exp_edges = simple_edge_parser(fn)
        d_exp_edges = ThreePartEdgeParser(fn)
        m_exp = dict2matrix(d_nodes,d_exp_edges,fn+".Graph")
        del d_exp_edges
        print 'Starting Graph ',time.time()
        g_exp = Graph(d_nodes,m_exp,edge_maker)
        del m_exp
        print 'Finishing Graph', time.time()

        LLS = compare_graphs(g_exp,gold_bin)
        output = fn+"__"+fn_gold+".pkl"
        results.append([LLS,output])
        print fn
        with open(fn+"__"+fn_gold+".pkl",'w') as g:
            pickle.dump(g_exp,g)

    return results


def serial_weighted_sum(results_list,fn_gold):
    """Takes a list of [[LLS,file.pkl],[]] for all the files to be compared"""
    """This should really be a parallel processing thing, but time constraints..."""
    forget = 1.8
    results = sorted(results_list,reverse=True,key=itemgetter(0))
    with open(results[0][1],'r') as f:
        data = pickle.load(f)
        data = data.edges * results[0][0]
        norm = results[0][0]
    for i in xrange(len(results)-1):
        i = i+1
        with open(results[i][1],'r') as ff:
            data1 = pickle.load(ff)
        
        data1 = data1.edges * results[i][0] / (forget*i)
        norm1 = results[i][0] / (forget*i)
        data = data + data1
        norm = norm + norm1
        
    data = data / norm

    #gs_exp.append(g_exp)
    #del g_exp
    #ws = weighted_sum(gs_exp,g_gold)

    output = fn_gold+".LLS_WS"
    with open(output,'w') as g:
        pickle.dump(data,g)

def file2graph(fn,d_nodes):
    d_exp_edges = ThreePartEdgeParser(fn)
    m_exp = dict2matrix(d_nodes,d_exp_edges,fn+".Graph")
    print 'Starting Graph ',time.time()
    g_exp = Graph(d_nodes,m_exp,edge_maker)
    print 'Finishing Graph', time.time()
    return g_exp
    


def input2(fn_dict,fn_gold,fns_exp):

    fn_dict = "mock_nodes"
    fn_gold = "mock_edges"
    fns_exp = ["mock_exp","mock_exp2","mock_exp3"]
    edge_maker = simple_thresh
    d_nodes = node_parser(fn_dict)    
    d_gold_edges =simple_edge_parser(fn_gold)
    m_gold = dict2matrix(d_nodes,d_gold_edges,fn_gold+".Graph")
    g_gold = Graph(d_nodes,m_gold,edge_maker)

    gold_bin = g_gold.give_edges()
    del g_gold
    results = serial_LLS_comparison(d_nodes,gold_bin,fns_exp,edge_maker,fn_gold)
    serial_weighted_sum(results,fn_gold)




def test_with_random_data():
    size = random.randint(3,12)
    d = dict(zip([i for i in st.uppercase[:size]],range(size)))
    gold = Graph(d,np.matrix([1 if random.random()>0.7 else 0 for  _ in xrange(size*size)]).reshape((size,size)),edge_maker)
    mat_list = [np.matrix([random.random() \
               for _ in xrange(size*size)]).reshape((size,size)) \
               for __ in xrange(4)]
    graph_list = [Graph(d,mat,edge_maker) for mat in mat_list]
    ws = weighted_sum(graph_list,gold)



class Graph():
    """Graph carries edges and nodes"""
    def __init__(self,d_nodes,matrix_edges,edge_maker=lambda m:m):
        self.nodes = d_nodes
        self.edges = matrix_edges
        self.maker = edge_maker

    def give_nodes(self):
        """"This method will return the nodes, but hopefully will be replaced someday"""
        return self.nodes

    def give_edges(self):
        """This method will use a paring function to return a binary sparse array
        of the called edges"""

        print "In give_edges, Generalissimo: ",time.time()

        fctn = np.frompyfunc(self.maker,1,1)
        bool_matrix = np.matrix(fctn(self.edges),dtype=int)
        
        bool_matrix = scipy.sparse.csc_matrix(scipy.sparse.lil_matrix(bool_matrix))
        print "Made it a CSC, Admiral: ", time.time()
        return bool_matrix

    def Write(self):
        """Will write the nodes and edges as two pkl files"""
        #nodes = self.Nodes()
        #edges = self.Edges()
        pass


"""
==================================================
"""

###DO THAT FROMPYFUNC DANCE

def simple_thresh(weight):
    threshold = 0.9
    return 1 if weight > 0.9 else 0

def thresh(indecies,weight,var=""):
    """This function will determine how to threshold a given edge """
    #np.ndenumerate gives "(index1,index2), value"
    cutoff = 0.9
    if abs(weight)> 0.9:
        return 1.0
    else:
        return 0.0

def simple_edge_parser(fn):
    """Parses a file of A,B \n A,C"""
    """Outputs a dictionary of A:(B,1)"""
    print 'In simple_edge_parser ',time.time()
    new_edges = {}
    with open(fn,'r') as f:
        for line in f:
            edges = line.split()
            new_edges.setdefault(edges[0],[])
            new_edges[edges[0]].append((edges[1],1))
            new_edges.setdefault(edges[1],[])
            new_edges[edges[1]].append((edges[0],1))
                 
    return new_edges    

def ThreePartEdgeParser(fn):
    """Parses a file of A \t B \t Weight """
    print 'In ThreePartEdgeParser'
    new_edges = {}
    with open(fn,'r') as f:
        for line in f:
            edges = line.split()
            new_edges.setdefault(edges[0],[])
            new_edges[edges[0]].append([edges[1],edges[2]])
            new_edges.setdefault(edges[1],[])
            new_edges[edges[1]].append([edges[0],edges[2]])

    return new_edges


def edge_parser(fn):
    """Parses a file of A,(B,0.4),(C,0.3)"""
    """Outputs a dictionary of edges"""
    print 'In edge_parser ',time.time()
    new_edges = {}
    with open(fn,'r') as f:
        for line in f:
            assert "," in line
            assert "(" in line
            assert ")" in line
            edges = line.split("(")
            lead = edges[0].strip()
            lead = lead.strip(",")
            lead = lead.strip()
            new_edges.setdefault(lead,[])
            for edge in edges[1:]:
                edge = edge.strip("\n")
                edge = edge.strip(" ")
                edge = edge.strip(",")
                edge = edge.strip("\)")
                edge = edge.split(",")
                edge = (edge[0],float(edge[1]))
                new_edges[lead].append(edge)
            
            nodes = sorted(new_edges.keys())
            d_nodes = {}
            for i,node in nodes:
                d_nodes[node] = i 

    return d_nodes, new_edges    

@profile
def dict2matrix(d_nodes,d_edges,fn_out,write=""):
    print 'In dict2matrix ', time.time()
    size = len(d_nodes.keys())
    mat = np.matrix(np.zeros((size,size)))

    with open(fn_out+".badnodes",'w') as gg:
        for i,lead in enumerate(sorted(d_edges.keys())):
            others = d_edges[lead]
            for other in others:
                if other[0] in d_nodes.keys():
                    mat[i,d_nodes[other[0]]] = other[1]
                else:
                    gg.write(other[0]+"\n")

    if write!="":
        output = fn_out    
        with open(output,'w') as g:
            g.write("!"+",".join(d_nodes.keys())+"\n")
            for line in mat.tolist():
                g.write(",".join([str(x) for x in line])+"\n")        

    return mat

def Matrix_Parser(fn):
    """Takes in a file with !Node_List and Array of length Node_list by Node_list"""
    """Makes a pkl of d_nodes and mat, returns same"""
    print 'In Matrix_Parser ',time.time()
    output = fn
    d_nodes = {}
    with open(fn,'r') as f:
        count = 0 
        for line in f:
            assert "," in line
            if line[0]=="!":
                nodes = line.split(",")
                nodes = [node.strip() for node in nodes]
                for i, node in enumerate(nodes):
                    d_nodes[node] = i
            else:
                weights = [float(x) for x in line.split(",")]
                size = len(weights)
                mat = np.matrix(np.zeros((size,size)))
                for j in size:
                    mat[count,j] = weights[j]                
                count += 1
    out_array = output+"_matrix.pkl"
    out_nodes = output+"_nodes.pkl"
    with open(out_array,'w') as g:
        pickle.dump(g,mat)
    with open(out_nodes,'w') as g:
        pickle.dump(g,d_nodes)

    return d_nodes,mat

def pickle_Matrix_Parser(pkl_matrix,pkl_nodes):
    """Takes in a file with pkled array and d_nodes"""
    """Returns pkled values"""
    print 'In pickle_Matrix_Parser'
    with open(pkl_matrix,'r') as f:
        mat  = pickle.load(f)
    
    with open(pkl_nodes,'r') as f:
        nodes = pickle.load(f)
    
    return d_nodes,mat


def pickle_to_readable(pkl_matrix,pkl_nodes):
    """Takes in a file with pkled array and d_nodes"""
    """Returns readable files"""
    print 'In pickle_to_readable'
    with open(pkl_matrix,'r') as f:
        mat = pickle.load(f)
    
    with open(pkl_nodes,'r') as f:
        nodes = pickle.load(f)
    
    output = "".join(pkl_matrix.split("_")[:-1])
        
    with open(output,'w') as g:
        g.write("!"+",".join(d_nodes.keys())+"\n")
        for line in mat.tolist():
            g.write(",".join([str(x) for x in line])+"\n")

    return d_nodes,mat

def node_parser(fn):
    """Parses a list of nodes, outputs a dictionary"""
    print 'In node_parser ', time.time()
    with open(fn,'r') as f:
        for line in f:
            assert "," in line
            nodes = line.split(",")
    nodes = [node.strip() for node in nodes]
    nodes = sorted(nodes)
    d_nodes = {}
    for i,node in enumerate(nodes):
        d_nodes[node] = i

    return d_nodes
            

def sparse_decider(mat):
    """Turns array into matrix, decides if it needs to be sparse or not"""
    print 'In sparse_decider'
    # WRITE SOME KIND OF DECIDER TO MAKE IT SPARSE OR NOT
    return mat

"""
==============================
"""
def compare_graphs(exp,gold_bin):
    """Take a Graph object and compare it to another"""
    print 'In compare_graph ', time.time()
    exp_bin = exp.give_edges()
    print "Methinks you might enjoy thine exp_bin edges, sire: ",time.time()
    print "Bonjour, cela sont ton gold_bin edges, monsieur: ", time.time()
    max_size = exp_bin.shape[0]
    print "Whao, that size is huge! ",time.time()
    poss = (max_size -1) * max_size 
    print "This shouldn't have taken any time"
    print "Gonna intersect that fish, check it out: ", time.time()
    isct = (exp_bin + gold_bin) / 2
    print "Intersected that fish, what up: ",time.time()
    isct = isct.astype(int)
    print "Made it an int, can't stop me now", time.time()
    exp_sum  = float(len(exp_bin.nonzero()[0]))
    gold_sum = float(len(gold_bin.nonzero()[0]))
    isct_sum = float(len(isct.nonzero()[0]))
    print "Calculated those values like B-O-S-S: ",time.time()
    assert isct_sum != 0, "No overlap with gold standard"
    assert gold_sum != 0, "Gold standard is empty"
    assert isct_sum != exp_sum, "Experimental graph is gold standard"
    assert gold_sum != poss, "Gold standard is all possible edges"
    num = isct_sum / (exp_sum - isct_sum)
    den = gold_sum / (poss - gold_sum)
    LLS = log(num/den)
    print LLS
    return LLS

@profile
def weighted_sum(graph_list,gold):
    """Combine a list of [score,graph] data, sort, and collapse"""
    print 'In Weighted Sum ',time.time()
    gold_bin = gold.give_edges()
    del gold
    forget = 1.8
    score_graph_list = sorted([[compare_graphs(exp,gold_bin),exp.edges] for exp in graph_list],reverse=True,key=itemgetter(0))
    enum = [[i,j] for i,j in enumerate(score_graph_list)]
    norm = reduce(lambda x,y: x+y,map(lambda x: forget**(x[0]-1)*x[1][0],enum))
    ws = reduce(lambda x,y: x+y,map(lambda x: forget**(x[0]-1)*x[1][0]*x[1][1],enum))
    ws = ws / norm
    print "Hey man, did I do good?: ",time.time()
    print "Dude, it's been real: ", time.time()
    return ws

if __name__ == "__main__":
    main()
