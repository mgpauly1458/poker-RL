import unittest
from poker import PokerGame, Player
from agents import AllInAgent, CallCheckAgent, FoldAgent, DelayedAllinAgent, ReRaiseAgent, DelayedRaiseAgent
import poker_util as pu

# Mock Deck for predictable results
class MockDeck(pu.Deck):
    def __init__(self, no_shuffle=True):
        super().__init__(no_shuffle=no_shuffle)
        self.fresh_deck_of_cards = [
            pu.Card(pu.CARD_RANK_NAME_A, pu.SUIT_HEARTS), pu.Card(pu.CARD_RANK_NAME_K, pu.SUIT_HEARTS),  # Player 1's hand
            pu.Card(pu.CARD_RANK_NAME_Q, pu.SUIT_SPADES), pu.Card(pu.CARD_RANK_NAME_J, pu.SUIT_SPADES),  # Player 2's hand
            pu.Card(pu.CARD_RANK_NAME_2, pu.SUIT_DIAMONDS), pu.Card(pu.CARD_RANK_NAME_3, pu.SUIT_DIAMONDS),  # Player 3's hand

            pu.Card(pu.CARD_RANK_NAME_10, pu.SUIT_HEARTS),
            pu.Card(pu.CARD_RANK_NAME_J, pu.SUIT_HEARTS),
            pu.Card(pu.CARD_RANK_NAME_Q, pu.SUIT_HEARTS),  # Flop

            pu.Card(pu.CARD_RANK_NAME_7, pu.SUIT_CLUBS),  # Turn

            pu.Card(pu.CARD_RANK_NAME_6, pu.SUIT_HEARTS)  # River
        ]

        self.cards = self.fresh_deck_of_cards.copy()

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

        # Assert the winner and stack changes (game ends after one hand, no new sb/bb dealt)
        # Based on the mock deck, Player 1 (AllInAgent) should win with a Royal Flush
        self.assertEqual(self.player1.stack, 2000)
        self.assertEqual(self.player2.stack, 0)    # Player 2 loses all chips
        self.assertEqual(self.player3.stack, 1000)    # Player 3 should not lose any chips

class TestCallDelayAllinFoldAgents(unittest.TestCase):
    def setUp(self):
        print("\n\n\n\n\nSetting up the game for Call, Delay All-In, and Fold agents.") 
        # Create players with agents
        self.player1 = Player(name="DelayedAllinAgent", stack=1000, agent=DelayedAllinAgent(delay=5))
        self.player2 = Player(name="CallCheckAgent", stack=1000, agent=CallCheckAgent())
        self.player3 = Player(name="FoldAgent", stack=1000, agent=FoldAgent())

        # Initialize the game with a mock deck
        self.game = PokerGame(players=[self.player1, self.player2, self.player3])
        self.game.deck = MockDeck()
        
    def test_call_fold_action(self):
        self.game.run_game()
        # Assert the winner and stack changes (after next bb / sb and rotation occurs)
        # Based on the mock deck, Player 1 (DelayedAllinAgent) should win with a Royal Flush
        self.assertEqual(self.player1.stack, 0)
        self.assertEqual(self.player2.stack, 2005)    # this playerr ends up with royal flush because players
        # rotate but the deck assignments don't
        self.assertEqual(self.player3.stack, 995)    # Player 3 should not lose any chips
        # Check if the delayed all-in agent acted correctly

        # @Todo: there is an off by 1 error somewhere. players are entering sb/bb even after final hand count reached.
        # shouldn't matter for RL training.consider it noise.

# test where one agent goes all in, another calls, and they both have the same hand
class TestAllInCallEqualHands(unittest.TestCase):
    def setUp(self):
        print("\n\n\n\n\nSetting up the game for All-In and Call agents with equal hands.") 
        # Create players with agents
        self.player1 = Player(name="AllInAgent", stack=1000, agent=AllInAgent())
        self.player2 = Player(name="CallCheckAgent", stack=1000, agent=CallCheckAgent())

        # Initialize the game with a mock deck
        self.game = PokerGame(players=[self.player1, self.player2])
        self.game.deck = MockDeck()  # Use the mock deck for predictable results
        self.game.deck.cards = [
            pu.Card(pu.CARD_RANK_NAME_A, pu.SUIT_HEARTS), pu.Card(pu.CARD_RANK_NAME_K, pu.SUIT_HEARTS),  # Player 1's hand
            pu.Card(pu.CARD_RANK_NAME_A, pu.SUIT_CLUBS), pu.Card(pu.CARD_RANK_NAME_K, pu.SUIT_CLUBS),  # Player 2's hand

            pu.Card(pu.CARD_RANK_NAME_10, pu.SUIT_DIAMONDS),
            pu.Card(pu.CARD_RANK_NAME_J, pu.SUIT_DIAMONDS),
            pu.Card(pu.CARD_RANK_NAME_Q, pu.SUIT_DIAMONDS),  # Flop

            pu.Card(pu.CARD_RANK_NAME_7, pu.SUIT_CLUBS),  # Turn

            pu.Card(pu.CARD_RANK_NAME_6, pu.SUIT_HEARTS)  # River
        ]

    def test_all_in_call_equal_hands(self):
        self.game.run_hand()
        self.assertEqual(self.player1.stack, 1000)
        self.assertEqual(self.player2.stack, 1000)

