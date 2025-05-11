import random
import poker as pk
import poker_util as pu
import numpy as np

class BaseAgent:
    def call(self, game_state: pk.PokerGameStateSnapshot) -> pk.Action:
        current_player = game_state.current_player
        amount_to_call = game_state.current_bet - current_player.current_bet
        return pk.Action(current_player, type=pk.PLAYER_ACTION_CALL, amount=amount_to_call)
    
    def fold(self, game_state: pk.PokerGameStateSnapshot) -> pk.Action:
        current_player = game_state.current_player
        return pk.Action(current_player, type=pk.PLAYER_ACTION_FOLD, amount=0)
    
    def check(self, game_state: pk.PokerGameStateSnapshot) -> pk.Action:
        current_player = game_state.current_player
        return pk.Action(current_player, type=pk.PLAYER_ACTION_CHECK, amount=0)
    
    def raise_bet(self, game_state: pk.PokerGameStateSnapshot, amount: int) -> pk.Action:
        current_player = game_state.current_player
        return pk.Action(current_player, type=pk.PLAYER_ACTION_RAISE, amount=amount)
    
    def all_in(self, game_state: pk.PokerGameStateSnapshot) -> pk.Action:
        current_player = game_state.current_player
        return pk.Action(current_player, type=pk.PLAYER_ACTION_ALL_IN, amount=current_player.stack)

    def someone_has_raised(self, game_state: pk.PokerGameStateSnapshot) -> bool:
        """Check if someone has raised."""
        current_player = game_state.current_player
        return game_state.current_bet > current_player.current_bet
    
    def no_one_has_raised(self, game_state: pk.PokerGameStateSnapshot) -> bool:
        """Check if no one has raised."""
        current_player = game_state.current_player
        return game_state.current_bet == current_player.current_bet

class AllInAgent(BaseAgent):
    def act(self, game_state: pk.PokerGameStateSnapshot) -> pk.Action:
        """Goes all in on the turn, otherwise checks or calls."""
        current_player = game_state.current_player
        if game_state.phase == pk.PHASE_TURN:
            # Get current player's stack amount
            return self.all_in(game_state)
        elif self.someone_has_raised(game_state):
            return self.call(game_state)
        return self.check(game_state)

class CallCheckAgent(BaseAgent):
    def act(self, game_state: pk.PokerGameStateSnapshot)-> pk.Action:
        """Always calls if there's a bet, otherwise checks."""
        if self.someone_has_raised(game_state):
            # If there's a bet, call it
            return self.call(game_state)
        else:
            # If not, check
            return self.check(game_state)

class FoldAgent(BaseAgent):
    def act(self, game_state: pk.PokerGameStateSnapshot) -> pk.Action:
        """Always folds."""
        if self.someone_has_raised(game_state):
            return self.fold(game_state)
        return self.check(game_state)

class DelayedAllinAgent(BaseAgent):
    def __init__(self, delay: int = 1):
        self.delay = delay
        self.current_delay = 0

    def act(self, game_state: pk.PokerGameStateSnapshot) -> pk.Action:
        """Delays going all in by a specified number of rounds."""
        if self.current_delay < self.delay:
            self.current_delay += 1
            if self.someone_has_raised(game_state):
                return self.call(game_state)
            else:
                return self.check(game_state)
        else:
            return self.all_in(game_state)

class DelayedRaiseAgent(BaseAgent):
    def __init__(self, delay: int = 1, raise_amount: int = 100):
        self.delay = delay
        self.current_delay = 0
        self.raise_amount = raise_amount

    def act(self, game_state: pk.PokerGameStateSnapshot) -> pk.Action:
        """Delays raising by a specified number of rounds."""

        # if someone raises call. if the delay is not up and no one has raised check
        # if the delay is up and no one has raised raise
        if self.current_delay < self.delay:
            self.current_delay += 1
            if self.someone_has_raised(game_state):
                return self.call(game_state)
            else:
                return self.check(game_state)
        else:
            if self.someone_has_raised(game_state):
                return self.call(game_state)
            else:
                return self.raise_bet(game_state, self.raise_amount)
        
class ReRaiseAgent(BaseAgent):
    def __init__(self, re_raise_amount: int = 10):
        self.re_raise_amount = re_raise_amount
        self.current_phase = None
        self.did_check = False

    def act(self, game_state: pk.PokerGameStateSnapshot) -> pk.Action:
        # reset for new round

        if game_state.phase != self.current_phase:
            self.current_phase = game_state.phase
            self.did_check = False

        if self.someone_has_raised(game_state):
            if self.did_check:
                return self.raise_bet(game_state, self.re_raise_amount)
            else:
                # will call if in position and someone raises
                return self.call(game_state)

        self.did_check = True
        return self.check(game_state)
    
