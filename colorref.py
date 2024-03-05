from graph import *
from graph_io import *
from line_profiler_pycharm import profile


@profile
def basic_colorref(path):
    # create a list of all graphs in the file
    with open(path) as G:
        glist = read_graph_list(Graph, G)[0]

    # create a dictionary for storing colors and initiate with degree coloring
    graph_dict = degree_coloring(glist)

    # iterate over every graph
    for i in range(len(graph_dict)):
        iteration = 0
        vertex_dict = graph_dict[i]
        current = {}
        previous = {}
        # populate 'current' with key = neighbors , value = vertex label
        for v in range(len(vertex_dict) - 1):
            current[glist[i].vertices[v].neighbours] = v

        # start refining process
        while current != previous:
            # update dictionaries and iteration counter
            iteration += 1
            previous = current.copy()
            current.clear()
            #DO SOMETHING WITH PREVIOUS
            # iterate over every vertex
            for v in range(len(vertex_dict) - 1):
                print(v, vertex_dict[v], glist[i].vertices[v].neighbours[0].label)
    # print(i)
    # print(graph_dict[i])


# create a dictionary with key = graph index , value vertex dictionary with key = vertex index , value = color
# sets all vertices to uniform color = 1
def degree_coloring(glist):
    graph_dict = {}
    for g in range(len(glist)):
        vertex_dict = {}
        for v in range(len(glist[g].vertices)):
            vertex_dict[v] = glist[g].vertices[v].degree
        # creates an entry in the dictionary with a variable that stores the highest used color
        vertex_dict["highest_color"] = max(vertex_dict.values())
        graph_dict[g] = vertex_dict
    return graph_dict


basic_colorref("./SampleGraphsBasicColorRefinement/colorref_smallexample_4_16.grl")
