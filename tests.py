import unittest
from poker import Card, Hand, Rank, Result, betterHand

INVALID_HANDS = [
    '',
    '2C',
    '2C 3C 4C 5C 6C 7C',
    '2C 2C 2C 2C 2C',
    'AC 2C 3C 4C AC',
    '11C',
    '1C'
]

class TestValidInput(unittest.TestCase):
    def test_valid_input(self):
        for hand in INVALID_HANDS:
            with self.subTest(hand=hand):
                with self.assertRaises(ValueError):
                    Hand(hand)

RANK_TO_HAND = {
    Rank.STRAIGHT_FLUSH: '2C 6C 4C 5C 3C',
    Rank.FOUR_KIND: '2C 2H 2D 6C 2S',
    Rank.FULL_HOUSE: '2C 5S 2D 5H 5C',
    Rank.FLUSH: '2C 4C 7C 8C 9C',
    Rank.STRAIGHT: '3C 4S 5D 2H 6S',
    Rank.THREE_KIND: '4D 2C 9S 4C 4S',
    Rank.TWO_PAIR: '7S 7C KD 3H KH',
    Rank.PAIR: 'AC 7S 9S KH AH',
    Rank.HIGH_CARD: '7S 2H 3C 4C JD'
}

class TestRank(unittest.TestCase):
    def test_rank(self):
        for rank, hand in RANK_TO_HAND.items():
            with self.subTest(rank=rank, hand=hand):
                self.assertEqual(rank, Hand(hand).rank)

    def test_straight(self):
        self.assertEqual(Rank.STRAIGHT, Hand('AC 5D 4S 2C 3C').rank)

HIGH_CARD_TO_HAND = {
    3: '3C 2C 2H 2D 2S',
    4: '4C 2C 2H 2D 2S',
    5: '5C 2C 2H 2D 2S',
    6: '6C 2C 2H 2D 2S',
    7: '7C 2C 2H 2D 2S',
    8: '8C 2C 2H 2D 2S',
    9: '9C 2C 2H 2D 2S',
    10: '10C 2C 2H 2D 2S',
    11: 'JC 2C 2H 2D 2S',
    12: 'QC 2C 2H 2D 2S',
    13: 'KC 2C 2H 2D 2S',
    14: 'AC 2C 2H 2D 2S'
}

class TestHighCard(unittest.TestCase):
    def test_high_card(self):
        for highcard, hand in HIGH_CARD_TO_HAND.items():
            with self.subTest(highcard=highcard, hand=hand):
                self.assertEqual(highcard, Hand(hand).vals[-1])

class TestBetterHand(unittest.TestCase):
    def test_better_rank(self):
        for i in range(2,11):
            for j in range(i+1,11):
                hand1, hand2 = RANK_TO_HAND[Rank(i)], RANK_TO_HAND[Rank(j)]
                with self.subTest(rank1=i, rank2=j, hand1=hand1, hand2=hand2):
                    hand1, hand2 = Hand(hand1), Hand(hand2)
                    self.assertEqual(Result.WIN, betterHand(hand1, hand2))
                    self.assertEqual(Result.LOSE, betterHand(hand2, hand1))

    def test_better_highcard(self):
        for i in range(4,15):
            for j in range(3,i):
                hand1, hand2 = HIGH_CARD_TO_HAND[i], HIGH_CARD_TO_HAND[j]
                with self.subTest(highcard1=i, highcard2=j, hand1=hand1, hand2=hand2):
                    hand1, hand2 = Hand(hand1), Hand(hand2)
                    self.assertEqual(Result.WIN, betterHand(hand1, hand2))
                    self.assertEqual(Result.LOSE, betterHand(hand2, hand1))

TIEBREAKERS = [
    ('5C 7C 6C 4C 3C', '2C 6C 4C 5C 3C'), # Rank.STRAIGHT_FLUSH
    ('2C 6C 4C 5C 3C', '2C AC 4C 5C 3C'), # Rank.STRAIGHT_FLUSH
    ('3C 3H 3D 4C 3S', '2C 2H 2D 6C 2S'), # Rank.FOUR_KIND
    ('2C 2H 2D 7C 2S', '2C 2H 2D 6C 2S'), # Rank.FOUR_KIND
    ('2C 6S 2D 6H 6C', 'KC 5S KD 5H 5C'), # Rank.FULL_HOUSE
    ('AC 5S AD 5H 5C', 'JC 5S JD 5H 5C'), # Rank.FULL_HOUSE
    ('2C AC 7C 8C 9C', '2C 4C 7C 8C 9C'), # Rank.FLUSH
    ('3C 4C 7C 8C 9C', '2C 4C 7C 8C 9C'), # Rank.FLUSH
    ('3C 4S 5D 7H 6S', '3C 4S 5D 2H 6S'), # Rank.STRAIGHT
    ('3C 4S 5D 2H 6S', '3C 4S 5D 2H AS'), # Rank.STRAIGHT
    ('4D 2C 9S 4C 4S', '3D AC 9S 3C 3S'), # Rank.THREE_KIND
    ('4D AC 9S 4C 4S', '4D 2C 9S 4C 4S'), # Rank.THREE_KIND
    ('7S 7C KD AH KH', '7S 7C KD 3H KH'), # Rank.TWO_PAIR
    ('8S 8C KD 3H KH', '7S 7C KD AH KH'), # Rank.TWO_PAIR
    ('7S 7C JD 2H JH', '8S 8C 10D AH 10H'), # Rank.TWO_PAIR
    ('2C 7S 9S KH 7H', '6C 7S 9S 6H AH'), # Rank.PAIR
    ('AC 8S 9S KH AH', 'AC 7S 9S KH AH'), # Rank.PAIR
    ('7S 5H 3C 4C JD', '7S 2H 3C 4C JD') # Rank.HIGH_CARD
]

class TestTiebreakers(unittest.TestCase):
    def test_tiebreakers(self):
        for hand1, hand2 in TIEBREAKERS:
            with self.subTest(hand1=hand1, hand2=hand2):
                hand1, hand2 = Hand(hand1), Hand(hand2)
                self.assertEqual(Result.WIN, betterHand(hand1, hand2))
                self.assertEqual(Result.LOSE, betterHand(hand2, hand1))

TIES = [
    ('2C 6C 4C 5C 3C', '2D 6D 4D 5D 3D'), # Rank.STRAIGHT_FLUSH
    ('2C 2H 2D 6D 2S', '2C 2H 2D 6C 2S'), # Rank.FOUR_KIND
    ('5D 2H 2D 5C 5S', '2C 5S 2D 5H 5C'), # Rank.FULL_HOUSE
    ('2D 8D 9D 4D 7D', '2C 4C 7C 8C 9C'), # Rank.FLUSH
    ('3H 4D 5S 2S 6H', '3C 4S 5D 2H 6S'), # Rank.STRAIGHT
    ('4H 2D 9D 4C 4S', '4D 2C 9S 4C 4S'), # Rank.THREE_KIND
    ('7H KS 3D KC 7D', '7S 7C KD 3H KH'), # Rank.TWO_PAIR
    ('AD 9D KC AS 7C', 'AC 7S 9S KH AH'), # Rank.PAIR
    ('7C 2S 4S JS 3S', '7S 2H 3C 4C JD') # Rank.HIGH_CARD
]

class TestTiedHand(unittest.TestCase):
    def test_tied_hand(self):
        for hand1, hand2 in TIES:
            with self.subTest(hand1=hand1, hand2=hand2):
                self.assertEqual(Result.TIE, betterHand(Hand(hand1), Hand(hand2)))

if __name__ == '__main__':
    unittest.main()
