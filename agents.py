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