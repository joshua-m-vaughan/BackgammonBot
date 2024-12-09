# TODO

- Implement existing model from literature for comparison against previous iterations in the field.
  - TD Gammon 3.0: 3-depth search of model
  - Compare performance of the performance of these two models.

- [ ] Implement novel self-guided implementation for agent and train.
  - [ ] Alpha Go approach: Take the TD Gammon 3.0 trained network and then use self-play to generate a many games, then implement a different NN to learn the valuation of different positions, to see if we can achieve an improved performance.

- [ ] Refactor lists and most datastructures in Numpy objects to facilitate integration with PyTorch.
