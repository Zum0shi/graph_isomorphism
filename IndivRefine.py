from graph import *
from graph_io import *
from colorref import *


def doBranching(path):
    # read the file
    with open(path) as G:
        glist = read_graph_list(Graph, G)[0]

    # a list that keeps track of isomorphic graphs and their number of automorphisms [([graphs],automorphisms), ....]
    aut = []

    # pass file to colorref
    data, vertex_dict, last_color = basic_colorref(glist)
    print(data)

    # do branching per equivalence class
    for eq_class in data:
        # if the graphs are already discrete then no need to branch them
        if eq_class[2]:
            aut.append((eq_class[0], 1))
            continue
        # do branching for pairs in said equivalence class
        for i in range(len(eq_class[0])):
            for j in range(i + 1, len(eq_class[0])):
                countIsomorphism(isolateGraphs(vertex_dict, eq_class[0][i], eq_class[0][j]))
    print(aut)
    # base cases
    # for g in data:
    # if


def isolateGraphs(vertex_dict, i, j):
    print(vertex_dict)


def countIsomorphism(data):
    print("wewe")


doBranching("./SampleGraphsBasicColorRefinement/colorref_smallexample_6_15.grl")