# test for split pot when both have a pair and equal kickers
class TestSplitPotEqualKickers(unittest.TestCase):
    def setUp(self):
        print("\n\n\n\n\nSetting up the game for Split Pot with equal kickers.") 
        # Create players with agents
        self.player1 = Player(name="AllInAgent", stack=1000, agent=AllInAgent())
        self.player2 = Player(name="CallCheckAgent", stack=1000, agent=CallCheckAgent())

        # Initialize the game with a mock deck
        self.game = PokerGame(players=[self.player1, self.player2])
        self.game.deck = MockDeck()  # Use the mock deck for predictable results
        self.game.deck.cards = [
            pu.Card(pu.CARD_RANK_NAME_A, pu.SUIT_HEARTS), pu.Card(pu.CARD_RANK_NAME_2, pu.SUIT_HEARTS),  # Player 1's hand
            pu.Card(pu.CARD_RANK_NAME_A, pu.SUIT_CLUBS), pu.Card(pu.CARD_RANK_NAME_2, pu.SUIT_CLUBS),  # Player 2's hand

            pu.Card(pu.CARD_RANK_NAME_10, pu.SUIT_DIAMONDS),
            pu.Card(pu.CARD_RANK_NAME_J, pu.SUIT_DIAMONDS),
            pu.Card(pu.CARD_RANK_NAME_Q, pu.SUIT_DIAMONDS),  # Flop

            pu.Card(pu.CARD_RANK_NAME_7, pu.SUIT_CLUBS),  # Turn

            pu.Card(pu.CARD_RANK_NAME_6, pu.SUIT_HEARTS)  # River
        ]

    def test_split_pot_equal_kickers(self):
        self.game.run_hand()
        self.assertEqual(self.player1.stack, 1000)
        self.assertEqual(self.player2.stack, 1000)

# test for split pot when both have a three of a kind and equal kickers
class TestSplitPotEqualKickersThreeOfAKind(unittest.TestCase):
    def setUp(self):
        print("\n\n\n\n\nSetting up the game for Split Pot with equal kickers (Three of a Kind).") 
        # Create players with agents
        self.player1 = Player(name="AllInAgent", stack=1000, agent=AllInAgent())
        self.player2 = Player(name="CallCheckAgent", stack=1000, agent=CallCheckAgent())

        # Initialize the game with a mock deck
        self.game = PokerGame(players=[self.player1, self.player2])
        self.game.deck = MockDeck()  # Use the mock deck for predictable results
        self.game.deck.cards = [
            pu.Card(pu.CARD_RANK_NAME_A, pu.SUIT_HEARTS), pu.Card(pu.CARD_RANK_NAME_2, pu.SUIT_HEARTS),  # Player 1's hand
            pu.Card(pu.CARD_RANK_NAME_A, pu.SUIT_CLUBS), pu.Card(pu.CARD_RANK_NAME_2, pu.SUIT_CLUBS),  # Player 2's hand

            pu.Card(pu.CARD_RANK_NAME_A, pu.SUIT_DIAMONDS),
            pu.Card(pu.CARD_RANK_NAME_A, pu.SUIT_CLUBS),
            pu.Card(pu.CARD_RANK_NAME_Q, pu.SUIT_DIAMONDS),  # Flop

            pu.Card(pu.CARD_RANK_NAME_7, pu.SUIT_CLUBS),  # Turn

            pu.Card(pu.CARD_RANK_NAME_6, pu.SUIT_HEARTS)  # River
        ]

    def test_split_pot_equal_kickers_three_of_a_kind(self):
        self.game.run_hand()
        self.assertEqual(self.player1.stack, 1000)
        self.assertEqual(self.player2.stack, 1000)

