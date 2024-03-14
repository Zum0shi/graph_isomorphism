from graph import *
from graph_io import *
from colorref import *


def individualisedRefinement(path):
    with open(path) as G:
        glist = read_graph_list(Graph, G)[0]

    data, vertices, last_color = basic_colorref(glist)


individualisedRefinement("./SampleGraphsBasicColorRefinement/colorref_smallexample_6_15.grl")
