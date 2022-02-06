from enum import Enum
from collections import Counter

class Suit(Enum):
    HEART = 'Hearts'
    SPADE = 'Spades'
    DIAMOND = 'Diamonds'
    CLUB = 'Clubs'

class Rank(Enum):
    STRAIGHT_FLUSH = 2
    FOUR_KIND = 3
    FULL_HOUSE = 4
    FLUSH = 5
    STRAIGHT = 6
    THREE_KIND = 7
    TWO_PAIR = 8
    PAIR = 9
    HIGH_CARD = 10

class Result(Enum):
    WIN = 1
    LOSE = 2
    TIE = 3

STR_TO_VAL = {'J': 11, 'Q': 12, 'K': 13, 'A': 14}
STR_TO_SUIT = {'H': Suit.HEART, 'S': Suit.SPADE, 'D': Suit.DIAMOND, 'C': Suit.CLUB}

class Card:
    def __init__(self, val):
        valStr, suitStr = val[:-1], val[-1]
        if valStr.isdigit() and 2 <= int(valStr) <= 10:
            self.val = int(valStr)
        elif valStr in STR_TO_VAL:
            self.val = STR_TO_VAL[valStr]
        else:
            raise ValueError
        if suitStr in STR_TO_SUIT:
            self.suit = STR_TO_SUIT[suitStr]
        else:
            raise ValueError

class Hand:
    def __init__(self, cardVals):
        vals = cardVals.split()
        if len(vals) != 5 or len(set(vals)) != 5:
            raise ValueError
        self.cards = [Card(val) for val in vals]
        self.evaluate()

    def evaluate(self):
        self.vals = sorted(card.val for card in self.cards)
        flush = all(card.suit == self.cards[0].suit for card in self.cards)
        straight = all(self.vals[i] + 1 == self.vals[j] or (self.vals[j] == 14 and self.vals[0] == 2) for i,j in zip(range(4), range(1,5)))
        counts = Counter(self.vals).most_common()
        self.tiebreaker = ()
        if flush and straight:
            self.rank = Rank.STRAIGHT_FLUSH
            if self.vals[-1] == 14 and self.vals[0] == 2:
                self.vals[-1] = 1
                self.vals.sort()
        elif counts[0][1] == 4:
            self.rank = Rank.FOUR_KIND
            self.tiebreaker = counts[0][0],
        elif counts[0][1] == 3 and counts[1][1] == 2:
            self.rank = Rank.FULL_HOUSE
            self.tiebreaker = counts[0][0], counts[1][0]
        elif flush:
            self.rank = Rank.FLUSH
        elif straight:
            self.rank = Rank.STRAIGHT
            if self.vals[-1] == 14 and self.vals[0] == 2:
                self.vals[-1] = 1
                self.vals.sort()
        elif counts[0][1] == 3:
            self.rank = Rank.THREE_KIND
            self.tiebreaker = counts[0][0],
        elif counts[0][1] == 2 and counts[1][1] == 2:
            self.rank = Rank.TWO_PAIR
            self.tiebreaker = max(counts[0][0], counts[1][0]), min(counts[0][0], counts[1][0])
        elif counts[0][1] == 2:
            self.rank = Rank.PAIR
            self.tiebreaker = counts[0][0],
        else:
            self.rank = Rank.HIGH_CARD

# Assume it is okay to have duplicates across hands, ie the same card can be in both hands
def betterHand(hand1, hand2):
    # Better ranked hand wins
    if hand1.rank.value < hand2.rank.value:
        return Result.WIN
    elif hand1.rank.value > hand2.rank.value:
        return Result.LOSE
    # Some hands have higher priority for certain cards, check those first for tiebreakers
    for val1, val2 in zip(hand1.tiebreaker, hand2.tiebreaker):
        if val1 > val2:
            return Result.WIN
        elif val1 < val2:
            return Result.LOSE
    # If the high priority tiebreakers are the same, any higher card wins
    for i in range(4,-1,-1):
        if hand1.vals[i] > hand2.vals[i]:
            return Result.WIN
        elif hand1.vals[i] < hand2.vals[i]:
            return Result.LOSE
    # Both hands have the same value
    return Result.TIE

if __name__ == '__main__':
    print('Enter 5 card values and suits, with cards separated by spaces')
    print('Values from 2-10 or JQKA, suits from HSDC ex. "2C AD 7C KS 10H"')
    try:
        while True:
            print('Enter the first hand:')
            hand1 = Hand(input())
            print('Enter the second hand:')
            hand2 = Hand(input())
            result = betterHand(hand1, hand2)
            if result == Result.WIN:
                print('Hand 1 wins')
            elif result == Result.LOSE:
                print('Hand 2 wins')
            else:
                print('Tie')
    except ValueError:
        print('Invalid input')
