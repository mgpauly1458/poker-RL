import unittest
from poker_util import (
    Card, RoyalFlush, StraightFlush, FourOfAKind, FullHouse, Flush, Straight,
    ThreeOfAKind, TwoPair, OnePair, HighCard, PokerException
)

class TestPokerHands(unittest.TestCase):

    def test_royal_flush(self):
        cards = [
            Card('10', 'Hearts'), Card('J', 'Hearts'), Card('Q', 'Hearts'),
            Card('K', 'Hearts'), Card('A', 'Hearts')
        ]
        hand = RoyalFlush(cards)
        self.assertIsInstance(hand, RoyalFlush)

    def test_straight_flush(self):
        cards = [
            Card('9', 'Spades'), Card('10', 'Spades'), Card('J', 'Spades'),
            Card('Q', 'Spades'), Card('K', 'Spades')
        ]
        hand = StraightFlush(cards)
        self.assertIsInstance(hand, StraightFlush)

    def test_four_of_a_kind(self):
        cards = [
            Card('A', 'Clubs'), Card('A', 'Diamonds'), Card('A', 'Hearts'),
            Card('A', 'Spades'), Card('K', 'Hearts')
        ]
        hand = FourOfAKind(cards)
        self.assertIsInstance(hand, FourOfAKind)

    def test_full_house(self):
        cards = [
            Card('Q', 'Clubs'), Card('Q', 'Diamonds'), Card('Q', 'Hearts'),
            Card('K', 'Spades'), Card('K', 'Hearts')
        ]
        hand = FullHouse(cards)
        self.assertIsInstance(hand, FullHouse)

    def test_flush(self):
        cards = [
            Card('2', 'Diamonds'), Card('5', 'Diamonds'), Card('8', 'Diamonds'),
            Card('J', 'Diamonds'), Card('K', 'Diamonds')
        ]
        hand = Flush(cards)
        self.assertIsInstance(hand, Flush)

    def test_straight(self):
        cards = [
            Card('4', 'Clubs'), Card('5', 'Diamonds'), Card('6', 'Hearts'),
            Card('7', 'Spades'), Card('8', 'Hearts')
        ]
        hand = Straight(cards)
        self.assertIsInstance(hand, Straight)

    def test_three_of_a_kind(self):
        cards = [
            Card('9', 'Clubs'), Card('9', 'Diamonds'), Card('9', 'Hearts'),
            Card('J', 'Spades'), Card('K', 'Hearts')
        ]
        hand = ThreeOfAKind(cards)
        self.assertIsInstance(hand, ThreeOfAKind)

    def test_two_pair(self):
        cards = [
            Card('10', 'Clubs'), Card('10', 'Diamonds'), Card('J', 'Hearts'),
            Card('J', 'Spades'), Card('K', 'Hearts')
        ]
        hand = TwoPair(cards)
        self.assertIsInstance(hand, TwoPair)

    def test_one_pair(self):
        cards = [
            Card('3', 'Clubs'), Card('3', 'Diamonds'), Card('7', 'Hearts'),
            Card('9', 'Spades'), Card('K', 'Hearts')
        ]
        hand = OnePair(cards)
        self.assertIsInstance(hand, OnePair)

    def test_high_card(self):
        cards = [
            Card('2', 'Clubs'), Card('5', 'Diamonds'), Card('7', 'Hearts'),
            Card('9', 'Spades'), Card('K', 'Hearts')
        ]
        hand = HighCard(cards)
        self.assertIsInstance(hand, HighCard)

    def test_invalid_hand(self):
        cards = [
            Card('2', 'Clubs'), Card('2', 'Diamonds'), Card('2', 'Hearts'),
            Card('3', 'Spades'), Card('4', 'Hearts')
        ]
        with self.assertRaises(PokerException):
            RoyalFlush(cards)

    def test_gt_operator(self):
        royal_flush = RoyalFlush([
            Card('10', 'Hearts'), Card('J', 'Hearts'), Card('Q', 'Hearts'),
            Card('K', 'Hearts'), Card('A', 'Hearts')
        ])
        straight_flush = StraightFlush([
            Card('9', 'Spades'), Card('10', 'Spades'), Card('J', 'Spades'),
            Card('Q', 'Spades'), Card('K', 'Spades')
        ])
        four_of_a_kind = FourOfAKind([
            Card('A', 'Clubs'), Card('A', 'Diamonds'), Card('A', 'Hearts'),
            Card('A', 'Spades'), Card('K', 'Hearts')
        ])
        full_house = FullHouse([
            Card('Q', 'Clubs'), Card('Q', 'Diamonds'), Card('Q', 'Hearts'),
            Card('K', 'Spades'), Card('K', 'Hearts')
        ])

        self.assertTrue(royal_flush > straight_flush)
        self.assertTrue(straight_flush > four_of_a_kind)
        self.assertTrue(four_of_a_kind > full_house)

    def test_invalid_royal_flush(self):
    # Invalid because it doesn't contain all cards from 10 to Ace of the same suit
        cards = [
            Card('10', 'Hearts'), Card('J', 'Hearts'), Card('Q', 'Hearts'),
            Card('K', 'Hearts'), Card('9', 'Hearts')
        ]
        with self.assertRaises(PokerException):
            RoyalFlush(cards)

    def test_invalid_straight_flush(self):
        # Invalid because the cards are not sequential
        cards = [
            Card('9', 'Spades'), Card('10', 'Spades'), Card('J', 'Spades'),
            Card('Q', 'Spades'), Card('A', 'Spades')
        ]
        with self.assertRaises(PokerException):
            StraightFlush(cards)

    def test_invalid_four_of_a_kind(self):
        # Invalid because it doesn't have four cards of the same rank
        cards = [
            Card('A', 'Clubs'), Card('A', 'Diamonds'), Card('A', 'Hearts'),
            Card('K', 'Spades'), Card('K', 'Hearts')
        ]
        with self.assertRaises(PokerException):
            FourOfAKind(cards)

    def test_invalid_full_house(self):
        # Invalid because it doesn't have three cards of one rank and two of another
        cards = [
            Card('Q', 'Clubs'), Card('Q', 'Diamonds'), Card('K', 'Hearts'),
            Card('K', 'Spades'), Card('A', 'Hearts')
        ]
        with self.assertRaises(PokerException):
            FullHouse(cards)

    def test_invalid_flush(self):
        # Invalid because not all cards are of the same suit
        cards = [
            Card('2', 'Diamonds'), Card('5', 'Diamonds'), Card('8', 'Diamonds'),
            Card('J', 'Diamonds'), Card('K', 'Hearts')
        ]
        with self.assertRaises(PokerException):
            Flush(cards)

    def test_invalid_straight(self):
        # Invalid because the cards are not sequential
        cards = [
            Card('4', 'Clubs'), Card('5', 'Diamonds'), Card('6', 'Hearts'),
            Card('8', 'Spades'), Card('9', 'Hearts')
        ]
        with self.assertRaises(PokerException):
            Straight(cards)

    def test_invalid_three_of_a_kind(self):
        # Invalid because it doesn't have exactly three cards of the same rank
        cards = [
            Card('9', 'Clubs'), Card('9', 'Diamonds'), Card('J', 'Hearts'),
            Card('J', 'Spades'), Card('K', 'Hearts')
        ]
        with self.assertRaises(PokerException):
            ThreeOfAKind(cards)

    def test_invalid_two_pair(self):
        # Invalid because it doesn't have two pairs
        cards = [
            Card('10', 'Clubs'), Card('10', 'Diamonds'), Card('J', 'Hearts'),
            Card('K', 'Spades'), Card('A', 'Hearts')
        ]
        with self.assertRaises(PokerException):
            TwoPair(cards)

    def test_invalid_one_pair(self):
        # Invalid because it doesn't have exactly one pair
        cards = [
            Card('3', 'Clubs'), Card('4', 'Diamonds'), Card('7', 'Hearts'),
            Card('9', 'Spades'), Card('K', 'Hearts')
        ]
        with self.assertRaises(PokerException):
            OnePair(cards)

    def test_invalid_high_card(self):
        # Invalid because HighCard should accept any 5 cards, so no exception here
        cards = [
            Card('2', 'Clubs'), Card('5', 'Diamonds'), Card('7', 'Hearts'),
            Card('9', 'Spades'), Card('K', 'Hearts')
        ]
        hand = HighCard(cards)
        self.assertIsInstance(hand, HighCard)  # HighCard should always be valid

    def test_gt_operator_all_classes(self):
        # Create instances of all hand types
        royal_flush = RoyalFlush([
            Card('10', 'Hearts'), Card('J', 'Hearts'), Card('Q', 'Hearts'),
            Card('K', 'Hearts'), Card('A', 'Hearts')
        ])
        straight_flush = StraightFlush([
            Card('9', 'Spades'), Card('10', 'Spades'), Card('J', 'Spades'),
            Card('Q', 'Spades'), Card('K', 'Spades')
        ])
        four_of_a_kind = FourOfAKind([
            Card('A', 'Clubs'), Card('A', 'Diamonds'), Card('A', 'Hearts'),
            Card('A', 'Spades'), Card('K', 'Hearts')
        ])
        full_house = FullHouse([
            Card('Q', 'Clubs'), Card('Q', 'Diamonds'), Card('Q', 'Hearts'),
            Card('K', 'Spades'), Card('K', 'Hearts')
        ])
        flush = Flush([
            Card('2', 'Diamonds'), Card('5', 'Diamonds'), Card('8', 'Diamonds'),
            Card('J', 'Diamonds'), Card('K', 'Diamonds')
        ])
        straight = Straight([
            Card('4', 'Clubs'), Card('5', 'Diamonds'), Card('6', 'Hearts'),
            Card('7', 'Spades'), Card('8', 'Hearts')
        ])
        three_of_a_kind = ThreeOfAKind([
            Card('9', 'Clubs'), Card('9', 'Diamonds'), Card('9', 'Hearts'),
            Card('J', 'Spades'), Card('K', 'Hearts')
        ])
        two_pair = TwoPair([
            Card('10', 'Clubs'), Card('10', 'Diamonds'), Card('J', 'Hearts'),
            Card('J', 'Spades'), Card('K', 'Hearts')
        ])
        one_pair = OnePair([
            Card('3', 'Clubs'), Card('3', 'Diamonds'), Card('7', 'Hearts'),
            Card('9', 'Spades'), Card('K', 'Hearts')
        ])
        high_card = HighCard([
            Card('2', 'Clubs'), Card('5', 'Diamonds'), Card('7', 'Hearts'),
            Card('9', 'Spades'), Card('K', 'Hearts')
        ])

        # Test comparisons
        self.assertTrue(royal_flush > straight_flush)
        self.assertTrue(straight_flush > four_of_a_kind)
        self.assertTrue(four_of_a_kind > full_house)
        self.assertTrue(full_house > flush)
        self.assertTrue(flush > straight)
        self.assertTrue(straight > three_of_a_kind)
        self.assertTrue(three_of_a_kind > two_pair)
        self.assertTrue(two_pair > one_pair)
        self.assertTrue(one_pair > high_card)

        # Test reverse comparisons
        self.assertFalse(straight_flush > royal_flush)
        self.assertFalse(four_of_a_kind > straight_flush)
        self.assertFalse(full_house > four_of_a_kind)
        self.assertFalse(flush > full_house)
        self.assertFalse(straight > flush)
        self.assertFalse(three_of_a_kind > straight)
        self.assertFalse(two_pair > three_of_a_kind)
        self.assertFalse(one_pair > two_pair)
        self.assertFalse(high_card > one_pair)

        # Test equality (if applicable)
        self.assertFalse(royal_flush == straight_flush)
        self.assertFalse(four_of_a_kind == full_house)

    def test_same_hand_type_comparisons(self):
        # Straight comparison (higher rank wins)
        straight1 = Straight([
            Card('4', 'Clubs'), Card('5', 'Diamonds'), Card('6', 'Hearts'),
            Card('7', 'Spades'), Card('8', 'Hearts')
        ])
        straight2 = Straight([
            Card('5', 'Clubs'), Card('6', 'Diamonds'), Card('7', 'Hearts'),
            Card('8', 'Spades'), Card('9', 'Hearts')
        ])
        self.assertTrue(straight2 > straight1)
        self.assertFalse(straight1 > straight2)
    
        # Flush comparison (highest card in flush wins)
        flush1 = Flush([
            Card('2', 'Diamonds'), Card('5', 'Diamonds'), Card('8', 'Diamonds'),
            Card('J', 'Diamonds'), Card('K', 'Diamonds')
        ])
        flush2 = Flush([
            Card('3', 'Hearts'), Card('6', 'Hearts'), Card('9', 'Hearts'),
            Card('Q', 'Hearts'), Card('A', 'Hearts')
        ])
        self.assertTrue(flush2 > flush1)
        self.assertFalse(flush1 > flush2)
    
        # Full House comparison (three-of-a-kind rank decides)
        full_house1 = FullHouse([
            Card('Q', 'Clubs'), Card('Q', 'Diamonds'), Card('Q', 'Hearts'),
            Card('K', 'Spades'), Card('K', 'Hearts')
        ])
        full_house2 = FullHouse([
            Card('K', 'Clubs'), Card('K', 'Diamonds'), Card('K', 'Hearts'),
            Card('Q', 'Spades'), Card('Q', 'Hearts')
        ])
        self.assertTrue(full_house2 > full_house1)
        self.assertFalse(full_house1 > full_house2)
    
        # Three of a Kind comparison (kickers decide if three-of-a-kind ranks tie)
        three_of_a_kind1 = ThreeOfAKind([
            Card('9', 'Clubs'), Card('9', 'Diamonds'), Card('9', 'Hearts'),
            Card('J', 'Spades'), Card('K', 'Hearts')
        ])
        three_of_a_kind2 = ThreeOfAKind([
            Card('9', 'Clubs'), Card('9', 'Diamonds'), Card('9', 'Hearts'),
            Card('Q', 'Spades'), Card('K', 'Hearts')
        ])
        self.assertTrue(three_of_a_kind2 > three_of_a_kind1)
        self.assertFalse(three_of_a_kind1 > three_of_a_kind2)
    
        # Two Pair comparison (higher pair wins, then second pair, then kicker)
        two_pair1 = TwoPair([
            Card('10', 'Clubs'), Card('10', 'Diamonds'), Card('J', 'Hearts'),
            Card('J', 'Spades'), Card('K', 'Hearts')
        ])
        two_pair2 = TwoPair([
            Card('10', 'Clubs'), Card('10', 'Diamonds'), Card('Q', 'Hearts'),
            Card('Q', 'Spades'), Card('K', 'Hearts')
        ])
        self.assertTrue(two_pair2 > two_pair1)
        self.assertFalse(two_pair1 > two_pair2)
    
        # One Pair comparison (kickers decide if pair ranks tie)
        one_pair1 = OnePair([
            Card('3', 'Clubs'), Card('3', 'Diamonds'), Card('7', 'Hearts'),
            Card('9', 'Spades'), Card('K', 'Hearts')
        ])
        one_pair2 = OnePair([
            Card('3', 'Clubs'), Card('3', 'Diamonds'), Card('8', 'Hearts'),
            Card('9', 'Spades'), Card('K', 'Hearts')
        ])
        self.assertTrue(one_pair2 > one_pair1)
        self.assertFalse(one_pair1 > one_pair2)
    
        # High Card comparison (kickers decide in order)
        high_card1 = HighCard([
            Card('2', 'Clubs'), Card('5', 'Diamonds'), Card('7', 'Hearts'),
            Card('9', 'Spades'), Card('K', 'Hearts')
        ])
        high_card2 = HighCard([
            Card('2', 'Clubs'), Card('5', 'Diamonds'), Card('7', 'Hearts'),
            Card('9', 'Spades'), Card('A', 'Hearts')
        ])
        self.assertTrue(high_card2 > high_card1)
        self.assertFalse(high_card1 > high_card2)
    
        # High Card comparison with multiple kickers
        high_card3 = HighCard([
            Card('2', 'Clubs'), Card('5', 'Diamonds'), Card('7', 'Hearts'),
            Card('9', 'Spades'), Card('A', 'Hearts')
        ])
        high_card4 = HighCard([
            Card('2', 'Clubs'), Card('5', 'Diamonds'), Card('7', 'Hearts'),
            Card('10', 'Spades'), Card('A', 'Hearts')
        ])
        self.assertTrue(high_card4 > high_card3)
        self.assertFalse(high_card3 > high_card4)
    
        # High Card comparison with third kicker
        high_card5 = HighCard([
            Card('2', 'Clubs'), Card('5', 'Diamonds'), Card('8', 'Hearts'),
            Card('10', 'Spades'), Card('A', 'Hearts')
        ])

        self.assertTrue(high_card5 > high_card4)
        self.assertFalse(high_card4 > high_card5)

        # High Card comparison with fourth kicker
        high_card6 = HighCard([
            Card('3', 'Clubs'), Card('5', 'Diamonds'), Card('8', 'Hearts'),
            Card('10', 'Spades'), Card('A', 'Hearts')
        ])

        self.assertTrue(high_card6 > high_card5)
        self.assertFalse(high_card5 > high_card6)


if __name__ == "__main__":
    unittest.main()