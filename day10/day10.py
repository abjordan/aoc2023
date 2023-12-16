#!/usr/bin/env python3

import matplotlib.pyplot as plt
import networkx as nx
import sys

# Pipe connections:
#   F - 7
#   |   |
#   L - J

def make_map(data):
    lines = data.split("\n")
    rows = len(lines)
    cols = len(lines[0])
    print(f"Grid is {rows} x {cols}")
    g = nx.DiGraph()

    start_node = None
    for r, row in enumerate(lines):
        for c, col in enumerate(row):
            match col:
                case ".":
                    continue
                case "-":   # East-West
                    g.add_edge( (r,c), (r,c-1) )
                    g.add_edge( (r,c), (r,c+1) )
                case "7":   # West-South
                    g.add_edge( (r,c), (r,c-1) )
                    g.add_edge( (r,c), (r+1,c) )
                case "|":   # North-South
                    g.add_edge( (r,c), (r-1,c) )
                    g.add_edge( (r,c), (r+1,c) )
                case "L":   # North-West
                    g.add_edge( (r,c), (r-1,c) )
                    g.add_edge( (r,c), (r,c+1) )
                case "F":
                    g.add_edge( (r,c), (r,c+1) )
                    g.add_edge( (r,c), (r+1,c) )
                case "J":
                    g.add_edge( (r,c), (r-1,c) )
                    g.add_edge( (r,c), (r,c-1) )
                case "S":
                    start_node = (r,c)
                case _:
                    print(f"Unknown symbol at ({r},{c}): {col}")

    color_map = [ 'blue' if n == start_node else 'green' for n in g]

    subax1 = plt.subplot(121)
    #nx.draw(g, with_labels=True, node_color=color_map)
    #plt.show()

    # Filter edges
    edges_to_remove = []
    edges_to_add = []
    for u, v in g.edges():
        # The start node is connected to whoever is connected to it
        if v == start_node:
            edges_to_add.append( (v,u) )
            continue
        if not g.has_edge(v, u):
            edges_to_remove.append( (u,v) )

    g.remove_edges_from(edges_to_remove)
    g.add_edges_from(edges_to_add)
    subax2 = plt.subplot(122)
    #nx.draw(g, with_labels=True, node_color=color_map)
    #plt.show()

    # Remove any nodes that aren't connected to the start node
    # ???

    return g, start_node

if __name__ == "__main__":
    with open(sys.argv[1], "r") as infile:
        data = infile.read()
        grid, start_node = make_map(data)

        # Part 1: how far is the farthest point from the start?
        distances = nx.single_source_shortest_path_length(grid, start_node)
        max_dist = 0
        for node, dist in distances.items():
            max_dist = max(max_dist, dist)
        print(f"Maximum distance: {max_dist}")
