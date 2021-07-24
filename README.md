# Cribbage

A repository exploring the mathematics behind cribbage. It is a simple CLI application that can score a cribbage hand, determine the expected average and determine the optimal discard.

The program uses letters to represent the card suits:

- H - Hearts
- D - Diamonds
- C - Clubs
- S - Spades

It also uses numbers for the ranks except for:

- A - Ace
- T - Ten
- J - Jack
- Q - Queen
- K - King

To input the `Ace of Spades` to the program use `AS`. For the two of diamonds use `2D`.

## Score

[Scoring][1.1] a cribbage hand is not trivial and takes practice. The scoring function helps with practicing.

[1.1]: https://bicyclecards.com/how-to-play/cribbage/


```bash
$ cribbage score 4H 5D 5C 6S JD 

Hand = 4♥, 5♦, 5♣, 6♠
Cut  = J♦
------------------
4 Fifteens for 8
1 Pairs for    2
2 Runs for     6
Flush for      0
Nobs for       0
Nibs for       0
------------------
Total:         16

Fifteens:

1 - 5♦, J♦
2 - 5♣, J♦
3 - 4♥, 5♦, 6♠
4 - 4♥, 5♣, 6♠

Pairs:

1, 5♦, 5♣

Runs:

1 - 4♥, 5♦, 6♠
2 - 4♥, 5♣, 6♠
```


## Average

The [expected average][1.2] for a 4 card hand is simply the average value of all the possible hands that can be made with the remain cards in the deck assuming each card is drawn as a cut card.

[1.2]: https://en.wikipedia.org/wiki/Expected_value

```bash

$ cribbage average 3H 4D 5D 5S JS 2C --verbose

Hand = 3♥, 4♦, 5♦, 5♠
Discard = J♠, 2♣

 0: 3♥, 4♦, 5♦, 5♠, A♦ = 10
 1: 3♥, 4♦, 5♦, 5♠, A♥ = 10
 2: 3♥, 4♦, 5♦, 5♠, A♣ = 10
 3: 3♥, 4♦, 5♦, 5♠, A♠ = 10
 4: 3♥, 4♦, 5♦, 5♠, 2♦ = 12
 5: 3♥, 4♦, 5♦, 5♠, 2♥ = 12
 6: 3♥, 4♦, 5♦, 5♠, 2♠ = 12
 7: 3♥, 4♦, 5♦, 5♠, 3♦ = 20
 8: 3♥, 4♦, 5♦, 5♠, 3♣ = 20
 9: 3♥, 4♦, 5♦, 5♠, 3♠ = 20
10: 3♥, 4♦, 5♦, 5♠, 4♥ = 16
11: 3♥, 4♦, 5♦, 5♠, 4♣ = 16
12: 3♥, 4♦, 5♦, 5♠, 4♠ = 16
13: 3♥, 4♦, 5♦, 5♠, 5♥ = 17
14: 3♥, 4♦, 5♦, 5♠, 5♣ = 17
15: 3♥, 4♦, 5♦, 5♠, 6♦ = 14
16: 3♥, 4♦, 5♦, 5♠, 6♥ = 14
17: 3♥, 4♦, 5♦, 5♠, 6♣ = 14
18: 3♥, 4♦, 5♦, 5♠, 6♠ = 14
19: 3♥, 4♦, 5♦, 5♠, 7♦ = 12
20: 3♥, 4♦, 5♦, 5♠, 7♥ = 12
21: 3♥, 4♦, 5♦, 5♠, 7♣ = 12
22: 3♥, 4♦, 5♦, 5♠, 7♠ = 12
23: 3♥, 4♦, 5♦, 5♠, 8♦ = 10
24: 3♥, 4♦, 5♦, 5♠, 8♥ = 10
25: 3♥, 4♦, 5♦, 5♠, 8♣ = 10
26: 3♥, 4♦, 5♦, 5♠, 8♠ = 10
27: 3♥, 4♦, 5♦, 5♠, 9♦ =  8
28: 3♥, 4♦, 5♦, 5♠, 9♥ =  8
29: 3♥, 4♦, 5♦, 5♠, 9♣ =  8
30: 3♥, 4♦, 5♦, 5♠, 9♠ =  8
31: 3♥, 4♦, 5♦, 5♠, T♦ = 12
32: 3♥, 4♦, 5♦, 5♠, T♥ = 12
33: 3♥, 4♦, 5♦, 5♠, T♣ = 12
34: 3♥, 4♦, 5♦, 5♠, T♠ = 12
35: 3♥, 4♦, 5♦, 5♠, J♦ = 12
36: 3♥, 4♦, 5♦, 5♠, J♥ = 12
37: 3♥, 4♦, 5♦, 5♠, J♣ = 12
38: 3♥, 4♦, 5♦, 5♠, Q♦ = 12
39: 3♥, 4♦, 5♦, 5♠, Q♥ = 12
40: 3♥, 4♦, 5♦, 5♠, Q♣ = 12
41: 3♥, 4♦, 5♦, 5♠, Q♠ = 12
42: 3♥, 4♦, 5♦, 5♠, K♦ = 12
43: 3♥, 4♦, 5♦, 5♠, K♥ = 12
44: 3♥, 4♦, 5♦, 5♠, K♣ = 12
45: 3♥, 4♦, 5♦, 5♠, K♠ = 12

Value = 8
Average Value = 12.478
```

