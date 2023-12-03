#!/usr/bin/env python

import re

#DATAFILE = "sample.txt"
DATAFILE = "input-1.txt"
#DATAFILE = "sample-pt2.txt"

#### Part 2

values = {
    "one" : 1,
    "two" : 2,
    "three" : 3,
    "four" : 4,
    "five" : 5,
    "six" : 6,
    "seven" : 7,
    "eight" : 8,
    "nine" : 9,
    "zero" : 0,
}

digit_or_word = re.compile(r'[0-9]|one|two|three|four|five|six|seven|eight|nine|zero')

digit_rev = re.compile(r'[0-9]|eno|owt|eerht|ruof|evif|xis|neves|thgie|enin|orez')

with open(DATAFILE, "r") as infile:
    sum = 0
    for line in infile.readlines():
        line = line.strip()
        m = digit_or_word.search(line)
        tens = int(m[0]) if m[0].isdigit() else values[m[0]]

        m = digit_rev.search("".join(reversed(line)))
        ones = int(m[0]) if m[0].isdigit() else values["".join(reversed(m[0]))]
        print(tens, ones)
        sum += 10 * tens + ones

print(sum)