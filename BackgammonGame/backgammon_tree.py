# INFORMATION -------------------------------------------------------- #

# Author:  Josh Vaughan
# Date:    XX/07/2024
# Purpose: Implements a tree structure for storing Backgammon play
#          sequences.

# IMPORTS ------------------------------------------------------------ #

# CONSTANTS ---------------------------------------------------------- #

# CLASS DEF ---------------------------------------------------------- #

class PlayNode():

    # Implement variables for tracking instances.
    next_node_id = 0

    def __init__(self, parent, state, move:tuple = None) -> None:
        
        # Assign node an ID.
        self.id = PlayNode.next_node_id
        PlayNode.next_node_id += 1

        # Assign attribute values.
        self.parent = parent
        self.children = [] # TODO: Confirm if this is correct.
        self.state = state
        self.move = move
    
    def __str__(self, level=0) -> str:
        s = "\t"*level + str(tuple([self.id, self.move])) + "\n"
        for child in self.children:
            s += child.__str__(level+1)
        return s
    
# END ---------------------------------------------------------------- #