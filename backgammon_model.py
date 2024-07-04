# INFORMATION -------------------------------------------------------- #

# Author:  Josh Vaughan, leveraging the extended form game framework
#          from COMP90054 Assignment 3.
# Date:    03/07/2024
# Purpose: Implements Backgammon for the purposes of developing an AI
#          agent for ME344: Introduction to building High Performance
#          Computing clusters, at Stanford Summer Session 2024.

# IMPORTS ------------------------------------------------------------ #

from collections import defaultdict
from copy import deepcopy
import itertools
import random
from ExtendedFormGame.template import GameState, GameRules, Action

# CONSTANTS ---------------------------------------------------------- #

MIN_DICE_VALUE:int = 1
MAX_DICE_VALUE:int = 6
NUM_BACKGAMMON_AGENTS:int = 2
BLACK_ID:int = 0
WHITE_ID:int = 1
BLACK_HOME_POINT:int = 25
WHITE_HOME_POINT:int = 0
INIT_BOARD_CONFIG = [(1,2), (12,5), (17,3), (19,5)]
DOUBLES_MULTIPLIER:int = 4
CHECKERS_BLOCKED:int = 2

# CLASS DEF ---------------------------------------------------------- #

class BackgammonState(GameState):
    
    def __init__(self,
                 num_agents:int =NUM_BACKGAMMON_AGENTS,
                 agent_id:int =BLACK_ID) -> None:
        """__init__
        Initialise an instance of BackgammonState class.

        Args:
            num_agents (int, optional): Number of agents in the game.
            Defaults to 2.
            STARTING_AGENT_ID (int, optional): Starting Agent ID.
            Defaults to BLACK_ID.

        """
        # Assert expected input from Game builder.
        assert (num_agents == 2)
        assert (agent_id == 0)

        # Initialise GameState attributes.
        self.num_agents = num_agents
        self.current_agent_id = agent_id

        # Initialise the board state attributes.
        self.points_content = [0] * 26
        self.black_checkers = []
        self.white_checkers = []
        for point, num_checkers in INIT_BOARD_CONFIG:
            # Black Setup
            self.points_content[point] = num_checkers
            self.black_checkers.append(point)
            # White Setup
            self.points_content[BLACK_HOME_POINT - point] = -num_checkers
            self.white_checkers = [BLACK_HOME_POINT - point] + self.white_checkers
        self.black_checkers_taken = 0
        self.white_checkers_taken = 0

        # Initialise the dice attributes.
        self.dice = [random.randint(MIN_DICE_VALUE, MAX_DICE_VALUE),
                     random.randint(MIN_DICE_VALUE, MAX_DICE_VALUE)]
    
    def __str__(self) -> str:
        output = ""
        for i in range(len(self.points_content)):
            if self.points_content[i] > 0:
                output += (str(i) +" "+("B"*self.points_content[i]) + "\n")
            elif self.points_content[i] < 0:
                output += (str(i) +" "+("W"*-self.points_content[i]) + "\n")
            else:
                output += (str(i) + "\n")
        output += str("DICE: "+str(self.dice[0])+" "+str(self.dice[1]))
        return output

    def roll(self) -> None:
        """roll
        Roll the dice to generate a new set of two dice representation.
        """

        self.dice = [random.randint(MIN_DICE_VALUE, MAX_DICE_VALUE),
                     random.randint(MIN_DICE_VALUE, MAX_DICE_VALUE)]
        
        return None


