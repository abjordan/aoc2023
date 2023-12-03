#!/usr/bin/env python

import re

#DATAFILE = "sample.txt"
#DATAFILE = "input-1.txt"
DATAFILE = "sample-pt2.txt"

with open(DATAFILE, "r") as infile:
    sum = 0
    for line in infile.readlines():
        line = line.strip()
        digits = [x for x in line if x.isdigit()]
        sum += int(digits[0] + digits[-1])
print(sum)

#### Part 2

digit_or_word = re.compile(r'[0-9]|one|two|three|four|five|six|seven|eight|nine|zero')

with open(DATAFILE, "r") as infile:
    sum = 0
    for line in infile.readlines():
        line = line.strip()
        m = digit_or_word.findall(line)
        print(m)
        