# TODO

- [X] Validate game scripts for game runner.
- [X] Implement end game exit to store details of the final game conditions.
- [X] Create training script for agent.
- [X] Finish training file storage for backgammon games.
- [X] Extended training to beyond the run scope of the game.
- [ ] Implement existing model from literature for comparison against previous iterations in the field.

    - [X] TD Gammon 0.0 requires onpolicy learning: this will unlikely be able to use PyTorch due to the specific gradient descent method.
    - [ ] TD Gammon 3.0: use MCTS for a 3-depth search into the 
    - [ ] Compare performance of the performance of these two models.

- [X] Create an evaluation script for agent.
- [ ] Implement novel self-guided implementation for agent and train.

    - [ ] Alpha Go approach: Take the TD Gammon 3.0 trained network and then use self-play to generate a many games, then implement a different NN to learn the valuation of different positions, to see if we can achieve an improved performance.

- [X] Fix unable to play move when largest is unplayable - if this generates nothing, then skip to smallest one.

    - TECH DEBT: This has been addressed by implementing a reverse order validation, which breaks the largest face first rule that prevents players from not playing a move when they can.

- [X] Fix tied endings, and why it is possible to have this occur.
- [ ] Refactor lists and most datastructures in Numpy objects - to facilitate integration with PyTorch.
- [ ] Fix incorrect typecasting of an action to a tuple of tuples once they are finalised etc.