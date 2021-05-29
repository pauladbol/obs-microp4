import matplotlib.pyplot as plt
import networkx as nx
import csv


# Data  = open('stanford_topo.csv', "r")
# read = csv.reader(Data)
# Graphtype=nx.Graph()   # use net.Graph() for undirected graph


Data = open('stanford_topo.csv', "r")
Graphtype = nx.Graph()

G = nx.parse_edgelist(Data, comments='t', delimiter=',', create_using=Graphtype,
                      nodetype=int, data=(('weight', float),))

# G = nx.read_edgelist(read, create_using=Graphtype, nodetype=int, data=(('weight',float),))

# for x in G.nodes():
#       print ("Node:", x, "has total #degree:",G.degree(x), " , In_degree: ", G.out_degree(x)," and out_degree: ", G.in_degree(x))   
# for u,v in G.edges():
#       print ("Weight of Edge ("+str(u)+","+str(v)+")", G.get_edge_data(u,v))

nx.draw(G)
plt.show()