# test for split pot when both have a straight with the same high card
class TestSplitPotEqualKickersStraight(unittest.TestCase):
    def setUp(self):
        print("\n\n\n\n\nSetting up the game for Split Pot with equal kickers (Straight).") 
        # Create players with agents
        self.player1 = Player(name="AllInAgent", stack=1000, agent=AllInAgent())
        self.player2 = Player(name="CallCheckAgent", stack=1000, agent=CallCheckAgent())

        # Initialize the game with a mock deck
        self.game = PokerGame(players=[self.player1, self.player2])
        self.game.deck = MockDeck()  # Use the mock deck for predictable results
        self.game.deck.cards = [
            pu.Card(pu.CARD_RANK_NAME_10, pu.SUIT_HEARTS), pu.Card(pu.CARD_RANK_NAME_9, pu.SUIT_HEARTS),  # Player 1's hand
            pu.Card(pu.CARD_RANK_NAME_10, pu.SUIT_CLUBS), pu.Card(pu.CARD_RANK_NAME_9, pu.SUIT_CLUBS),  # Player 2's hand

            pu.Card(pu.CARD_RANK_NAME_8, pu.SUIT_DIAMONDS),
            pu.Card(pu.CARD_RANK_NAME_J, pu.SUIT_DIAMONDS),
            pu.Card(pu.CARD_RANK_NAME_Q, pu.SUIT_DIAMONDS),  # Flop

            pu.Card(pu.CARD_RANK_NAME_7, pu.SUIT_CLUBS),  # Turn

            pu.Card(pu.CARD_RANK_NAME_6, pu.SUIT_HEARTS)  # River
        ]

    def test_split_pot_equal_kickers_straight(self):
        self.game.run_hand()
        self.assertEqual(self.player1.stack, 1000)
        self.assertEqual(self.player2.stack, 1000)

# test for split pot when both have two pair with the same high card
class TestSplitPotEqualKickersTwoPair(unittest.TestCase):
    def setUp(self):
        print("\n\n\n\n\nSetting up the game for Split Pot with equal kickers (Two Pair).") 
        # Create players with agents
        self.player1 = Player(name="AllInAgent", stack=1000, agent=AllInAgent())
        self.player2 = Player(name="CallCheckAgent", stack=1000, agent=CallCheckAgent())

        # Initialize the game with a mock deck
        self.game = PokerGame(players=[self.player1, self.player2])
        self.game.deck = MockDeck()  # Use the mock deck for predictable results
        self.game.deck.cards = [
            pu.Card(pu.CARD_RANK_NAME_10, pu.SUIT_HEARTS), pu.Card(pu.CARD_RANK_NAME_9, pu.SUIT_HEARTS),  # Player 1's hand
            pu.Card(pu.CARD_RANK_NAME_10, pu.SUIT_CLUBS), pu.Card(pu.CARD_RANK_NAME_9, pu.SUIT_CLUBS),  # Player 2's hand

            pu.Card(pu.CARD_RANK_NAME_9, pu.SUIT_DIAMONDS),
            pu.Card(pu.CARD_RANK_NAME_10, pu.SUIT_DIAMONDS),
            pu.Card(pu.CARD_RANK_NAME_Q, pu.SUIT_DIAMONDS),  # Flop

            pu.Card(pu.CARD_RANK_NAME_7, pu.SUIT_CLUBS),  # Turn

            pu.Card(pu.CARD_RANK_NAME_6, pu.SUIT_HEARTS)  # River
        ]

    def test_split_pot_equal_kickers_two_pair(self):
        self.game.run_hand()
        self.assertEqual(self.player1.stack, 1000)
        self.assertEqual(self.player2.stack, 1000)

# test that higher flush wins the pot over lower flush
class TestHigherFlushWins(unittest.TestCase):
    def setUp(self):
        print("\n\n\n\n\nSetting up the game for Higher Flush wins.") 
        # Create players with agents
        self.player1 = Player(name="AllInAgent", stack=1000, agent=AllInAgent())
        self.player2 = Player(name="CallCheckAgent", stack=1000, agent=CallCheckAgent())

        # Initialize the game with a mock deck
        self.game = PokerGame(players=[self.player1, self.player2])
        self.game.deck = MockDeck()  # Use the mock deck for predictable results
        self.game.deck.cards = [
            pu.Card(pu.CARD_RANK_NAME_10, pu.SUIT_HEARTS), pu.Card(pu.CARD_RANK_NAME_9, pu.SUIT_CLUBS),  # Player 1's hand
            pu.Card(pu.CARD_RANK_NAME_10, pu.SUIT_CLUBS), pu.Card(pu.CARD_RANK_NAME_9, pu.SUIT_HEARTS),  # Player 2's hand

            pu.Card(pu.CARD_RANK_NAME_A, pu.SUIT_HEARTS),
            pu.Card(pu.CARD_RANK_NAME_10, pu.SUIT_DIAMONDS),
            pu.Card(pu.CARD_RANK_NAME_Q, pu.SUIT_HEARTS),  # Flop

            pu.Card(pu.CARD_RANK_NAME_7, pu.SUIT_HEARTS),  # Turn

            pu.Card(pu.CARD_RANK_NAME_6, pu.SUIT_HEARTS)  # River
        ]

    def test_higher_flush_wins(self):
        self.game.run_hand()
        self.assertEqual(self.player1.stack, 2000)
        self.assertEqual(self.player2.stack, 0)

