import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import kendalltau
import random



def PageRank(numberOfIterations,precision,dampingFactor, graph : nx.classes.digraph.DiGraph):
    
    if(not graph.is_directed):
        graph = nx.to_directed(graph)

    n = graph.number_of_nodes()
    precisionHelper = precision
    PageRankValues = {}
    arrayHelper = {}
    for node in graph._node:
        PageRankValues[node] = 1/n
        arrayHelper[node] = 0

    while(numberOfIterations > 0 and precisionHelper >= precision):
        numberOfIterations-=1
        for node in graph._node:
            arrayHelper[node] = 0
            for neighbor in graph.neighbors(node):
                    arrayHelper[node] = arrayHelper[node] + PageRankValues[neighbor] / graph.out_degree(neighbor)
            arrayHelper[node] = (1 - dampingFactor) / n + dampingFactor * arrayHelper[node]     

        norm = np.asarray(list(arrayHelper.values()))
        norm = np.linalg.norm(norm)
        
        for node in graph._node:  
            arrayHelper[node] = arrayHelper[node] / norm
            
        precisionHelper= 0

        for node in graph._node:
            precisionHelper = precisionHelper + abs(arrayHelper[node] - PageRankValues[node])
            PageRankValues[node] = arrayHelper[node]

    return PageRankValues

 
def genereteWebGraph():
    graph = nx.DiGraph()
    scc = random.randrange(100,1000)
    inn = random.randrange(50,200)
    out = random.randrange(50,200)
    
    for i in range (scc+inn+out):
        graph.add_node(i)

    # add edges in inn 
    for firstNode in range (inn):
        for secondNode in range (inn):
            if(firstNode != secondNode):
                chanceForEdge = random.random()
                if(chanceForEdge<0.1):
                    graph.add_edge(firstNode,secondNode)

    # add edges in out 
    for firstNode in range (inn+scc,inn+scc+out):
        for secondNode in range (inn+scc,inn+scc+out):
            if(firstNode != secondNode):
                chanceForEdge = random.random()
                if(chanceForEdge<0.1):
                    graph.add_edge(firstNode,secondNode)                    

    # add edges in scc
    for firstNode in range (inn,inn+scc):
        for secondNode in range (inn,inn+scc):
            if(firstNode != secondNode):
                chanceForEdge = random.random()
                if(chanceForEdge<0.2):
                    graph.add_edge(firstNode,secondNode)

    #betweeb inn and scc
    for firstNode in range (inn):
        for secondNode in range (inn,inn+scc):
                chanceForEdge = random.random()
                if(chanceForEdge<0.01):
                    graph.add_edge(firstNode,secondNode)                                   

    #betweeb scc and out
    for firstNode in range (inn+scc,inn+scc+out):
        for secondNode in range (inn,inn+scc):
                chanceForEdge = random.random()
                if(chanceForEdge<0.01):
                    graph.add_edge(secondNode,firstNode)

    #tubes
    for firstNode in range (inn):
        for secondNode in range (inn,inn+scc):
                chanceForEdge = random.random()
                if(chanceForEdge<0.001):
                    graph.add_edge(firstNode,secondNode)
                chanceForEdge = random.random()
                if(chanceForEdge<0.001):
                    graph.add_edge(secondNode,firstNode)      
    return graph


def test(graph = None):

    if(graph == None):
        graph = genereteWebGraph()

    list1 = (PageRank(100,0.00001,0.85,graph))
    list2 =(nx.pagerank(graph, alpha=0.85, personalization=None, max_iter=100, tol=0.00001 ,dangling=None))   
    return kendalltau(list(list1.values()),list(list2.values()))


#za testiranje graf 
graph = nx.karate_club_graph()
graph = nx.to_directed(graph)
print(test(graph))

#test na random grafu
print(test())    