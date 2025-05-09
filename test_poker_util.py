import unittest
from poker_util import (
    Card, PokerRules, RoyalFlush, StraightFlush, FourOfAKind, FullHouse, Flush,
    Straight, ThreeOfAKind, TwoPair, OnePair, HighCard
)

class TestPokerRules(unittest.TestCase):
    def setUp(self):
        self.poker_rules = PokerRules()

    def test_get_best_hand(self):
        # Create a list of hands
        hands = [
            [Card('10', 'Hearts'), Card('J', 'Hearts'), Card('Q', 'Hearts'), Card('K', 'Hearts'), Card('A', 'Hearts')],  # Royal Flush
            [Card('9', 'Spades'), Card('10', 'Spades'), Card('J', 'Spades'), Card('Q', 'Spades'), Card('K', 'Spades')],  # Straight Flush
            [Card('A', 'Clubs'), Card('A', 'Diamonds'), Card('A', 'Hearts'), Card('A', 'Spades'), Card('K', 'Hearts')],  # Four of a Kind
            [Card('Q', 'Clubs'), Card('Q', 'Diamonds'), Card('Q', 'Hearts'), Card('K', 'Spades'), Card('K', 'Hearts')],  # Full House
            [Card('2', 'Diamonds'), Card('5', 'Diamonds'), Card('8', 'Diamonds'), Card('J', 'Diamonds'), Card('K', 'Diamonds')],  # Flush
        ]

        # Get the best hand
        best_hand = self.poker_rules.get_best_hand(hands)

        # Assert the best hand is the Royal Flush
        expected_best_hand = RoyalFlush(hands[0])
        self.assertEqual(type(best_hand), type(expected_best_hand))
        self.assertEqual(best_hand.cards, expected_best_hand.cards)

    def test_get_best_hand_with_tie(self):
        # Create a list of hands with a tie
        hands = [
            [Card('10', 'Hearts'), Card('J', 'Hearts'), Card('Q', 'Hearts'), Card('K', 'Hearts'), Card('A', 'Hearts')],  # Royal Flush
            [Card('10', 'Spades'), Card('J', 'Spades'), Card('Q', 'Spades'), Card('K', 'Spades'), Card('A', 'Spades')],  # Royal Flush (tie)
        ]

        # Get the best hand
        best_hand = self.poker_rules.get_best_hand(hands)

        # Assert the best hand is one of the Royal Flushes
        expected_best_hand = RoyalFlush(hands[0])
        self.assertEqual(type(best_hand), type(expected_best_hand))
        self.assertIn(best_hand.cards, hands)

    def test_get_best_hand_with_low_hands(self):
        # Create a list of low-ranking hands
        hands = [
            [Card('2', 'Clubs'), Card('3', 'Diamonds'), Card('5', 'Hearts'), Card('7', 'Spades'), Card('9', 'Hearts')],  # High Card
            [Card('3', 'Clubs'), Card('3', 'Diamonds'), Card('5', 'Hearts'), Card('7', 'Spades'), Card('9', 'Hearts')],  # One Pair
            [Card('4', 'Clubs'), Card('4', 'Diamonds'), Card('6', 'Hearts'), Card('6', 'Spades'), Card('9', 'Hearts')],  # Two Pair
        ]

        # Get the best hand
        best_hand = self.poker_rules.get_best_hand(hands)

        # Assert the best hand is the Two Pair
        expected_best_hand = TwoPair(hands[2])
        self.assertEqual(type(best_hand), type(expected_best_hand))
        self.assertEqual(best_hand.cards, expected_best_hand.cards)

if __name__ == "__main__":
    unittest.main()