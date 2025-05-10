from poker_util import (
    Card, Deck, PokerRules, WorstPokerHand
)

DEBUG = True

PHASE_PRE_FLOP = 'pre-flop'
PHASE_FLOP = 'flop'
PHASE_TURN = 'turn'
PHASE_RIVER = 'river'
PHASE_SHOWDOWN = 'showdown'

POSITION_SMALL_BLIND = 0
POSITION_BIG_BLIND = 1
POSITION_UNDER_THE_GUN = 2
POSITION_UNDER_THE_GUN_PLUS_ONE = 3
POSITION_MIDDLE_POSITION = 4
POSITION_LOWJACK = 5
POSITION_HIGHJACK = 6
POSITION_CUT_OFF = 7
POSITION_BUTTON = 8

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

GAME_SHOULD_CONTINUE = 'continue'

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
            actual_bet_amount = self.stack
            self.stack = 0
            self.current_bet += actual_bet_amount
            self.status = PLAYER_STATUS_ALL_IN
            return actual_bet_amount
        self.stack -= amount
        self.current_bet += amount
        return amount

    def reset_player_for_new_hand(self):
        self.current_bet = 0
        self.status = PLAYER_STATUS_WAITING
        self.hand = []

    def take_action(self, game_state):
        """Query the agent for an action based on the game state."""
        if self.agent:
            return self.agent.act(game_state)
        raise NotImplementedError(f"{self.name} does not have an agent to decide actions.")

    def __str__(self):
        return f"Player(name={self.name}, stack={self.stack}, status={self.status}, hand={self.hand})"

