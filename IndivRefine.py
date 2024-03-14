from graph import *
from graph_io import *


def individualisedRefinement(path):
    with open(path) as G:
        glist = read_graph_list(Graph, G)[0]