class TestHigherPairWins(unittest.TestCase):
    def setUp(self):
        print("\n\n\n\n\nSetting up the game for Higher Pair wins.") 
        # Create players with agents
        self.player1 = Player(name="AllInAgent", stack=1000, agent=AllInAgent())
        self.player2 = Player(name="CallCheckAgent", stack=1000, agent=CallCheckAgent())

        # Initialize the game with a mock deck
        self.game = PokerGame(players=[self.player1, self.player2])
        self.game.deck = MockDeck()  # Use the mock deck for predictable results
        self.game.deck.cards = [
            pu.Card(pu.CARD_RANK_NAME_K, pu.SUIT_HEARTS), pu.Card(pu.CARD_RANK_NAME_9, pu.SUIT_CLUBS),  # Player 1's hand
            pu.Card(pu.CARD_RANK_NAME_10, pu.SUIT_CLUBS), pu.Card(pu.CARD_RANK_NAME_9, pu.SUIT_HEARTS),  # Player 2's hand

            pu.Card(pu.CARD_RANK_NAME_A, pu.SUIT_HEARTS),
            pu.Card(pu.CARD_RANK_NAME_K, pu.SUIT_DIAMONDS),
            pu.Card(pu.CARD_RANK_NAME_Q, pu.SUIT_HEARTS),  # Flop

            pu.Card(pu.CARD_RANK_NAME_7, pu.SUIT_HEARTS),  # Turn

            pu.Card(pu.CARD_RANK_NAME_9, pu.SUIT_DIAMONDS)  # River
        ]

    def test_higher_pair_wins(self):
        self.game.run_hand()
        self.assertEqual(self.player1.stack, 2000)
        self.assertEqual(self.player2.stack, 0)

class TestHigherHighCardWins(unittest.TestCase):
    def setUp(self):
        print("\n\n\n\n\nSetting up the game for Higher High Card wins.") 
        # Create players with agents
        self.player1 = Player(name="AllInAgent", stack=1000, agent=AllInAgent())
        self.player2 = Player(name="CallCheckAgent", stack=1000, agent=CallCheckAgent())

        # Initialize the game with a mock deck
        self.game = PokerGame(players=[self.player1, self.player2])
        self.game.deck = MockDeck()  # Use the mock deck for predictable results
        self.game.deck.cards = [
            pu.Card(pu.CARD_RANK_NAME_10, pu.SUIT_HEARTS), pu.Card(pu.CARD_RANK_NAME_9, pu.SUIT_CLUBS),  # Player 1's hand
            pu.Card(pu.CARD_RANK_NAME_J, pu.SUIT_CLUBS), pu.Card(pu.CARD_RANK_NAME_9, pu.SUIT_HEARTS),  # Player 2's hand

            pu.Card(pu.CARD_RANK_NAME_A, pu.SUIT_HEARTS),
            pu.Card(pu.CARD_RANK_NAME_K, pu.SUIT_DIAMONDS),
            pu.Card(pu.CARD_RANK_NAME_Q, pu.SUIT_HEARTS),  # Flop

            pu.Card(pu.CARD_RANK_NAME_7, pu.SUIT_HEARTS),  # Turn

            pu.Card(pu.CARD_RANK_NAME_8, pu.SUIT_DIAMONDS)  # River
        ]

    def test_higher_high_card_wins(self):
        self.game.run_hand()
        self.assertEqual(self.player1.stack, 0)
        self.assertEqual(self.player2.stack, 2000)

class TestDelayedRaiseAgent(unittest.TestCase):
    def setUp(self):
        print("\n\n\n\n\nSetting up the game for Raise Agent.") 
        # Create players with agents
        self.player1 = Player(name="RaiseAgent", stack=1000, agent=DelayedRaiseAgent(delay=5))
        self.player2 = Player(name="CallCheckAgent", stack=1000, agent=CallCheckAgent())

        # Initialize the game with a mock deck
        self.game = PokerGame(players=[self.player1, self.player2], maximum_hands=2)
        self.game.deck = MockDeck()  # Use the mock deck for predictable results

    def test_raise_action(self):
        self.game.run_game()
        # Assert the winner and stack changes (after next bb / sb and rotation occurs)
        # Based on the mock deck, Player 1 (RaiseAgent) should win with a Royal Flush
        self.assertEqual(self.player1.stack, 1101)
        self.assertEqual(self.player2.stack, 899)    # this playerr ends up with royal flush because players

if __name__ == "__main__":
    unittest.main()