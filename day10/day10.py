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

    # Remove any nodes that aren't connected to the start node
    # ???

    return grid, g, start_node, (rows, cols)

def part_b(grid, rows, cols, main_loop_nodes):
    # Nodes are "outside" if you can get from the start to the edge
    # 
    # To go north or south, you get blocked by a -
    # To go east or west, you get blocked by a |
    innies = []
    outies = []
    secret_outies = []
    for (r,c), symbol in grid.items():
        if symbol == ".":
            #print(f"({r},{c}) = {symbol}")
            # Check to see if anything to the left is |
            stopped_west = False
            for i in range(c, 0, -1):
                #print(f"  ({r},{i}) {symbol}")
                if grid[(r,i)] == '|':
                    #print("  stopped w")
                    stopped_west = True
                    break
            
            stopped_east = False
            for j in range(c, cols):
                #print(f"  ({r},{j}) {symbol}")
                if grid[(r,j)] == '|':
                    #print("  stopped e")
                    stopped_east = True
                    break
            
            stopped_north = False
            for m in range(r, 0, -1):
                #print(f"  ({m},{c}) {symbol}")
                if grid[(m, c)] == '-':
                    #print("  stopped n")
                    stopped_north = True
                    break
            
            stopped_south = False
            for n in range(r, rows):
                #print(f"  ({n},{c}) {symbol}")
                if grid[(n,c)] == '-':
                    #print("  stopped s")
                    stopped_south = True
                    break
            
            if (stopped_north and stopped_south and stopped_west and stopped_east):
                innies.append((r,c))
                #print(f"Found innie at ({r},{c})")
            else:
                #print(f"Found outie at ({r},{c})")
                outies.append((r,c))

    # If you are an innie but your neighbor is an outie, you're an outie now too.
    # But not diagonally, I hope
    for (ir,ic) in innies:
        if ((ir-1,ic) in outies) or ((ir+1,ic) in outies) or ((ir,ic-1) in outies) or ((ir,ic+1) in outies):
            secret_outies.append((ir,ic))

    #print(f"Found some secret outies! {secret_outies}")
    real_innies = set(innies) - set(secret_outies)
                
    return real_innies

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
        # Actually, not useless... the nodes that aren't connected to the
        # start node can be replaced with '.' before we process it
        #for node in graph.nodes():
        #    if not node in distances.keys():
        #        print(f"Removing {node}")
        #        grid[node] = '.'
            
        innies = part_b(grid, rows, cols)
        print(f"Found {len(innies)} innies")