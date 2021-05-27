from collections import defaultdict
import sys
import argparse

class Graph(object):

    def __init__(self, edges, directed=False):
        self.adj = defaultdict(set)
        self.directed = directed
        self.add_edges(edges)


    def get_vertices(self):
        return list(self.adj.keys())


    def get_edges(self):
        return [(k, v) for k in self.adj.keys() for v in self.adj[k]]


    def add_edges(self, edges):
        for u, v in edges:
            self.add_arc(u, v)


    def add_arc(self, u, v):
        self.adj[u].add(v)
        if not self.directed:
            self.adj[v].add(u)


    def edge_exists(self, u, v):
        return u in self.adj and v in self.adj[u]

    def get_dependencies(self, v):
        dependencies = set()
        for vt in self.adj:
            if v in self.adj[vt]:
                dependencies.add(vt)
        return dependencies

    def get_dependencies_rec(self, v):
        dependencies = set()
        for vt in self.adj:
            if v in self.adj[vt]:
                dependencies.add(vt)
                for item in self.get_dependencies_rec(vt):
                    dependencies.add(item)
        return dependencies


    def __len__(self):
        return len(self.adj)


    def __str__(self):
        return '{}({})'.format(self.__class__.__name__, dict(self.adj))


    def __getitem__(self, v):
        return self.adj[v]

parser = argparse.ArgumentParser(description='One Big Switch program distribution')
parser.add_argument('--filename', help='Name of the program that will be distributed',
                    type=str, action="store", required=True)
parser.add_argument('--module', help='Name of the module that will be distributed',
                    type=str, action="store", required=True)
args = parser.parse_args()

filename = open(args.filename, "r")

edges = [('ethernet', 'ipv4'), ('ethernet', 'ipv6'), ('ipv4', ''), ('ipv6', '')]
graph = Graph(edges, directed=True)

dependencies = graph.get_dependencies_rec(args.module)
dependencies.add('all')
dependencies.add(args.module)

should_write = False

with filename as f:
    buff = []
    for line in f:
        line_test = line.lower()

        if any(word+'-begins' in line_test for word in dependencies):
            should_write = True

        if should_write:
            buff.append(line)

        if any(word+'-ends' in line_test for word in dependencies):
            should_write = False

    output = open("output_" + args.module  + "_" + args.filename, "w")
    output.write("".join(buff))
    output.close()
