from graph import *
from collections import defaultdict
from graph_io import *
from line_profiler_pycharm import profile


@profile
def basic_colorref(path):
    # create a list of all graphs in the file
    with open(path) as G:
        glist = read_graph_list(Graph, G)[0]

    # create a dictionary for storing colors for all vertices of all graphs and initiate with degree coloring
    graph_dict = degree_coloring(glist)
    result_dict = defaultdict(list)
    all_stable = False
    to_stabilize = len(glist)

    while not all_stable:
        # print("~~~~~~~~~~~~~~~~~~~~~~~~ Iteration ", iteration, "~~~~~~~~~~~~~~~~~~~~~~~~~")
        # for each graph in the file do this iteration
        for i in range(len(graph_dict)):
            vertex_dict = graph_dict[i]

            # continue iterating on this graph only if it's not stable
            if not vertex_dict["stable"]:

                # increment iteration of this graph
                vertex_dict["iteration"] += 1

                # reset color dictionaries
                current_color_classes = defaultdict(set)
                new_color_classes = defaultdict(set)

                # populate 'current_color_classes' with key = color , value = set(vertex labels)
                for key in vertex_dict:
                    if type(key) == int:
                        current_color_classes[vertex_dict[key]].add(key)
                sorted_current_color_classes = dict(sorted(current_color_classes.items()))

                # for each color class create a dictionary of key = neighborhood colors, value = set(vertex labels)
                vertex_dict_copy = vertex_dict.copy()
                for c in sorted_current_color_classes:
                    have_same_neighborhood = defaultdict(set)

                    # populate have_same_neighborhood
                    for k in sorted_current_color_classes[c]:
                        if type(k) == int:
                            have_same_neighborhood[
                                tuple(get_neighbor_colors(glist[i].vertices[k].neighbours, vertex_dict_copy))].add(k)
                    # if i == 0 or i == 2:
                    #     print("Graph ", i, " Color ", c, " ", have_same_neighborhood)

                    for index, n in enumerate(have_same_neighborhood):
                        if index > 0:
                            vertex_dict["last_color"] += 1
                            for ve in have_same_neighborhood[n]:
                                vertex_dict[ve] = vertex_dict["last_color"]

                # populate 'new_color_classes' with key = color , value = set(vertex labels)
                for h in vertex_dict:
                    if type(h) == int:
                        new_color_classes[vertex_dict[h]].add(h)

                # check if finished refining
                if current_color_classes == new_color_classes:
                    # print("Graph " , i, " finished with number of iterations: ", vertex_dict["iteration"])
                    # print(sorted_current_color_classes)
                    to_stabilize -= 1
                    vertex_dict["stable"] = True

                    # prepping end result
                    partition_key = {"iteration": vertex_dict["iteration"],
                                     "is_discrete": len(current_color_classes) == len(glist[i].vertices)}
                    for c in sorted_current_color_classes:
                        partition_key[c] = len(sorted_current_color_classes[c])
                    result_dict[tuple(partition_key.items())].append(i)

            if to_stabilize == 0:
                all_stable = True

    return parse_data(result_dict)


def degree_coloring(glist):
    graph_dict = {}
    for g in range(len(glist)):
        vertex_dict = {}
        for v in range(len(glist[g].vertices)):
            vertex_dict[v] = glist[g].vertices[v].degree
        # creates an entry in the dictionary with a variable that stores the highest used color
        vertex_dict["last_color"] = max(vertex_dict.values())
        vertex_dict["stable"] = False
        vertex_dict["iteration"] = 0
        graph_dict[g] = vertex_dict
    return graph_dict


# takes a list of neighbors and a vertex_dict and returns a sorted list of their colors
def get_neighbor_colors(vlist, vertex_dict):
    result = []
    for v in vlist:
        result.append(vertex_dict[v.label])
    result.sort()
    return result


def parse_data(data):
    result = []
    for entry in data:
        tup = (data[entry], entry[0][1], entry[1][1])
        result.append(tup)
    print("Sets of possibly isomorphic graphs:")
    for tup in result:
        print(tup[0], tup[1], tup[2])
    print("")
    print(result)

    return result


# basic_colorref("./SampleGraphsBasicColorRefinement/colorref_largeexample_6_960.grl")
