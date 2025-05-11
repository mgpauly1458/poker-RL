import unittest
from poker import PokerGame, Player
import agents as ag
import poker_util as pu

# Mock Deck for predictable results
class MockDeck(pu.Deck):
    def __init__(self):
        self.cards = [
            # PairBetterAgent's hand
            pu.Card(pu.CARD_RANK_NAME_5, pu.SUIT_HEARTS), pu.Card(pu.CARD_RANK_NAME_10, pu.SUIT_SPADES),
            # CallCheckAgent's hand
            pu.Card(pu.CARD_RANK_NAME_9, pu.SUIT_DIAMONDS), pu.Card(pu.CARD_RANK_NAME_8, pu.SUIT_CLUBS),
            # Community cards
            pu.Card(pu.CARD_RANK_NAME_2, pu.SUIT_HEARTS),
            pu.Card(pu.CARD_RANK_NAME_3, pu.SUIT_DIAMONDS),
            pu.Card(pu.CARD_RANK_NAME_4, pu.SUIT_CLUBS),
            pu.Card(pu.CARD_RANK_NAME_5, pu.SUIT_SPADES),
            pu.Card(pu.CARD_RANK_NAME_7, pu.SUIT_HEARTS)
        ]

    def draw(self):
        return self.cards.pop(0)

class TestPairBetterAgent(unittest.TestCase):
    def setUp(self):
        print("\nSetting up the game for PairBetterAgent vs CallCheckAgent.")
        # Create players with agents
        self.player1 = Player(name="PairBetterAgent", stack=1000, agent=ag.PairBetterAgent())
        self.player2 = Player(name="CallCheckAgent", stack=1000, agent=ag.CallCheckAgent())

        # Initialize the game with a mock deck
        self.game = PokerGame(players=[self.player1, self.player2])
        self.game.deck = MockDeck()

    def test_pair_better_wins(self):
        self.game.run_hand()

        # Assert the PairBetterAgent wins
        self.assertEqual(self.player1.stack, 1202)  # PairBetterAgent wins the pot
        self.assertEqual(self.player2.stack, 798)    # CallCheckAgent loses all chips

class TestFlushBetterAgent(unittest.TestCase):
    def setUp(self):
        print("\nSetting up the game for FlushBetterAgent vs CallCheckAgent.")
        # Create players with agents
        self.player1 = Player(name="FlushBetterAgent", stack=1000, agent=ag.FlushBetterAgent())
        self.player2 = Player(name="CallCheckAgent", stack=1000, agent=ag.CallCheckAgent())

        # Initialize the game with a mock deck
        self.game = PokerGame(players=[self.player1, self.player2])
        self.game.deck = MockDeck()

        self.game.deck.cards = [
            # FlushBetterAgent's hand
            pu.Card(pu.CARD_RANK_NAME_2, pu.SUIT_HEARTS), pu.Card(pu.CARD_RANK_NAME_3, pu.SUIT_HEARTS),
            # CallCheckAgent's hand
            pu.Card(pu.CARD_RANK_NAME_9, pu.SUIT_DIAMONDS), pu.Card(pu.CARD_RANK_NAME_8, pu.SUIT_CLUBS),
            # Community cards
            pu.Card(pu.CARD_RANK_NAME_4, pu.SUIT_HEARTS),
            pu.Card(pu.CARD_RANK_NAME_5, pu.SUIT_HEARTS),
            pu.Card(pu.CARD_RANK_NAME_K, pu.SUIT_CLUBS),
            pu.Card(pu.CARD_RANK_NAME_7, pu.SUIT_HEARTS),
            pu.Card(pu.CARD_RANK_NAME_10, pu.SUIT_CLUBS)
        ]

    def test_flush_better_wins(self):
        self.game.run_hand()

        # Assert the FlushBetterAgent wins
        self.assertEqual(self.player1.stack, 1202)  # FlushBetterAgent wins the pot
        self.assertEqual(self.player2.stack, 798)    # CallCheckAgent loses all chips


