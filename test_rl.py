import unittest
import numpy as np
import agents as ag
from poker_game import Player
import poker_util as pu
import poker_game as pk

class TestRLAgentVectorization(unittest.TestCase):
    def setUp(self):
        # Create an RLAgent
        self.rl_agent = ag.RLAgent()
        self.current_player = Player(name="RLAgent", stack=1000, agent=self.rl_agent)
        self.current_player.hand =[
                pu.Card(pu.CARD_RANK_NAME_A, pu.SUIT_HEARTS),
                pu.Card(pu.CARD_RANK_NAME_K, pu.SUIT_HEARTS)
            ]
        # Create a mock game state
        self.game_state = pk.PokerGameStateSnapshot(
            pot=100,
            current_bet=50,
            phase=pk.PHASE_FLOP,
            community_cards=[
                pu.Card(pu.CARD_RANK_NAME_10, pu.SUIT_HEARTS),
                pu.Card(pu.CARD_RANK_NAME_J, pu.SUIT_HEARTS),
                pu.Card(pu.CARD_RANK_NAME_Q, pu.SUIT_HEARTS),
                pu.Card(pu.CARD_RANK_NAME_K, pu.SUIT_CLUBS)

            ],
            current_player=self.current_player,
            players = [self.current_player],
            actions = []
        )

    def test_vectorize_game_state(self):
        # Expected vector
        expected_vector = np.array([
            100,  # Pot
            50,   # Current bet
            1,    # Phase (FLOP)
            10, 0, 11, 0, 12, 0, 13, 2, 0, 0, # Community cards (10, J, Q, K)
            14, 0, 13, 0, # Player's hand (A, K)
            1000, # Player's stack
            0, # player's status
        ])

        # Vectorize the game state
        state_vector = self.rl_agent.vectorize_game_state(self.game_state)

        # Assert the vector matches the expected vector
        np.testing.assert_array_equal(state_vector, expected_vector)

class MockDeck(pu.Deck):
    def __init__(self):
        super().__init__(no_shuffle=True)
        self.fresh_deck_of_cards = [
            # PairBetterAgent's hand
            pu.Card(pu.CARD_RANK_NAME_5, pu.SUIT_HEARTS), pu.Card(pu.CARD_RANK_NAME_10, pu.SUIT_SPADES),
            # FlushBetterAgent's hand
            pu.Card(pu.CARD_RANK_NAME_2, pu.SUIT_HEARTS), pu.Card(pu.CARD_RANK_NAME_3, pu.SUIT_HEARTS),
            # Community cards, give the flush better agent a flush on the turn
            pu.Card(pu.CARD_RANK_NAME_4, pu.SUIT_HEARTS),
            pu.Card(pu.CARD_RANK_NAME_J, pu.SUIT_HEARTS),
            pu.Card(pu.CARD_RANK_NAME_9, pu.SUIT_SPADES),
            pu.Card(pu.CARD_RANK_NAME_7, pu.SUIT_HEARTS),
            pu.Card(pu.CARD_RANK_NAME_A, pu.SUIT_CLUBS)
        ]
        self.cards = self.fresh_deck_of_cards.copy()

    def draw(self):
        return self.cards.pop(0)

class TestRLShowdownAnalysis(unittest.TestCase):
    def setUp(self):
        # Create players with agents
        self.player1 = Player(name="PairBetterAgent", stack=1000, agent=ag.RLAgent())
        self.player2 = Player(name="FlushBetter", stack=1000, agent=ag.FlushBetterAgent())

        # Initialize the game with a mock deck
        self.game = pk.PokerGame(players=[self.player1, self.player2], maximum_hands=5)
        self.game.deck = MockDeck()

    def test_rl_loses_to_flush_better(self):
        self.game.run_hand()
        # print final stacks
        print(f"Final stacks: {self.player1.name}: {self.player1.stack}, {self.player2.name}: {self.player2.stack}")

    def test_rl_wins_to_flush_better(self):
        pass


class TestRLEpisodeAnalysis(unittest.TestCase):
    pass

if __name__ == "__main__":
    unittest.main()