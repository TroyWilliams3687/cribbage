#!/usr/bin/env python3
#-*- coding:utf-8 -*-

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
    Hand,
)

# -------------



# -------------
# Test Card - init

# suits = 'D', 'H', 'C', 'S'
# rank  = 'A', '2','3','4','5','6','7','8','9','T','J','Q','K'

data = [
    ('8D', Card(rank='8', suit='D')),
    ('8d', Card(rank='8', suit='D')),
    ('9H', Card(rank='9', suit='H')),
    ('9H', Card('9', 'H')),
    ('9H', Card(*'9H')),
    ('TC', Card('T', 'C')),
    (('2','H'), Card(rank='2', suit='H')),
]

@pytest.mark.parametrize('data', data)
def test_card_init(data):

    left, right = data

    c = Card(*left)

    assert c == right


# -------------
# Test Card - value

data = [
    ('8D', 8),
    ('9H', 9),
    ('TH', 10),
    ('AS', 1),
    ('KC', 10),
    ('JD', 10),
    ('QS', 10),
    ('2C', 2),
]

@pytest.mark.parametrize('data', data)
def test_card_value(data):

    left, right = data

    c = Card(*left)

    assert c.value() == right

# -------------
# Test Card - str

data = [
    ('8D', '8D'),
    ('9H', '9H'),
    ('TH', 'TH'),
    ('AS', 'AS'),
    ('KC', 'KC'),
    ('JD', 'JD'),
    ('QS', 'QS'),
    ('2C', '2C'),
]

@pytest.mark.parametrize('data', data)
def test_card_str(data):

    left, right = data

    c = Card(*left)

    assert str(c) == right


# -------------
# Test Card - cool display

data = [
    ('8D', '8' + u'\u2666'),
    ('9H', '9' + u'\u2665'),
    ('TH', 'T' + u'\u2665'),
    ('AS', 'A' + u'\u2660'),
    ('KC', 'K' + u'\u2663'),
    ('JD', 'J' + u'\u2666'),
    ('QS', 'Q' + u'\u2660'),
    ('2C', '2' + u'\u2663'),
]

@pytest.mark.parametrize('data', data)
def test_card_cool(data):

    left, right = data

    c = Card(*left)

    assert c.cool_display() == right


# -------------
# Test Card - add

data = [
    (('8D', '9C'), 17),
    (('AS', '9C', '3H'), 13),
    (('6C', '9C'), 15),
    (('TD', 'JC', 'AS'), 21),
    (('TD', 'JC', 'KS'), 30),
]

@pytest.mark.parametrize('data', data)
def test_card_add(data):

    left, right = data

    value = sum([Card(*c) for c in left])

    assert value == right

# -------------
# Test Card - sort


data = [
    (('TC', 'AS', '3H'), ('AS', '3H', 'TC')),
    (('TC', 'AS', '3H', '6C', '4D'), ('AS', '3H', '4D', '6C', 'TC')),
]

@pytest.mark.parametrize('data', data)
def test_card_sort(data):

    left, right = data

    cards = sorted([Card(*c) for c in left])

    assert tuple(str(c) for c in cards) == right

# -------------
# Test Card - Exceptions

data = [
    'H5',
    'S6',
    'SS',
    'A ',
    '1S',
    'GH',
]

@pytest.mark.parametrize('data', data)
def test_card_exception(data):

    with pytest.raises(ValueError):
        c = Card(*data)


# -------------
# Test make_deck

def test_card_sort():

    deck = make_deck()

    assert len(deck) == 52

    assert Card(*'3H') in deck


# -------------
# Test Hand - Init


data = [
    (('TC', 'AS', '3H'), Hand([Card(*'TC'), Card(*'AS'), Card(*'3H')])),
    (('9C', 'AS', '3D'), Hand([Card(*'9C'), Card(*'AS'), Card(*'3D')])),
    (('9C', 'AS', '3D', 'Ac', 'ah'), Hand([Card(*'9C'), Card(*'AS'), Card(*'3D'), Card(*'AC'), Card(*'AH')])),
]

@pytest.mark.parametrize('data', data)
def test_hand_init(data):

    left, right = data

    cards = Hand([Card(*c) for c in left])

    assert cards == right

# -------------
# Test Hand - Init - Exception - Duplicates

data = [
    ('TC', 'AS', '3H', 'tc'),
    ('9C', 'AS', 'as', '3D'),
    ('9C', 'AS', '3D',  '3D', 'Ac', 'ah'),
]

@pytest.mark.parametrize('data', data)
def test_card_exception(data):

    with pytest.raises(ValueError):
        cards = Hand([Card(*c) for c in data])

# -------------
# Test Hand - Display

