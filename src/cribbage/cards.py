#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# -----------
# SPDX-License-Identifier: MIT
# Copyright (c) 2021 Troy Williams

# uuid:   56f0700a-d69d-11eb-87bb-1b4177236484
# author: Troy Williams
# email:  troy.williams@bluebill.net
# date:   2021-06-26
# -----------

"""
A module implement various aspects of the Cribbage objects and scoring system


Cribbage Scoring - <https://en.wikipedia.org/wiki/Rules_of_cribbage>

"""

# ------------
# System Modules - Included with Python

from dataclasses import dataclass

from itertools import (
    chain,
    combinations,
    product,
    groupby,
)

from collections.abc import MutableSequence

# ------------
# 3rd Party - From pip

# ------------
# Custom Modules


# -------------

# Shared tuple that stores the card ranks
RANKS = (
    "A",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "T",
    "J",
    "Q",
    "K",
)

# shared tuple that stores the card suits
SUITS = ("D", "H", "C", "S")

SUIT_SYMBOLS = {
    "C": "♣",  # u'\u2663',
    "D": "♦",  # u'\u2666',
    "H": "♥",  # u'\u2665',
    "S": "♠",  # u'\u2660',
}

RANK_SORT = {
    "A": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "T": 11,
    "J": 12,
    "Q": 13,
    "K": 14,
}

SUIT_SORT = {
    "H": 0,
    "D": 100,
    "S": 200,
    "C": 300,
}


# TODO: Implement the card sort order instead of using the grouping

CARD_SYMBOLS = {
    # Spades
    "AS": "🂡",  # "\U0001F0A1" - Ace of Spades
    "2S": "🂢",  # "\U0001F0A2" - Two of Spades
    "3S": "🂣",  # "\U0001F0A3" - Three of Spades
    "4S": "🂤",  # "\U0001F0A4" - Four of Spades
    "5S": "🂥",  # "\U0001F0A5" - Five of Spades
    "6S": "🂦",  # "\U0001F0A6" - Six of Spades
    "7S": "🂧",  # "\U0001F0A7" - Seven of Spades
    "8S": "🂨",  # "\U0001F0A8" - Eight of Spades
    "9S": "🂩",  # "\U0001F0A9" - Nine of Spades
    "TS": "🂪",  # "\U0001F0AA" - Ten of Spades
    "JS": "🂫",  # "\U0001F0AB" - Jack of Spades
    "QS": "🂭",  # "\U0001F0AD" - Queen of Spades
    "KS": "🂮",  # "\U0001F0AE" - King of Spades
    # Hearts
    "AH": "🂱",  # "\U0001F0B1" - Ace of Hearts
    "2H": "🂲",  # "\U0001F0B2" - Two of Hearts
    "3H": "🂳",  # "\U0001F0B3" - Three of Hearts
    "4H": "🂴",  # "\U0001F0B4" - Four of Hearts
    "5H": "🂵",  # "\U0001F0B5" - Five of Hearts
    "6H": "🂶",  # "\U0001F0B6" - Six of Hearts
    "7H": "🂷",  # "\U0001F0B7" - Seven of Hearts
    "8H": "🂸",  # "\U0001F0B8" - Eight of Hearts
    "9H": "🂹",  # "\U0001F0B9" - Nine of Hearts
    "TH": "🂺",  # "\U0001F0BA" - Ten of Hearts
    "JH": "🂻",  # "\U0001F0BB" - Jack of Hearts
    "QH": "🂽",  # "\U0001F0BD" - Queen of Hearts
    "KH": "🂾",  # "\U0001F0BE" - King of Hearts
    # Diamonds
    "AD": "🃁",  # "\U0001F0C1" - Ace of Diamonds
    "2D": "🃂",  # "\U0001F0C2" - Two of Diamonds
    "3D": "🃃",  # "\U0001F0C3" - Three of Diamonds
    "4D": "🃄",  # "\U0001F0C4" - Four of Diamonds
    "5D": "🃅",  # "\U0001F0C5" - Five of Diamonds
    "6D": "🃆",  # "\U0001F0C6" - Six of Diamonds
    "7D": "🃇",  # "\U0001F0C7" - Seven of Diamonds
    "8D": "🃈",  # "\U0001F0C8" - Eight of Diamonds
    "9D": "🃉",  # "\U0001F0C9" - Nine of Diamonds
    "TD": "🃊",  # "\U0001F0CA" - Ten of Diamonds
    "JD": "🃋",  # "\U0001F0CB" - Jack of Diamonds
    "QD": "🃍",  # "\U0001F0CD" - Queen of Diamonds
    "KD": "🃎",  # "\U0001F0CE" - King of Diamonds
    # Clubs
    "AC": "🃑",  # "\U0001F0D1" - Ace of Clubs
    "2C": "🃒",  # "\U0001F0D2" - Two of Clubs
    "3C": "🃓",  # "\U0001F0D3" - Three of Clubs
    "4C": "🃔",  # "\U0001F0D4" - Four of Clubs
    "5C": "🃕",  # "\U0001F0D5" - Five of Clubs
    "6C": "🃖",  # "\U0001F0D6" - Six of Clubs
    "7C": "🃗",  # "\U0001F0D7" - Seven of Clubs
    "8C": "🃘",  # "\U0001F0D8" - Eight of Clubs
    "9C": "🃙",  # "\U0001F0D9" - Nine of Clubs
    "TC": "🃚",  # "\U0001F0DA" - Ten of Clubs
    "JC": "🃛",  # "\U0001F0DB" - Jack of Clubs
    "QC": "🃝",  # "\U0001F0DD" - Queen of Clubs
    "KC": "🃞",  # "\U0001F0DE" - King of Clubs
}

