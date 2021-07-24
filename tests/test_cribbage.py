#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# -----------
# SPDX-License-Identifier: MIT
# Copyright (c) 2021 Troy Williams

# uuid:   6323e100-d778-11eb-822d-e7a609cf0d07
# author: Troy Williams
# email:  troy.williams@bluebill.net
# date:   2021-06-27
# -----------

"""
Test module for testing them the cribbage methods.
"""

# ------------
# System Modules - Included with Python


# ------------
# 3rd Party - From pip

import pytest

# ------------
# Custom Modules

from cribbage.cards import (
    Card,
    make_deck,
    display_hand,
    hand_combinations,
    find_fifteens,
    find_pairs,
    find_runs,
    find_flushes,
    find_combinations,
    score,
)

from cribbage.analytics import (
    # maximum_four_card_score,
    expected_average,
    # discard_max_hand_value,
    expected_average_crib,
)

# -------------


# -------------
# Test Card - init

# suits = 'D', 'H', 'C', 'S'
# rank  = 'A', '2','3','4','5','6','7','8','9','T','J','Q','K'

data = [
    ("8D", Card(rank="8", suit="D")),
    ("8d", Card(rank="8", suit="D")),
    ("9H", Card(rank="9", suit="H")),
    ("9H", Card("9", "H")),
    ("9H", Card(*"9H")),
    ("TC", Card("T", "C")),
    (("2", "H"), Card(rank="2", suit="H")),
]


@pytest.mark.parametrize("data", data)
def test_card_init(data):

    left, right = data

    c = Card(*left)

    assert c == right


# -------------
# Test Card - value

data = [
    ("8D", 8),
    ("9H", 9),
    ("TH", 10),
    ("AS", 1),
    ("KC", 10),
    ("JD", 10),
    ("QS", 10),
    ("2C", 2),
]


@pytest.mark.parametrize("data", data)
def test_card_value(data):

    left, right = data

    c = Card(*left)

    assert c.value() == right


# -------------
# Test Card - str

data = [
    ("8D", "8D"),
    ("9H", "9H"),
    ("TH", "TH"),
    ("AS", "AS"),
    ("KC", "KC"),
    ("JD", "JD"),
    ("QS", "QS"),
    ("2C", "2C"),
]


@pytest.mark.parametrize("data", data)
def test_card_str(data):

    left, right = data

    c = Card(*left)

    assert str(c) == right


# -------------
# Test Card - cool display

data = [
    ("8D", "8" + u"\u2666"),
    ("9H", "9" + u"\u2665"),
    ("TH", "T" + u"\u2665"),
    ("AS", "A" + u"\u2660"),
    ("KC", "K" + u"\u2663"),
    ("JD", "J" + u"\u2666"),
    ("QS", "Q" + u"\u2660"),
    ("2C", "2" + u"\u2663"),
]


@pytest.mark.parametrize("data", data)
def test_card_cool(data):

    left, right = data

    c = Card(*left)

    assert c.cool_display() == right


data = [
    ("8D", "🃈"),
    ("9H", "🂹"),
    ("TH", "🂺"),
    ("AS", "🂡"),
    ("KC", "🃞"),
    ("JD", "🃋"),
    ("QS", "🂭"),
    ("2C", "🃒"),
]


@pytest.mark.parametrize("data", data)
def test_card_cool2(data):

    left, right = data

    c = Card(*left)

    assert c.cool_display(display_card=True) == right


# -------------
# Test Card - add

# data = [
#     (("8D", "9C"), 17),
#     (("AS", "9C", "3H"), 13),
#     (("6C", "9C"), 15),
#     (("TD", "JC", "AS"), 21),
#     (("TD", "JC", "KS"), 30),
# ]


# @pytest.mark.parametrize("data", data)
# def test_card_add(data):

#     left, right = data

#     value = sum([Card(*c) for c in left])

#     assert value == right


# -------------
# Test Card - sort


data = [
    (("TC", "AS", "3H"), ("AS", "3H", "TC")),
    (("TC", "AS", "3H", "6C", "4D"), ("AS", "3H", "4D", "6C", "TC")),
    (("4S", "3H", "5C", "4D"), ("3H", "4D", "4S", "5C")),
]


@pytest.mark.parametrize("data", data)
def test_card_sort(data):

    left, right = data

    cards = sorted([Card(*c) for c in left])

    assert tuple(str(c) for c in cards) == right


