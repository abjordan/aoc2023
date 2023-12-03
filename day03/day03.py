from collections import defaultdict
from collections import OrderedDict
import re
import sys

# Intuition: each number is a span on a line,
# and if any digit in the span is adjacent to a 
# symbol, then the number is a part number

number_re = re.compile(r"\d+")
symbol_re = re.compile(r'[^\.^\d]')

numbers = OrderedDict()
symbols = defaultdict(dict)
with open(sys.argv[1], "r") as infile:
    lines = [s.strip() for s in infile.readlines()]
    row = 0
    for line in lines:
        for m in number_re.finditer(line):
            value = int(m.group(0))
            start = m.start()
            stop = m.end() - 1
            numbers[(row, (start, stop))] = value
            #print(row, (start, stop), value)

        for m in symbol_re.finditer(line):
            symbol = m.group(0)
            start = m.start()
            symbols[row][start] = symbol

        row += 1

    total = 0
    num_rows = row
    for (row, (col_start, col_stop)), number in numbers.items():
        # need to check:
        #  (row - 1, col_start -1) --> (row - 1, col_stop + 1)
        #  (row, col_start - 1)
        #  (row, col_stop + 1)
        #  (row + 1, col_start -1) --> (row + 1, col_stop + 1)
        hit = False
        if (row - 1) in symbols.keys():
            #print("Check row - 1")
            for c in range(col_start - 1, col_stop + 2):
                if c in symbols[row-1].keys():
                    hit = True
        
        if row in symbols.keys():
            #print("Check row")
            if (col_start - 1) in symbols[row].keys() or (col_stop + 1) in symbols[row].keys():
                hit = True

        if (row + 1) in symbols.keys():
            #print("Check row + 1")
            for c in range(col_start - 1, col_stop + 2):
                #print(f"  check {c}")
                if c in symbols[row+1].keys():
                    hit = True

        #print(number, (row, (col_start, col_stop)), hit)
        if hit:
            total += number
        #break

    print(total)