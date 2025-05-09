CARD_RANK_NAME_A = 'A'
CARD_RANK_NAME_K = 'K'
CARD_RANK_NAME_Q = 'Q'
CARD_RANK_NAME_J = 'J'
CARD_RANK_NAME_10 = '10'
CARD_RANK_NAME_9 = '9'
CARD_RANK_NAME_8 = '8'
CARD_RANK_NAME_7 = '7'
CARD_RANK_NAME_6 = '6'
CARD_RANK_NAME_5 = '5'
CARD_RANK_NAME_4 = '4'
CARD_RANK_NAME_3 = '3'
CARD_RANK_NAME_2 = '2'

CARD_RANK_VALUE_A = 14
CARD_RANK_VALUE_K = 13
CARD_RANK_VALUE_Q = 12
CARD_RANK_VALUE_J = 11
CARD_RANK_VALUE_10 = 10
CARD_RANK_VALUE_9 = 9
CARD_RANK_VALUE_8 = 8
CARD_RANK_VALUE_7 = 7
CARD_RANK_VALUE_6 = 6
CARD_RANK_VALUE_5 = 5
CARD_RANK_VALUE_4 = 4
CARD_RANK_VALUE_3 = 3
CARD_RANK_VALUE_2 = 2

SUIT_HEARTS = 'Hearts'
SUIT_DIAMONDS = 'Diamonds'
SUIT_CLUBS = 'Clubs'
SUIT_SPADES = 'Spades'

ROYAL_FLUSH = "Royal Flush"
STRAIGHT_FLUSH = "Straight Flush"
FOUR_OF_A_KIND = "Four of a Kind"
FULL_HOUSE = "Full House"
FLUSH = "Flush"
STRAIGHT = "Straight"
THREE_OF_A_KIND = "Three of a Kind"
TWO_PAIR = "Two Pair"
ONE_PAIR = "One Pair"
HIGH_CARD = "High Card"

FIRST_KICKER_WINS = 1
SECOND_KICKER_WINS = -1
KICKERS_TIE = 0

class PokerException(Exception):
    pass

class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        return f"{self.rank} of {self.suit}"
    
    def __repr__(self):
        return f"Card({self.rank}, {self.suit})"
    
    def __eq__(self, other):
        if isinstance(other, Card):
            return self.rank == other.rank and self.suit == other.suit
        return False
    
    def __lt__(self, other):
        if isinstance(other, Card):
            return self.get_card_rank_value(self.rank) < self.get_card_rank_value(other.rank)
        return NotImplemented
    
    def __gt__(self, other):
        if isinstance(other, Card):
            return self.get_card_rank_value(self.rank) > self.get_card_rank_value(other.rank)
        return NotImplemented
    
    def get_card_rank_value(self, rank):
        return {
            CARD_RANK_NAME_A: CARD_RANK_VALUE_A,
            CARD_RANK_NAME_K: CARD_RANK_VALUE_K,
            CARD_RANK_NAME_Q: CARD_RANK_VALUE_Q,
            CARD_RANK_NAME_J: CARD_RANK_VALUE_J,
            CARD_RANK_NAME_10: CARD_RANK_VALUE_10,
            CARD_RANK_NAME_9: CARD_RANK_VALUE_9,
            CARD_RANK_NAME_8: CARD_RANK_VALUE_8,
            CARD_RANK_NAME_7: CARD_RANK_VALUE_7,
            CARD_RANK_NAME_6: CARD_RANK_VALUE_6,
            CARD_RANK_NAME_5: CARD_RANK_VALUE_5,
            CARD_RANK_NAME_4: CARD_RANK_VALUE_4,
            CARD_RANK_NAME_3: CARD_RANK_VALUE_3,
            CARD_RANK_NAME_2: CARD_RANK_VALUE_2
        }.get(rank, 0)

class Deck:
    def __init__(self):
        self.cards = [Card(rank, suit) for suit in [SUIT_HEARTS, SUIT_DIAMONDS, SUIT_CLUBS, SUIT_SPADES]
                      for rank in [CARD_RANK_NAME_A, CARD_RANK_NAME_K, CARD_RANK_NAME_Q, CARD_RANK_NAME_J,]    
                      ]
        self.shuffle()

    def shuffle(self):
        import random
        random.shuffle(self.cards)

    def draw(self):
        return self.cards.pop() if self.cards else None

