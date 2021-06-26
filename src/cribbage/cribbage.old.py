#!/usr/bin/env python3
#-*- coding:utf-8 -*-

"""
Classes and methods for using in cribbage analysis

Copyright (c) 2018 Troy Williams

License: The MIT License (http://www.opensource.org/licenses/mit-license.php)
"""

# Constants
__uuid__ = ''
__author__ = 'Troy Williams'
__email__ = 'troy.williams@bluebill.net'
__copyright__ = 'Copyright (c) 2017, Troy Williams'
__date__ = '2018-02-18'
__maintainer__ = 'Troy Williams'


# import random
from itertools import chain, combinations, product
from itertools import groupby


# Shared tuple that stores the card ranks
ranks = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')

# shared tuple that stores the card suits
suits = ('D', 'H', 'C', 'S')


class Card(object):
    """
    This is a card object, it has a rank, a value, a suit, and a display.
    Value is an integer rank, suit and display are strings.
    """

# code for the class was inspired from:
# https://github.com/CJOlsen/Cribbage-Helper/blob/master/cribbage.py
# I have made some heavy modifications to the basic program

    def __init__(self, rank=None, suit=None):
        """
        Parameters
        ----------
        rank - a string representing the rank of the card: A, 2, 3, 4, 5, 6, 7,
               8, 9, 10, J, Q, K

        suit - a string representing the suit of the card D, H, C or S

        NOTE: If you send a combined string like '3H' or 'AS' in the rank slot.
              This will be split into the rank and suit. The order matters 'H3'
              or 'h3' or 'sa' won't be accepted.
        """

        if rank and suit:
            assert type(rank) == str and rank in ranks
            assert type(suit) == str and suit in suits

        elif rank:
            assert type(rank) == str
            assert len(rank) == 2

            r, s = rank.upper()

            # make sure the values are in the right order
            if r in ranks and s in suits:
                rank = r
                suit = s

            elif r in suits and s in ranks:
                rank = s
                suit = r

            else:
                raise ValueError('Rank and/or suit do not match!')

        else:
            raise ValueError('Rank and suit not properly set!')

        # at this point the rank and suit should be sorted
        self.rank = rank
        self.suit = suit

        if rank == 'A':
            self.value = 1

        elif rank in ('T', 'J', 'Q', 'K'):
            self.value = 10

        else:
            self.value = int(rank)

        self.display = rank + suit

        suit_symbols = {'H': u'\u2665',
                        'D': u'\u2666',
                        'S': u'\u2660',
                        'C': u'\u2663'}

        # TBW 2016-07-20
        # display the card with the rank and a graphical symbol
        # representing the suit
        self.cool_display = rank + suit_symbols[suit]

        # set the cards sorting order - useful for sorting a list of cards.
        rank_sort_order_map = {'A': 1,
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
                               'K': 13}

        self.sort_order = rank_sort_order_map[rank]

    def __eq__(self, other):
        """
        This overrides the == operator to check for equality
        """
        return self.__dict__ == other.__dict__

    def __add__(self, other):
        """
        """
        return self.value + other.value

    def __radd__(self, other):
        """
        """
        return self.value + other

    # TBW 2016-07-21
    def __lt__(self, other):
        """
        Make the item sortable
        """
        return self.sort_order < other.sort_order

    def __hash__(self):
        """
        Make the item hashable
        """
        return hash(self.display)

    def __str__(self):
        return self.cool_display

    def __repr__(self):
        # return "Card('{}', '{}')".format(self.rank, self.suit)
        return self.__str__()  # I don't need to produce the above...


def make_deck():
    """
    Creates a deck of 52 cards. Returns the deck as a list
    """

    cards = []
    for p in product(ranks, suits):
        cards.append(Card(*p))

    return cards


class Hand(list):
    """
    A hand is a list of ***Card*** objects.
    """

    def __init__(self, *args):
        list.__init__(self, *args)

    def display(self):
        """
        Returns a list of ***Card*** objects in the hand in a format suitable
        for display: [AD, 1D, 3S,4C]
        """
        return [c.display for c in self]

    def cool_display(self):
        """
        Returns a list of ***Card*** objects in the hand in a format suitable
        for display: [A♦, 1♦, 3♠, 4♣]
        """
        return [c.cool_display for c in self]

    def value(self):
        """
        Returns the value of ***Card*** objects in the hand by summing
        the individual card values.
        A = 1
        J,Q,K = 10

        and the other cards are equal to the value of their rank.
        """
        return sum([c.value for c in self])

    def sorted(self):
        """
        Return a new ***Hand*** in sorted order.
        """
        return Hand(sorted(self, key=lambda c: c.sort_order, reverse=False))

    def every_combination(self, **kwargs):
        """
        A generator that will yield all possible combination of hands
        from the current hand.
        """

        if 'count' in kwargs:
            for combo in combinations(self, kwargs['count']):
                yield Hand(combo)
        else:
            for combo in chain.from_iterable(combinations(self, r)
                                             for r in range(len(self) + 1)):
                yield Hand(combo)


def make_hand(deck, count):
    """
    Takes a deck and makes a hand out of it with the *count* number of
    cards.

    NOTE: the cards will be automatically removed from the deck
    """

    hand = Hand(deck[:count])
    del deck[:count]

    return hand


