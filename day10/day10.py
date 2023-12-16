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

    grid = {}

    start_node = None
    for r, row in enumerate(lines):
        for c, col in enumerate(row):
            grid[(r,c)] = col
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

    start_r, start_c = start_node
    connected_north = g.has_edge( (start_r,start_c), (start_r-1,start_c) )
    connected_south = g.has_edge( (start_r,start_c), (start_r+1,start_c) )
    connected_west = g.has_edge( (start_r,start_c), (start_r,start_c-1) )
    connected_east = g.has_edge( (start_r,start_c), (start_r,start_c+1) )
    if (connected_north and connected_east):
        grid[start_node] = 'L'
    elif (connected_north and connected_south):
        grid[start_node] = '|'
    elif (connected_north and connected_west):
        grid[start_node] = 'J'
    elif (connected_south and connected_west):
        grid[start_node] = '7'
    elif (connected_south and connected_east):
        grid[start_node] = 'F'
    elif (connected_east and connected_west):
        grid[start_node] = '-'
    else:
        print("Can't figure out what S should be")
    print(f"Set S to {grid[start_node]}")

    return grid, g, start_node, (rows, cols)

def part_b(grid, rows, cols, main_loop_nodes):
    # Nodes are "inside" if you cross the loop an odd number of times.
    # https://en.wikipedia.org/wiki/Even%E2%80%93odd_rule
    # 
    # This is a REAlLY COOL algorithm - it doesn't matter which direction
    # you cast your "ray" -- if you cross the loop 
    innies = []
    outies = []
    for (r,c), symbol in grid.items():
        if (r,c) not in main_loop_nodes:
            # Cast the ray due south, for arbitrary reasons
            hits = 0
            for x in range(r, rows):
                if (x,c) in main_loop_nodes and not (grid[(x,c)] in {'|', 'F', 'L'}):
                    hits += 1

            if hits % 2 == 1:
                innies.append((r,c))
                #print(f"Found innie at ({r},{c})")
            else:
                #print(f"Found outie at ({r},{c})")
                outies.append((r,c))
                
    return innies

if __name__ == "__main__":
    with open(sys.argv[1], "r") as infile:
        data = infile.read()
        grid, graph, start_node, (rows, cols) = make_map(data)

        # Part 1: how far is the farthest point from the start?
        distances = nx.single_source_shortest_path_length(graph, start_node)
        max_dist = 0
        for node, dist in distances.items():
            #print(node, dist)
            max_dist = max(max_dist, dist)
        print(f"Maximum distance: {max_dist}")

        # Part 2: how much area is enclosed by the main loop?
        # Nodes are enclosed by the loop if you can't get to the edge
        # without crossing a pipe. I think our solution to Part A is...
        # totally useless here?  😱

        # We have to replace the start node with the node type it "should" be
        # to make the part B algorithm work.

        # Actually, not useless... the nodes that aren't connected to the
        # start node can be replaced with '.' before we process it
        #for node in graph.nodes():
        #    if not node in distances.keys():
        #        print(f"Removing {node}")
        #        grid[node] = '.'
            
        innies = part_b(grid, rows, cols, distances.keys())
        print(f"Found {len(innies)} innies")