class Hand:
    def __init__(self, cards):
        self.cards = cards
        if len(cards) != 5:
            raise PokerException("Hand must contain exactly 5 cards")

    def evaluate_kickers(self, kickers1, kickers2):
        #convert kickers to their values using the get_card_rank_value method of the Card class
        kickers1_values = [card.get_card_rank_value(card.rank) for card in kickers1]
        kickers2_values = [card.get_card_rank_value(card.rank) for card in kickers2]

        #compare the kickers
        for k1, k2 in zip(kickers1_values, kickers2_values):
            if k1 > k2:
                return FIRST_KICKER_WINS
            elif k1 < k2:
                return SECOND_KICKER_WINS
        return KICKERS_TIE

class WorstPokerHand(Hand):
    def __init__(self):
        super().__init__([
            Card(CARD_RANK_NAME_2, SUIT_HEARTS),
            Card(CARD_RANK_NAME_3, SUIT_DIAMONDS),
            Card(CARD_RANK_NAME_4, SUIT_CLUBS),
            Card(CARD_RANK_NAME_5, SUIT_SPADES),
            Card(CARD_RANK_NAME_7, SUIT_HEARTS)
        ])

    def __gt__(self, other):
        if isinstance(other, Hand):
            return False
        return NotImplemented

class RoyalFlush(Hand):
    def __init__(self, cards: list[Card]):
        super().__init__(cards)
        try:
            straight_flush = StraightFlush(cards)
            if straight_flush.highest_straight_flush_card_rank == CARD_RANK_NAME_A:
                return
            else:
                raise PokerException("Invalid Royal Flush")
        except Exception as e:
            raise PokerException("Invalid Royal Flush") from e

    def __gt__(self, other):
        if isinstance(other, Hand):
            return True
        return NotImplemented

class StraightFlush(Hand):
    def __init__(self, cards: list[Card]):
        super().__init__(cards)
        try:
            straight = Straight(cards)
            if straight:
                flush = Flush(cards)
                if flush:
                    self.highest_straight_flush_card_rank = straight.highest_straight_card_rank
                    return
        except Exception as e:
            raise PokerException("Invalid Straight Flush") from e

    def __gt__(self, other):
        if isinstance(other, Hand):
            if isinstance(other, RoyalFlush):
                return False
            if isinstance(other, StraightFlush):
                return self.highest_straight_flush_card > other.highest_straight_flush_card
            return True
        return NotImplemented

class FourOfAKind(Hand):
    def __init__(self, cards: list[Card]):
        super().__init__(cards)

        for card in cards:
            ranks = [c.rank for c in cards]
            if ranks.count(card.rank) == 4:
                self.rank = card
                self.kicker = [c for c in cards if c.rank != card.rank][0]
                return
        raise PokerException("Invalid Four of a Kind")

    def __gt__(self, other):
        if isinstance(other, Hand):
            if isinstance(other, RoyalFlush):
                return False
            if isinstance(other, StraightFlush):
                return False
            if isinstance(other, FourOfAKind):
                return self.rank > other.rank
            return True
        return NotImplemented
    
class FullHouse(Hand):
    def __init__(self, cards: list[Card]):
        super().__init__(cards)
        self.three_of_a_kind_rank = None
        self.pair_rank = None
        for card in cards:
            ranks = [c.rank for c in cards]
            if ranks.count(card.rank) == 3:
                self.three_of_a_kind_rank = card
            elif ranks.count(card.rank) == 2:
                self.pair_rank = card
        if self.three_of_a_kind_rank and self.pair_rank:
            return
        raise PokerException("Invalid Full House")

    def __gt__(self, other):
        if isinstance(other, Hand):
            if isinstance(other, RoyalFlush):
                return False
            if isinstance(other, StraightFlush):
                return False
            if isinstance(other, FourOfAKind):
                return False
            if isinstance(other, FullHouse):
                if self.three_of_a_kind_rank > other.three_of_a_kind_rank:
                    return True
                elif self.three_of_a_kind_rank == other.three_of_a_kind_rank:
                    return self.pair_rank > other.pair_rank
                else:
                    return False
            return True
        return NotImplemented
    
