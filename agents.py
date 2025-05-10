import random
import poker as pk

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

class AllInAgent(BaseAgent):
    def act(self, game_state: pk.PokerGameStateSnapshot) -> pk.Action:
        """Goes all in on the turn, otherwise checks or calls."""
        current_player = game_state.current_player
        if game_state.phase == pk.PHASE_TURN:
            # Get current player's stack amount
            return self.all_in(game_state)
        elif game_state.current_bet > current_player.current_bet:
            return self.call(game_state)
        return self.check(game_state)

class CallCheckAgent(BaseAgent):
    def act(self, game_state: pk.PokerGameStateSnapshot)-> pk.Action:
        current_player = game_state.current_player
        """Always calls if there's a bet, otherwise checks."""
        print(game_state)
        if game_state.current_bet > current_player.current_bet:
            # If there's a bet, call it
            return self.call(game_state)
        else:
            # If not, check
            return self.check(game_state)

class FoldAgent(BaseAgent):
    def act(self, game_state: pk.PokerGameStateSnapshot) -> pk.Action:
        """Always folds."""
        current_player = game_state.current_player
        if game_state.current_bet > current_player.current_bet:
            return self.fold(game_state)
        return self.check(game_state)

class DelayedAllinAgent(BaseAgent):
    def __init__(self, delay: int = 1):
        self.delay = delay
        self.current_delay = 0

    def act(self, game_state: pk.PokerGameStateSnapshot) -> pk.Action:
        """Delays going all in by a specified number of rounds."""
        current_player = game_state.current_player
        if self.current_delay < self.delay:
            self.current_delay += 1
            if game_state.current_bet > current_player.current_bet:
                return self.call(game_state)
            else:
                return self.check(game_state)
        else:
            return self.all_in(game_state)