# -------------
# Test Card - Exceptions

data = [
    "H5",
    "S6",
    "SS",
    "A ",
    "1S",
    "GH",
]


@pytest.mark.parametrize("data", data)
def test_card_exception(data):

    with pytest.raises(ValueError):
        c = Card(*data)


# -------------
# Test make_deck


def test_make_deck():

    deck = make_deck()

    assert len(deck) == 52

    assert Card(*"3H") in deck

    assert Card(*"5S") in deck

    assert Card(*"AS") in deck


def test_make_deck_delete():

    deck = make_deck()
    assert len(deck) == 52

    c = Card(*"3H")
    assert c in deck

    deck.remove(c)
    assert len(deck) == 51
    assert c not in deck


# -------------
# Test display_hand

data = [
    (("TC", "AS", "3H"), ("TC", "AS", "3H")),
    (("9C", "AS", "3D"), ("9C", "AS", "3D")),
    (("9C", "AS", "3D", "Ac", "ah"), ("9C", "AS", "3D", "AC", "AH")),
]


@pytest.mark.parametrize("data", data)
def test_hand_display(data):

    left, right = data

    cards = [Card(*c) for c in left]

    items = display_hand(cards)

    # writing the test like this because we don't care (at this point)
    # if it is a list or tuple, just that the elements are the same and
    # in the same order.

    assert len(items) == len(right)
    assert all([a == b for a, b in zip(items, right)])


# # -------------
# # Test count_hand

# data = [
#     (("TC", "AS", "3H"), 14),
#     (("9C", "AS", "3D"), 13),
#     (("9C", "AS", "3D", "Ac", "ah"), 15),
# ]


# @pytest.mark.parametrize("data", data)
# def test_hand_value(data):

#     left, right = data

#     assert count_hand([Card(*c) for c in left]) == right


# -------------
# Test Hand - Sorted

data = [
    (("TC", "AS", "3H"), ("AS", "3H", "TC")),
    (("9C", "AS", "3D"), ("AS", "3D", "9C")),
    (("9C", "AS", "3D", "Ac", "ah"), ("AH", "AS", "AC", "3D", "9C")),
]


@pytest.mark.parametrize("data", data)
def test_hand_sorted(data):

    left, right = data

    cards = [Card(*c) for c in left]

    # Create a new sorted list
    items = display_hand(sorted(cards))

    print(items)

    assert len(items) == len(right)
    assert all([a == b for a, b in zip(items, right)])

    # Sort the Cards inline
    cards.sort()
    items = display_hand(cards)

    assert len(items) == len(right)
    assert all([a == b for a, b in zip(items, right)])


# -------------
# Test hand_combinations


left = ("TC", "AS", "3H")
right = (
    [],
    [Card(rank="T", suit="C")],
    [Card(rank="A", suit="S")],
    [Card(rank="3", suit="H")],
    [Card(rank="T", suit="C"), Card(rank="A", suit="S")],
    [Card(rank="T", suit="C"), Card(rank="3", suit="H")],
    [Card(rank="A", suit="S"), Card(rank="3", suit="H")],
    [Card(rank="T", suit="C"), Card(rank="A", suit="S"), Card(rank="3", suit="H")],
)

data = [(left, right)]

left = ("TC", "AS", "3H", "QD")
right = (
    [],
    [Card(rank="T", suit="C")],
    [Card(rank="A", suit="S")],
    [Card(rank="3", suit="H")],
    [Card(rank="Q", suit="D")],
    [Card(rank="T", suit="C"), Card(rank="A", suit="S")],
    [Card(rank="T", suit="C"), Card(rank="3", suit="H")],
    [Card(rank="T", suit="C"), Card(rank="Q", suit="D")],
    [Card(rank="A", suit="S"), Card(rank="3", suit="H")],
    [Card(rank="A", suit="S"), Card(rank="Q", suit="D")],
    [Card(rank="3", suit="H"), Card(rank="Q", suit="D")],
    [Card(rank="T", suit="C"), Card(rank="A", suit="S"), Card(rank="3", suit="H")],
    [Card(rank="T", suit="C"), Card(rank="A", suit="S"), Card(rank="Q", suit="D")],
    [Card(rank="T", suit="C"), Card(rank="3", suit="H"), Card(rank="Q", suit="D")],
    [Card(rank="A", suit="S"), Card(rank="3", suit="H"), Card(rank="Q", suit="D")],
    [
        Card(rank="T", suit="C"),
        Card(rank="A", suit="S"),
        Card(rank="3", suit="H"),
        Card(rank="Q", suit="D"),
    ],
)

