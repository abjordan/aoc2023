from collections import defaultdict

import functools
import re
import sys
#            winners     |          our numbers
# Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
#
# If you match N, you get copies of the next N scratchcards
# This is... a little ridiculous

with open(sys.argv[1], 'r') as infile:
    lines = [s.strip() for s in infile.readlines()]

    total_value = 0

    pattern = re.compile(r"Card\s+(\d+):(.*)\|(.*)")

    card_copies = defaultdict(lambda: 1)

    for line in lines:
        m = pattern.match(line)
        if m is None:
            print("Weird line: %r" % line)
        idx, winners, ours = m.groups()

        idx = int(idx)
        if idx not in card_copies.keys():
            card_copies[idx] = 1
        winners = set( [int(x) for x in winners.strip().split(" ") if x != ""] )
        ours = set( [int(x) for x in ours.strip().split(" ") if x != ""] )
        
        # Payout is 2 to the number of winners in "ours"
        matches = len(ours.intersection(winners))

        for i in range(idx + 1, idx + matches + 1):
            #print(f"Bumping {i}")
            card_copies[i] += card_copies[idx]

        #print(f"Card {idx} (count {card_copies[idx]}) --> made {matches} copies")
    
    total_count = 0
    for idx, count in card_copies.items():
        print(f"{idx} --> {count}")
        total_count += count

    print(total_count)