# # set the cards sorting order - useful for sorting a list of cards.
# rank_sort_order_map = {
#     'A': 1,
#     '2': 2,
#     '3': 3,
#     '4': 4,
#     '5': 5,
#     '6': 6,
#     '7': 7,
#     '8': 8,
#     '9': 9,
#     'T': 10,
#     'J': 11,
#     'Q': 12,
#     'K': 13,
# }


@dataclass(frozen=True)
class Card:
    """
    The Card class represents a playing card with a value rank and suit.
    The rank is a string and can be one of:

    - A - Ace
    - 2
    - 3
    - 4
    - 5
    - 6
    - 7
    - 8
    - 9
    - T - Ten
    - J - Jack
    - Q - Queen
    - K - King

    The suit is a string and can be one of:
    - D - Diamond
    - H - Heart
    - C - Club
    - S - Spade

    # NOTE

    If you have a string representing the card ('6D') you can use this
    fact, that a string is an iterable and you can unpack:

    rank = '6D'
    r, s = rank.upper()

    or

    Card(*rank)

    """

    rank: str = None
    suit: str = None

    def __post_init__(self):
        """
        This method is called after the __init__ is finished. Normally
        this is used for validation for dataclass objects
        """

        if self.rank is None:
            raise ValueError("Card.rank is not set!")

        if self.suit is None:
            raise ValueError("Card.suit is not set!")

        # We only want upper case values for the rank and suit and we
        # have to use this call because the class is frozen
        object.__setattr__(self, "rank", self.rank.upper())
        object.__setattr__(self, "suit", self.suit.upper())

        if self.rank not in RANKS:
            raise ValueError(f"INVALID Rank ({self.rank})! Must be one of: {RANKS}!")

        if self.suit not in SUITS:
            raise ValueError(f"INVALID Suit ({self.suit})! Must be one of: {SUITS}!")

    def value(self) -> int:
        """
        Given a card, return the face value it is worth in a cribbage game.

        - A = 1
        - 2 = 2
        - 3 = 3
        - 4 = 4
        - 5 = 5
        - 6 = 6
        - 7 = 7
        - 8 = 8
        - 9 = 9
        - T = 10
        - J = 10
        - Q = 10
        - K = 10

        # Return

        An integer representing the point value of the card

        """

        if self.rank == "A":
            return 1

        elif self.rank in ("T", "J", "Q", "K"):
            return 10

        else:
            return int(self.rank)

    def cool_display(self, display_card=False) -> str:
        """

        By default, display a card, 2H like this:
        2♥.

        If the display_card option is True, it will display like this:

        🂲

        """

        if display_card:

            return CARD_SYMBOLS[self.rank + self.suit]

        else:

            return self.rank + SUIT_SYMBOLS[self.suit]

    def __add__(self, other):
        """
        By implementing this we can add the value of cards together
        using c1 + c2 instead of c1.value() + c2.value()
        """

        if isinstance(other, Card):
            return self.value() + other.value()

        return self.value() + other

    def __radd__(self, other):
        """

        A + B

        This is called if the left object, A doesn't have an __add__
        defined or it doesn't know how to handle addition to B.
        """

        return self.value() + other

    def __lt__(self, other):
        """
        Make the item sortable by rank

        This will sort by suit, then rank effectively grouping cards
        that are the same suit together.

        If you need something different, use the key function on the
        sorted method for a list of cards:

        sorted(hand, key=lambda x: RANK_SORT[x.rank]))

        """

        return (SUIT_SORT[self.suit], RANK_SORT[self.rank]) < (
            SUIT_SORT[other.suit],
            RANK_SORT[other.rank],
        )

    def __str__(self):
        """

        Return a string representation of the card.

        """

        return self.rank + self.suit