class SmartAgentBase(BaseAgent):

    def __init__(self):
        self.rules = pk.PokerRules()

    def get_current_players_best_hand(self, game_state: pk.PokerGameStateSnapshot) -> pu.Hand:
        """Get the best hand of the player."""
        current_player = game_state.current_player
        hand = current_player.hand
        community_cards = game_state.community_cards

        # Combine hand and community cards to evaluate the best hand
        all_cards = hand + community_cards
        import itertools
        all_combinations = list(itertools.combinations(all_cards, 5))

        best_hand = self.rules.get_best_hand(all_combinations)
        return best_hand

    def i_have_at_least_a_pair(self, game_state: pk.PokerGameStateSnapshot) -> bool:
        #"""Check if the player has at least a pair."""
        best_hand:pu.Hand = self.get_current_players_best_hand(game_state)
        return isinstance(best_hand, pu.OnePair) or \
                isinstance(best_hand, pu.TwoPair) or \
                isinstance(best_hand, pu.ThreeOfAKind) or \
                isinstance(best_hand, pu.Straight) or \
                isinstance(best_hand, pu.Flush) or \
                isinstance(best_hand, pu.FullHouse) or \
                isinstance(best_hand, pu.FourOfAKind) or \
                isinstance(best_hand, pu.StraightFlush) or \
                isinstance(best_hand, pu.RoyalFlush)

    def i_have_at_least_two_pair(self, game_state: pk.PokerGameStateSnapshot) -> bool:
        """Check if the player has at least two pair."""
        best_hand:pu.Hand = self.get_current_players_best_hand(game_state)
        return isinstance(best_hand, pu.TwoPair) or \
                isinstance(best_hand, pu.ThreeOfAKind) or \
                isinstance(best_hand, pu.Straight) or \
                isinstance(best_hand, pu.Flush) or \
                isinstance(best_hand, pu.FullHouse) or \
                isinstance(best_hand, pu.FourOfAKind) or \
                isinstance(best_hand, pu.StraightFlush) or \
                isinstance(best_hand, pu.RoyalFlush)
    
    def i_have_at_least_three_of_a_kind(self, game_state: pk.PokerGameStateSnapshot) -> bool:
        """Check if the player has at least three of a kind."""
        best_hand:pu.Hand = self.get_current_players_best_hand(game_state)
        return isinstance(best_hand, pu.ThreeOfAKind) or \
                isinstance(best_hand, pu.Straight) or \
                isinstance(best_hand, pu.Flush) or \
                isinstance(best_hand, pu.FullHouse) or \
                isinstance(best_hand, pu.FourOfAKind) or \
                isinstance(best_hand, pu.StraightFlush) or \
                isinstance(best_hand, pu.RoyalFlush)
    
    def i_have_at_least_a_straight(self, game_state: pk.PokerGameStateSnapshot) -> bool:
        """Check if the player has at least a straight."""
        best_hand:pu.Hand = self.get_current_players_best_hand(game_state)
        return isinstance(best_hand, pu.Straight) or \
                isinstance(best_hand, pu.Flush) or \
                isinstance(best_hand, pu.FullHouse) or \
                isinstance(best_hand, pu.FourOfAKind) or \
                isinstance(best_hand, pu.StraightFlush) or \
                isinstance(best_hand, pu.RoyalFlush)
    
    def i_have_at_least_a_flush(self, game_state: pk.PokerGameStateSnapshot) -> bool:
        """Check if the player has at least a flush."""
        best_hand:pu.Hand = self.get_current_players_best_hand(game_state)
        return isinstance(best_hand, pu.Flush) or \
                isinstance(best_hand, pu.FullHouse) or \
                isinstance(best_hand, pu.FourOfAKind) or \
                isinstance(best_hand, pu.StraightFlush) or \
                isinstance(best_hand, pu.RoyalFlush)
    
    def i_have_at_least_a_full_house(self, game_state: pk.PokerGameStateSnapshot) -> bool:
        """Check if the player has at least a full house."""
        best_hand:pu.Hand = self.get_current_players_best_hand(game_state)
        return isinstance(best_hand, pu.FullHouse) or \
                isinstance(best_hand, pu.FourOfAKind) or \
                isinstance(best_hand, pu.StraightFlush) or \
                isinstance(best_hand, pu.RoyalFlush)
    
    def i_have_at_least_a_four_of_a_kind(self, game_state: pk.PokerGameStateSnapshot) -> bool:
        """Check if the player has at least a four of a kind."""
        best_hand:pu.Hand = self.get_current_players_best_hand(game_state)
        return isinstance(best_hand, pu.FourOfAKind) or \
                isinstance(best_hand, pu.StraightFlush) or \
                isinstance(best_hand, pu.RoyalFlush)
    
    def i_have_at_least_a_straight_flush(self, game_state: pk.PokerGameStateSnapshot) -> bool:
        """Check if the player has at least a straight flush."""
        best_hand:pu.Hand = self.get_current_players_best_hand(game_state)
        return isinstance(best_hand, pu.StraightFlush) or \
                isinstance(best_hand, pu.RoyalFlush)
    
    def i_have_at_least_a_royal_flush(self, game_state: pk.PokerGameStateSnapshot) -> bool:
        """Check if the player has at least a royal flush."""
        best_hand:pu.Hand = self.get_current_players_best_hand(game_state)
        return isinstance(best_hand, pu.RoyalFlush)

