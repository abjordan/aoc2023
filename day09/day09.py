#!/usr/bin/env python3

import itertools
import functools

# There's some really deep math here. I think this is another one of 
# those puzzles where if you understand the algorithm it's simple and
# if you don't, you're never gonna get a star.  

# The naive approach here is recursion. This being AoC, this will work
# for part A, but will not work for part B. I think this should be 
# properly tail recursive, which means that you can evaluate it in 
# some other languages much more efficiently.
def process(values: list) -> int:
    '''This function returns the value to add to the list above it'''
    #print(values)

    # Base case: all zeros means we're at the bottom of the pile
    if functools.reduce(lambda x,y: x and y, [x == 0 for x in values]):
        #print("Done")
        return 0
    
    # Deltafy the list
    deltas = [y-x for x,y in itertools.pairwise(values)]

    # Return the last delta value plus the result of processing it
    addend = process(deltas)
    #print(f"<-- {deltas[-1]} + {addend}")
    return deltas[-1] + addend


if __name__ == "__main__":
    import sys
    with open(sys.argv[1], "r") as infile:
        lines = infile.read().split("\n")

        sum_pred = 0
        for line in lines:
            values = [int(x) for x in line.split()]

            # For part B... isn't this the same as just 
            # reversing the list? Arrow of time and all that?
            if len(sys.argv) > 2: 
                values = list(reversed(values))

            prediction = values[-1] + process(values)
            print(f"Prediction: {prediction}")
            sum_pred += prediction

        print(f"Total of predictions: {sum_pred}")
            