def make_deck():
    """
    Creates a deck of 52 cards.

    # Parameters

    # Return

    Returns a list of cards containing 52 - all of the suits and ranks.

    """

    return [Card(*p) for p in product(RANKS, SUITS)]


# class Hand(MutableSequence):
#     """
#     A hand is a simple container for a number of cards.


#     https://docs.python.org/3/reference/datamodel.html
#     https://docs.python.org/3/library/collections.abc.html
#     https://treyhunner.com/2019/04/why-you-shouldnt-inherit-from-list-and-dict-in-python/

#     """

#     def __init__(self, *args):

#         if len(args) > 0:
#             if len(set(*args)) != len(*args):
#                 raise ValueError('Duplicate cards are not allowed!')

#         self.values = list(*args)

#         # list.__init__(self, *args)

#     def __getitem__(self, key):
#         return self.values[key]

#     def __setitem__(self, key, value):
#         self.values[key] = value

#     def __delitem__(self, key):
#         del self.values[key]

#     def __len__(self):
#         return len(self.values)

#     def __eq__(self, other):
#         return self.values == other

#     def __str__(self):
#         return self.values.__str__()

#     def __repr__(self):
#         return self.values.__repr__()

#     def insert(self, key, value):
#         self.insert(key, value)

#     def display(self):
#         """

#         Return a list of strings representing the cards in the hand.

#         [AD, 1D, 3S, 4C]

#         """

#         return [str(c) for c in self]

#     def cool_display(self):
#         """
#         Return a list of strings representing the cards in the hand
#         using unicode characters to represent the suits.

#         [A♦, 1♦, 3♠, 4♣]
#         """
#         return [c.cool_display() for c in self]

#     def value(self):
#         """

#         Return the total value of the hand summing each individual card
#         value.

#         # NOTE

#         If the hand is empty, by default the sum function returns 0.

#         """

#         return sum([c.value() for c in self])

#     def sort(self, key=None, reverse=False):
#         """
#         Return a new Hand list in sorted order.

#         The new order will account for the rank of the card.

#         Given:

#         [AD, 4D, 6S, 4C]

#         Returns:

#         [AD, 4C, 4D, 6S]

#         # NOTE

#         It may be more preferable to sort from lowest to highest and
#         group-by suit. That is make sure that all diamonds are
#         consecutive.

#         """

#         self.values.sort(key=key, reverse=reverse)

#     def every_combination(self, **kwargs):
#         """

#         Iterate through every combination of cards from 0 to len
#         (self) yielding the result as it is created.

#         This is a generator method. It will iterate through all the single
#         cards, than pairs than triples etc.

#         Optionally, you can specify a `count` and limit the return
#         values to hands of that length. For example if count=2, then
#         all 2 card combinations are returned.

#         # Parameters (kwargs)

#         count:int
#             - The number of cards to take.

#         # Return

#         A Hand containing the cards in the combination.

#         """

#         if 'count' in kwargs:
#             # From this hand, generate a list of all hands of length
#             # count

#             # If count = 2 and m = [x,y,z,w]

#             # >>>from itertools import combinations
#             # >>> m = ['x', 'y', 'z', 'w']
#             # >>> [c for c in combinations(m,2)]
#             # [('x', 'y'), ('x', 'z'), ('x', 'w'),
#             #  ('y', 'z'), ('y', 'w'), ('z', 'w')]

#             for combo in combinations(self, kwargs['count']):
#                 yield Hand(combo)

#         else:

#             # Generate all possible combinations of Hands from 0 to n

