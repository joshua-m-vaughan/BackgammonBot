# BackgammonBot
An AI agent that plays a implementation of a Backgammon board game using Reinforcement Learning techniques.

## Motivation
The motivation behind this project stems from multiple areas that have affected me, as outlined below:
1. The countless competitive games of Backgammon against friends, family, and most importantly my partner. These games left me wanting more skill than being simply subjected to the whim of the dice!
2. The lecture given by Ge Wang at Stanford that touched on that we might be missing something when designing products to always solve problems, and that there was a need for play when designing and creating. The joy that building something that I can use to pit against my family, friends, and partner in Backgammon is exciting!
3. The course run by Steve Jones on building High Performance Computing clusters at Stanford was the catalyst, as the access to additional compute resources and a framework to test our code in this high performance environemnt was enough to get me kicked into gear on this project.
4. I am also hoping to consolidate my knowledge and learning from taking the AI Planning for Autonomy course at the University of Melbourne through the development of an additional board game playing agent, and one that I am able to share publically.

## Backgammon Board Game Overview
The Backgammon board game is centred on removing all of the pieces off of the board prior to your opponent doing so. The following section will outline the technicalities of the board layout, and the rules of the game.

### Board Configuration
The board layout is detailed as follows:
TBC.

In specifying an efficient representation of the backgammon board configuration throughout the game, I have opted to follow the representation proposed by Lishout, Chaslot, and Uiterwijk [[1]](#references). The configuration is represented as follows:
- `PointsContent[25]`: An array where the $i^{th}$ cell indicates how many checkers are on the $i^{th}$ point. $+x$ indicates that $x$ black checkers are present, $-x$ that $x$ white checkers are present, and 0 that the point is empty.[[1]](#references)
- `BlackCheckers`: A vector whose first element is the number of points containing black checkers, and the other elements are the corresponding point number in **increasing** order.[[1]](#references)
- `WhiteCheckers`: A vector whose first elements is the number of points containing whtie checkers, and the other elements are the corresponding point number in **decreasing** order.[[1]](#references)
- `BlackCheckersTaken` and `WhiteCheckersTaken`: Two integers which give the amount of black / white checkers taken.[[1]](#references)

### Game Rules
The rules of the game are as follows:
TBC.

### Strategy
Some examples of player strategies are as follows:
TBC.

## Reinforcement Learning Model Specification
### State-Space Model
Backgammon is a two-person non-deterministic perfect information extensive form game that can be defined as a Stochastic game, as outlined below:
- TBC.

### Analysis of State Space
TBC.

### Analysis of Action Space
TBC.

## Approach
TBC.

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

TODO: Clean-up reference formatting.

[1]: Monte-Carlo Tree Search in Backgammon, Francois