From the Above command you can see that the expected average for the hand: 3♥, 4♦, 5♦, 5♠ with a discard of J♠, 2♣ is 12.478. There are 46 cards left in the deck, each one is drawn as a cut card and the hand value is computed. The average of the computed values is known as the expected average. From the above out put, depending on the cut card you could have a had with a value of 20 or as low as 8. On average you can expect to score about 12 or 13 points.


You don't have to see the complete calculations by excluding the `--verbose` flag from the command:

```bash

$ cribbage average 3H 4D 5D 5S JS 2C

Hand = 3♥, 4♦, 5♦, 5♠
Discard = J♠, 2♣

Value = 8
Average Value = 12.478
```

## Discard

This is where things get interesting, given 6 cards, which 2 should you discard to the crib? The program will examine the cards and determine the expected average for all combinations of discards. It will examine two cases: the dealer and the pone.

The dealer has the advantage of the crib while the pone does not. Therefore your strategy will be different depending on which side of the table you are sitting on. The Pone wants to minimize the value of the crib. She doesn't want to give the dealer any points if possible. With that in mind the Pone should aim to minimize the number of points to the crib. In most cases they are trying to maximize the points in their hand and minimize the points in the crib.

On the other hand, the dealer wants to maximize the number of points they discard to the crib. After all, they pick up the points from the crib. In some cases this might mean discarding some good cards to the crib (we can see that on line 1, below, in the dealer table).

