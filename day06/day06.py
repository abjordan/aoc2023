import re
import sys


def calc_race(duration, record):
    # How many ways can you beat the record?
    # Distance = press * duration - press ^ 2
    # How many distances are > record?

    count = 0
    for p in range(0, duration + 1):
        dist = p * duration - p**2
        if dist > record:
            count += 1
    return count

def process(lines):
    times    = [int(x) for x in lines[0].split(":")[1].split()]
    records  = [int(x) for x in lines[1].split(":")[1].split()]
    print(times)
    print(records)

    total = 1
    for t,r in zip(times, records):
        count = calc_race(t, r)
        print(f"Race ({t}, {r}) --> {count}")
        total = total * count

    print(f"Total: {total}")

if __name__ == "__main__":

    with open(sys.argv[1], "r") as infile:
        lines = [l.strip() for l in infile.readlines()]
        process(lines)