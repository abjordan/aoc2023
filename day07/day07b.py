from collections import Counter
import functools
from itertools import groupby
import re
import sys

# Restructured per the writeup at https://advent-of-code.xavd.id/writeups/2023/day/7/
# I was doing essentially the same thing (see day07.py), but much less elegantly. I 
# really like the structural matching -- I didn't know you could do that with whole
# lists of values!

hand_ranking= reversed(['five', 'four', 'full', 'three', 'two_pair', 'pair', 'high'])
card_ranking = reversed(["A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2", "J"])

def explicit_order(xs):
    """Return a key function that, when passed to sort or sorted, will sort
    the elements in the order they appear in this list.
    """
    keys = {x: i for i, x in enumerate(xs)}
    def key_function(x):
        if not x in keys:
            raise RuntimeError(f"Unknown key: {x}")
        return keys[x]
    return key_function

hand_order = explicit_order(hand_ranking)
card_order = explicit_order(card_ranking)

def score_hand(hand):
    cards = hand.copy()
    
    # Count 'em all up
    hand_values = sorted(Counter(cards).values())
    print(hand_values)

    num_jokers = cards.count("J")
    if 0 < num_jokers < 5:
        hand_values.remove(num_jokers)
        hand_values[-1] += num_jokers

    match hand_values:
        case [5]:
            return 'five'
        case [1, 4]:
            return 'four'
        case [2, 3]:
            return 'full'
        case [1, 1, 3]:
            return 'three'
        case [1, 2, 2]:
            return 'two_pair'
        case [1, 1, 1, 2]:
            return 'pair'
        case [1, 1, 1, 1, 1]:
            return 'high'
        case _:
            raise ValueError(f"Unknown hand: {cards}")
                
@functools.total_ordering
class Hand:
    def __init__(self, _cards, _bid):
        self.cards = [*_cards]
        self.bid = _bid
        self.hand_type = score_hand(self.cards)
        #print(f"{_cards} --> {self.hand_type}")

    def __str__(self):
        return "".join(self.cards) + " " + str(self.bid)

    def _is_valid_operand(self, other):
        return isinstance(other, Hand)

    def __lt__(self, other):
        #print(f"Comparing {self.cards} < {other.cards}")
        if not self._is_valid_operand(other):
            return NotImplemented
        if self.__eq__(other):
            return False
        # See if hand type is weaker than other hand type
        if hand_order(self.hand_type) < hand_order(other.hand_type):
            #print(f"{self.hand_type} < {other.hand_type}")
            return True
        elif hand_order(self.hand_type) > hand_order(other.hand_type):
            return False
        else:
            # Tiebreaker!
            pass
        
        # If they're the same, then tie breaker is string order
        for s, o in zip(self.cards, other.cards):
            #print(f"  {s} <? {o}")
            if card_order(s) < card_order(o):
                #print(f"{s} < {o}")
                return True
            elif card_order(s) > card_order(o):
                return False
            else:
                # keep looking
                pass
            
        return self.bid < other.bid
        
    def __eq__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented
        return ("".join(self.cards) == "".join(other.cards)) and (self.bid == other.bid)

def process(lines):
    # Each line is a hand, followed by a bid amount
    hands = []
    for line in lines:
        toks = line.split(" ")
        hand = Hand(toks[0], int(toks[1]))
        hands.append(hand)

    assert(hands[-1] == hands[-1])
    assert(hands[-1] != hands[0])

    # Sort the hands by their strength, smallest to largest
    hands = sorted(hands)
    #for h in hands:
    #    print(h)

    # Calculate the payout
    winnings = 0
    for index, hand in enumerate(hands, start=1):
        print(f"{index} = {''.join(hand.cards)} ; {hand.hand_type} ; {hand.bid} ")
        winnings += index * hand.bid
    print(winnings)

if __name__ == "__main__":

    with open(sys.argv[1], "r") as infile:
        lines = [l.strip() for l in infile.readlines()]
        process(lines)