data = [
    (('TC', 'AS', '3H'), ('TC', 'AS', '3H') ),
    (('9C', 'AS', '3D'), ('9C', 'AS', '3D') ),
    (('9C', 'AS', '3D', 'Ac', 'ah'), ('9C', 'AS', '3D', 'AC', 'AH') ),
]

@pytest.mark.parametrize('data', data)
def test_hand_display(data):

    left, right = data

    cards = Hand([Card(*c) for c in left])


    items = cards.display()

    # writing the test like this because we don't care (at this point)
    # if it is a list or tuple, just that the elements are the same and
    # in the same order.

    assert len(items) == len(right)
    assert all([a == b for a, b in zip(items, right)])



# -------------
# Test Hand - Value

data = [
    (('TC', 'AS', '3H'),  14),
    (('9C', 'AS', '3D'),  13),
    (('9C', 'AS', '3D', 'Ac', 'ah'),  15),
]

@pytest.mark.parametrize('data', data)
def test_hand_value(data):

    left, right = data

    assert Hand([Card(*c) for c in left]).value() == right


# -------------
# Test Hand - Sorted

data = [
    (('TC', 'AS', '3H'), ('AS', '3H', 'TC') ),
    (('9C', 'AS', '3D'), ('AS', '3D', '9C') ),
    (('9C', 'AS', '3D', 'Ac', 'ah'), ('AS', 'AC', 'AH', '3D', '9C')),
]

@pytest.mark.parametrize('data', data)
def test_hand_sorted(data):

    left, right = data

    cards = Hand([Card(*c) for c in left])

    assert isinstance(cards, Hand)

    # Create a new sorted list
    items = Hand(sorted(cards)).display()

    assert len(items) == len(right)
    assert all([a == b for a, b in zip(items, right)])

    # Sort the Cards inline
    cards.sort()
    items = cards.display()

    assert len(items) == len(right)
    assert all([a == b for a, b in zip(items, right)])

# -------------
# Test Hand - combinations


left = ('TC', 'AS', '3H')
right = (
    [],
    [Card(rank='T', suit='C')],
    [Card(rank='A', suit='S')],
    [Card(rank='3', suit='H')],
    [Card(rank='T', suit='C'), Card(rank='A', suit='S')],
    [Card(rank='T', suit='C'), Card(rank='3', suit='H')],
    [Card(rank='A', suit='S'), Card(rank='3', suit='H')],
    [Card(rank='T', suit='C'), Card(rank='A', suit='S'), Card(rank='3', suit='H')]
)

data = [(left, right)]

left = ('TC', 'AS', '3H', 'QD')
right = (
    [],
    [Card(rank='T', suit='C')],
    [Card(rank='A', suit='S')],
    [Card(rank='3', suit='H')],
    [Card(rank='Q', suit='D')],
    [Card(rank='T', suit='C'), Card(rank='A', suit='S')],
    [Card(rank='T', suit='C'), Card(rank='3', suit='H')],
    [Card(rank='T', suit='C'), Card(rank='Q', suit='D')],
    [Card(rank='A', suit='S'), Card(rank='3', suit='H')],
    [Card(rank='A', suit='S'), Card(rank='Q', suit='D')],
    [Card(rank='3', suit='H'), Card(rank='Q', suit='D')],
    [Card(rank='T', suit='C'), Card(rank='A', suit='S'), Card(rank='3', suit='H')],
    [Card(rank='T', suit='C'), Card(rank='A', suit='S'), Card(rank='Q', suit='D')],
    [Card(rank='T', suit='C'), Card(rank='3', suit='H'), Card(rank='Q', suit='D')],
    [Card(rank='A', suit='S'), Card(rank='3', suit='H'), Card(rank='Q', suit='D')],
    [Card(rank='T', suit='C'), Card(rank='A', suit='S'), Card(rank='3', suit='H'), Card(rank='Q', suit='D')],
)

data.append((left, right))

@pytest.mark.parametrize('data', data)
def test_hand_combinations(data):

    left, right = data

    cards = Hand([Card(*c) for c in left])

    combo = [c for c in cards.every_combination()]

    assert len(combo) == len(right)

    assert all(a == b for a,b in zip(combo, right))


left = ('TC', 'AS', '3H')
right = (
    [Card(rank='T', suit='C'), Card(rank='A', suit='S')],
    [Card(rank='T', suit='C'), Card(rank='3', suit='H')],
    [Card(rank='A', suit='S'), Card(rank='3', suit='H')]
)

data = [(left, right)]

@pytest.mark.parametrize('data', data)
def test_hand_combinations2(data):

    left, right = data

    cards = Hand([Card(*c) for c in left])

    combo = [c for c in cards.every_combination(count=2)]

    assert len(combo) == len(right)
    assert all(a == b for a,b in zip(combo, right))


# -------------
# Test find_fifteens