#             # if the hand count is 4, it will generate 16 hands.

#             # >>> from itertools import chain
#             # >>> from itertools import combinations
#             # >>> m = ['x', 'y', 'z', 'w']
#             # >>> [r for r in range(len(m) + 1)]
#             # [0, 1, 2, 3, 4]
#             # >>> [c for c in chain.from_iterable(
#             #   combinations(m, r) for r in range(len(m) + 1))]
#             # [(), ('x',), ('y',), ('z',), ('w',), ('x', 'y'),
#             #  ('x', 'z'), ('x', 'w'), ('y', 'z'), ('y', 'w'), ('z', 'w'),
#             #  ('x', 'y', 'z'), ('x', 'y', 'w'), ('x', 'z', 'w'),
#             #  ('y', 'z', 'w'), ('x', 'y', 'z', 'w')]

#             for combo in chain.from_iterable(
#                 combinations(self, r) for r in range(len(self) + 1)
#             ):
#                 yield Hand(combo)


# def hand_duplicates(hand):
#     """
#     """

#     if len(set(hand)) != len(hand):
#         raise ValueError('Duplicate cards are not allowed!')


def display_hand(hand, cool=False, super_cool=False):
    """
    Given a list of Cards, return a list of strings representing the
    rank and suit of each card.

    # Parameters

    hand:list(Card)
        - The list of cards to convert to a string representation

    cool:bool
        - If this option is turned on, the suit will be converted to a
          unicode representation displaying 'AH' as 'A♥'.
        - DEFAULT - False

    super_cool:bool
        - if this option is set, will display the 'AS' as 🂱
        - DEFAULT - False

    # Return

    A list of strings representing the cards.


    """

    if cool:
        return [card.cool_display(display_card=super_cool) for card in hand]

    else:
        return [str(card) for card in hand]


def count_hand(hand):
    """

    Given the list of cards, return the total count based on the face
    value of the cards.

    # Parameters

    hand:list(Card)
        - The list of cards to convert to a string representation

    # Return

    An integer representing the total face value of the cards in the
    hand.

    # NOTE

    If the hand is empty, by default the sum function returns 0.

    """

    return sum([card.value() for card in hand])


def hand_combinations(hand, combination_length=None):
    """
    Given a hand, iterate through every combination of that hand at
    every hand length from 0, to the number of cards within the hand.

    >>> from itertools import chain
    >>> from itertools import combinations
    >>> m = ['x', 'y', 'z', 'w']
    >>> [r for r in range(len(m) + 1)]
    [0, 1, 2, 3, 4]
    >>> [c for c in chain.from_iterable(
      combinations(m, r) for r in range(len(m) + 1))]
    [(), ('x',), ('y',), ('z',), ('w',), ('x', 'y'),
     ('x', 'z'), ('x', 'w'), ('y', 'z'), ('y', 'w'), ('z', 'w'),
     ('x', 'y', 'z'), ('x', 'y', 'w'), ('x', 'z', 'w'),
     ('y', 'z', 'w'), ('x', 'y', 'z', 'w')]


    Iterate through every combination of cards from 0 to len
    (self) yielding the result as it is created.

    This is a generator method. It will iterate through all the single
    cards, than pairs than triples etc.

    Optionally, you can specify a `count` and limit the return
    values to hands of that length. For example if count=2, then
    all 2 card combinations are returned.

    # Parameters (kwargs)

    count:int
        - The number of cards to take.

    # Return

    A list containing the cards in the combination.

    """

    if combination_length:

        # From this hand, generate a list of all hands of length
        # count

        # If count = 2 and m = [x,y,z,w]

        # >>>from itertools import combinations
        # >>> m = ['x', 'y', 'z', 'w']
        # >>> [c for c in combinations(m,2)]
        # [('x', 'y'), ('x', 'z'), ('x', 'w'),
        #  ('y', 'z'), ('y', 'w'), ('z', 'w')]

        for combo in combinations(hand, combination_length):
            yield combo

    else:
        # Generate all possible combinations of Hands from 0 to n

        # if the hand count is 4, it will generate 16 hands.

        # >>> from itertools import chain
        # >>> from itertools import combinations
        # >>> m = ['x', 'y', 'z', 'w']
        # >>> [r for r in range(len(m) + 1)]
        # [0, 1, 2, 3, 4]
        # >>> [c for c in chain.from_iterable(
        #   combinations(m, r) for r in range(len(m) + 1))]
        # [(), ('x',), ('y',), ('z',), ('w',), ('x', 'y'),
        #  ('x', 'z'), ('x', 'w'), ('y', 'z'), ('y', 'w'), ('z', 'w'),
        #  ('x', 'y', 'z'), ('x', 'y', 'w'), ('x', 'z', 'w'),
        #  ('y', 'z', 'w'), ('x', 'y', 'z', 'w')]

        for combo in chain.from_iterable(
            combinations(hand, r) for r in range(len(hand) + 1)
        ):
            yield combo


