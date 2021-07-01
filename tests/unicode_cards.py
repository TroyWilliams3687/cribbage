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

"""

# ------------
# System Modules - Included with Python

# ------------
# 3rd Party - From pip

# ------------
# Custom Modules

print('Spades:')

spades = [
    "\U0001F0A1", # 🂡
    "\U0001F0A2", # 🂢
    "\U0001F0A3", # 🂣
    "\U0001F0A4", # 🂤
    "\U0001F0A5", # 🂥
    "\U0001F0A6", # 🂦
    "\U0001F0A7", # 🂧
    "\U0001F0A8", # 🂨
    "\U0001F0A9", # 🂩
    "\U0001F0AA", # 🂪
    "\U0001F0AB", # 🂫
    "\U0001F0AC", # 🂬
    "\U0001F0AD", # 🂭
    "\U0001F0AE", # 🂮
]


for s in spades:
    print(s)


# ----------------
print()
print('Hearts')

hearts = [
    "\U0001F0B1", # 🂱
    "\U0001F0B2", # 🂲
    "\U0001F0B3", # 🂳
    "\U0001F0B4", # 🂴
    "\U0001F0B5", # 🂵
    "\U0001F0B6", # 🂶
    "\U0001F0B7", # 🂷
    "\U0001F0B8", # 🂸
    "\U0001F0B9", # 🂹
    "\U0001F0BA", # 🂺
    "\U0001F0BB", # 🂻
    "\U0001F0BC", # 🂼
    "\U0001F0BD", # 🂽
    "\U0001F0BE", # 🂾
]

for h in hearts:
    print(h)

# ----------------
print()
print('Diamonds')

diamonds = [
    "\U0001F0C1", # 🃁
    "\U0001F0C2", # 🃂
    "\U0001F0C3", # 🃃
    "\U0001F0C4", # 🃄
    "\U0001F0C5", # 🃅
    "\U0001F0C6", # 🃆
    "\U0001F0C7", # 🃇
    "\U0001F0C8", # 🃈
    "\U0001F0C9", # 🃉
    "\U0001F0CA", # 🃊
    "\U0001F0CB", # 🃋
    "\U0001F0CC", # 🃌
    "\U0001F0CD", # 🃍
    "\U0001F0CE", # 🃎
]

for h in diamonds:
    print(h)


# ----------------

print()
print('Clubs')

clubs = [
    "\U0001F0D1", #🃑
    "\U0001F0D2", #🃒
    "\U0001F0D3", #🃓
    "\U0001F0D4", #🃔
    "\U0001F0D5", #🃕
    "\U0001F0D6", #🃖
    "\U0001F0D7", #🃗
    "\U0001F0D8", #🃘
    "\U0001F0D9", #🃙
    "\U0001F0DA", #🃚
    "\U0001F0DB", #🃛
    "\U0001F0DC", #🃜
    "\U0001F0DD", #🃝
    "\U0001F0DE", #🃞
]

for h in clubs:
    print(h)

# --------------

card_symbols = {

    # Spades

    'AS':'🂡', # "\U0001F0A1" - Ace of Spades
    '2S':'🂢', # "\U0001F0A2" - Two of Spades
    '3S':'🂣', # "\U0001F0A3" - Three of Spades
    '4S':'🂤', # "\U0001F0A4" - Four of Spades
    '5S':'🂥', # "\U0001F0A5" - Five of Spades
    '6S':'🂦', # "\U0001F0A6" - Six of Spades
    '7S':'🂧', # "\U0001F0A7" - Seven of Spades
    '8S':'🂨', # "\U0001F0A8" - Eight of Spades
    '9S':'🂩', # "\U0001F0A9" - Nine of Spades
    'TS':'🂪', # "\U0001F0AA" - Ten of Spades
    'JS':'🂫', # "\U0001F0AB" - Jack of Spades
    'CS':'🂬', # "\U0001F0AC" - Knight of Spades
    'QS':'🂭', # "\U0001F0AD" - Queen of Spades
    'KS':'🂮', # "\U0001F0AE" - King of Spades

    # Hearts

    'AH':'🂱', # "\U0001F0B1" - Ace of Hearts
    '2H':'🂲', # "\U0001F0B2" - Two of Hearts
    '3H':'🂳', # "\U0001F0B3" - Three of Hearts
    '4H':'🂴', # "\U0001F0B4" - Four of Hearts
    '5H':'🂵', # "\U0001F0B5" - Five of Hearts
    '6H':'🂶', # "\U0001F0B6" - Six of Hearts
    '7H':'🂷', # "\U0001F0B7" - Seven of Hearts
    '8H':'🂸', # "\U0001F0B8" - Eight of Hearts
    '9H':'🂹', # "\U0001F0B9" - Nine of Hearts
    'TH':'🂺', # "\U0001F0BA" - Ten of Hearts
    'JH':'🂻', # "\U0001F0BB" - Jack of Hearts
    'CH':'🂼', # "\U0001F0BC" - Knight of Hearts
    'QH':'🂽', # "\U0001F0BD" - Queen of Hearts
    'KH':'🂾', # "\U0001F0BE" - King of Hearts

    # Diamonds

    'AD':'🃁', # "\U0001F0C1" - Ace of Diamonds
    '2D':'🃂', # "\U0001F0C2" - Two of Diamonds
    '3D':'🃃', # "\U0001F0C3" - Three of Diamonds
    '4D':'🃄', # "\U0001F0C4" - Four of Diamonds
    '5D':'🃅', # "\U0001F0C5" - Five of Diamonds
    '6D':'🃆', # "\U0001F0C6" - Six of Diamonds
    '7D':'🃇', # "\U0001F0C7" - Seven of Diamonds
    '8D':'🃈', # "\U0001F0C8" - Eight of Diamonds
    '9D':'🃉', # "\U0001F0C9" - Nine of Diamonds
    'TD':'🃊', # "\U0001F0CA" - Ten of Diamonds
    'JD':'🃋', # "\U0001F0CB" - Jack of Diamonds
    'CD':'🃌', # "\U0001F0CC" - Knight of Diamonds
    'QD':'🃍', # "\U0001F0CD" - Queen of Diamonds
    'KD':'🃎', # "\U0001F0CE" - King of Diamonds

    # Clubs

    'AC':'🃑', # "\U0001F0D1" - Ace of Clubs
    '2C':'🃒', # "\U0001F0D2" - Two of Clubs
    '3C':'🃓', # "\U0001F0D3" - Three of Clubs
    '4C':'🃔', # "\U0001F0D4" - Four of Clubs
    '5C':'🃕', # "\U0001F0D5" - Five of Clubs
    '6C':'🃖', # "\U0001F0D6" - Six of Clubs
    '7C':'🃗', # "\U0001F0D7" - Seven of Clubs
    '8C':'🃘', # "\U0001F0D8" - Eight of Clubs
    '9C':'🃙', # "\U0001F0D9" - Nine of Clubs
    'TC':'🃚', # "\U0001F0DA" - Ten of Clubs
    'JC':'🃛', # "\U0001F0DB" - Jack of Clubs
    'CC':'🃜', # "\U0001F0DC" - Knight of Clubs
    'QC':'🃝', # "\U0001F0DD" - Queen of Clubs
    'KC':'🃞', # "\U0001F0DE" - King of Clubs

}


for k,v in card_symbols.items():
    print(f'{k} -> {v}')










