def find_fifteens_combos(hand):
    """
    A generator that takes a hand of cards and finds all of the combinations of
    cards that sum to 15. It returns a sub-hand containing the combination
    """
    for combo in hand.every_combination():
        if combo.value() == 15:
            yield combo


def count_fifteens(hand):
    """
    Counts the number of combinations within the hand of cards that sum to 15.
    Each combination is worth 2 points.

    Returns a tuple containing the total number of combinations and the total
    points.
    """
    combos = list(find_fifteens_combos(hand))
    return len(combos), len(combos)*2


def find_pairs(hand):
    """
    A generator that will iterate through all of the combinations and yield
    pairs of cards.
    """
    for combo in hand.every_combination(count=2):
        if combo[0].rank == combo[1].rank:
            yield combo


def count_pairs(hand):
    """
    Returns the score due to all the pairs found in the hand. Each pair is
    worth 3 points.
    """
    pairs = list(find_pairs(hand))
    return len(pairs), len(pairs)*2


def find_runs(hand):
    """
    A generator that takes a hand of cards and finds all runs of 3 or more
    cards. Returns each set of cards that makes a run.
    """
    runs = []
    for combo in chain.from_iterable(combinations(hand, r)
                                     for r in range(3, len(hand)+1)):

        for k, g in groupby(enumerate(Hand(combo).sorted()),
                            lambda ix: ix[0] - ix[1].sort_order):

            # strip out the enumeration and get the cards in the group
            new_hand = Hand([i[1] for i in g])
            if len(new_hand) < 3:
                continue

            m = set(new_hand)

            # check to see if the new run is a subset of an existing run
            if any([m.issubset(s) for s in runs]):
                continue

            # if the new run is a super set of previous runs, we need to remove
            # them
            l = [m.issuperset(s) for s in runs]
            if any(l):
                runs = [r for r, t in zip(runs, l) if not t]

            if m not in runs:
                runs.append(m)

    return [Hand(list(r)).sorted() for r in runs]


def count_runs(hand):
    """
    Count the number of points in all the runs. 1 point per card in the run
    (at least 3 cards).
    """
    runs = list(find_runs(hand))
    return len(runs), sum([len(r) for r in runs])


def count_flushes(hand, cut, is_crib=False):
    """
    Scores the points for flushes.
    """

    assert len(hand) == 4

    m = set([c.suit for c in hand])
    if len(m) == 1:
        score = 4

        if cut and m.pop() == cut.suit:
            score += 1

        if is_crib:
            # The crib can only score a flush if all the cards
            # in the crib are the same suit and the cut card
            # is the same suit. Otherwise a flush isn't counted.
            if score != 5:
                return 0

        return score

    else:
        return 0


def count_nobs(hand, cut):
    """
    Takes a 4 card hand and a cut card. If the hand contains a jack and it is
    the same suit as the cut card than a point is scored. This is called nobs.
    """
    assert len(hand) == 4

    if not cut:
        return 0

    if any([c.suit == cut.suit and c.rank == 'J' for c in hand]):
        return 1

    else:
        return 0


def score_hand(hand, cut, **kwargs):
    """
    Takes a 4 card crib hand and the cut card and scores it.

    Returns a dictionary containing the various items
    """

    # defaults
    is_crib = False if 'is_crib' not in kwargs else kwargs['is_crib']

    full_hand = Hand(hand + [cut]) if cut else hand
    scores = {}  # contain the scores
    count = {}  # contain the counts for items that can hit multiple times

    number, value = count_fifteens(full_hand)
    count['fifteen'] = number
    scores['fifteen'] = value

    number, value = count_pairs(full_hand)
    count['pair'] = number
    scores['pair'] = value

    number, value = count_runs(full_hand)
    count['run'] = number
    scores['run'] = value

    scores['flush'] = count_flushes(hand, cut, is_crib)
    scores['nobs'] = count_nobs(hand, cut)

    return scores, count


def display_points(hand, cut, scores, counts):
    print('Hand      = {}'.format(','.join(hand.sorted().cool_display())))
    print('Cut       = {}'.format(cut.cool_display if cut else 'N/A'))
    print()

    print('{} Fifteens for {}'.format(counts['fifteen'], scores['fifteen']))
    print('{} Pairs for    {}'.format(counts['pair'], scores['pair']))
    print('{} Runs for     {}'.format(counts['run'], scores['run']))
    print('Flush for      {}'.format(scores['flush']))
    print('Nobs for       {}'.format(scores['nobs']))
    print('-----------------')
    print('Total          {}'.format(sum([v for k, v in scores.items()])))
    print()

    full_hand = Hand(hand + [cut]) if cut else hand
    print('Fifteens====')
    for combo in find_fifteens_combos(full_hand):
        print('{} = 15'.format(', '.join(combo.cool_display())))

    print()
    print('Pairs====')
    for combo in find_pairs(full_hand):
        print('{}'.format(', '.join(combo.cool_display())))

    print()
    print('Runs====')
    for combo in find_runs(full_hand):
        print(', '.join(combo.cool_display()))
