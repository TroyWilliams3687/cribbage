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
    Card,
)

# ------------


@click.group()
@click.version_option()
@click.pass_context
def main(*args, **kwargs):
    """ """

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
    help="Count crib.",
)
@click.option(
    "--dealer",
    is_flag=True,
    help="Count dealer hand.",
)
@click.argument('hand',
    nargs=4,
    type=str,
)
@click.argument('cut',
    nargs=1,
    type=str,
)
@click.pass_context
def score(*args, **kwargs):
    """
    Given the 4 cards in your hand and a cut card, score the hand.

    This command expects the first four cards to represent the hand and
    the fifth card to represent the cut card:

    cribbage score H1 H2 H3 H4 C

    It recognizes the cards as a two letter rank/suit combination. The
    rank values are:

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

    The suit values are represented by the single letter:
    - D - Diamond
    - H - Heart
    - C - Club
    - S - Spade

    So a card, the 10 of hearts would be TH or the Ace of Spades would be AS.

    OPTIONALLY, you can specify the `--crib` or `--dealer` switches to
    indicate we want to count the hand as a crib hand or a dealer hand.
    If either of these switches are not specified, then we assume a
    pone hand.

    # NOTE

    You can use lower case letters like `as` and that will work.
    However, you must specify the rank first and the suit second.

    """

    ctx = args[0]
    # config = ctx.obj["config"]

    hand = [Card(*c) for c in kwargs['hand']]
    cut = Card(*kwargs['cut'])

    hand.sort()

    # click.echo(list(str(c) for c in hand))
    # click.echo(str(cut))

    # Count Everything -
    results = score_hand(
        hand,
        cut,
        include_nibs=kwargs['dealer'],
        five_card_flush=kwargs['crib'],
        basic=True,
    )

    click.echo()
    click.echo("\n".join(results))
