import unittest
from poker import PokerGame, Player
from agents import AllInAgent, CallCheckAgent, FoldAgent
import poker_util as pu

# Mock Deck for predictable results
class MockDeck(pu.Deck):
    def __init__(self):
        self.cards = [
            pu.Card(pu.CARD_RANK_NAME_A, pu.SUIT_HEARTS), pu.Card(pu.CARD_RANK_NAME_K, pu.SUIT_HEARTS),  # Player 1's hand
            pu.Card(pu.CARD_RANK_NAME_Q, pu.SUIT_SPADES), pu.Card(pu.CARD_RANK_NAME_J, pu.SUIT_SPADES),  # Player 2's hand
            pu.Card(pu.CARD_RANK_NAME_2, pu.SUIT_DIAMONDS), pu.Card(pu.CARD_RANK_NAME_3, pu.SUIT_DIAMONDS),  # Player 3's hand

            pu.Card(pu.CARD_RANK_NAME_10, pu.SUIT_HEARTS),
            pu.Card(pu.CARD_RANK_NAME_J, pu.SUIT_HEARTS),
            pu.Card(pu.CARD_RANK_NAME_Q, pu.SUIT_HEARTS),  # Flop

            pu.Card(pu.CARD_RANK_NAME_7, pu.SUIT_CLUBS),  # Turn

            pu.Card(pu.CARD_RANK_NAME_6, pu.SUIT_HEARTS)  # River
        ]

    def draw(self):
        return self.cards.pop(0)

class TestEndToEndGame(unittest.TestCase):
    def setUp(self):
        # Create players with agents
        self.player1 = Player(name="AllInAgent", stack=1000, agent=AllInAgent())
        self.player2 = Player(name="CallCheckAgent", stack=1000, agent=CallCheckAgent())
        self.player3 = Player(name="CallCheckAgent2", stack=1000, agent=CallCheckAgent())

        # Initialize the game with a mock deck
        self.game = PokerGame(players=[self.player1, self.player2, self.player3])
        self.game.deck = MockDeck()  # Use the mock deck for predictable results

    def test_full_game(self):
        # Deal hands and play the game
        self.game.run_hand()  # This will run the game until completion

        # Assert the winner and stack changes
        # Based on the mock deck, Player 1 (AllInAgent) should win with a Royal Flush
        self.assertEqual(self.player1.stack, 3000)  # Player 1 wins the pot
        self.assertEqual(self.player2.stack, 0)    # Player 2 loses all chips
        self.assertEqual(self.player3.stack, 0)    # Player 3 loses all chips

class TestFoldAllInAgent(unittest.TestCase):

    def setUp(self):
        # Create a player with the FoldAgent
        self.player1 = Player(name="FoldAgent", stack=1000, agent=FoldAgent())
        self.player2 = Player(name="AllInAgent", stack=1000, agent=AllInAgent())
        self.game = PokerGame(players=[self.player1, self.player2])
        self.game.deck = MockDeck()  # Use the mock deck for predictable results

    def test_fold_action(self):
        self.game.run_hand()

class TestCallAllInFoldAgents(unittest.TestCase):
    def setUp(self):
        print("Setting up the game for Call, All-In, and Fold agents.") 
        # Create players with agents
        self.player1 = Player(name="AllInAgent", stack=1000, agent=AllInAgent())
        self.player2 = Player(name="CallCheckAgent", stack=1000, agent=CallCheckAgent())
        self.player3 = Player(name="FoldAgent", stack=1000, agent=FoldAgent())

        # Initialize the game with a mock deck
        self.game = PokerGame(players=[self.player1, self.player2, self.player3])
        self.game.deck = MockDeck()  # Use the mock deck for predictable results

    def test_call_fold_action(self):
        self.game.run_hand()

        # Assert the winner and stack changes (after next bb / sb and rotation occurs)
        # Based on the mock deck, Player 1 (AllInAgent) should win with a Royal Flush
        self.assertEqual(self.player1.stack, 1998)
        self.assertEqual(self.player2.stack, 0)    # Player 2 loses all chips
        self.assertEqual(self.player3.stack, 999)    # Player 3 should not lose any chips

if __name__ == "__main__":
    unittest.main()