class TestPairBetterBetsOnFlush(unittest.TestCase):
    def setUp(self):
        print("\nSetting up the game for PairBetterAgent vs CallCheckAgent with a flush.")
        # Create players with agents
        self.player1 = Player(name="PairBetterAgent", stack=1000, agent=ag.PairBetterAgent())
        self.player2 = Player(name="CallCheckAgent", stack=1000, agent=ag.CallCheckAgent())

        # Initialize the game with a mock deck
        self.game = PokerGame(players=[self.player1, self.player2])
        self.game.deck = MockDeck()

        self.game.deck.cards = [
            # FlushBetterAgent's hand
            pu.Card(pu.CARD_RANK_NAME_2, pu.SUIT_HEARTS), pu.Card(pu.CARD_RANK_NAME_3, pu.SUIT_HEARTS),
            # CallCheckAgent's hand
            pu.Card(pu.CARD_RANK_NAME_9, pu.SUIT_DIAMONDS), pu.Card(pu.CARD_RANK_NAME_8, pu.SUIT_CLUBS),
            # Community cards
            pu.Card(pu.CARD_RANK_NAME_4, pu.SUIT_HEARTS),
            pu.Card(pu.CARD_RANK_NAME_5, pu.SUIT_HEARTS),
            pu.Card(pu.CARD_RANK_NAME_K, pu.SUIT_CLUBS),
            pu.Card(pu.CARD_RANK_NAME_7, pu.SUIT_HEARTS),
            pu.Card(pu.CARD_RANK_NAME_10, pu.SUIT_CLUBS)
        ]

    def test_pair_better_bets_on_flush(self):
        self.game.run_hand()

        # Assert the PairBetterAgent wins
        self.assertEqual(self.player1.stack, 1202)  # PairBetterAgent wins the pot
        self.assertEqual(self.player2.stack, 798)    # CallCheckAgent loses all chips

class TestFlushBetterDoesNotBetOnPair(unittest.TestCase):
    def setUp(self):
        print("\nSetting up the game for FlushBetterAgent vs CallCheckAgent with a pair.")
        # Create players with agents
        self.player1 = Player(name="FlushBetterAgent", stack=1000, agent=ag.FlushBetterAgent())
        self.player2 = Player(name="CallCheckAgent", stack=1000, agent=ag.CallCheckAgent())

        # Initialize the game with a mock deck
        self.game = PokerGame(players=[self.player1, self.player2])
        self.game.deck = MockDeck()

        self.game.deck.cards = [
            # FlushBetterAgent's hand
            pu.Card(pu.CARD_RANK_NAME_5, pu.SUIT_HEARTS), pu.Card(pu.CARD_RANK_NAME_10, pu.SUIT_SPADES),
            # CallCheckAgent's hand
            pu.Card(pu.CARD_RANK_NAME_9, pu.SUIT_DIAMONDS), pu.Card(pu.CARD_RANK_NAME_8, pu.SUIT_CLUBS),
            # Community cards
            pu.Card(pu.CARD_RANK_NAME_4, pu.SUIT_HEARTS),
            pu.Card(pu.CARD_RANK_NAME_5, pu.SUIT_HEARTS),
            pu.Card(pu.CARD_RANK_NAME_K, pu.SUIT_CLUBS),
            pu.Card(pu.CARD_RANK_NAME_7, pu.SUIT_HEARTS),
            pu.Card(pu.CARD_RANK_NAME_8, pu.SUIT_DIAMONDS)
        ]

    def test_flush_better_does_not_bet_on_pair(self):
        self.game.run_hand()

        # Assert the FlushBetterAgent wins
        self.assertEqual(self.player1.stack, 998)  # FlushBetterAgent wins the pot
        self.assertEqual(self.player2.stack, 1002)    # CallCheckAgent loses all chips


if __name__ == "__main__":
    unittest.main()