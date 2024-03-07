from graph_io import *


def visualize(path):
    with open(path, 'r') as f:
        Glist = read_graph_list(Graph, f)[0]

    counter = 0
    for g in Glist:
        string = "graph" + str(counter) + ".dot"
        with open(string, 'w') as f:
            write_dot(g, f)
        counter +=1


visualize("./SampleGraphsBasicColorRefinement/colorref_smallexample_6_15.grl")