from graph import *
from collections import defaultdict
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
        print("STARTING GRAPH " + str(i) + " #####################################################################")
        iteration = 0
        vertex_dict = graph_dict[i]
        have_same_neighborhood = defaultdict(set)
        new_color_classes = defaultdict(set)
        old_color_classes = {}

        # populate 'new_color_classes' with key = color , value = set(vertex labels)
        for v in range(len(vertex_dict) - 1):
            new_color_classes[vertex_dict[v]].add(v)

        # start refining process
        while old_color_classes != new_color_classes:
            # update dictionaries and iteration counter
            iteration += 1
            old_color_classes = new_color_classes
            new_color_classes = {}

            # iterate over all color classes
            for c in old_color_classes:
                have_same_neighborhood.clear()

                # create a dictionary of neighborhoods of the vertices in said color class
                vertex_dict_copy = vertex_dict.copy()
                for vtx in old_color_classes[c]:
                    have_same_neighborhood[
                        tuple(get_neighbor_colors(glist[i].vertices[vtx].neighbours, vertex_dict))].add(vtx)

                # iterate over all neighborhoods that share a color and change colors of all except the first
                temp = list(have_same_neighborhood.keys())[1:]
                for n in temp:
                    vertex_dict["last_color"] += 1
                    for ve in have_same_neighborhood[n]:
                        vertex_dict[ve] = vertex_dict["last_color"]

            # updated color class
            for v in range(len(vertex_dict) - 1):
                new_color_classes[vertex_dict[v]].add(v)

            # print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ END OF ITERATION ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

        # printing of some results for debugging
        result = []
        for h in old_color_classes:
            result.append(len(old_color_classes[h]))
        result.sort()
        print(old_color_classes)
        print("list of partition: " + str(result))
        print("number of iterations: " + str(iteration))


def degree_coloring(glist):
    graph_dict = {}
    for g in range(len(glist)):
        vertex_dict = {}
        for v in range(len(glist[g].vertices)):
            vertex_dict[v] = glist[g].vertices[v].degree
        # creates an entry in the dictionary with a variable that stores the highest used color
        vertex_dict["last_color"] = max(vertex_dict.values())
        graph_dict[g] = vertex_dict
    return graph_dict


# takes a list of neighbors and a vertex_dict and returns a sorted list of their colors
def get_neighbor_colors(vlist, vertex_dict):
    result = []
    for v in vlist:
        result.append(vertex_dict[v.label])
    result.sort()
    return result


basic_colorref("./SampleGraphsBasicColorRefinement/colorref_smallexample_4_16.grl")
