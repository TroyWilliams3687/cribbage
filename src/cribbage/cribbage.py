#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# -----------
# SPDX-License-Identifier: MIT
# Copyright (c) 2021 Troy Williams

# uuid:   060527ea-d69c-11eb-87bb-1b4177236484
# author: Troy Williams
# email:  troy.williams@bluebill.net
# date:   2021-06-26
# -----------

"""
"""

# ------------
# System Modules - Included with Python

from pathlib import Path

# ------------
# 3rd Party - From pip

import click

# ------------
# Custom Modules


from .cards import (
    score_hand,
    score_hand_breakdown,
    Card,
    display_hand,
)

from .analytics import (
    average_hand_value,
)

# ------------


@click.group()
@click.version_option()
@click.pass_context
def main(*args, **kwargs):
    """

    This application will perform various calculations on cribbage hands.

    # Scoring

    Using the score command you can calculate the score of a hand along
    with the breakdown showing how the score was calculated.

    $ cribbage score 4H 5D 5C 6S JD

    """

    # Initialize the shared context object to a dictionary and configure it for the app
    ctx = args[0]
    ctx.ensure_object(dict)


# -----------
# Add the child menu options

# main.add_command(save)
# main.add_command(restore)


@main.command("score")
@click.option(
    "--crib",
    is_flag=True,
    help="Count the cards assuming this is the crib.",
)
@click.option(
    "--dealer",
    is_flag=True,
    help="Count the cards assuming this is a dealers hand.",
)
@click.argument(
    "hand",
    nargs=4,
    type=str,
)
@click.argument(
    "cut",
    nargs=1,
    type=str,
)
@click.pass_context
def score(*args, **kwargs):
    """
    Given the 4 cards in your hand and a cut card, score the hand using
    cribbage rules and scoring conventions.

    This command expects the first four cards to represent the hand and
    the fifth card to represent the cut card:

    cribbage score H1 H2 H3 H4 C

    It recognizes the cards as a two letter rank/suit combination.

    The rank values are:

    A (Ace), 2, 3, 4, 5, 6, 7, 8, 9, T (Ten), J (Jack), Q (Queen), K
    (King)

    The suit values are:

    D (Diamond), H (Heart), C (Club), S (Spade)

    So a card, the 10 of hearts would be TH or the Ace of Spades would
    be AS.

    # Optional

    You can specify the `--crib` or `--dealer` switches to indicate we
    want to count the hand as a crib hand or a dealer hand. If either
    of these switches are not specified, then we assume a pone hand.

    # NOTE

    You can use lower case letters like `as` for the Ace of Spades.
    However, you must specify the rank first and the suit second.

    # Usage

    $ cribbage score 4H 5D 5C 6S JD

    Hand = ['4H', '5D', '6S', '5C'] Cut = JD
    -----------------------
    4 Fifteens for 8
    1 Pairs for    2
    2 Runs for     6
    Flush for      0
    Nobs for       0
    Nibs for       0
    -----------------------
    Total:         16

    Fifteens:

    1 - ['5D', 'JD']
    2 - ['5C', 'JD']
    3 - ['4H', '5D', '6S']
    4 - ['4H', '6S', '5C']

    Pairs:

    1, ['5D', '5C']

    Runs:

    1 - ['4H', '5D', '6S']
    2 - ['4H', '5C', '6S']


    """

    hand = [Card(*c) for c in kwargs["hand"]]
    cut = Card(*kwargs["cut"])

    hand.sort()

    # Count Everything -
    results = score_hand_breakdown(
        hand,
        cut,
        include_nibs=kwargs["dealer"],
        five_card_flush=kwargs["crib"],
        basic=True,
    )

    click.echo()
    click.echo("\n".join(results))

@main.command("average")
@click.argument(
    "hand",
    nargs=4,
    type=str,
)
@click.argument(
    "discard",
    nargs=-1,
    type=str,
)
@click.pass_context
def average(*args, **kwargs):
    """

    Takes 4 cards as a hand and computes the average value of that hand.
    It uses the fact that the 4 cards in the hand cannot appear as cut
    cards. It proceed to calculate the hand value of every combination
    of hand and cut card. From there it can determine the average value
    of the hand.

    You need to specify 4 cards (separated by spaces) for your hand
    otherwise an error will be raised.

    Optionally, you can specify any number of `discard` cards, separated
    by spaces,. The discards are cards that you know cannot turn up as
    a cut card because they are not in the deck. Typically, you will
    specify the 2 cards you want to discard to the crib. In reality, it
    is simply a list of cards that you know cannot appear as cut
    cards.

    # Usage

    $ cribbage average 4H 5D 5C 6S

    """

    hand = [Card(*c) for c in kwargs["hand"]]
    discard = [Card(*c) for c in kwargs["discard"]]

    hand_average = average_hand_value(hand, discard)

    click.echo()
    click.echo(f"Hand = {display_hand(hand, cool=True)}")

    if discard:
        click.echo(f"Discard = {display_hand(discard, cool=True)}")

    click.echo(f"Average Value = {hand_average:.2f}")
    click.echo()
