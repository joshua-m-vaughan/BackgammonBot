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
                 move:tuple = None) -> None:
        
        # Assign node an ID.
        self.id = PlayNode.next_node_id
        PlayNode.next_node_id += 1

        # Assign attribute values.
        self._parent = parent
        self._children = None # TODO: Confirm if this is correct.
        self._state = state
        self._move = move

        return None
    
    def get_parent(self):
        """get_parent
        Returns the parent attribute of the PlayNode instance.

        Returns:
            PlayNode: Parent node of current node.
        """
        return self._parent
    
    def get_children(self):
        """get_children
        Returns the children attribute of the PlayNode instance.

        Returns:
            list[PlayNode]: List of children nodes of current node.
        """
        return self._children
    
    def get_state(self):
        """get_state
        Returns the state attribute of the PlayNode instance.

        Returns:
            BackgammonState: Backgammon state.
        """
        return self._state
    
    def get_move(self):
        """get_action
        Returns the move attribute of the PlayNode instance.

        Returns:
            tuple: Three tuple detailing fromPoint, toPoint, and face
            value of a move.
        """
        return self._move
    
# END ---------------------------------------------------------------- #