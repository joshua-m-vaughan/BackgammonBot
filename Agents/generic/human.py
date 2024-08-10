# INFORMATION ------------------------------------------------------------------------------------------------------- #

# Author:  Josh Vaughan, leveraging the extended form game framework
#          from COMP90054 Assignment 3.
# Date:    10/08/2024
# Purpose: Implements a human interface for a Backgammon game.

# IMPORTS ------------------------------------------------------------------------------------------------------------#

from BackgammonGame.backgammon_model import BackgammonRules
from ExtendedFormGame.template import Agent, GameState

# CONSTANTS ----------------------------------------------------------------------------------------------------------#


# CLASS DEF ----------------------------------------------------------------------------------------------------------#  

class myAgent(Agent):
    def __init__(self,_id: int) -> None:
        super().__init__(_id)
        self.game_rules:BackgammonRules = BackgammonRules()
    
    def select_action(self, game_state:GameState,
                      actions:list[tuple]) -> tuple:
        """select_action
        Given a set of available actions for the agent to execute, and
        a copy of the current game state (including that of the agent),
        select one of the actions to execute.

        Args:
            game_state (GameState): Instance of GameState.
            actions (list[Action]): List of Action instances.

        Returns:
            Action: Selected action instance.
        """
        # Generate valid actions.
        valid_actions:list[list[tuple]] = self.game_rules.get_legal_actions(game_state, self.id)
        print(str(game_state))


        while True:
            # Request user input.
            action_str = input("Enter your turn: ")
            print()
            
            try:
                # Parse string into action.
                action:list[tuple] = []
                action_str = action_str.split()
                for move_str in action_str:
                    # Clean up inputs.
                    move_str = move_str.strip("()")
                    move_str = move_str.split(",")

                    # Cast strings to integers.
                    move:list = []
                    for pos in move_str:
                        move.append(int(pos))

                    # Store move.
                    action.append(tuple(move))

                # Check validity.
                if action in valid_actions:
                    return action
                else:
                    raise ValueError
        
            except ValueError:
                # Invalid action.
                print("Invalid action entered. Please enter a new action in the form: (start,fin,roll) (start,fin,roll)")
            except EOFError:
                exit()
                
    
    def update_endgame_weights(self, history:dict) -> None:
        """update_endstate_weights
        Updates the weights using the history printout for the match to
        accurately capture rewards at endgame state.

        Args:
            history (dict): Dictionary storing winning results and the
            history for the game.
        """
        # Do nothing - not a learning-based approach.
        return None
    
    def save_weights(self, filepath:str) -> None:
        """save_weights
        Save training weights for learning-based agents.
        """
        # Do nothing - not a learning-based approach.
        return None
# END ---------------------------------------------------------------- #