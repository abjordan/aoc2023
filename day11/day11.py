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
        d = abs(p[0][0] - p[1][0]) + abs(p[0][1] - p[1][1])
        distance_sum += d
        #print(f"({p[0][0]},{p[0][1]}) --> ({p[1][0]},{p[1][1]}) = {d}")
    return distance_sum

def between(bound_a, bound_b, query):
    #print(f"{bound_a} < {query} < {bound_b}")
    if bound_a < bound_b:
        return ((query > bound_a) and (query < bound_b))
    elif bound_b < bound_a:
        return ((query > bound_b) and (query < bound_a))
    else:
        # This smells like a bug waiting to happen
        return False


def part_b(field, expansion_factor=1):
    # The trick here is to find the rows and columns that are empty
    # and then check to see how many of them are between you in each
    # dimension. You can just add that much to each distance as you
    # calculate the Manhattan distance, rather than generating the actual
    # starfield.
    row_sums = np.sum(field, axis=1)
    col_sums = np.sum(field, axis=0)
    
    expansion_factor -= 1   # If it "grows by 10", you add 9 spaces

    empty_rows = []
    empty_cols = []
    for r_idx, row in enumerate(row_sums):
        if row == 0:
            empty_rows.append(r_idx)
    for c_idx, col in enumerate(col_sums):
        if col == 0:
            empty_cols.append(c_idx)
    print("Rows: ", empty_rows)
    print("Cols: ", empty_cols)

    galaxy_coords = np.transpose(np.nonzero(field))
    galaxy_pairs = itertools.combinations(galaxy_coords, 2)

    distance_sum = 0
    for p in galaxy_pairs:
        m_dist = abs(p[0][0] - p[1][0]) + abs(p[0][1] - p[1][1])
        # For each empty row between the galaxies, add the expansion factor
        for er in empty_rows:
            if between(p[0][0], p[1][0], er):
                #print("_")
                m_dist += expansion_factor
        for ec in empty_cols:
            if between(p[0][1], p[1][1], ec):
                #print("_")
                m_dist += expansion_factor
        distance_sum += m_dist
        #print(f"({p[0][0]},{p[0][1]}) --> ({p[1][0]},{p[1][1]}) = {m_dist}")
        #break
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
        print(f"Part A: Sum of galaxy distances is {result_a}")

        print('-----------------------------')
        result_b = part_b(field, 2)
        print(f"Part B: Sum of 1x expanded distances is {result_b}")

        result_b = part_b(field, 10)
        print(f"Part B: Sum of 10x expanded distances is {result_b}")

        result_b = part_b(field, 100)
        print(f"Part B: Sum of 100x expanded distances is {result_b}")

        result_b = part_b(field, 1000000)
        print(f"Part B: Sum of 100x expanded distances is {result_b}")
