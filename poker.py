from poker_util import (
    Card, Deck, PokerRules
)

DEBUG = True

PHASE_PRE_FLOP = 'pre-flop'
PHASE_FLOP = 'flop'
PHASE_TURN = 'turn'
PHASE_RIVER = 'river'

POSITION_SMALL_BLIND = 'SB'
POSITION_BIG_BLIND = 'BB'
POSITION_UNDER_THE_GUN = 'UTG'
POSITION_UNDER_THE_GUN_PLUS_ONE = 'UTG+1'
POSITION_UNDER_THE_GUN_PLUS_TWO = 'UTG+2'
POSITION_LOWJACK = 'LJ'
POSITION_HIGHJACK = 'HJ'
POSITION_MIDDLE_POSITION = 'MP'
POSITION_CUT_OFF = 'CO'
POSITION_BUTTON = 'BTN'

PLAYER_STATUS_WAITING = 'waiting'
PLAYER_STATUS_FOLDED = 'folded'
PLAYER_STATUS_CHECKED = 'checked'
PLAYER_STATUS_CALLED = 'called'
PLAYER_STATUS_RAISED = 'raised'
PLAYER_STATUS_ALL_IN = 'all_in'

PLAYER_ACTION_FOLD = 'fold'
PLAYER_ACTION_CHECK = 'check'
PLAYER_ACTION_CALL = 'call'
PLAYER_ACTION_RAISE = 'raise'
PLAYER_ACTION_RERAISE = 'reraise'
PLAYER_ACTION_ALL_IN = 'all_in'

class Player:
    def __init__(self, name, stack, agent=None):
        self.name = name
        self.stack = stack
        self.current_bet = 0
        self.status = PLAYER_STATUS_WAITING  # Can be "waiting", "folded", "checked", "called", "raised"
        self.hand = []
        self.agent = agent  # Agent object to decide actions

    def place_bet(self, amount):
        if amount > self.stack:
            raise ValueError(f"{self.name} does not have enough chips to bet {amount}.")
        self.stack -= amount
        self.current_bet += amount

    def reset_for_new_round(self):
        self.current_bet = 0
        self.status = PLAYER_STATUS_WAITING
        self.hand = []

    def take_action(self, game_state):
        """Query the agent for an action based on the game state."""
        if self.agent:
            return self.agent.act(game_state)
        raise NotImplementedError(f"{self.name} does not have an agent to decide actions.")

class Action:
    def __init__(self, player, type, amount=0):
        self.player = player
        self.type = type  # e.g., fold, check, call, raise, reraise, all_in
        self.amount = amount  # Amount of chips involved in the action

    def __repr__(self):
        return f"Action(player={self.player.name}, type={self.action_type}, amount={self.amount})"

