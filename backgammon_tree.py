# INFORMATION -------------------------------------------------------- #

# Author:  Josh Vaughan
# Date:    XX/07/2024
# Purpose: Implements a tree structure for storing Backgammon play
#          sequences.

# IMPORTS ------------------------------------------------------------ #

from backgammon_model import BackgammonState

# CONSTANTS ---------------------------------------------------------- #

# CLASS DEF ---------------------------------------------------------- #

class PlayNode():

    # Implement variables for tracking instances.
    next_node_id = 0

    def __init__(self, parent, state:BackgammonState,
                 action:tuple = None) -> None:
        
        # Assign node an ID.
        self.id = PlayNode.next_node_id
        PlayNode.next_node_id += 1

        # Assign attribute values.
        self._parent = parent
        self._children = None # TODO: Confirm if this is correct.
        self._state = state
        self._action = action

        return None
    

# END ---------------------------------------------------------------- #