```bash
$ cribbage discard 3H 4D 5D 5S JS 2C

Processing....
 
Processing Pone Hands....
 1 3♥, 4♦, 5♦, 5♠ (8); 2♣, J♠, EA = 12.478, CEA =  3.855, Δ =  8.623
 2 3♥, 5♦, 5♠, J♠ (6); 2♣, 4♦, EA =  9.152, CEA =  4.624, Δ =  4.528
 3 2♣, 3♥, 5♦, 5♠ (4); 4♦, J♠, EA =  8.391, CEA =  4.012, Δ =  4.379
 4 2♣, 5♦, 5♠, J♠ (6); 3♥, 4♦, EA =  8.761, CEA =  4.962, Δ =  3.799
 5 4♦, 5♦, 5♠, J♠ (6); 2♣, 3♥, EA =  9.761, CEA =  6.833, Δ =  2.928
 6 2♣, 4♦, 5♦, 5♠ (2); 3♥, J♠, EA =  6.304, CEA =  3.865, Δ =  2.439
 7 3♥, 4♦, 5♦, J♠ (5); 2♣, 5♠, EA =  8.087, CEA =  5.662, Δ =  2.425
 8 3♥, 4♦, 5♠, J♠ (5); 2♣, 5♦, EA =  8.087, CEA =  5.662, Δ =  2.425
 9 2♣, 3♥, 4♦, 5♠ (4); 5♦, J♠, EA =  8.478, CEA =  7.126, Δ =  1.352
10 2♣, 3♥, 4♦, 5♦ (4); 5♠, J♠, EA =  8.478, CEA =  7.600, Δ =  0.878
11 2♣, 3♥, 5♦, J♠ (4); 4♦, 5♠, EA =  7.326, CEA =  6.878, Δ =  0.449
12 2♣, 3♥, 5♠, J♠ (4); 4♦, 5♦, EA =  7.326, CEA =  7.352, Δ = -0.026
13 2♣, 3♥, 4♦, J♠ (5); 5♦, 5♠, EA =  8.174, CEA =  9.092, Δ = -0.918
14 2♣, 4♦, 5♠, J♠ (2); 3♥, 5♦, EA =  4.935, CEA =  6.193, Δ = -1.258
15 2♣, 4♦, 5♦, J♠ (2); 3♥, 5♠, EA =  4.935, CEA =  6.193, Δ = -1.258

Processing Dealer Hands....
 1 2♣, 3♥, 4♦, J♠ (5); 5♦, 5♠, EA =  8.174, CEA =  9.092, Δ = 17.266
 2 4♦, 5♦, 5♠, J♠ (6); 2♣, 3♥, EA =  9.761, CEA =  6.833, Δ = 16.594
 3 3♥, 4♦, 5♦, 5♠ (8); 2♣, J♠, EA = 12.478, CEA =  3.855, Δ = 16.333
 4 2♣, 3♥, 4♦, 5♦ (4); 5♠, J♠, EA =  8.478, CEA =  7.600, Δ = 16.079
 5 2♣, 3♥, 4♦, 5♠ (4); 5♦, J♠, EA =  8.478, CEA =  7.126, Δ = 15.604
 6 2♣, 3♥, 5♠, J♠ (4); 4♦, 5♦, EA =  7.326, CEA =  7.352, Δ = 14.678
 7 2♣, 3♥, 5♦, J♠ (4); 4♦, 5♠, EA =  7.326, CEA =  6.878, Δ = 14.204
 8 3♥, 5♦, 5♠, J♠ (6); 2♣, 4♦, EA =  9.152, CEA =  4.624, Δ = 13.777
 9 3♥, 4♦, 5♦, J♠ (5); 2♣, 5♠, EA =  8.087, CEA =  5.662, Δ = 13.749
10 3♥, 4♦, 5♠, J♠ (5); 2♣, 5♦, EA =  8.087, CEA =  5.662, Δ = 13.749
11 2♣, 5♦, 5♠, J♠ (6); 3♥, 4♦, EA =  8.761, CEA =  4.962, Δ = 13.723
12 2♣, 3♥, 5♦, 5♠ (4); 4♦, J♠, EA =  8.391, CEA =  4.012, Δ = 12.403
13 2♣, 4♦, 5♦, J♠ (2); 3♥, 5♠, EA =  4.935, CEA =  6.193, Δ = 11.128
14 2♣, 4♦, 5♠, J♠ (2); 3♥, 5♦, EA =  4.935, CEA =  6.193, Δ = 11.128
15 2♣, 4♦, 5♦, 5♠ (2); 3♥, J♠, EA =  6.304, CEA =  3.865, Δ = 10.170

Started  - 2021-07-24 13:07:31.796342-04:00
Finished - 2021-07-24 13:07:37.760893-04:00
Elapsed:   0:00:05.964551
```

Both tables have the following columns:

- The first number indicates the hand number and helps to differentiate between different hands
- The next four values are the cards in the hand
- The following number in parenthesis is the value of the 4 card hand only
- Following the value is the cards to discard to the crib.
- The `EA` column represents the expected average for the hand.
- The `CEA` column represents the expected average for the crib.
- The `Δ` column represents the sum of (EA + CEA) for a dealer hand and the difference (EA - CEA) for a pone hand.

The goal is to maximize the delta column (`Δ`). Simply select the hand with the largest value in the delta column.

## License

[MIT](https://choosealicense.com/licenses/mit/)

