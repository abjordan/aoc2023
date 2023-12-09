#!/usr/bin/env python3

import itertools
import math
import re
import sys

class Node:
    def __init__(self, label, left, right):
        self.label = label
        self.left = left
        self.right = right

    def next(self, direction):
        match direction:
            case "L":
                return self.left
            case "R":
                return self.right
            case _:
                raise ValueError(f"Uknown direction: {direction}")


nodetoks = re.compile(r'(...) = \((...), (...)\)')

def create_nodes(nodelines: list) -> dict:
    nodes = {}
    for line in nodelines.split("\n"):
        label, left, right = nodetoks.search(line).groups()
        nodes[label] = Node(label, left, right)
    return nodes


def traverse(nodes: dict, directions: str, start: str, stop) -> int:
    current = start
    path_len = 0
    for d in itertools.cycle(directions):
        next_label = nodes[current].next(d)
        #print(f"{current} --{d}--> {next_label}")
        path_len += 1
        if stop(next_label):
            return path_len
        current = next_label

def ghostwalk(nodes: dict, directions: str) -> int:
    # Find all nodes that end with A
    start_nodes = list(filter(lambda x: x.endswith("A"), nodes.keys()))
    
    # Find the path length for each of the start nodes
    pathlens = [ traverse(nodes, directions, s, lambda x: x.endswith("Z")) \
                for s in start_nodes]
    print(pathlens)
    return math.lcm(*pathlens)

if __name__ == "__main__":
    with open(sys.argv[1], "r") as infile:
        chunks = infile.read().split("\n\n")
        directions = chunks[0]
        nodelist = chunks[1]

        nodes = create_nodes(nodelist)
        if len(sys.argv) > 2:
            pathlen = ghostwalk(nodes, directions)
            print(f"Ghost length from **A to **Z: {pathlen}")
        else:
            pathlen = traverse(nodes, directions, "AAA", lambda x: x == "ZZZ")
            print(f"Path length from AAA to ZZZ: {pathlen}")