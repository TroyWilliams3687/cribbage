#!/usr/bin/env python3
#-*- coding:utf-8 -*-

# -----------
# SPDX-License-Identifier: MIT
# Copyright (c) 2021 Troy Williams

# uuid:   56f0700a-d69d-11eb-87bb-1b4177236484
# author: Troy Williams
# email:  troy.williams@bluebill.net
# date:   2021-06-26
# -----------

"""
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

# ------------
# 3rd Party - From pip

# ------------
# Custom Modules


# -------------

# Shared tuple that stores the card ranks
 = (
    'A',
    '2', '3', '4', '5', '6', '7', '8', '9',
    'T', 'J', 'Q', 'K',
    )

# shared tuple that stores the card suits
 = ('D', 'H', 'C', 'S')

suit_symbols = {
    'H': u'\u2665',
    'D': u'\u2666',
    'S': u'\u2660',
    'C': u'\u2663',
}

# set the cards sorting order - useful for sorting a list of cards.
rank_sort_order_map = {
    'A': 1,
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    'T': 10,
    'J': 11,
    'Q': 12,
    'K': 13,
}


@dataclass()
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
            raise ValueError('Card.rank is not set!')

        if self.suit is None:
            raise ValueError('Card.suit is not set!')

        self.rank = self.rank.upper()
        self.suit = self.suit.upper()

        if self.rank not in ranks:
            raise ValueError(f'INVALID Rank ({self.rank})! Must be one of: {ranks}!')

        if self.suit not in suits:
            raise ValueError(f'INVALID Suit ({self.suit})! Must be one of: {suits}!')


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

        if self.rank == 'A':
            return 1

        elif self.rank in ('T', 'J', 'Q', 'K'):
            return 10

        else:
            return int(self.rank)

    def cool_display(self) -> str:
        """
        """

        return self.rank + suit_symbols[self.suit]

    def __add__(self, other):
        """
        By implementing this we can add the value of cards together
        using c1 + c2 instead of c1.value() + c2.value()
        """

        return self.value() + other.value()

    def __lt__(self, other):
        """
        Make the item sortable
        """

        return rank_sort_order_map[self.value] < rank_sort_order_map[other.value]

    def __str__(self):
        """

        Return a unicode representation of the card.

        """

        return self.rank + self.suit


def make_deck():
    """
    Creates a deck of 52 cards.

    # Parameters

    # Return

    Returns a list of cards containing 52 - all of the suits and ranks.

    """

    return [Card(*p) p for p in product(ranks, suits)]


class Hand(list):
    """
    A hand is a simple container for a number of cards.
    """

    def __init__(self, *args):
        list.__init__(self, *args)

    def display(self):
        """

        Return a list of strings representing the cards in the hand.

        [AD, 1D, 3S,4C]

        """

        return [str(c) for c in self]

    def cool_display(self):
        """
        Return a list of strings representing the cards in the hand.

        [A♦, 1♦, 3♠, 4♣]
        """
        return [c.cool_display() for c in self]

    def value(self):
        """
        Return the total value of the hand based on the sum of the
        individual cards.

        # NOTE

        sum([]) evalutes to 0

        """
        return sum([c.value() for c in self])

    def sorted(self):
        """
        Return a new ***Hand*** in sorted order.
        """
        # return Hand(sorted(self, key=lambda c: c.sort_order, reverse=False))
        return Hand(sorted(self))

    def every_combination(self, **kwargs):
        """
        A generator that will yield all possible combination of hands
        from the current hand. It will iterate through all the single
        cards, than pairs than triples etc.

        # Parameters (kwargs)

        count:int
            - The number of cards to take.

        # Return

        A Hand containing the cards in the combination.

        """

        if 'count' in kwargs:
            # From this hand, generate a list of all hands of length count

            # If count = 2
            # hand = [x,y,z,w]

            # >>>from itertools import combinations
            # >>> m = ['x', 'y', 'z', 'w']
            # >>> [c for c in combinations(m,2)]
            # [('x', 'y'), ('x', 'z'), ('x', 'w'), ('y', 'z'), ('y', 'w'), ('z', 'w')]


            for combo in combinations(self, kwargs['count']):
                yield Hand(combo)

        else:

            # Generate all possible combinations of Hands from 0 to n

            # if the hand count is 4, it will generate 16 hands.

            # >>> from itertools import chain
            # >>> from itertools import combinations
            # >>> m = ['x', 'y', 'z', 'w']
            # >>> [r for r in range(len(m) + 1)]
            # [0, 1, 2, 3, 4]
            # >>> [c for c in chain.from_iterable(combinations(m, r) for r in range(len(m) + 1))]
            # [(), ('x',), ('y',), ('z',), ('w',), ('x', 'y'), ('x', 'z'), ('x', 'w'), ('y', 'z'), ('y', 'w'), ('z', 'w'), ('x', 'y', 'z'), ('x', 'y', 'w'), ('x', 'z', 'w'), ('y', 'z', 'w'), ('x', 'y', 'z', 'w')]

            for combo in chain.from_iterable(combinations(self, r) for r in range(len(self) + 1)):
                yield Hand(combo)

def deal_hand(deck, count):
    """
    Deals a hand with `count` cards from the deck. The dealt cards are
    removed from the deck.

    # Parameters

    deck:list[Card]
        - A list of cards

    count:int
        - The number cards to deal to form a hand.


    # NOTE

    The cards will be automatically removed from the deck

    This has to be revised - we don't deal 5 cards to the pone
    and then 5 cards to the dealer. They are dealt alternating
    starting with the pones hand, then the dealer, back and forth.

    """

    hand = Hand(deck[:count])
    del deck[:count]

    return hand