class Flush(Hand):
    def __init__(self, cards: list[Card]):
        super().__init__(cards)
        suits = [card.suit for card in cards]
        if len(set(suits)) == 1:
            return
        else:
            raise PokerException("Invalid Flush")

    def __gt__(self, other):
        if isinstance(other, Hand):
            if isinstance(other, RoyalFlush):
                return False
            if isinstance(other, StraightFlush):
                return False
            if isinstance(other, FourOfAKind):
                return False
            if isinstance(other, FullHouse):
                return False
            if isinstance(other, Flush):
                result = self.evaluate_kickers(self.cards, other.cards)
                if result == FIRST_KICKER_WINS:
                    return True
                elif result == SECOND_KICKER_WINS:
                    return False
                else:
                    Exception("something went wrong")
            return True
        return NotImplemented

class Straight(Hand):
    def __init__(self, cards: list[Card]):
        super().__init__(cards)
        ranks = sorted([card.get_card_rank_value(card.rank) for card in cards])
        if len(ranks) != 5:
            raise PokerException("Invalid Straight")
        if ranks == list(range(ranks[0], ranks[0] + 5)):
            highest_card = max(cards, key=lambda card: card.get_card_rank_value(card.rank))
            self.highest_straight_card_rank = highest_card.rank
            return
        # check for the special case of A, 2, 3, 4, 5
        if ranks == [2, 3, 4, 5, 14]:
            self.highest_straight_card_rank = CARD_RANK_NAME_5
            return
        raise PokerException("Invalid Straight")
    
    def __gt__(self, other):
        if isinstance(other, Hand):
            if isinstance(other, RoyalFlush):
                return False
            if isinstance(other, StraightFlush):
                return False
            if isinstance(other, FourOfAKind):
                return False
            if isinstance(other, FullHouse):
                return False
            if isinstance(other, Flush):
                return False
            if isinstance(other, Straight):
                if self.highest_straight_card_rank > other.highest_straight_card_rank:
                    return True
                else:
                    return False
            return True
        return NotImplemented
    
class ThreeOfAKind(Hand):
    def __init__(self, cards: list[Card]):
        super().__init__(cards)
        ranks = [card.rank for card in cards]
        for rank in ranks:
            if ranks.count(rank) == 3:
                self.rank = rank
                self.kickers = [card for card in cards if card.rank != rank]
                return
        raise PokerException("Invalid Three of a Kind")
    
    def __gt__(self, other):
        if isinstance(other, Hand):
            if isinstance(other, RoyalFlush):
                return False
            if isinstance(other, StraightFlush):
                return False
            if isinstance(other, FourOfAKind):
                return False
            if isinstance(other, FullHouse):
                return False
            if isinstance(other, Flush):
                return False
            if isinstance(other, Straight):
                return False
            if isinstance(other, ThreeOfAKind):
                if self.rank < other.rank:
                    return False
                elif self.rank == other.rank:
                    result = self.evaluate_kickers(self.kickers, other.kickers)
                    if result == FIRST_KICKER_WINS:
                        return True
                    elif result == SECOND_KICKER_WINS:
                        return False
                    else:
                        # @Todo: need to implement kicker tie breaker
                        raise Exception("Kickers tied")
            return True
        return NotImplemented

class TwoPair(Hand):
    def __init__(self, cards: list[Card]):
        super().__init__(cards)
        ranks = [card.rank for card in cards]
        first_pair_rank = None
        second_pair_rank = None
        for rank in ranks:
            if ranks.count(rank) == 2:
                if first_pair_rank is None:
                    first_pair_rank = rank
                elif second_pair_rank is None and rank != first_pair_rank:
                    second_pair_rank = rank
        if first_pair_rank and second_pair_rank:
            self.first_pair_rank = first_pair_rank
            self.second_pair_rank = second_pair_rank
            self.kicker = [card for card in cards if card.rank != first_pair_rank and card.rank != second_pair_rank][0]
            return
        raise PokerException("Invalid Two Pair")
    
    def __gt__(self, other):
        if isinstance(other, Hand):
            if isinstance(other, RoyalFlush):
                return False
            if isinstance(other, StraightFlush):
                return False
            if isinstance(other, FourOfAKind):
                return False
            if isinstance(other, FullHouse):
                return False
            if isinstance(other, Flush):
                return False
            if isinstance(other, Straight):
                return False
            if isinstance(other, ThreeOfAKind):
                return False
            if isinstance(other, TwoPair):
                if self.first_pair_rank > other.first_pair_rank:
                    return True
                elif self.first_pair_rank == other.first_pair_rank:
                    if self.second_pair_rank < other.second_pair_rank:
                        return False
                    elif self.second_pair_rank == other.second_pair_rank:
                        result = self.evaluate_kickers([self.kicker], [other.kicker])
                        if result == FIRST_KICKER_WINS:
                            return True
                        elif result == SECOND_KICKER_WINS:
                            return False
                        else:
                            raise Exception("Kickers tied")
            return True
        return NotImplemented

