from collections import defaultdict
from functools import reduce
import re
import sys

# Intuition: each number is a span on a line,
# and if any digit in the span is adjacent to a 
# symbol, then the number is a part number

number_re = re.compile(r"\d+")
symbol_re = re.compile(r'[^\.^\d]')

numbers = defaultdict(dict)
symbols = defaultdict(dict)
with open(sys.argv[1], "r") as infile:
    lines = [s.strip() for s in infile.readlines()]
    row = 0
    for line in lines:
        for m in number_re.finditer(line):
            value = int(m.group(0))
            start = m.start()
            stop = m.end() - 1
            numbers[row][(start, stop)] = value
            #print(row, (start, stop), value)

        for m in symbol_re.finditer(line):
            if m.group(0) != "*":
                continue
            symbol = m.group(0)
            start = m.start()
            symbols[row][start] = symbol

        row += 1

    total = 0
    num_rows = row

    # Check each symbol to see if it is a *. If it is, check to see
    # if it's adjacent to exactly two numbers
    for r in symbols:
        for c in symbols[r]:
            if symbols[r][c] != "*":
                continue            
            

            hits = []
            # Check to see if (r-1, c-1:c+1) belongs to a number
            # Check to see if (r, c-1) or (r, c+1) belongs to a number
            # Check to see if (r+1, c-1:c+1) belongs to a number
            if (r-1) in numbers.keys():
                for (start, stop), value in numbers[r-1].items():
                    if c in range(start-1, stop+2):
                        hits.append(value)
            if r in numbers.keys():
                for (start, stop), value in numbers[r].items():
                    if (stop == c - 1) or (start == c + 1):
                        hits.append(value)
            if (r+1) in numbers.keys():
                for (start, stop), value in numbers[r+1].items():
                    if c in range(start-1, stop+2):
                        hits.append(value)
            print(f"({r},{c}) --> {hits}")
            if len(hits) == 2:
                power = reduce(lambda x,y: x * y, hits)
                total += power

    print(total)