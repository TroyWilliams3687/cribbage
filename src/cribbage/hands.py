#!/usr/bin/env python3
#-*- coding:utf-8 -*-

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