# def deal_hand(deck, count):
#     """
#     Deals a hand with `count` cards from the deck. The dealt cards are
#     removed from the deck.

#     # Parameters

#     deck:list[Card]
#         - A list of cards

#     count:int
#         - The number cards to deal to form a hand.


#     # NOTE

#     The cards will be automatically removed from the deck

#     This has to be revised - we don't deal 5 cards to the pone
#     and then 5 cards to the dealer. They are dealt alternating
#     starting with the pones hand, then the dealer, back and forth.

#     May need to implment fisher-yates algorithm
#         - https://emctackett.medium.com/fisher-yates-shuffle-randomly-shuffle-a-list-in-place-30a05b05a9cb

#     """

#     hand = Hand(deck[:count])
#     del deck[:count]

#     return hand


def find_fifteens(hand):
    """

    Given a hand, find all of the combination of cards that sum to 15.

    This is a generator method that will iterate through all of the card
    combinations in the hand for combinations that sum to 15. When a
    combination is found that sums to 15 it is returned and the
    iteration is paused.

    # Parameters

    hand:Hand
        - The list of cards to find combinations that adds to 15.

    # Return

    For each iteration of this method, a Hand containing the combination
    that adds to 15.

    """
    for combo in hand_combinations(hand):
        if count_hand(combo) == 15:
            yield combo


def find_pairs(hand):
    """
    Given a hand, fine all of the combination of cards that are pairs,
    that is, cards that contain matching ranks.

    A generator that will iterate through all of the combinations and
    yield pairs of cards.
    """

    for left, right in hand_combinations(hand, combination_length=2):
        if left.rank == right.rank:
            yield left, right

    # for combo in hand.every_combination(count=2):
    #     if combo[0].rank == combo[1].rank:
    #         yield combo


def find_runs(hand):
    """
    Determine all runs within the Hand.

    A run is at least 3 Cards containing a sequence of incrementing rank
    values. For example:

    [1,2,3]

    [4,5,6]

    [T,J,Q,K]

    This method is a generator that that will find all runs of 3 or more
    Cards yielding the combinations.

    """

    # Iterate through every combination of at least 3 cards or more. We
    # are looking for combinations that have delta values between the
    # ranks of the Card elements in the hand having a value equal to 1.

    # [3,4,5] -> [4 - 3 = 1, 5 - 6 = 1]

    # NOTE: We'll use the chain from iterable though the list of lists, one
    # list of cards at a time

    runs = []  # Store the sets of runs

    for combo in chain.from_iterable(
        combinations(hand, r) for r in range(3, len(hand) + 1)
    ):

        # The groupby method works by using the enumeration and
        # iterating through all the items in the list. It looks for
        # constant distance between the enumeration value and the list
        # item. For example, take the data set below:

        # >>> data = [ 1,  4,5,6, 10, 15,16,17,18, 22, 25,26,27,28]

        # Applying the following groupby setup, we have the following
        # groups created:

        # [(0, 1)]
        # [(1, 4), (2, 5), (3, 6)]
        # [(4, 10)]
        # [(5, 15), (6, 16), (7, 17), (8, 18)]
        # [(9, 22)]
        # [(10, 25), (11, 26), (12, 27), (13, 28)]

        # 1 - 4 = -3, 2 - 5 = -3, 3 - 6 = -3

        # The enumeration value is by definition a monotonic increasing
        # value. If each element in our sequence is one unit greater,
        # we have a constant factor

        # That is what defines the grouping key!

        # We need to sort the combos, by ranks, otherwise the groupby will not work properly
        # NOTE: Runs/Straights are not dependent on suits

        for k, g in groupby(
            enumerate(sorted(combo, key=lambda x: RANK_SORT[x.rank])),
            lambda x: x[0] - RANK_SORT[x[1].rank],
        ):

            values = list(g)

            # We need at least 3 cards to make a run
            if len(values) < 3:
                continue

            cards = [c[1] for c in values]

            # create a set so that membership testing is trivial
            candidate = set(cards)

            # Is this run a subset of an existing run
            if any([candidate.issubset(s) for s in runs]):
                continue

            # Is this run a superset of an existing run
            l = [candidate.issuperset(s) for s in runs]
            if any(l):
                # l will be a list of True/False values indicating if
                # any of the sets in the runs list is a subset of candidate.
                # Add the runs to the list as long as they are not
                # subsets of candidate. This effectively removes the subsets.

                runs = [r for r, t in zip(runs, l) if not t]

            if candidate not in runs:
                runs.append(candidate)

    # Convert the sets to list and sort by rank so we can see the runs
    return [sorted(list(r), key=lambda x: RANK_SORT[x.rank]) for r in runs]