class Action:
    def __init__(self, player, type, amount=0):
        self.player = player
        self.type = type  # e.g., fold, check, call, raise, reraise, all_in
        self.amount = amount  # Amount of chips involved in the action

        if DEBUG:
            print(f"Action taken: {self.player.name} {self.type} {self.amount}")

    def __repr__(self):
        return f"Action(player={self.player.name}, type={self.type}, amount={self.amount})"

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
        self.hand_number = 0  # Track the number of hands played
        if len(players) < 2:
            raise ValueError("At least two players are required to start a game.")
        
    def deal_hands(self):
        """Deal two cards to each player."""
        for player in self.players:
            player.hand = [self.deck.draw(), self.deck.draw()]

    def rotate_position(self):
        """Move to the next player's position."""
        self.table_position = (self.table_position + 1) % len(self.players)

    def rotate_player_positions_on_table(self):
        """Rotate player positions on the table."""
        self.players = self.players[1:] + [self.players[0]]

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
            if call_amount == 0:
                raise ValueError(f"{player.name} cannot call because they have already matched the current bet. Check instead")
            actual_bet_amount = player.place_bet(call_amount)
            print('actual_bet_amount: ', actual_bet_amount)
            self.pot += actual_bet_amount
            if player.status != PLAYER_STATUS_ALL_IN:
                player.status = PLAYER_STATUS_CALLED
            self.actions.append(action)
        elif action.type == PLAYER_ACTION_RAISE:
            raise_amount = action.amount
            if raise_amount <= self.current_bet:
                raise ValueError(f"Raise must be greater than the current bet of {self.current_bet}.")
            player.place_bet(raise_amount)
            self.pot += raise_amount
            self.current_bet = player.current_bet
            player.status = PLAYER_STATUS_RAISED
            self.actions.append(action)
        elif action.type == PLAYER_ACTION_RERAISE:
            reraise_amount = action.amount
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
            if self.current_bet < player.current_bet:
                self.current_bet = player.current_bet
            player.status = PLAYER_STATUS_ALL_IN
            self.actions.append(action)

    def calculate_preflop_starting_position(self):
        if len(self.players) == 2:
            return POSITION_SMALL_BLIND
        else:
            return POSITION_UNDER_THE_GUN
        
    def calculate_non_preflop_starting_position(self):
        # find first player in list who has not folded, return their position
        for i in range(len(self.players)):
            if self.players[i].status != PLAYER_STATUS_FOLDED:
                return i
        raise ValueError("No active players found.")

    def calculate_next_position(self, current_position):

        # take the current position index and get all the players that come after it in the list
        remaining_players = self.players[current_position + 1:]
        if len(remaining_players) == 0:
            current_position = -1  # reset to the beginning of the list
            remaining_players = self.players
        
        print(f"Remaining players after {self.players[current_position].name}: {[player.name for player in remaining_players]}")
        # get all remaining players who have not folded
        remaining_players = [player for player in remaining_players if player.status != PLAYER_STATUS_FOLDED]
        if self.phase == PHASE_PRE_FLOP and len(remaining_players) == 0:
            # if there are no remaining players, return the first player in the list
            return POSITION_SMALL_BLIND

        # find the first player in the list who has not folded and is not all in
        for player in remaining_players:
            if player.status != PLAYER_STATUS_FOLDED and player.status != PLAYER_STATUS_ALL_IN:
                return self.players.index(player)
            
        # if everyone is all in or folded, return the next all in player
        # this means everyone is either all in or folded, so we need to find the next all in player.
        # the game will handle this scenario outside this function.
        for player in remaining_players:
            if player.status == PLAYER_STATUS_ALL_IN:
                return self.players.index(player)
        raise ValueError("No active players found after the current position.")

    def map_position_to_position_name(self, position):
        """Map position index to position name."""
        position_names = {
            POSITION_SMALL_BLIND: "Small Blind",
            POSITION_BIG_BLIND: "Big Blind",
            POSITION_UNDER_THE_GUN: "UTG",
            POSITION_UNDER_THE_GUN_PLUS_ONE: "UTG+1",
            POSITION_MIDDLE_POSITION: "MP",
            POSITION_LOWJACK: "LJ",
            POSITION_HIGHJACK: "HJ",
            POSITION_CUT_OFF: "CO",
            POSITION_BUTTON: "Button"
        }
        return position_names.get(position, "Unknown Position")

    def betting_round(self):
        """Conduct a betting round."""
        if DEBUG:
            print(f"\n\n\n###########################################")
            print(f"Starting betting round for phase: {self.phase}")
            for player in self.players:
                index_of_player = self.players.index(player)
                print(f"{player.name} - Position: {self.map_position_to_position_name(index_of_player)} Stack: {player.stack}, Status: {player.status}, Hand: {player.hand}")
        
        """Run a betting round."""
        # iniitialize starting position. if phase is preflop, set the first player to act as the UTG player.
        # if the phase is not fre flop, set the first player to act as the first player to come after the dealer.
        if self.phase == PHASE_PRE_FLOP:
            self.table_position = self.calculate_preflop_starting_position()
        else:
            self.table_position = self.calculate_non_preflop_starting_position()
            self.current_bet = 0  # Reset current bet for the new betting round
        self.actions = []  # Reset actions for the current phase

        
        while True:

            print("\n")
            current_player = self.players[self.table_position]
            print(f"Current player: {current_player.name}, Position: {self.map_position_to_position_name(self.table_position)}")
            # Check if current player is all-in
            if current_player.status == PLAYER_STATUS_ALL_IN:
                if self.betting_round_should_end():
                    break
                # Skip the player if they are all-in
                self.table_position = self.calculate_next_position(self.table_position)
                continue

            if current_player.status != PLAYER_STATUS_FOLDED:
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

            if self.betting_round_should_end():
                print(f"Betting round ended. Current player: {current_player.name}, Status: {current_player.status}")
                break

            self.table_position = self.calculate_next_position(self.table_position)
            print(f"Next player: {self.players[self.table_position].name}, Position: {self.map_position_to_position_name(self.table_position)}")

        print(f"End of betting round. Pot is now {self.pot}.")
        # reset non folded players' status to waiting
        self.reset_non_all_in_players_and_folded_players_status()

    def reset_non_all_in_players_and_folded_players_status(self):
        for player in self.players:
            if player.status != PLAYER_STATUS_ALL_IN and player.status != PLAYER_STATUS_FOLDED:
                player.status = PLAYER_STATUS_WAITING

    def betting_round_should_end(self)-> bool:

        # check if any player has a waiting status
        waiting_player_statuses = [p.status for p in self.players if p.status == PLAYER_STATUS_WAITING]
        if len(waiting_player_statuses) != 0:
            return False

        # check if all players have checked or folded
        active_player_statuses = [p.status for p in self.players if p.status != PLAYER_STATUS_FOLDED]
        if len(set(active_player_statuses)) == 1 and active_player_statuses[0] in [PLAYER_STATUS_CHECKED, PLAYER_STATUS_FOLDED]:
            return True
        
        active_player_current_bets = [p.current_bet for p in self.players if p.status != PLAYER_STATUS_FOLDED]
        # check if all players have the same current bet
        if len(set(active_player_current_bets)) == 1:
            return True
        
        # check if all players have folded or are all in
        all_in_and_folded_statuses = [p.status for p in self.players if p.status in [PLAYER_STATUS_ALL_IN, PLAYER_STATUS_FOLDED]]
        if len(all_in_and_folded_statuses) == len(self.players):
            return True       

        return False

    def reset_game_for_new_hand(self):
        """Reset the game state for a new round."""
        self.pot = 0
        self.current_bet = 0
        self.community_cards = []
        for player in self.players:
            player.reset_player_for_new_hand()
        self.phase = PHASE_PRE_FLOP  # Reset phase to pre-flop

        #remove all players with a stack of 0 from the game
        self.players = [p for p in self.players if p.stack > 0]

        # ensure there are at least 2 players left in the game
        if len(self.players) < 2:
            return False

        # things to do after first hand
        if self.hand_number != 0:
            self.rotate_player_positions_on_table()
            self.deck.reset_cards()  # Shuffle the deck for the next hand

        # initialize the sb / bb
        self.players[POSITION_SMALL_BLIND].place_bet(1)
        self.players[POSITION_BIG_BLIND].place_bet(2)
        self.pot = 3  # Add the blinds to the pot
        self.current_bet = 2  # Set the current bet to the big blind amount

        self.hand_number += 1  # Increment the hand number
        return True

    def determine_winner(self):
        rules = PokerRules()
        player_and_current_best_hand = {
            'player': None,
            'best_hand': WorstPokerHand(),
            'tied_hands': []
        }

        # get all active players who have not folded
        active_players = [p for p in self.players if p.status != "folded"]
        if len(active_players) == 1:
            # If only one player remains, they win the pot
            winner = active_players[0]
            print(f"{winner.name} wins the pot of {self.pot} as everyone else folded!")
            winner.stack += self.pot
            return GAME_SHOULD_CONTINUE

        for player in active_players:
            # get player's cards and all community cards in a list
            all_cards = player.hand + self.community_cards
            # get all possible 5 card combinations combinations from the player's hand and community cards
            from itertools import combinations
            all_combinations = list(combinations(all_cards, 5))
            # get the best hand from all combinations
            best_hand = rules.get_best_hand(all_combinations)

            # check if hand is equal to current best hand
            if best_hand == player_and_current_best_hand['best_hand']:
                player_and_current_best_hand['tied_hands'].append(player)

            if best_hand > player_and_current_best_hand['best_hand']:
                player_and_current_best_hand['best_hand'] = best_hand
                player_and_current_best_hand['player'] = player
                player_and_current_best_hand['tied_hands'] = [] # reset tied hands
        
        # There is a tie
        if len(player_and_current_best_hand['tied_hands']) > 0:
            # If there are tied hands, split the pot among the winners
            print(f"It's a tie between {', '.join([p.name for p in player_and_current_best_hand['tied_hands']])} with {player_and_current_best_hand['best_hand']}!")
            split_pot = self.pot // len(player_and_current_best_hand['tied_hands'])
            for player in player_and_current_best_hand['tied_hands']:
                player.stack += split_pot
            return GAME_SHOULD_CONTINUE
        
        # If there is a winner, give them the pot
        print(f"{player_and_current_best_hand['player']} wins with {player_and_current_best_hand['best_hand']}!")
        player_and_current_best_hand['player'].stack += self.pot
        return GAME_SHOULD_CONTINUE

    def add_community_card(self):
        """Add a card to the community cards."""
        self.community_cards.append(self.deck.draw())

    def advance_phase(self):
        """Advance to the next phase of the game."""
        if self.phase == PHASE_PRE_FLOP:
            self.phase = PHASE_FLOP
            for _ in range(3):  # Deal the flop
                self.add_community_card()
        elif self.phase == PHASE_FLOP:
            self.phase = PHASE_TURN
            self.add_community_card()
        elif self.phase == PHASE_TURN:
            self.phase = PHASE_RIVER
            self.add_community_card()
        elif self.phase == PHASE_RIVER:
            self.phase = PHASE_SHOWDOWN

    def run_hand(self):
        """Run the game. Will return False if the game is over."""
        if not self.reset_game_for_new_hand():
            print("Game over! Not enough players to continue.")
            return False
        self.deal_hands()
        while self.phase != PHASE_SHOWDOWN:
            self.betting_round()
            if self.phase != PHASE_SHOWDOWN:
                self.advance_phase()
        print("Hand is over.")
        return self.determine_winner()

    def run_game(self):
        """Run the game until completion."""
        while True:
            print(f"\n\n\n###########################################")
            print(f"Starting hand number {self.hand_number}")
            if self.hand_number > 3:
                print("Max Hands Reached!")
                break
            if self.run_hand() is not GAME_SHOULD_CONTINUE:
                print("Someone won the game!")
                break

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

    def __str__(self):
        return f"PokerGameStateSnapshot(pot={self.pot}, current_bet={self.current_bet}, phase={self.phase}, players={self.players}, community_cards={self.community_cards}, actions={self.actions}, current_player={self.current_player})"