class BackgammonRules(GameRules):
    
    def __init__(self):
        """__init__
        Initialise an instance of GameRules class.
        """
        super().__init__(NUM_BACKGAMMON_AGENTS)

    def initial_game_state(self) -> BackgammonState:
        """initial_game_state
        Returns the intial game state for the games rules.

        Returns:
            BackgammonState: An instance of BackgammonState class.
        """
        return BackgammonState(self.num_agents)

    def get_legal_actions(self, game_state:BackgammonState,
                          agent_id:int) -> list[Action]:
        """get_legal_actions
        Returns a list of Action instances that are legal for Agent ID
        in a given GameState.

        Args:
            game_state (BackgammonState): BackgammonState s.
            agent_id (int): Agent ID.

        Returns:
            list[Action]: List of Action instances that are valid in
            BackgammonState s.
        """
        # Validate dice to determine available moves.
        [dice_a, dice_b] = game_state.dice
        if dice_a == dice_b:
            steps = [dice_a] * DOUBLES_MULTIPLIER
        else:
            steps = game_state.dice

        # Generate all possible valid moves with the form of:
        #   [from_point, to_point].
        # A move is valid if it:
        #   - Moves to a position given by a rolled step.
        #   - Is within the bounds of the board game.
        #   - Doesn't land on a point with 2 or more opposing checkers.
        moves = [defaultdict(lambda: set())] * len(steps)

        if agent_id == BLACK_ID:
            for i in range(len(steps)):
                # Generate the moves for each of the free pieces on the
                # board.
                for point in game_state.black_checkers:
                
                    # NOTE: Could efficiency be picked up here for when
                    # doubles are rolled.
                    
                    # Validate move for positioning.
                    if ((point+steps[i]) <= BLACK_HOME_POINT and
                        (game_state.points_content[point+steps[i]] >
                          -CHECKERS_BLOCKED)):
                        moves[i]["free"].add((point, point+steps[i]))
                
                # Generate the move from the taken position on the
                # board.
                if game_state.black_checkers_taken > 0:
                    moves[i]["taken"].add((WHITE_HOME_POINT,
                                           WHITE_HOME_POINT+steps[i]))


                        
        elif agent_id == WHITE_ID:
            for i in range(len(steps)):
                # Generate the moves for each of the free pieces on the
                # board.
                for point in game_state.white_checkers:
                
                    # NOTE: Could efficiency be picked up here for when
                    # doubles are rolled.

                    # Validate move for positioning.
                    if ((point-steps[i]) >= WHITE_HOME_POINT and
                        (game_state.points_content[point-steps[i]] <
                          CHECKERS_BLOCKED)):
                        
                        moves[i].add((point, point-steps[i]))
                
                # Generate the move from the taken position on the
                # board.
                if game_state.white_checkers_taken > 0:
                    moves[i]["taken"].add((BLACK_HOME_POINT,
                                           BLACK_HOME_POINT-steps[i]))
        # Generate move combinations.
        if agent_id == BLACK_ID:
            num_taken_moves = min(game_state.black_checkers_taken, len(moves))
            num_free_moves = len(moves) - num_taken_moves

            taken_combos = list(itertools.combinations())

        elif agent_id == WHITE_ID:
            pass
        for combo in itertools.combinations(moves, len(steps)):
            print(combo)

    def calculate_score(self, game_state:BackgammonState,
                        agent_id:int) -> int:
        """calculate_score
        Returns the pip score for agent ID in BackgammonState s.

        Args:
            game_state (BackgammonState): BackgammonState s.
            agent_id (int): Agent ID.

        Returns:
            int: Integer representing the agent's score.
        """
        pip_score = 0
        if (agent_id == BLACK_ID):
            for point in game_state.black_checkers:
                pip_score += (game_state.points_content[point] *
                              abs(BLACK_HOME_POINT - point))
        elif (agent_id == WHITE_ID):
            for point in game_state.white_checkers:
                pip_score += (game_state.points_content[point] *
                              abs(WHITE_HOME_POINT - point))

        return pip_score

    def game_ends(self, game_state:BackgammonState) -> bool:
        """game_ends
        Returns whether the game ends in BackgammonState.

        Args:
            game_state (BackgammonState): BackgammonState s.
        
        Returns:
            bool: Boolean indicating the completion of the game.
        """
        if game_state.current_agent_id == BLACK_ID:
            if (len(game_state.black_checkers) == 1 and
                game_state.black_checkers[0] == BLACK_HOME_POINT and
                game_state.black_checkers_taken == 0):
                # Black has moved all pieces to its home position.
                return True
            else:
                return False
        elif game_state.current_agent_id == WHITE_ID:
            if (len(game_state.white_checkers) == 1 and
                game_state.white_checkers[0] == WHITE_HOME_POINT and
                game_state.white_checkers_taken == 0):
                # White has moved all pieces to its home position.
                return True
            else:
                return False
        else:
            raise ValueError("Invalid Agent ID passed to game_ends.")

class BackgammonAction(Action):
    pass

if __name__ == "__main__":
    bs = BackgammonState()
    print(str(bs))
    bgr = BackgammonRules()
    print("BLACK PIP SCORE: "+str(bgr.calculate_score(bs, BLACK_ID)))
    bgr.get_legal_actions(bs, 0)

# END ---------------------------------------------------------------- #