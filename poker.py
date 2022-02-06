from enum import Enum
from collections import Counter

class Suit(Enum):
    HEART = 'Hearts'
    SPADE = 'Spades'
    DIAMOND = 'Diamonds'
    CLUB = 'Clubs'

class Result(Enum):
    WIN = 1
    LOSE = 2
    TIE = 3

STR_TO_VAL = {'J': 11, 'Q': 12, 'K': 13, 'A': 14}
STR_TO_SUIT = {'H': Suit.HEART, 'S': Suit.SPADE, 'D': Suit.DIAMOND, 'C': Suit.CLUB}
VAL_TO_STR = {11: 'Jack', 12: 'Queen', 13: 'King', 14: 'Ace'}

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

    def __str__(self):
        valStr = VAL_TO_STR[self.val] if self.val in VAL_TO_STR else str(self.val)
        return '{0} of {1}'.format(valStr, self.suit.value)

class Hand:
    def __init__(self, cardVals):
        vals = cardVals.split()
        if len(vals) != 5 or len(set(vals)) != 5:
            raise ValueError
        self.cards = [Card(val) for val in vals]
        self.getRank()

    def __str__(self):
        return ', '.join([str(card) for card in self.cards])

    def getRank(self):
        vals = sorted(card.val for card in self.cards)
        self.highcard = vals[-1]
        flush = all(card.suit == self.cards[0].suit for card in self.cards)
        straight = all(vals[i] + 1 == vals[j] or (vals[j] == 14 and vals[0] == 2) for i,j in zip(range(4), range(1,5)))
        counts = Counter(vals)
        numMatches = counts.most_common(1)[0][1]
        if flush and straight:
            self.rank = 2
        elif numMatches == 4:
            self.rank = 3
        elif numMatches == 3 and len(counts) == 2:
            self.rank = 4
        elif flush:
            self.rank = 5
        elif straight:
            self.rank = 6
        elif numMatches == 3:
            self.rank = 7
        elif numMatches == 2 and len(counts) == 3:
            self.rank = 8
        elif numMatches == 2:
            self.rank = 9
        else:
            self.rank = 10

def betterHand(hand1, hand2):
    if hand1.rank < hand2.rank or (hand1.rank == hand2.rank and hand1.highcard > hand2.highcard):
        return Result.WIN
    elif hand1.rank > hand2.rank or (hand1.rank == hand2.rank and hand1.highcard < hand2.highcard):
        return Result.LOSE
    else:
        return Result.TIE

if __name__ == '__main__':
    print('Enter 5 card values and suits, with cards separated by spaces')
    print('Values from 2-10 or JQKA, suits from HSDC ex. "2C AD 7C KS 10H"')
    try:
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
