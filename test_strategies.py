import unittest
import poker as pg
from poker import PokerGame, Player
import agents as ag
import poker_util as pu

class TestPairBetterVSFolder(unittest.TestCase):
    def setUp(self):
        print("\nSetting up the game for PairBetterAgent vs FolderLong.")
        # Create players with agents
        self.player1 = Player(name="PairBetterAgent", stack=1000, agent=ag.PairBetterAgent())
        self.player2 = Player(name="FolderLong", stack=1000, agent=ag.FoldAgent())

        # Initialize the game with a mock deck
        self.game = PokerGame(players=[self.player1, self.player2], maximum_hands=100)
        self.game.deck = pu.Deck()

    def test_pair_better_vs_folder_long(self):
        self.game.run_game()
        print(f"Final stacks: {self.player1.name}: {self.player1.stack}, {self.player2.name}: {self.player2.stack}")

class TestPairBetterVSFlushBetter(unittest.TestCase):
    def setUp(self):
        print("\nSetting up the game for PairBetterAgent vs TwoPairBetter.")
        # Create players with agents
        self.player1 = Player(name="PairBetterAgent", stack=1000, agent=ag.PairBetterAgent())
        self.player2 = Player(name="FlushBetter", stack=1000, agent=ag.FlushBetterAgent())

        # Initialize the game with a mock deck
        self.game = PokerGame(players=[self.player1, self.player2], maximum_hands=100)
        self.game.deck = pu.Deck()

    def test_pair_better_vs_flush_better(self):
        self.game.run_game()

        print(f"Final stacks: {self.player1.name}: {self.player1.stack}, {self.player2.name}: {self.player2.stack}")