data.append((left, right))


@pytest.mark.parametrize("data", data)
def test_hand_combinations(data):

    left, right = data

    cards = [Card(*c) for c in left]

    combo = [c for c in hand_combinations(cards)]

    assert len(combo) == len(right)

    for a, b in zip(combo, right):
        assert all(u == v for u, v in zip(a, b))


left = ("TC", "AS", "3H")
right = (
    (Card(rank="T", suit="C"), Card(rank="A", suit="S")),
    (Card(rank="T", suit="C"), Card(rank="3", suit="H")),
    (Card(rank="A", suit="S"), Card(rank="3", suit="H")),
)

data = [(left, right)]


@pytest.mark.parametrize("data", data)
def test_hand_combinations2(data):

    left, right = data

    cards = [Card(*c) for c in left]

    combo = [c for c in hand_combinations(cards, combination_length=2)]

    assert len(combo) == len(right)

    for a, b in zip(combo, right):
        assert all(u == v for u, v in zip(a, b))


# -------------
# Test find_fifteens

left = ("TC", "5D", "3H", "2H", "6S")
right = (
    ("TC", "5D"),
    ("TC", "3H", "2H"),
)

data = [(left, right)]


@pytest.mark.parametrize("data", data)
def test_find_fiffteens(data):

    left, right = data

    cards = [Card(*c) for c in left]

    counts = [c for c in find_fifteens(cards)]

    assert len(counts) == len(right)

    for a, b in zip(counts, right):
        assert all(str(u) == v for u, v in zip(a, b))


# -------------
# Test find_pairs

# NOTE: The order matters - we don't sort in this portion

left = ("TC", "5D", "5H", "5C", "6S")
right = (
    ("5D", "5H"),
    ("5D", "5C"),
    ("5H", "5C"),
)

data = [(left, right)]


@pytest.mark.parametrize("data", data)
def test_find_pairs(data):

    left, right = data

    cards = [Card(*c) for c in left]

    counts = [c for c in find_pairs(cards)]

    assert len(counts) == len(right)

    for a, b in zip(counts, right):
        assert all(str(u) == v for u, v in zip(a, b))


# -------------
# Test find_runs


left = ("2C", "3D", "3H", "4C", "TS")
right = (
    ("2C", "3D", "4C"),
    ("2C", "3H", "4C"),
)

data = [(left, right)]


@pytest.mark.parametrize("data", data)
def test_find_runs(data):

    left, right = data

    cards = [Card(*c) for c in left]

    counts = [c for c in find_runs(cards)]

    print(counts)

    assert len(counts) == len(right)

    for a, b in zip(counts, right):
        assert all(str(u) == v for u, v in zip(a, b))


# -------------
# Test find_flushes

left = (("2C", "3C", "4C", "8C"), ("QS"))
right = ("2C", "3C", "4C", "8C")

data = [(left, right)]

left = (("2C", "3S", "4C", "8C"), ("TD"))
right = ()

data.append((left, right))


left = (("2C", "3S", "4C", "8C"), ("TC"))
right = ("2C", "4C", "8C", "TC")

data.append((left, right))


@pytest.mark.parametrize("data", data)
def test_find_flushes(data):

    left, right = data

    hand_left, cut_left = left

    cards = [Card(*c) for c in hand_left]
    hand = [c for c in find_flushes(cards, Card(*cut_left))]

    assert len(hand) == len(right)

    assert all(str(u) == v for u, v in zip(hand, right))


# -------------
# Test find_combinations


left = (("4C", "5C", "6D", "5S"), ("QS"))  # 16 point hand
right = {
    "fifteen": [
        (Card(rank="5", suit="C"), Card(rank="Q", suit="S")),
        (Card(rank="5", suit="S"), Card(rank="Q", suit="S")),
        (Card(rank="4", suit="C"), Card(rank="5", suit="C"), Card(rank="6", suit="D")),
        (Card(rank="4", suit="C"), Card(rank="6", suit="D"), Card(rank="5", suit="S")),
    ],
    "pair": [(Card(rank="5", suit="C"), Card(rank="5", suit="S"))],
    "run": [
        [Card(rank="4", suit="C"), Card(rank="5", suit="C"), Card(rank="6", suit="D")],
        [Card(rank="4", suit="C"), Card(rank="5", suit="S"), Card(rank="6", suit="D")],
    ],
    "flush": [],
    "nobs": [],
    "nibs": [],
}