class OnePair(Hand):
    def __init__(self, cards: list[Card]):
        super().__init__(cards)
        ranks = [card.rank for card in cards]
        for rank in ranks:
            if ranks.count(rank) == 2:
                self.rank = rank
                self.kickers = [card for card in cards if card.rank != rank]
                return
        raise PokerException("Invalid One Pair")

    def __gt__(self, other):
        if isinstance(other, Hand):
            if isinstance(other, RoyalFlush):
                return False
            if isinstance(other, StraightFlush):
                return False
            if isinstance(other, FourOfAKind):
                return False
            if isinstance(other, FullHouse):
                return False
            if isinstance(other, Flush):
                return False
            if isinstance(other, Straight):
                return False
            if isinstance(other, ThreeOfAKind):
                return False
            if isinstance(other, TwoPair):
                return False
            if isinstance(other, OnePair):
                if self.rank < other.rank:
                    return False
                elif self.rank == other.rank:
                    result = self.evaluate_kickers(self.kickers, other.kickers)
                    if result == FIRST_KICKER_WINS:
                        return True
                    elif result == SECOND_KICKER_WINS:
                        return False
                    else:
                        raise Exception("Kickers tied")
            return True
        return NotImplemented

class HighCard(Hand):
    def __init__(self, cards: list[Card]):
        super().__init__(cards)
        #use the get_card_rank_value method to get the rank value of the cards
        self.highest_card = max(cards, key=lambda card: card.get_card_rank_value(card.rank))

    def __gt__(self, other):
        if isinstance(other, Hand):
            if isinstance(other, RoyalFlush):
                return False
            if isinstance(other, StraightFlush):
                return False
            if isinstance(other, FourOfAKind):
                return False
            if isinstance(other, FullHouse):
                return False
            if isinstance(other, Flush):
                return False
            if isinstance(other, Straight):
                return False
            if isinstance(other, ThreeOfAKind):
                return False
            if isinstance(other, TwoPair):
                return False
            if isinstance(other, OnePair):
                return False
            if isinstance(other, HighCard):
                result = self.evaluate_kickers(self.cards ,other.cards)
                if result == FIRST_KICKER_WINS:
                    return True
                elif result == SECOND_KICKER_WINS:
                    return False
                else:
                    raise Exception("Kickers tied")
            return True
        return NotImplemented

class PokerRules:
    def __init__(self):
        pass

    def get_best_hand(self, hands: list[list[Card]]) -> Hand:
        """
        Given a list of hands, return the best hand.
        """
        best_hand = None
        for hand in hands:
            # try to create a hand object
            try:
                current_hand = self.create_hand_object(hand)
                if best_hand is None or current_hand > best_hand:
                    best_hand = current_hand
            except PokerException:
                continue
        return best_hand
    
    def create_hand_object(self, hand: list[Card]) -> Hand:
        """
        Given a hand, return the appropriate hand object.
        """
        try:
            return RoyalFlush(hand)
        except PokerException:
            pass
        try:
            return StraightFlush(hand)
        except PokerException:
            pass
        try:
            return FourOfAKind(hand)
        except PokerException:
            pass
        try:
            return FullHouse(hand)
        except PokerException:
            pass
        try:
            return Flush(hand)
        except PokerException:
            pass
        try:
            return Straight(hand)
        except PokerException:
            pass
        try:
            return ThreeOfAKind(hand)
        except PokerException:
            pass
        try:
            return TwoPair(hand)
        except PokerException:
            pass
        try:
            return OnePair(hand)
        except PokerException:
            pass
        try:
            return HighCard(hand)
        except PokerException:
            raise PokerException("Invalid Hand") from None