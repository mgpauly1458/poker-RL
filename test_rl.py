import unittest
import numpy as np
from agents import RLAgent
from poker_game import Player
import poker_util as pu
import poker_game as pk

class TestRLAgentVectorization(unittest.TestCase):
    def setUp(self):
        # Create an RLAgent
        self.rl_agent = RLAgent()
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

if __name__ == "__main__":
    unittest.main()