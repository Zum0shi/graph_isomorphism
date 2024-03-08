from graph import *
from collections import defaultdict
from graph_io import *
from line_profiler_pycharm import profile


@profile
def basic_colorref(path):
    # create a list of all graphs in the file
    with open(path) as G:
        glist = read_graph_list(Graph, G)[0]

    # a dictionary containing key = (graph_index, vertex.label), value = color | after degree coloring
    vertex_dict = degree_coloring(glist)
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
                    print(vertex_dict)
                    for vertex in glist[g].vertices:
                        result_dict[(g, vertex.label)] = vertex_dict[(g, vertex.label)]
                        del vertex_dict[(g, vertex.label)]
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
                    last_color += 1
                    for vertex in neighborhoods[n]:
                        new_vertex_dict[vertex] = last_color

        for g in graph_dict:
            print(g, graph_dict[g][1])

        # check if refining process finished
        if vertex_dict == new_vertex_dict:
            for g in graph_dict:
                print(g, graph_dict[g][1])
            # add remaining vertices
            for entry in vertex_dict:
                result_dict[entry] = vertex_dict[entry]

            all_stable = True

        else:
            # check if any graphs have been stabilized during this iteration
            check_stability(glist, graph_dict, vertex_dict, new_vertex_dict)
            vertex_dict = new_vertex_dict

    return parse_data(result_dict, graph_dict)


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
def check_stability(glist, graph_dict, vertex_dict, new_vertex_dict):
    for i, g in enumerate(glist):
        if not graph_dict[i][0]:
            vertices = []
            for vertex in g.vertices:
                tup = (i, vertex.label)
                vertices.append(tup)
            set(vertices)
            graph_dict[i][0] = True
            for key in vertices:
                if vertex_dict[key] != new_vertex_dict[key]:
                    graph_dict[i][0] = False
                    break


def parse_data(result_dict, graph_dict):
    print(result_dict)
    color_partition_per_graph = defaultdict()
    for g in graph_dict:
        color_dict = defaultdict(list)
        color_len = defaultdict()
        for key in result_dict:
            temp = []
            if key[0] == g:
                color_dict[result_dict[key]].append(result_dict[key])
                tup = (result_dict[key], len(color_dict[result_dict[key]]))
                temp.append(tup)
                color_len[result_dict[key]] = len(color_dict[result_dict[key]])
                color_len = dict(sorted(color_len.items()))
        color_partition_per_graph[g] = color_len

    for s in color_partition_per_graph:
        print(s , color_partition_per_graph[s])
    # print(color_partition_per_graph)


#     result = []
#     for entry in color_partition_per_graph:
#         tup = []

    # color_partition_per_graph[key[0]].append(result_dict[key])
    # print(result_dict)

    # print(cc)
    # print(v)
    # cc_per_graph[v[0]].append(cc)
    # print(cc_per_graph)

    # cc_per_graph[v[0]] = v[1]

    # temp = {}
    # for g in graph_dict:
    #     temp[g] = [graph_dict[g][1], ]


basic_colorref("./SampleGraphsBasicColorRefinement/cref9vert3comp_10_27.grl")