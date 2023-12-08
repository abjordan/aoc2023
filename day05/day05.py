#!/usr/bin/env python

import re
import sys

from collections import defaultdict

# Parse the input
# x-to-y map:
# dst_start src_start length
# ...
# <blank line>
# y-to-z map:
# dst_start src_start length
# ...
# etc.

maps = defaultdict(lambda: defaultdict(list))

map_re = re.compile(r"(\S+)-to-(\S+) map")

with open(sys.argv[1], "r") as infile:
    data = infile.read()
    chunks = data.split("\n\n")
    
    for chunk in chunks:
        if chunk.startswith("seeds: "):
            toks = chunk.split(" ")
            seeds = [int(x) for x in toks[1:]]
        else:
            # This is a map
            lines = chunk.split("\n")
            m = map_re.match(lines[0])
            src, dst = m.groups()
            
            for line in lines[1:]:
                dst_start, src_start, length = [int(x) for x in line.split(" ")]
                maps[src][dst].append((src_start, dst_start, length))    
                # Inline function definition goes here!

    print(seeds)

    # for src in maps.keys():
    #     for dst in maps[src].keys():
    #         for mapping in maps[src][dst]:
    #             print(f"{src}->{dst}: {mapping}")

    # Try each seed through the maps
    #
    # If there's no value in the mapping ranges, then 
    # you keep your value.
    #
    # The sample has small ranges, but the real input has very
    # large ranges. If we tried to do it explicitly, it would be rough
    def check_range(value, mapping):
        src_start, dst_start, length = mapping
        if (value >= src_start) and (value <= src_start + length):
            offset = value - src_start
            #print(f"Hit: {value} in {mapping}")
            return dst_start + offset
        else:
            return None
        
    def check_ranges(value, mappings):
        output = None
        for mapping in mappings:
            output = check_range(value, mapping)
            if output is not None:
                break
        if output is None:
            output = value
        return output

    lowest_result = 9999999999999999999999
    chain = ['seed', 'soil', 'fertilizer', 'water', 'light', 'temperature', 'humidity', 'location']
    for seed in seeds:
        input = seed
        output = None
        for i in range(0, len(chain) - 1):
            src = chain[i]
            dst = chain[i+1]
            output = check_ranges(input, maps[src][dst])
            print(f"{dst} {output} ", end="")
            input = output
        lowest_result = min(lowest_result, output)
        print("")
    print(lowest_result)