from poker import PokerGame, Player
from agents import AllInAgent, CallCheckAgent
from poker_util import Deck, Card

# Mock Deck for predictable results
class MockDeck(Deck):
    def __init__(self):
        self.cards = [
            Card('A', 'Hearts'), Card('K', 'Hearts'),  # Player 1's hand
            Card('Q', 'Spades'), Card('J', 'Spades'),  # Player 2's hand
            Card('2', 'Diamonds'), Card('3', 'Diamonds'),  # Player 3's hand
            Card('10', 'Diamonds'), Card('9', 'Diamonds'), Card('8', 'Diamonds'),  # Flop
            Card('7', 'Clubs'),  # Turn
            Card('6', 'Hearts')  # River
        ]

    def draw(self):
        return self.cards.pop(0)

# Test program
def main():
    # Create players with agents
    player1 = Player(name="AllInAgent", stack=1000, agent=AllInAgent())
    player2 = Player(name="CallCheckAgent", stack=1000, agent=CallCheckAgent())
    player3 = Player(name="CallCheckAgent2", stack=1000, agent=CallCheckAgent())

    # Initialize the game with a mock deck
    game = PokerGame(players=[player1, player2, player3])
    game.deck = MockDeck()  # Use the mock deck for predictable results
    # Deal hands and play the game
    game.deal_hands()
    for _ in range(4):  # Preflop, Flop, Turn, River
        game.betting_round()
        game.advance_phase()

    game.determine_winner()

if __name__ == "__main__":
    main()