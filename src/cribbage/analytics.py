#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# -----------
# SPDX-License-Identifier: MIT
# Copyright (c) 2021 Troy Williams

# uuid:
# author: Troy Williams
# email:  troy.williams@bluebill.net
# date:
# -----------

"""
A module containing advanced methods for the game of cribbage
"""

# ------------
# System Modules - Included with Python

# ------------
# 3rd Party - From pip

# ------------
# Custom Modules

from cribbage.cards import (
    hand_combinations,
    score_hand,
    make_deck,
    display_hand,
)

# -------------


def maximum_four_card_score(hand):
    """

    Given the hand, determine the maximum score of all 4 hand
    combinations.

    Generally, this is used to help decide which cards to discard after
    the deal. Normally you will supply 6 cards. However this method can
    work with any number of cards, but requires at least 4 cards
    (which won't be interesting).

    # Parameters

    hand:list(Card)
        - The list of cards we want to examine

    # Return

    The list of 4 cards that provide the maximum value


    """

    assert len(hand) >= 4

    max_score = 0
    best_hand = None

    for combo in hand_combinations(hand, combination_length=4):
        result = score_hand(combo, None)

        if result > max_score:
            max_score = result
            best_hand = combo

    return max_score, sorted(best_hand)


def expected_average(hand, discard=None):
    """

    Given a four card hand, what is the expected average hand value?
    That is, given the rest of the deck, how much on average is the
    hand worth with any particular cut card left in the deck.

    <https://en.wikipedia.org/wiki/Expected_value>

    We take the 4 cards in the hand and calculate all of the possible
    hands that include the cut cards that are left in the deck.

    Essentially, we are assuming that any of the remaining cards could
    be a cut card. We sum the the individual hand values and divide by
    the number of cards remaining in the deck. This yields the expected
    average value of the hand.

    If you want to look at what your discard options could be when dealt
    the 6 card starting hand, you can specify your hand and your
    discard cards.

    The list of discarded cards is a list of cards that you know are not
    in the deck and cannot possible show up as a cut card. These cards
    will be removed from the expected average calculation.

    # Parameter

    hand:list(Card)
        - The list of 4 cards that are the hand we want to analyze.

    discard:list(Card)
        - The list of cards that we know are not in the deck and are not
          a part of the hand.
        - DEFAULT - None

    # Return

    The average hand value

    """

    assert len(hand) == 4

    # Construct a deck of cards less the cards in the hand
    deck = [c for c in make_deck() if c not in hand]

    if discard:
        deck = [c for c in deck if c not in discard]

    total = sum([score_hand(hand, cut) for cut in deck])

    return total / len(deck)


def discard_max_hand_value(hand, **kwargs):
    """
    Given a 6 card hand and we have to decide which two cards to
    discard to the crib. This method will calculate the optimal discard
    that maximizes the expected average of the remaining 4 cards.

    # Parameters

    hand:list(Card)
        - The list of cards to determine the best discard
        - Expecting 6 cards.

    # Return

    A tuple (int, list(Card), list(Card)), containing the best average,
    the hand and the discard.

    """

    assert len(hand) == 6

    verbose = kwargs.get('verbose', False)
    messages = []

    best_average = 0
    best_hand = None
    best_discard = None

    for candidate_hand in hand_combinations(hand, combination_length=4):

        # use a set to figure out what cards were discarded
        discard = list(set(hand) - set(candidate_hand))

        combo_average = expected_average(
            list(candidate_hand),
            discard,
        )

        if verbose:
            #
            candidate_value = score_hand(list(candidate_hand), None)
            messages.append(f'Hand = {display_hand(sorted(candidate_hand), cool=True)}, value = {candidate_value}, average = {combo_average:.3f}')


        if combo_average > best_average:
            best_average = combo_average
            best_hand = candidate_hand
            best_discard = discard

    results = [best_average, sorted(best_hand), sorted(best_discard)]

    if verbose:
        results.append(messages)

    return tuple(results)




