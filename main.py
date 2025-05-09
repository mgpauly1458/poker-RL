from poker import PokerGame, Player
from agents import AllInAgent, CallCheckAgent
import poker_util as pu

# Mock Deck for predictable results
class MockDeck(pu.Deck):
    def __init__(self):
        self.cards = [
            pu.Card(pu.CARD_RANK_NAME_A, pu.SUIT_HEARTS), pu.Card(pu.CARD_RANK_NAME_K, pu.SUIT_HEARTS), # Player 1's hand
            pu.Card(pu.CARD_RANK_NAME_Q, pu.SUIT_SPADES), pu.Card(pu.CARD_RANK_NAME_J, pu.SUIT_SPADES), # Player 2's hand
            pu.Card(pu.CARD_RANK_NAME_2, pu.SUIT_DIAMONDS), pu.Card(pu.CARD_RANK_NAME_3, pu.SUIT_DIAMONDS), # Player 3's hand

            pu.Card(pu.CARD_RANK_NAME_10, pu.SUIT_HEARTS),
            pu.Card(pu.CARD_RANK_NAME_J, pu.SUIT_HEARTS),
            pu.Card(pu.CARD_RANK_NAME_Q, pu.SUIT_HEARTS), # Flop

            pu.Card(pu.CARD_RANK_NAME_7, pu.SUIT_CLUBS), # Turn

            pu.Card(pu.CARD_RANK_NAME_6, pu.SUIT_HEARTS)  # River
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