class PokerGame:
    def __init__(self, players):
        self.players = players  # List of Player objects
        self.pot = 0
        self.current_bet = 0
        self.table_position = 0  # Tracks the current player's position
        self.community_cards = []
        self.deck = Deck()
        self.phase = PHASE_PRE_FLOP  # Current phase of the game
        self.actions = []  # List of actions for the current phase

    def deal_hands(self):
        """Deal two cards to each player."""
        for player in self.players:
            player.hand = [self.deck.draw(), self.deck.draw()]

    def rotate_position(self):
        """Move to the next player's position."""
        self.table_position = (self.table_position + 1) % len(self.players)

    def map_position_to_position_name(self, position_index):
        """Map the position index to a position name."""
        position_names = [
            POSITION_UNDER_THE_GUN,
            POSITION_UNDER_THE_GUN_PLUS_ONE,
            POSITION_UNDER_THE_GUN_PLUS_TWO,
            POSITION_LOWJACK,
            POSITION_HIGHJACK,
            POSITION_MIDDLE_POSITION,
            POSITION_CUT_OFF,
            POSITION_BUTTON,
            POSITION_SMALL_BLIND,
            POSITION_BIG_BLIND
        ]
        return position_names[position_index % len(position_names)]

    def process_action(self, player, action):
        """Process a player's action."""
        if action.type == PLAYER_ACTION_FOLD:
            player.status = PLAYER_STATUS_FOLDED
            self.actions.append(action)
        elif action.type == PLAYER_ACTION_CHECK:
            if player.current_bet < self.current_bet:
                raise ValueError(f"{player.name} cannot check because they have not matched the current bet.")
            player.status = PLAYER_STATUS_CHECKED
            self.actions.append(action)
        elif action.type == PLAYER_ACTION_CALL:
            call_amount = self.current_bet - player.current_bet
            player.place_bet(call_amount)
            self.pot += call_amount
            player.status = PLAYER_STATUS_CALLED
            self.actions.append(action)
        elif action.type == PLAYER_ACTION_RAISE:
            raise_amount = action["amount"]
            if raise_amount <= self.current_bet:
                raise ValueError(f"Raise must be greater than the current bet of {self.current_bet}.")
            player.place_bet(raise_amount)
            self.pot += raise_amount
            self.current_bet = player.current_bet
            player.status = PLAYER_STATUS_RAISED
            self.actions.append(action)
        elif action.type == PLAYER_ACTION_RERAISE:
            reraise_amount = action["amount"]
            if reraise_amount <= self.current_bet:
                raise ValueError(f"Reraise must be greater than the current bet of {self.current_bet}.")
            player.place_bet(reraise_amount)
            self.pot += reraise_amount
            self.current_bet = player.current_bet
            player.status = PLAYER_STATUS_RAISED
            self.actions.append(action)
        elif action.type == PLAYER_ACTION_ALL_IN:
            if player.stack <= 0:
                raise ValueError(f"{player.name} cannot go all-in with a stack of {player.stack}.")
            all_in_amount = player.stack
            player.place_bet(all_in_amount)
            self.pot += all_in_amount
            player.status = PLAYER_STATUS_ALL_IN
            self.actions.append(action)

    def betting_round(self):
        """Run a betting round."""
        print(f"Starting betting round for phase: {self.phase}")

        # iniitialize starting position. if phase is preflop, set the first player to act as the UTG player.
        # if the phase is not fre flop, set the first player to act as the first player to come after the dealer.
        if self.phase == "preflop":
            self.table_position = 2
        else:
            self.table_position = 0

        self.actions = []  # Reset actions for the current phase
        while True:
            active_players = [p for p in self.players if p.status != "folded"]
            if len(active_players) == 1:
                # If only one player remains, they win the pot
                winner = active_players[0]
                print(f"{winner.name} wins the pot of {self.pot} as everyone else folded!")
                winner.stack += self.pot
                self.reset_for_new_round()
                return

            current_player = self.players[self.table_position]
            if DEBUG:
                print(f"Current player: {current_player.name}, Position: {self.map_position_to_position_name(self.table_position)}")

            if current_player.status != "folded":
                game_state = PokerGameStateSnapshot(
                    pot=self.pot,
                    current_bet=self.current_bet,
                    phase=self.phase,
                    players=[p for p in self.players],
                    community_cards=self.community_cards,
                    actions=self.actions,
                    current_player=current_player
                )
                action = current_player.take_action(game_state)
                self.process_action(current_player, action)

            self.rotate_position()

            # End the betting round if all active players have matched the current bet
            if all(p.status in ["folded", "checked", "called"] or p.current_bet == self.current_bet for p in self.players):
                break

        print(f"End of betting round. Pot is now {self.pot}.")

        if self.phase == "showdown":
            # If it's the showdown phase, determine the winner
            self.determine_winner()
            return
        
    def reset_for_new_round(self):
        """Reset the game state for a new round."""
        self.pot = 0
        self.current_bet = 0
        self.community_cards = []
        self.deck.shuffle()
        for player in self.players:
            player.reset_for_new_round()
        self.phase = "preflop"

    def determine_winner(self):
        rules = PokerRules()
        player_and_current_best_hand = {
            player: None,
            best_hand: None
        }

        # get all active players who have not folded
        active_players = [p for p in self.players if p.status != "folded"]

        for player in active_players:
            # get player's cards and all community cards in a list
            all_cards = player.hand + self.community_cards
            # get all possible 5 card combinations combinations from the player's hand and community cards
            from itertools import combinations
            all_combinations = list(combinations(all_cards, 5))
            # get the best hand from all combinations
            best_hand = rules.get_best_hand(all_combinations)
            if best_hand > player_and_current_best_hand[best_hand]:
                player_and_current_best_hand[best_hand] = player
                player_and_current_best_hand[player] = best_hand
        
        print(f"{player_and_current_best_hand[player]} wins with {player_and_current_best_hand[best_hand]}!")
        player_and_current_best_hand[player].stack += self.pot
        self.reset_for_new_round()

    def add_community_card(self):
        """Add a card to the community cards."""
        self.community_cards.append(self.deck.draw())

    def advance_phase(self):
        """Advance to the next phase of the game."""
        if self.phase == "preflop":
            self.phase = "flop"
            for _ in range(3):  # Deal the flop
                self.add_community_card()
        elif self.phase == "flop":
            self.phase = "turn"
            self.add_community_card()
        elif self.phase == "turn":
            self.phase = "river"
            self.add_community_card()
        elif self.phase == "river":
            self.phase = "showdown"

class PokerGameStateSnapshot:
    def __init__(self,
                 pot,
                 current_bet,
                phase,
                players,
                community_cards,
                actions,
                current_player):
        self.pot = pot
        self.current_bet = current_bet
        self.phase = phase
        self.players = players
        self.community_cards = community_cards
        self.actions = actions
        self.current_player = current_player

