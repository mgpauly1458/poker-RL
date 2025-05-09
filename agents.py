import random
import poker as pk

class AllInAgent:
    def act(self, game_state: pk.PokerGameStateSnapshot) -> pk.Action:
        """Always goes all-in."""
        current_player = game_state.current_player
        if game_state.phase == pk.PHASE_TURN:
            # Get current player's stack amount
            return pk.Action(current_player, type=pk.PLAYER_ACTION_ALL_IN, amount=current_player.stack)
        return pk.Action(current_player, type=pk.PLAYER_ACTION_CHECK, amount=0)

class CallCheckAgent:
    def act(self, game_state: pk.PokerGameStateSnapshot)-> pk.Action:
        current_player = game_state.current_player
        """Always calls if there's a bet, otherwise checks."""
        if game_state.phase == pk.PHASE_TURN:
            # Get current player's stack amount
            current_player = game_state.current_player
            if game_state.current_bet > 0:
                return pk.Action(current_player, type=pk.PLAYER_ACTION_CALL, amount=current_player.stack)
            else:
                return pk.Action(current_player, type=pk.PLAYER_ACTION_CHECK, amount=0)
        return pk.Action(current_player, type=pk.PLAYER_ACTION_CHECK, amount=0)

class FoldAgent:
    def act(self, game_state: pk.PokerGameStateSnapshot) -> pk.Action:
        """Always folds."""
        current_player = game_state.current_player

        if game_state.current_bet > 0:
            return pk.Action(current_player, type=pk.PLAYER_ACTION_FOLD, amount=0)
        return pk.Action(current_player, type=pk.PLAYER_ACTION_CHECK, amount=0)
    
    