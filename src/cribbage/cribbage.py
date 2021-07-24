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

from zoneinfo import ZoneInfo
from datetime import datetime

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
    expected_average,
    expected_average_crib,
    discard_consider_all_combos,
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

    Takes a 4 card hand and computes the average value of that hand. It
    will iterate through the remaining cards in the deck and pull one
    at a time as it it were the cut card. It will calculate the score
    of the hand and cut card taking the average value of all the
    hands.

    It uses the fact that the 4 cards in the hand cannot appear as cut
    cards. It proceed to calculate the hand value of every combination
    of hand and cut card. From there it can determine the average value
    of the hand.

    You need to specify 4 cards (separated by spaces) for your hand
    or it will raise an error.

    Optionally, you can specify any number of `discard` cards, separated
    by spaces. The discards are cards that you know cannot turn up as a
    cut card because they are not in the deck. Typically, you will
    specify the 2 cards you want to discard to the crib. In reality, it
    is simply a list of cards that you know cannot appear as cut cards.
    The program will take the first 4 cards as the hand and the rest as
    discard.

    # Usage

    $ cribbage average 4H 5D 5C 6S

    Hand = ['4♥', '5♦', '5♣', '6♠']
    Average Value = 15.96

    $ cribbage average 3H 4D 5D 5S JS 2C

    Hand = ['3♥', '4♦', '5♦', '5♠']
    Discard = ['J♠', '2♣']
    Average Value = 12.48
    """

    hand = [Card(*c) for c in kwargs["hand"]]
    discard = [Card(*c) for c in kwargs["discard"]]

    hand_average = expected_average(hand, discard)
    hand_value = score_hand(hand, None)

    click.echo()
    click.echo(f"Hand = {display_hand(hand, cool=True)}")

    if discard:
        click.echo(f"Discard = {display_hand(discard, cool=True)}")

    click.echo(f"Value = {hand_value}")
    click.echo(f"Average Value = {hand_average:.3f}")


def write_message(message):
    """
    Simple callback method to allow library code to write messages to
    STDOUT.
    """

    click.echo(message)


def display_discard_results(results, processing_message, delta_key, **kwargs):
    """ """

    dp = kwargs.get("dp", 3)
    sp = kwargs.get("sp", 6)

    click.echo(processing_message)

    for i, result in enumerate(results, start=1):

        message = [
            f"{i:>2} {display_hand(sorted(result['hand']), cool=True)} ({result['value']}); {display_hand(sorted(result['discard']), cool=True)}",
            f"EA = {result['expected_average']:>{sp}.{dp}f}",
            f"CEA = {result['expected_average_crib']:>{sp}.{dp}f}",
            f"Δ = {result[delta_key]:>{sp}.{dp}f}",
        ]

        click.echo(", ".join(message))


@main.command("discard")
@click.argument(
    "hand",
    nargs=6,
    type=str,
)
@click.option(
    "--verbose",
    is_flag=True,
    help="Display more information about the process.",
)
@click.pass_context
def discard(*args, **kwargs):
    """
    Given 6 cards, display all of the 4 card combinations with their
    expected average for each hand and the expected average for the
    crib. Display the best discard choice for the Pone and the Dealer.

    The idea for the dealer and pone is to maximize their overall score.
    For the dealer, they should maximize the sum of the hand expected
    average and the crib expected average. This may mean in some cases
    favoring a lower hand average.

    For the pone, they want to maximize the overall score, but they want
    to maximize the difference between the hand average and the crib
    average. In most cases, this means they should attempt to maximize
    the hand average value.

    What this method does is looks at the pone and dealer strategies. It
    will generate a table for each player. The table will have the
    following rows:

    \b
    1 ['3♥', '4♦', '5♦', '5♠'] (8); ['2♣', 'J♠'], EA = 12.478, CEA =  3.855, Δ =  8.623

    \b
    - The first column represents the hand configuration.
    - The second column represents the cards to keep in hand.
    - The third column represents the cards to discard to the crib.
    - The `EA` column represents the expected average for the hand.
    - The `CEA` column represents the expected average for the crib.
    - The Δ column represents the sum of (EA + CEA) for a dealer hand
      and the difference (EA - CEA) for a pone hand.

    # Usage

    $ cribbage discard 3H 4D 5D 5S JS 2C --verbose

    $ cribbage discard 3H 4D 5D 5S JS 2C --verbose

    $ cribbage discard KH 7D 9D AD 8C JD

    # NOTE

    \b
    EA  - Expected Average for the hand
    CEA - Expected Average for the Crib
    EA - CEA = The crib provides nothing to the pone. Subtract the crib value to determine the best hand to play.
    EA + CEA = We will augment the dealers hand by adding the crib average to the hand average.

    For both the dealer and the pone, you want the hand that generates the largest delta (Δ).

    """

    ctx = args[0]

    build_start_time = datetime.now().replace(tzinfo=ZoneInfo("America/Toronto"))

    click.echo()

    cards = [Card(*c) for c in kwargs["hand"]]

    # do we have duplicate cards?
    duplicates = set(cards)

    if len(cards) != 6:
        click.echo(f"6 Cards are required! Only {len(cards)} found.")
        ctx.abort()

    if len(duplicates) < len(cards):
        click.echo(f"Duplicate Cards are not Allowed!")
        ctx.abort()

    # --------------
    click.echo(f"Processing....")

    cb = write_message if kwargs["verbose"] else None

    results = discard_consider_all_combos(cards, callback=cb)

    click.echo()

    results_pone = sorted(
        results,
        key=lambda x: x["delta_pone"],
        reverse=True,
    )

    display_discard_results(
        results_pone, "Processing Pone Hands....", "delta_pone", dp=3, sp=6
    )
    click.echo()

    results_dealer = sorted(
        results,
        key=lambda x: x["delta_dealer"],
        reverse=True,
    )

    display_discard_results(
        results_dealer, "Processing Dealer Hands....", "delta_dealer", dp=3, sp=6
    )

    # --------------
    build_end_time = datetime.now().replace(tzinfo=ZoneInfo("America/Toronto"))

    click.echo("")
    click.echo(f"Started  - {build_start_time}")
    click.echo(f"Finished - {build_end_time}")
    click.echo(f"Elapsed:   {build_end_time - build_start_time}")
