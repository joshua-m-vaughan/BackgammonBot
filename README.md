# BackgammonBot

An AI agent that plays a implementation of a Backgammon board game using Reinforcement Learning techniques.

## Motivation

The motivation behind this project stems from multiple areas that have affected me, as outlined below:

1. The countless competitive games of Backgammon against friends, family, and most importantly my partner. These games left me wanting more skill than being simply subjected to the whim of the dice!
2. The lecture given by Ge Wang at Stanford that touched on that we might be missing something when designing products to always solve problems, and that there was a need for play when designing and creating. The joy that building something that I can use to pit against my family, friends, and partner in Backgammon is exciting!
3. The course run by Steve Jones on building High Performance Computing clusters at Stanford was the catalyst, as the access to additional compute resources and a framework to test our code in this high performance environemnt was enough to get me kicked into gear on this project.
4. I am also hoping to consolidate my knowledge and learning from taking the AI Planning for Autonomy course at the University of Melbourne through the development of an additional board game playing agent, and one that I am able to share publicly.

## Backgammon Board Game Overview

The Backgammon board game is centred on removing all of the pieces off of the board prior to your opponent doing so. The following section will outline the technicalities of the board layout, and the rules of the game.

### Board Configuration

The board layout consists of 24 points, with 6 points belonging to the black player's home board, and 6 points belonging to the white player's home board. Additionally, the board has two home positions, or bar positions that each player is trying to reach. Let 1 be the point next to the player's home board, and 24 be the furthest point from the player's home board. The board is laid out as detailed in the image below [[3]](#references):

![Backgammon Board Layout](res\bg_board_layout.gif)

In specifying an efficient representation of the backgammon board configuration throughout the game, I have implemented a modified representation proposed by Lishout, Chaslot, and Uiterwijk [[1]](#references). The configuration is represented as follows:

- `PointsContent[26]`: An array where the $i^{th}$ cell indicates how many checkers are on the $i^{th}$ point, with 0 and 25 being the respective player's home point. $+x$ indicates that $x$ black checkers are present, $-x$ that $x$ white checkers are present, and 0 that the point is empty.[[1]](#references)
- `BlackCheckers`: A vector that stores the points of the black player, where point numbers are stored in **increasing** order.[[1]](#references)
- `WhiteCheckers`: A vector that stores the points of the black player, where point numbers are stored in **decreasing** order.[[1]](#references)
- `BlackCheckersTaken` and `WhiteCheckersTaken`: Two integers which give the amount of black / white checkers taken.[[1]](#references)

### Game Rules

The rules of the game are as follows, when it is a player's turn they roll the dice. If the showing faces of the dice are the same number, then the player is able to move the four pieces towards their home position using the showing face of the dice. If they are two different numbers, then the player can move two pieces using each of the two values on the face of the dice.

When a player moves a piece, they cannot move it onto a point that has two or more pieces of the opposing player. If the point has one opposing piece, and a the player moves a piece to this point, the opposing piece is sent to the player's home position ("on the bar"). When you have a piece *on the bar*, you cannot move any other pieces until this piece has come off the bar.

When the player has moved all of their pieces into their home board, they are able to start to move pieces into their home position. If a player has rolled a face that is larger than furthest piece from the home position, they are able to move this piece to the home position, otherwise, all pieces must move as if under normal board conditions.

In the case, that a player cannot make all moves, the player must prioritise playing the largest face of the dice when making any move.

A key aspect of the board game that has been omitted is the doubling cube. This piece has an additional action that allows a player to double the points of the game each time it is used, and if the opposing player declines then the game is forfeited. I have not had sufficient time to implement the game simulator, so this aspect of the game, which is mainly used for gambling, has not been included in the current implementation.

To implement this in the simulator, I have used the technique proposed by Hans J. Berliner [[2]](#references) that utilises a tree of moves that generate sequence of a valid action. This technique takes advantage of the symmetry of playing multiple moves in a single turn action (e.g. playing a 3 and 5 on the same piece, is equivalent to playing a 5 and a 3 on the same piece.).

### Strategy

Backgammon is both a game of luck, and strategy. Some basic backgammon strategies are outlined as follows:

- **Running:** Move each piece to the home board as quickly as possible. This is typically moving the furthest pieces on the board towards home.
- **Blitz:** Attack your opponnent's vulnerable checkers when they become available.
- **Priming:** Build a prime (at least 4 points in a sequence with two or more pieces on each point) that makes it difficult for your opponent to pass your prime position. Typically, once the prime is established, you can move this around the board towards your home position to trap the opposing players pieces.
- **Holding:** Hold a key position on your opponent's board that increases the risk of having their piece taken into the end game.
- **Back game:** Hold multiple positions in your opponent's board to increase the risk of having their piece taken into the end game, and difficulty in having all pieces reach their home board. This can create risk with the opponent having a significantly lower PIP score than the player if the strategy is applied for too long.

May the best player win!

## Reinforcement Learning Model Specification

### State-Space Model

Backgammon is a two-person non-deterministic perfect information extensive form game that can be defined as a Stochastic game, as outlined below:

- TBC.

### Analysis of State Space

TBC.

### Analysis of Action Space

TBC.

## Approach

The approach used in the game is the TD-Gammon 0.0 agent framework outlined by Gerald Tesauro in his 1995 paper *Temporal Differenec Learning and TD-Gammon*. From Tesauro's implementation, after training the agent over 500,000 self-play games, the agent was at intermediate-level, and an impressive performance level when released.

Some notable features of the approach are the following:

- **Neural Network:** The neural network that is learned during self-play learns the value of a position for particular agents. Since the reward structure is zero, unless the agent wins, where it is one, the output layer indicates the expected probability that an agent wins in a particualr board position. The neural network consists of 198 input units which solely represent the board position, and no specific features (e.g. prime exists or not), a fully connected hidden layer of 40 units using a Sigmoid activation function, and a fully connected output layer of 4 units representing a win state for each player, and a gammon win state for each player. An important note is that my rules implementation doesn't consider a win by gammon, therefore, the output layer only has two output nodes.
- **1-ply evaluation:** Actions are selected based on the value of the outcome state after an action is played. For example, if the white player is considering their move, they play all possible valid actions, and evaluate their expected value in the future state where it is the black players turn to move.
- **Training Parameters:** The parameters that are set for training are $\alpha = 0.01$, $\gamma = 1.0$ and $\lamda = 0.7$.

## Experiment

### Experiment Design

TBC.

### Experiment Results

TBC.

### Analysis

TBC.

## Conclusion

TBC.

## References

[1]: Van Lishout, François & Chaslot, Guillaume & Uiterwijk, Jos. (2007). *Monte-Carlo tree search in backgammon*. Computer Games Workshop.

[2]: Berliner, Hans J. (1977) *BKG -- A Program that plays Backgammon*. Carnegie-Mellon University.

[3]: Backgammon Galore! (2024) *Rules of Backgammon*. <https://www.bkgm.com/rules.html> (accessed on 21 July 2024)