class PairBetterAgent(SmartAgentBase):
    def act(self, game_state: pk.PokerGameStateSnapshot) -> pk.Action:
        """Checks if the player has at least a pair."""
        if self.i_have_at_least_a_pair(game_state):
            if not self.someone_has_raised(game_state):
                return self.raise_bet(game_state, 100)
            else:
                return self.call(game_state)
        elif self.someone_has_raised(game_state):
            return self.call(game_state)
        else:
            return self.check(game_state)
        
class FlushBetterAgent(SmartAgentBase):
    def act(self, game_state: pk.PokerGameStateSnapshot) -> pk.Action:
        """Checks if the player has at least a flush."""
        if self.i_have_at_least_a_flush(game_state):
            if not self.someone_has_raised(game_state):
                return self.raise_bet(game_state, 100)
            else:
                return self.call(game_state)
        elif self.someone_has_raised(game_state):
            return self.call(game_state)
        else:
            return self.check(game_state)



class RLAgent(BaseAgent):
    def vectorize_game_state(self, game_state: pk.PokerGameStateSnapshot) -> np.ndarray:
        """
        Converts the game state into a numerical vector representation.
        """
        # Vectorize the pot size
        pot_size = game_state.pot
        print('pot_size: ', pot_size)

        # Vectorize the current bet
        current_bet = game_state.current_bet
        print('current_bet: ', current_bet)

        # Vectorize the phase of the game
        phase_vector = self._vectorize_phase(game_state.phase)
        print('phase_vector: ', phase_vector)

        # Vectorize the community cards
        community_cards_vector = self._vectorize_cards(game_state.community_cards, community=True)
        print('community_cards_vector: ', community_cards_vector)

        # Vectorize the current player's hand
        current_player_hand_vector = self._vectorize_cards(game_state.current_player.hand)
        print('current_player_hand_vector: ', current_player_hand_vector)

        # Vectorize the current player's stack
        current_player_stack = game_state.current_player.stack
        print('current_player_stack: ', current_player_stack)

        # Vectorize the current player's status
        current_player_status = self._vectorize_status(game_state.current_player.status)
        print('current_player_status: ', current_player_status)

        # Combine all vectors into a single numpy array
        state_vector = np.concatenate([
            [pot_size],
            [current_bet],
            [phase_vector],
            community_cards_vector,
            current_player_hand_vector,
            [current_player_stack],
            [current_player_status]
        ])

        return state_vector
    
    def _map_suit_to_number(self, suit: str) -> int:
        """
        Maps the suit of a card to a numerical value.
        """
        suit_mapping = {
            pu.SUIT_HEARTS: 0,
            pu.SUIT_DIAMONDS: 1,
            pu.SUIT_CLUBS: 2,
            pu.SUIT_SPADES: 3
        }
        return suit_mapping.get(suit, -1)

    def _vectorize_phase(self, phase: str):
        # map phase to a number
        phase_mapping = {
            pk.PHASE_PRE_FLOP: 0,
            pk.PHASE_FLOP: 1,
            pk.PHASE_TURN: 2,
            pk.PHASE_RIVER: 3
        }
        return phase_mapping.get(phase, -1)

    def _vectorize_cards(self, cards: list[pu.Card], community: bool = False):
        """
        Converts a list of cards into a numerical vector.
        Each card is represented by its rank and suit.
        """
        cards_vector = []

        for card in cards:
            rank_num = card.get_card_rank_value(card.rank)
            suit_num = self._map_suit_to_number(card.suit)
            cards_vector.append(rank_num)
            cards_vector.append(suit_num)

        if community:
            if len(cards) < 5:
                # Pad the vector with zeros if there are less than 5 cards
                for _ in range(5 - len(cards)):
                    cards_vector.append(0)
                    cards_vector.append(0)

        return cards_vector

    def _vectorize_status(self, status: str) -> int:
        """
        Converts the player's status into a numerical value.
        """
        statuses = {
            pk.PLAYER_STATUS_WAITING: 0,
            pk.PLAYER_STATUS_FOLDED: 1,
            pk.PLAYER_STATUS_CHECKED: 2,
            pk.PLAYER_STATUS_CALLED: 3,
            pk.PLAYER_STATUS_RAISED: 4,
            pk.PLAYER_STATUS_ALL_IN: 5
        }
        return statuses.get(status, -1)  # Default to -1 if status is unknown

    def act(self, game_state: pk.PokerGameStateSnapshot) -> pk.Action:
        """
        Example action method for RLAgent.
        This method can be extended to use the vectorized state for decision-making.
        """
        state_vector = self.vectorize_game_state(game_state)
        # Placeholder: Always checks for now
        return self.check(game_state)