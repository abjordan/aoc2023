#!/usr/bin/env python

import itertools

import numpy as np
import sys

def print_field(field):
    rows, cols = np.shape(field)
    for row in field:
        for col in row:
            char = '?'
            match col:
                case 0:
                    char = '.'
                case 1:
                    char = '#'
                case -1:
                    char = '_'
            print(char, end='')
        print()
        
def part_a(field):
    # Find rows that are all zeros
    row_sums = np.sum(field, axis=1)
    col_sums = np.sum(field, axis=0)
    print(f"Rows: {row_sums}")
    print(f"Cols: {col_sums}")
    
    expanded_field = field.copy()

    rows_to_add = []
    cols_to_add = []
    for r_idx, row in enumerate(row_sums):
        if row == 0:
            rows_to_add.append(r_idx)
    for c_idx, col in enumerate(col_sums):
        if col == 0:
            cols_to_add.append(c_idx)
    
    print("Rows to add: ", rows_to_add)
    print("Cols to add: ", cols_to_add)

    offset = 0
    for new_row in rows_to_add:
        expanded_field = np.insert(expanded_field, new_row + offset, 0, axis=0)
        offset += 1

    offset = 0
    for new_col in cols_to_add:
        expanded_field = np.insert(expanded_field, new_col + offset, 0, axis=1)
        offset += 1

    print_field(expanded_field)

    galaxy_coords = np.transpose(np.nonzero(expanded_field))
    galaxy_pairs = itertools.combinations(galaxy_coords, 2)

    distance_sum = 0
    for p in galaxy_pairs:
        # The metric here is Manhattan distance 
        distance_sum += abs(p[0][0] - p[1][0]) + abs(p[0][1] - p[1][1])
    return distance_sum

if __name__ == "__main__":

    with open(sys.argv[1], "r") as infile:
        # This would actually be easier to do in Excel...  >_<
        data = infile.read()
        lines = data.split("\n")
        rows = len(lines)
        cols = len(lines[0])

        field = np.zeros((rows,cols))
        for r, row in enumerate(lines):
            for c, col in enumerate(lines[r]):
                field[r,c] = 0 if col == '.' else 1
        print_field(field)
        print('-----------------------------')
        result_a = part_a(field)
        print(f"Sum of galaxy distances is {result_a}")