def find_flushes(hand, cut):
    """
    Find the flushes, only 4 card or 5 card flushes allowed

    Return the cards in the hand that form a flush and/or the cut card

    Hand =["2C", "3C", "4C", "8C"], Cut = 'QS'
    returns ("2C", "3C", "4C", "8C")

    Hand = ("2C", "3S", "4C", "8C") Cut = 'TC'
    returns ("2C", "4C", "8C", 'TC')

    # Return

    The list of cards forming a flush, it'll either be 4 or 5 cards.

    # NOTE

    If it is important to understand if the cut card is included, you'll
    have to check to see if it is in the returned list

    """

    assert len(hand) == 4

    # Does the hand contain a flush of 5?
    flush_5 = set([c.suit for c in hand] + [cut.suit])

    if len(flush_5) == 1:
        return hand + [cut]

    # We don't have a 5 card flush, do we have at least 3 cards + the
    # cut card forming a flush?

    for k, g in groupby(
            sorted(hand, key=lambda x: SUIT_SORT[x.suit]),
            lambda x: SUIT_SORT[x.suit],
        ):

        values = list(g)

        if len(values) == 3:

            # Do we have 4 cards with 3 from the hand and the cut card?

            if len(set([c.suit for c in values] + [cut.suit])) == 1:
                # we found enough cards, let's bale, there won't be anything
                # else

                return values + [cut]

        elif len(values) == 4:
            # we have 4 cards, we know the cut card doesn't need to be
            # counted otherwise we would have had a 5 card flush - we
            # are done here

            return values

        else:
            continue

    return []



def find_combinations(hand, cut):
    """
    Given the hand and cut card, find all interesting combinations of
    cards. This includes and dealer specific or cut specific
    combinations.

    We are looking for:

    - 15 - Search for all card combinations (hand and cut card
      combined), with the ranks adding to 15. E.g.: [5, 10], [2,3,10]

    - pairs - Search for all card pairs with matching ranks. That is two
      cards of the same rank e.g. [2D, 2S]

        - NOTE: Triples (2,2,2) and 4 of a kind (2,2,2,2) are simple
          scored by the number of combinations of pairs. A triple has 3
          pairs and would score 6 and a quad would have 6 pairs scoring
          12. This method would list the pairs and score correctly

    - straight/runs - A sequence of 3 or more cards, by rank e.g.
      [4H, 5D, 6S]. Smaller runs from a larger run are not counted. If
      you have [1,2,3,4], you cannot count [1,2,3] or [2,3,4]. If you
      have [2,3,3,4] you have a double run of [2,3,4]

    - flush - At least 4 cards of the same suit.

    - nobs - jack of same suit as starter/cut card

    - nibs - the cut card is a jack

    # Parameters

    hand:Hand
        - The hand we want to score.

    cut:Card
        - The cut card that will be counted along with the hand.

    # Return

    A dictionary containing all card combinations of interest with the
    following keys:
    - 'fifteen' - A list of cards that sum to 15
    - 'pair' - All of the car pair combinations found in the hand
    - 'run' - All of the runs found in the hand
    - 'flush' - All of the flush cards found in the hand
    - 'nobs' - The nobs card found in the hand.
    - 'nibs' - The cut card is a Jack.

    """

    full_hand = Hand(hand + [cut])

    return {
        "fifteen": list(find_fifteens(full_hand)),
        "pair": list(find_pairs(full_hand)),
        "run": list(find_runs(full_hand)),
        "flush": find_flushes(hand, cut),
        "nobs": [c for c in hand if c.suit == cut.suit and c.rank == "J"],
        "nibs": [cut] if cut.rank == "J" else [],
    }


