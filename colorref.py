from graph import *
from collections import defaultdict
from graph_io import *
from line_profiler_pycharm import profile


def basic_colorref(graphs, coloring=None):
    # the list of graphs to be refined
    glist = graphs

    # a dictionary containing key = (graph_index, vertex.label), value = color | after degree coloring
    if coloring is None:
        vertex_dict = degree_coloring(glist)
    else:
        vertex_dict = coloring

    # creates a dictionary with key = graph_index and value = list(isStable , iterations, isFinished)
    graph_dict = generate_graph_dict(glist)
    # dictionary to store data of successfully refined graphs
    result_dict = defaultdict(list)

    # variables for refinement
    all_stable = False
    last_color = max(vertex_dict.values())

    # begin refining process
    while not all_stable:

        # if graphs are stable pull their vertices out of vertex_dict, otherwise increase iteration count
        for g in graph_dict:
            if graph_dict[g][0]:
                if not graph_dict[g][2]:
                    for vertex in glist[g].vertices:
                        result_dict[(g, vertex.label)] = vertex_dict[(g, vertex.label)]
                        del vertex_dict[(g, vertex.label)]
                        # print("IM HERE HEHE")
                    graph_dict[g][2] = True
            else:
                graph_dict[g][1] += 1

        # reset color class dictionary and new_vertex_dict
        color_classes = defaultdict(set)
        new_vertex_dict = vertex_dict.copy()

        # populates color_classes, group vertices by color: dict{key = color , value = set{(graph, vertex.label)}}
        for key in vertex_dict:
            color_classes[vertex_dict[key]].add(key)
        color_classes = dict(sorted(color_classes.items()))

        # creates a dictionary for neighbors colors
        for cc in color_classes:
            neighborhoods = defaultdict(set)

            # populate neighborhoods
            for k in color_classes[cc]:
                neighborhoods[tuple(get_neighbor_colors(glist[k[0]].vertices[k[1]].neighbours, k[0], vertex_dict))].add(
                    k)

            # add updated colors to new dict
            for index, n in enumerate(neighborhoods):
                if index > 0:
                    # print("recoloring vertices: ", neighborhoods[n])
                    last_color += 1

                    for vertex in neighborhoods[n]:
                        new_vertex_dict[vertex] = last_color

        # check if refining process finished
        if vertex_dict == new_vertex_dict:
            # for g in graph_dict:
                # print(g, graph_dict[g][1])

            # add remaining vertices
            for entry in vertex_dict:
                result_dict[entry] = vertex_dict[entry]

            # end refinement process
            all_stable = True

        else:
            # check if any graphs have been stabilized during this iteration
            check_stability(glist, graph_dict, vertex_dict, new_vertex_dict, color_classes)
            vertex_dict = new_vertex_dict
    return parse_data(result_dict, graph_dict, glist), result_dict, last_color


# creates a dictionary of all vertices and their colors based on degree coloring
def degree_coloring(glist):
    result = defaultdict()
    for i, g in enumerate(glist):
        for vertex in g.vertices:
            tup = (i, vertex.label)
            result[tup] = vertex.degree
    return result


# creates a dictionary with key = graph and value = tuple(isStable , iterations)
def generate_graph_dict(glist):
    result = defaultdict(list)
    for i in range(len(glist)):
        result[i] = [False, 0, False]
    return result


# takes a list of neighbors and a vertex_dict and returns a sorted list of their colors
def get_neighbor_colors(vlist, graph_index, vertex_dict):
    result = []
    for v in vlist:
        result.append(vertex_dict[(graph_index, v.label)])
    result.sort()
    return result


# for each graph check whether it has stabilized
def check_stability(glist, graph_dict, vertex_dict, new_vertex_dict, color_classes):
    for i, g in enumerate(glist):
        if not graph_dict[i][0]:
            vertices = []
            colors_before = set()
            colors_after = set()
            for vertex in g.vertices:
                tup = (i, vertex.label)
                vertices.append(tup)
            set(vertices)
            graph_dict[i][0] = True

            for key in vertices:
                colors_before.add(vertex_dict[key])
                colors_after.add(new_vertex_dict[key])

            if len(colors_before) != len(colors_after):
                graph_dict[i][0] = False


# prepare data for codegrade
def parse_data(result_dict, graph_dict, glist):
    color_partition_per_graph = defaultdict(list)
    for g in graph_dict:
        color_dict = defaultdict(list)
        color_len = defaultdict()
        temp = []
        for key in result_dict:
            if key[0] == g:
                color_dict[result_dict[key]].append(result_dict[key])
                color_len[result_dict[key]] = len(color_dict[result_dict[key]])
                color_len = dict(sorted(color_len.items()))
        for vtx in color_len:
            tup = (vtx, color_len[vtx])
            temp.append(tup)
        color_partition_per_graph[tuple(temp)].append(g)

    result = []
    for s in color_partition_per_graph:
        # print(color_partition_per_graph[s], s)
        tupp = (color_partition_per_graph[s], graph_dict[color_partition_per_graph[s][0]][1],
                len(s) == len(glist[color_partition_per_graph[s][0]].vertices))
        result.append(tupp)

    # print(result)
    return result


# basic_colorref("./SampleGraphsBasicColorRefinement/colorref_smallexample_6_15.grl")
