import re
import sys
#            winners     |          our numbers
# Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53

with open(sys.argv[1], 'r') as infile:
    lines = [s.strip() for s in infile.readlines()]

    total_value = 0

    pattern = re.compile(r"Card\s+(\d+):(.*)\|(.*)")

    for line in lines:
        m = pattern.match(line)
        if m is None:
            print("Weird line: %r" % line)
        id, winners, ours = m.groups()

        winners = set( [int(x) for x in winners.strip().split(" ") if x != ""] )
        ours = set( [int(x) for x in ours.strip().split(" ") if x != ""] )
        
        # Payout is 2 to the number of winners in "ours"
        matches = ours.intersection(winners)
        if len(matches) > 0:
            payout = 2 ** (len(matches) - 1)
        else:
            payout = 0
        #print(payout)
        total_value += payout

    print(total_value)