def score(hands):
    """
    Once the combinations are discovered within the hand, this method
    will take the dictionary containing the combinations and score
    them.

    The dictionary is keyed as follows:

    - 'fifteen' - A list of cards that sum to 15
    - 'pair' - All of the car pair combinations found in the hand
    - 'run' - All of the runs found in the hand
    - 'flush' - All of the flush cards found in the hand
    - 'nobs' - The nobs card found in the hand.
    - 'nibs' - The jack cut card.

    This method will score the items as follows:

    - 'fifteen' - 2 points for every combination
    - 'pair' - 2 points for every pair
    - 'run' - 1 point per card in each of the runs
    - 'flush' - 1 point per card in the flush
    - 'nobs' - 1 point for nobs
    - 'nibs' - 2 points for his heels

    # Parameters

    hands:dict
        - The dictionary containing the hand combinations to score

    # Return

    A dictionary containing scores for the card combinations of interest
    with the following keys:
    - 'fifteen' - 2 points per card combination that sums to 15
    - 'pair' - 2 points per pair (triples and quads are accounted for)
    - 'run' - 1 point per card in each run
    - 'flush' - 1 point per card in the flush
    - 'nobs' - 1 point for nob
    - 'nibs' - 2 points for his heels

    """

    return {
        "fifteen": len(hands["fifteen"]) * 2,
        "pair": len(hands["pair"]) * 2,
        "run": sum([len(r) for r in hands["run"]]),
        "flush": len(hands["flush"]),
        "nobs": len(hands["nobs"]),
        "nibs": len(hands["nibs"]) * 2,
    }


def score_hand(hand, cut, **kwargs):
    """
    Score the pones hand and return a list of strings that can be
    printed.

    # Parameters
    hand:Hand
        - The hand to score

    cut:Card
        - The cut card to score with the hand

    # Parameters (kwargs)

    include_nibs:bool
        - Include the calculation of nibs.
        - Only dealer can claim this.
        - DEFAULT - False

    five_card_flush:bool
        - Only count the flush if it is 5 cards.
        - Only applied when counting the crib.
        - DEFAULT - False

    """

    include_nibs = kwargs.get("include_nibs", False)
    five_card_flush = kwargs.get("five_card_flush", False)

    hands = find_combinations(hand, cut)
    hand_scores = score(hands)

    # Flush is worth 5 points and only 5 points if we are counting the
    # crib (4 crib cards + cut). If we are not counting the crib we can
    # use the value of hand_scores directly.
    flush = 5 if hand_scores["flush"] == 5 and five_card_flush else hand_scores["flush"]

    # calculate the total excluding the nibs and flush
    total = sum([v for k, v in hand_scores.items() if k not in ["nibs", "flush"]])

    # add the flush separately based on the flush calculation above.
    total += flush

    # Are we counting the dealer hand?
    if include_nibs:
        total += hand_scores["nibs"]

    summary = [
        f"Hand      = {hand.sorted().cool_display()}",
        f"Cut       = {cut.cool_display()}",
        f'{len(hands["fifteen"])} Fifteens for {hand_scores["fifteen"]}',
        f'{len(hands["pair"])} Pairs for    {hand_scores["pair"]}',
        f'{len(hands["run"])} Runs for     {hand_scores["run"]}',
        f"Flush for      {flush}",
        f'Nobs for       {hand_scores["nobs"]}',
        f'Nibs for       {hand_scores["nibs"] if include_nibs else 0}',
        "-----------------",
        f"Total          {total}",
    ]

    if hands["fifteen"]:

        items = ["", "Fifteens ===="]
        for f in hands["fifteen"]:
            items.append(f"{f.cool_display()} = 15")

        summary.extend(items)

    if hands["pair"]:

        items = ["", "Pairs ===="]
        for f in hands["pair"]:
            items.append(f"{f.cool_display()}")

        summary.extend(items)

    if hands["run"]:

        items = ["", "Runs ===="]

        for f in hands["run"]:
            items.append(f"{f.cool_display()}")

        summary.extend(items)

    return summary
