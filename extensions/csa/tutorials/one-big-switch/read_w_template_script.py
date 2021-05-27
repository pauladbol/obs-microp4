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

obs_program = open(args.filename, "r")
template = open("common_template.up4", "r")

edges = [('ethernet', 'ipv4'), ('ethernet', 'ipv6'), ('ipv4', ''), ('ipv6', '')]
graph = Graph(edges, directed=True)

dependencies = graph.get_dependencies_rec(args.module)
dependencies.add('all')
dependencies.add(args.module)

write_declare = False
declare = []

write_instantiate = False
instantiate = []

write_invoke = False
invoke = []

# read one big switch program and get module declare, instance and invoke codes
with obs_program as file:
    for line in file:

        if any('@ModuleDeclareEnds(\"'+word+'\")' in line for word in dependencies):
            write_declare = False
        
        if write_declare:
            declare.append(line)

        if any('@ModuleDeclareBegin(\"'+word+'\")' in line for word in dependencies):
            write_declare = True

        if any('@ModuleInstantiateEnds(\"'+word+'\")' in line for word in dependencies):
            write_instantiate = False
        
        if write_instantiate:
            instantiate.append(line)

        if any('@ModuleInstantiateBegin(\"'+word+'\")' in line for word in dependencies):
            write_instantiate = True

        if any('@ModuleInvokeEnds(\"'+word+'\")' in line for word in dependencies):
            write_invoke = False
        
        if write_invoke:
            invoke.append(line)

        if any('@ModuleInvokeBegin(\"'+word+'\")' in line for word in dependencies):
            write_invoke = True

# read template and add program lines to new output file
with template as t:
    output_code = t.read()

output_code = output_code.replace(
    '//module-declare', ''.join(declare)
    ).replace(
        '//module-instantiate', ''.join(instantiate)
        ).replace(
            '//module-invoke', ''.join(invoke)
            )

output = open("output_w_template_" + args.module  + "_" + args.filename, "w")
output.write(output_code)
output.close()