data = [(left, right)]

left = (("3C", "2S", "6D", "8H"), ("3S"))  # 2 point hand
right = {
    "fifteen": [],
    "pair": [(Card(rank="3", suit="C"), Card(rank="3", suit="S"))],
    "run": [],
    "flush": [],
    "nobs": [],
    "nibs": [],
}

data.append((left, right))


@pytest.mark.parametrize("data", data)
def test_find_combinations(data):

    left, right = data

    hand_left, cut_left = left

    cards = [Card(*c) for c in hand_left]
    results = find_combinations(cards, Card(*cut_left))

    assert results == right


# -------------
# Test score

left = (("4C", "5C", "6D", "5S"), ("QS"))  # 16 point hand
right = {
    "fifteen": 8,
    "pair": 2,
    "run": 6,
    "flush": 0,
    "nobs": 0,
    "nibs": 0,
}

data = [(left, right)]

left = (("3C", "2S", "6D", "8H"), ("3S"))  # 2 point hand
right = {
    "fifteen": 0,
    "pair": 2,
    "run": 0,
    "flush": 0,
    "nobs": 0,
    "nibs": 0,
}

data.append((left, right))

left = (("3C", "2S", "TD", "8H"), ("6S"))
right = {
    "fifteen": 2,
    "pair": 0,
    "run": 0,
    "flush": 0,
    "nobs": 0,
    "nibs": 0,
}

data.append((left, right))

left = (("3C", "2S", "AS", "7H"), ("9S"))
right = {
    "fifteen": 2,
    "pair": 0,
    "run": 3,
    "flush": 0,
    "nobs": 0,
    "nibs": 0,
}

data.append((left, right))


left = (("3C", "TC", "AC", "8C"), ("KS"))
right = {
    "fifteen": 0,
    "pair": 0,
    "run": 0,
    "flush": 4,
    "nobs": 0,
    "nibs": 0,
}

data.append((left, right))

left = (("3C", "TC", "JS", "8C"), ("6S"))
right = {
    "fifteen": 0,
    "pair": 0,
    "run": 0,
    "flush": 0,
    "nobs": 1,
    "nibs": 0,
}

data.append((left, right))

left = (("3C", "TC", "KS", "8C"), ("JS"))
right = {
    "fifteen": 0,
    "pair": 0,
    "run": 0,
    "flush": 0,
    "nobs": 0,
    "nibs": 2,
}

data.append((left, right))


@pytest.mark.parametrize("data", data)
def test_score(data):

    left, right = data

    hand_left, cut_left = left

    cards = [Card(*c) for c in hand_left]
    results = score(find_combinations(cards, Card(*cut_left)))

    assert results == right

# ------------
# average_hand


left = (("3H", "4D", "5D", "5S"), ("JS", "2C"))
right = 12.478

data = [(left, right)]

left = (("4H", "5D", "5C", "6S"), None)
right = 15.958
data.append((left, right))

left = (("6C", "KS", "8S", "5C"), ("4S", "QH"))
right = 4.63
data.append((left, right))

left = (("3C", "4D", "5H", "5C"), ("2C", "JC"))
right = 12.478


@pytest.mark.parametrize("data", data)
def test_maximum_average_hand(data):

    left, right = data

    cards = [Card(*c) for c in left[0]]
    discard = [Card(*c) for c in left[1]] if left[1] else None

    average_value = expected_average(cards, discard)

    assert pytest.approx(average_value, rel=1e-4, abs=1e-12) == right


# ------------
# expected_average_crib

left = (("4C", "5C", "6D", "5S"), ("QS", 'KS'))
right = 4.0415

data = [(left, right)]

left = (("3C", "2S", "6D", "8H"), ("3S", '4D'))
right = 5.25955

data.append((left, right))

left = (("3C", "2S", "TD", "8H"), ("6S", '8S'))
right = 5.401844

data.append((left, right))

@pytest.mark.parametrize("data", data)
def test_expected_average_crib(data):

    left, right = data

    hand_left, discard_left = left

    hand = [Card(*c) for c in hand_left]
    discard = cards = [Card(*c) for c in discard_left]

    average_value = expected_average_crib(hand, discard)

    assert pytest.approx(average_value, rel=1e-6, abs=1e-12) == right
